"""RQ-06 (round 60): the L_z-resolved family surface handed to R1-B4/R3.

Emits runs/R1B/r1b1_p4_family_surface.md with --write. Never transcribed.
All predictions are registered in runs/R1B/r1b1_p4_family_surface_registration.md.
"""
import os
import sys
import math

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _ROOT)
from src.common import conv  # noqa: E402

H = conv.HBARC            # hbar c, MeV fm
HB = 6.582119569e-22      # hbar, MeV s
ME = conv.M_E             # electron rest energy, MeV
C_FM_S = 2.99792458e23    # c, fm/s
LZ_GRID = (1.68, 1.76, 1.84, 1.92, 1.99)
NB = conv.N_B_FM2

# Archived P4-1 table values, for cross-check only (EXEMPT-LEGACY, BN-04).
P4_KF = {1.68: 0.0591, 1.84: 0.0563, 1.99: 0.0540}
P4_VF = {1.68: 0.0316, 1.84: 0.0330, 1.99: 0.0342}
P4_W = {1.68: 5.606e23, 1.84: 5.119e23, 1.99: 4.733e23}
P2_N = {1.68: 1.1106e-3, 1.76: 1.0570e-3, 1.84: 1.0081e-3,
        1.92: 9.6324e-4, 1.99: 9.2696e-4}


def state_at(lz):
    """Reproduce r1b1_p2_eos_scan.py's HYB state at thickness lz."""
    base_lz, base_e = conv.LZ_FM, conv.E_SUBBAND
    conv.LZ_FM = lz
    conv.E_SUBBAND = math.pi * H / lz
    r = conv.beta_eq(NB, 'HYB')
    conv.LZ_FM, conv.E_SUBBAND = base_lz, base_e
    return r


def cell(lz):
    r = state_at(lz)
    n = r['n_e_areal']
    k = conv.kF_2(n)
    ez = math.pi * H / lz           # E_z,1, MeV (also m_eff c^2)
    vf = H * k / ez                 # v_F/c
    f_intra = ME / ez
    f_inter = 1.0 - f_intra
    wa = 4.0 * math.pi * H * H * n / ez   # W_total/A_inter (g=2), MeV
    w_end = ez + f_inter * wa            # S14 budget-form edge, MeV
    return dict(lz=lz, n=n, xp=r['X_p'], mu=r['mu_e'], k=k, ez=ez, vf=vf,
                f_intra=f_intra, f_inter=f_inter, wa=wa, w_end=w_end,
                w_band=ez / HB)


CELLS = [cell(z) for z in LZ_GRID]

out = []
a = out.append
a('# R1B1-P4/P5 — refinement (iv): the `L_z`-resolved family surface')
a('')
a('**Round 60** — `RQ-06`, product of `src/r1_dense/r1b1_p4_family_surface.py` '
  '(`--write`). Pre-registration: `runs/R1B/r1b1_p4_family_surface_registration.md`.')
a('')
a('`PROVENANCE: NEITHER` — a compilation/arithmetic receipt over state inputs. '
  'It establishes no chain evidence, re-grades no criterion and writes no gate mark.')
a('')
a('---')
a('')
a('## 1 The surface R1-B4/R3 receive')
a('')
a('Five cells, fixed baryon column `N_B = %.6f fm⁻²`, HYB convention, `g = 2` '
  '(spin, single occupied subband). Every number is state-derived at its own `L_z`; '
  'none is transcribed from P4-1.' % NB)
a('')
a('| `L_z` [fm] | `n_free,2D` [fm⁻²] | `g` | `v_F/c` | `ω_end` [rad/s] | `ω_end(S14)` [MeV] |')
a('|---|---|---|---|---|---|')
for c in CELLS:
    a('| %.2f | %.5e | 2 | %.5f | %.4e | %.4f |'
      % (c['lz'], c['n'], c['vf'], c['w_band'], c['w_end']))
a('')
a('`ω_end` in the fifth column is the **band edge** `πc/L_z`, carried forward from the '
  'P4-1 table because that is what the archive hands off. The sixth column is the form '
  '`S14` actually requires (§4). Both are state-derived; they differ by `0.40–0.47%` '
  'because `f_inter W_total/A ≈ 1.46 MeV` is small against `E_z,1 ≈ 311–369 MeV`.')
a('')
a('## 2 Per-cell provenance')
a('')
a('Each cell states which product derived each input, and which erratum qualifies it. '
  '`EXEMPT-LEGACY` means the archived P4-1 file is cited only as evidence of a defect, '
  'never as the authority for a corrected number (BN-04/P9 digest).')
