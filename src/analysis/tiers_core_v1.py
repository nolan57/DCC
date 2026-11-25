# -*- coding: utf-8 -*-
"""
tiers_core_v1.py -- the four intrinsic-tier estimators, extracted verbatim from
`src/route/structure_tiers.py` so that a cycle can measure a frame without running
that script's calibration block.

Authority: docs/specs/intrinsic_structure_tiers_v1.md (definitions and thresholds)
Lock:      runs/MATRIX/threshold_lock.json (+ .sha256)

This module does NOT define a threshold and does NOT choose a tier. It implements
the registered estimators:
  T0  Q0 = 1 - P0(u)/P0(null)                       (0-dim persistence)
  T1  Q1 = xi/h, xi from the axis-averaged ACF      (cells)
  T2  Q2 = (q2(u)-q2(null))/(1-q2(null))            (16-level conditional entropy)
  T3  Q3 = log2(1 + C_xi q / C_eye), xi/h >= 2      (DoG band-limited contrast)

The source hash is recorded by the calling cycle. Any divergence from
`structure_tiers.py` is a defect of this module, not a new estimator.
"""

import math

import numpy as np

GRID = 128
BINS = 64
CTX = 16
NULL_M = 16
NULL_SEED0 = 4000
Q_INSTR = 1.0
Q_REFL = 0.0
C_EYE = 0.01


def gauss_blur(u, sigma):
    W, H = u.shape
    fy = np.fft.fftfreq(W)[:, None]
    fx = np.fft.fftfreq(H)[None, :]
    filt = np.exp(-2.0 * (np.pi ** 2) * (sigma ** 2) * (fy ** 2 + fx ** 2))
    return np.real(np.fft.ifft2(np.fft.fft2(u) * filt))


def quant(u):
    lo, hi = float(u.min()), float(u.max())
    span = hi - lo if hi > lo else 1.0
    return np.clip(((u - lo) / span * BINS).astype(np.int32), 0, BINS - 1), span


def total_persistence(u):
    """0-dim persistence of the superlevel filtration, total lifetime per cell / range."""
    q, span = quant(u)
    W, H = q.shape
    flat = (q.ravel().astype(np.float64)) / float(BINS - 1)
    order = np.argsort(-flat, kind='stable')
    parent = np.full(flat.size, -1, dtype=np.int64)
    birth = np.zeros(flat.size, dtype=np.float64)
    total = 0.0

    def find(a):
        r = a
        while parent[r] != r:
            r = parent[r]
        while parent[a] != r:
            parent[a], a = r, parent[a]
        return r

    for idx in order:
        idx = int(idx)
        v = flat[idx]
        i, j = divmod(idx, H)
        nb = []
        if i > 0 and parent[idx - H] != -1:
            nb.append(find(idx - H))
        if i < W - 1 and parent[idx + H] != -1:
            nb.append(find(idx + H))
        if j > 0 and parent[idx - 1] != -1:
            nb.append(find(idx - 1))
        if j < H - 1 and parent[idx + 1] != -1:
            nb.append(find(idx + 1))
        seen = []
        for r in nb:
            if r not in seen:
                seen.append(r)
        birth[idx] = v
        parent[idx] = idx
        if not seen:
            continue
        eldest = max(seen, key=lambda r: birth[r])
        for r in seen:
            if r != eldest:
                total += max(0.0, birth[r] - v)
                parent[r] = eldest
        parent[idx] = eldest
    roots = set(find(x) for x in range(flat.size) if parent[x] != -1)
    for r in roots:
        total += max(0.0, birth[r] - flat.min())
    return total / flat.size


def char_scale(u):
    """axis-averaged normalised autocorrelation; xi = first lag below 1/e (interpolated)."""
    m = u - u.mean()
    F = np.fft.fft2(m)
    acf = np.real(np.fft.ifft2(F * np.conj(F)))
    if acf[0, 0] <= 0:
        return 0.0, 0.0
    acf /= acf[0, 0]
    W, H = u.shape
    lmax = min(W, H) // 2
    R = np.array([0.5 * (acf[l, 0] + acf[0, l]) for l in range(lmax + 1)])
    thr = math.exp(-1.0)
    for l in range(1, lmax + 1):
        if R[l] < thr:
            r0, r1 = R[l - 1], R[l]
            if r0 == r1:
                return float(l), float(R[l])
            frac = (r0 - thr) / (r0 - r1)
            return (l - 1) + frac, float(R[l])
    return float(lmax), float(R[lmax])


def plug_q2(u):
    q, _ = quant(u)
    W, H = q.shape
    p = np.bincount(q.ravel(), minlength=BINS).astype(np.float64)
    p /= p.sum()
    p = p[p > 0]
    Hm = float(-(p * np.log2(p)).sum())
    if Hm <= 0:
        return None, 0.0
    a = (q[:-1, 1:] * CTX) // BINS
    b = (q[1:, :-1] * CTX) // BINS
    c = a * CTX + b
    t = q[1:, 1:]
    joint = np.bincount((c * BINS + t).ravel(), minlength=CTX * CTX * BINS).reshape(CTX * CTX, BINS)
    tot = joint.sum()
    pc = joint.sum(axis=1) / tot
    nz = joint > 0
    Hc = 0.0
    for ci in range(CTX * CTX):
        if pc[ci] == 0:
            continue
        row = joint[ci][nz[ci]] / joint[ci].sum()
        Hc += pc[ci] * float(-(row * np.log2(row)).sum())
    return 1.0 - Hc / Hm, Hm


def q3(u, xi, qfactor):
    if xi < 2.0:
        return None
    dog = gauss_blur(u, xi / 2.0) - gauss_blur(u, 2.0 * xi)
    mean_abs = float(np.abs(u).mean())
    if mean_abs <= 0:
        return None
    C = float(dog.std()) / mean_abs
    return math.log2(1.0 + C * qfactor / C_EYE), C


def null_statistics(grid=GRID, m=NULL_M, seed0=NULL_SEED0):
    p0s, q2s = [], []
    for k in range(m):
        u = np.random.default_rng(seed0 + k).random((grid, grid))
        p0s.append(total_persistence(u))
        q2, _ = plug_q2(u)
        q2s.append(q2)
    return float(np.mean(p0s)), float(np.mean(q2s)), float(np.std(p0s)), float(np.std(q2s))