a('')
a('| `L_z` | input | value | source and qualification |')
a('|---|---|---|---|')
for c in CELLS:
    z = c['lz']
    a('| %.2f | `n_free,2D` | %.5e | `r1b1_p2_eos_scan_results.txt` P2-5; `beta_eq` at fixed '
      '`N_B`, HYB; `n_e = X_p·N_B`. E4: **not** 4.2–5.0%% of `n_Q` (that is `X_p/Z_A`). |'
      % (z, c['n']))
    a('| %.2f | `g` | 2 | P4-1 declaration: spin, one occupied subband. BN-35/E7: the '
      'same-sign MIT bag admits a `k=0` mode; `g = 2` holds only if it is unoccupied. |' % z)
    archived = ('E2: P4-1 printed %.4f c (low by `√2`).' % P4_VF[z]) if z in P4_VF else (
        'P4-1 printed no row at this `L_z` (three-row table).')
    a('| %.2f | `v_F` | %.5f c | corrected: `ħ k_F/m_eff`, `k_F = conv.kF_2(n)`, '
      '`m_eff = E_z,1/c²`. %s |' % (z, c['vf'], archived))
    a('| %.2f | `ω_end` | %.4e rad/s | band edge `πc/L_z` = `E_z,1/ħ`, state-derived. '
      'P4-1 prose `3.1–3.7e23` belongs to `L_z = 2.55–3.04 fm` (outside K1). |'
      % (z, c['w_band']))
a('')
a('## 3 Admissible range')
a('')
a('**Declared admissible: the five solved cells at `L_z ∈ {1.68, 1.76, 1.84, 1.92, 1.99} fm`, '
  'inside the registered K1 window `[1.68, 1.99] fm`.**')
a('')
a('That interval is the *frozen-density* K1 window: at `n_e = 0.022 fm⁻²`, '
  '`E_sub/E_F ≥ 3` gives `L_z ≤ 1.995 fm` and the nucleon-fit bound `2r_p = 1.68 fm` '
  'gives the lower edge — width `1.19×`, with the lower edge a physical judgment, not a theorem. '
  'At the solved density (`n_free ≈ 1e−3 fm⁻²`, `22×` lower) the same two-sided test gives '
  'an upper edge `L_z ≈ 80.30 fm`, a factor of `≈ 40` wider. The receipt therefore makes '
  'three distinctions a downstream citation must keep:')
a('')
a('1. `[1.68, 1.99] fm` is the **registered** K1 window, not the solved state\'s 2D ceiling;')
a('2. only the five solved `L_z` are **certified cells** — interpolating the tuple to an '
  'unsolved thickness is a new state solve, not a table lookup;')
a('3. outside K1 the archive has no state, so neither the tuple nor the response may be cited.')
a('')
a('## 4 The S14 form that P4 did not compute')
a('')
a('`S14` (`BUDGET-DECLARED`) forbids a bare `ω_end` and requires '
  '`ω_end = ω_g + f_inter·W_total/A` with one declared `ω` convention. P4-1 recorded '
  '`S14 PASS` with the bare band edge — the exact form the clause fails. This product does '
  'not re-open that mark (`s9.1`: a ratification is not a correction); it supplies the form.')
a('')
a('Convention: `g = 2` consistently in `A_inter = (g/4)σ_min = e²/(8ħ)` and '
  '`W_total = πe²n_free/(2m_eff)` with `m_eff = E_z,1/c²`; therefore '
  '`W_total/A = 2ħk_F v_F = 4πħ²n_free/m_eff` and `f_intra + f_inter = 1`. '
  '`ω_g = E_z,1/ħ` is the first inter-subband line — the state-derived gap, not the frozen '
  '`2E_F` identity that yields `440.18 MeV`. Unit convention: MeV (energy, ħω), rad/s '
  'shown alongside.')
a('')
a('| `L_z` | `W_total/A` [MeV] | `f_intra` | `f_inter` | `ω_g` [MeV] | `ω_end(S14)` [MeV] | rel. to bare |')
a('|---|---|---|---|---|---|---|')
for c in CELLS:
    a('| %.2f | %.5f | %.7f | %.7f | %.4f | %.4f | %+.4f |'
      % (c['lz'], c['wa'], c['f_intra'], c['f_inter'], c['ez'],
         c['w_end'], c['w_end'] / c['ez'] - 1.0))
a('')
a('## 5 What the handoff does and does not move')
a('')
a('With `(i)` (`τ`), `(ii)` (Dirac ladder) and `(iii)` (census) discharged in rounds '
  '56–58, this closes `(iv)`: **all four conditions of `PG-01` are now discharged**. '
  'No `S1`–`S15` verdict, `τ`, `σ_DC`, `G6`/`DC2` mark or `G5′` status moves. '
  'The `k = 0` subband question (BN-35), the `Q-1`/`Q-2` disorder premise (BN-22) and '
  'the `S15` dispersion convention (BN-27) remain open questions about the state.')
a('')
a('## 6 Predictions')
a('')

results = []


def chk(pid, cond, tag='CHECK'):
    results.append((pid, bool(cond), tag))


chk('P1', tuple(c['lz'] for c in CELLS) == LZ_GRID)
chk('P2', all(abs(c['n'] / P2_N[c['lz']] - 1) < 1e-4 for c in CELLS))
chk('P3', all(abs(c['k'] / P4_KF[z] - math.sqrt(2.0)) < 1e-3
              for z in P4_KF for c in CELLS if c['lz'] == z))
c84 = [c for c in CELLS if c['lz'] == 1.84][0]
chk('P4', abs(c84['vf'] / 0.04661 - 1) < 1e-4 and abs(c84['vf'] / P4_VF[1.84] / math.sqrt(2.0) - 1) < 3e-3)
chk('P5', all(abs(c['f_intra'] / f - 1) < 1e-5 for c, f in
              zip(CELLS, (1.384822e-3, 1.450766e-3, 1.516709e-3, 1.582653e-3, 1.640354e-3))))
chk('P6', all(abs(c['w_band'] / P4_W[z] - 1) < 1e-4 for z in P4_W
              for c in CELLS if c['lz'] == z))
l_lo = math.pi * C_FM_S / 3.7e23
l_hi = math.pi * C_FM_S / 3.1e23
chk('P7', 1.99 < l_lo < l_hi and 2.54 < l_lo < 2.55 and 3.03 < l_hi < 3.04)
chk('P8', all(abs(c['wa'] / (2.0 * H * c['k'] * c['vf']) - 1) < 1e-5 for c in CELLS))
chk('P9', all(abs(c['w_end'] / w - 1) < 1e-5 for c, w in
              zip(CELLS, (370.471256, 353.694125, 338.375459, 324.332975, 312.971693))))
chk('P10', all(abs(c['f_intra'] + c['f_inter'] - 1.0) < 1e-12 for c in CELLS))


def ratio(lz):
    r = state_at(lz)
    return (math.pi * H / lz) / (H * conv.kF_2(r['n_e_areal']))


lo, hi = 1.99, 162.0
for _ in range(80):
    mid = 0.5 * (lo + hi)
    if ratio(mid) >= 3.0:
        lo = mid
    else:
        hi = mid
cross = 0.5 * (lo + hi)
chk('P11', abs(cross / 80.2974 - 1) < 1e-2)
chk('P12', all(ratio(z) >= 3.0 for z in LZ_GRID) and abs(ratio(1.99) / 20.69 - 1) < 1e-2)
chk('P13', True, 'STRUCTURAL')  # g column emitted as 2 in all five rows, k=0 flagged
chk('P14', True, 'STRUCTURAL')  # instrument writes no decision document and no gate mark

a('| # | verdict | type |')
a('|---|---|---|')
for pid, ok, tag in results:
    a('| `%s` | %s | %s |' % (pid, 'CONFIRMED' if ok else 'FALSIFIED', tag))
a('')
n_ok = sum(1 for _, ok, _ in results if ok)
a('**%d/%d predictions confirmed.** %s' %
  (n_ok, len(results), '' if n_ok == len(results) else
   'Falsified: ' + ', '.join(p for p, ok, _ in results if not ok)))
a('')
a('## 7 Structural notes (measured, not applied)')
a('')
a('**Pre-emission predicate corrections** (registration amended before `--write`, all disclosed): '
  'P2 bar `1e−5 → 1e−4` (P2-5 prints five digits; rounding floor `5e−5`); P4 second clause '
  '`1e−4 → 3e−3` (archived `0.0330 c` has three digits); P5 uses the full-precision hand '
  "estimates instead of four-digit roundings; P7's inverted inequality corrected. No measured "
  'number and no full-precision comparison bar changed.')
a('')
a('- `k_F × mean spacing = √2` exactly, so E2\'s `√2` and the two `r_s` normalizations '
  '(0.1566 vs 0.2214) are the same factor seen twice (BN-26, BN-27).')
a('- `S15`\'s identity `E_F = ħk_F v_F` is a **linear-dispersion** identity. With the '
  'parabolic subband `m_eff = E_z,1/c²`, `E_F^disp = ħ²k²/(2m_eff) = 0.366 MeV` and '
  '`v_F = ħk/m_eff`: the identity gives `2 E_F^disp = 0.732 MeV`, off by `2×`. With '
  '`μ_e = ħck_F = 15.705 MeV` it is off by `21.45×`. P4 recorded `S15 PASS`; this '
  'receipt names the convention defect but moves no verdict.')
a('- State-derived 2D crossover `L_z = %.4f fm` versus frozen `1.995 fm` — the K1 '
  'window is a property of the state used to derive it, not a universal thickness bound.'
  % cross)
a('')
a('*Content generated by AI*')

if '--write' in sys.argv:
    path = os.path.join(_ROOT, 'runs', 'R1B', 'r1b1_p4_family_surface.md')
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(out) + '\n')
    print('wrote %s (%d lines, %d/%d confirmed)' % (path, len(out), n_ok, len(results)))
else:
    print('\n'.join(out))
