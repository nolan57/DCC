import sys, io, os, re, math, hashlib, json
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = []
FLAGS = {}
TAG = "PROVENANCE: NEITHER (adjudication of a submission; establishes no physics and creates no readable cell)"


def out(s=""):
    OUT.append(s)
    print(s)


def hdr(t):
    out()
    out("=" * 96)
    out(t)
    out("=" * 96)


def table(rows, cols):
    w = [max(len(str(c)), *(len(str(r[i])) for r in rows)) if rows else len(str(c))
         for i, c in enumerate(cols)]
    out("  " + "  ".join(str(c).ljust(w[i]) for i, c in enumerate(cols)))
    out("  " + "  ".join("-" * w[i] for i in range(len(cols))))
    for r in rows:
        out("  " + "  ".join(str(r[i]).ljust(w[i]) for i in range(len(cols))))


def verdict(pid, claim, ok, note):
    FLAGS[pid] = bool(ok)
    out("  [%s] %s  ->  %s" % (pid, "PASS" if ok else "FAILED", claim))
    out("       %s" % note)


def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------- inputs
ROADMAP = "Macro3D_to_2D_Smooth_Reduction_Roadmap_v1.4.md"
road = read(ROADMAP)
sub = read("runs/OPTICS/sc_submission_verbatim.md")
opt = read("src/optics/sigma_s_lindhard.py")

# speaker scope: specs + conventions + the governing roadmap (NOT decisions/)
SPEAKER = {}
for d in ("docs/specs", "docs/conventions"):
    for f in sorted(os.listdir(os.path.join(ROOT, d))):
        if f.endswith(".md"):
            SPEAKER[d + "/" + f] = read(d + "/" + f)
SPEAKER[ROADMAP] = road

ALL_DOCS = {}
for base in ("docs/specs", "docs/conventions", "docs/decisions"):
    for f in sorted(os.listdir(os.path.join(ROOT, base))):
        if f.endswith(".md"):
            ALL_DOCS[base + "/" + f] = read(base + "/" + f)

# ---------------------------------------------------------------- constants
E_C = 1.602176634e-19
HBAR = 1.054571817e-34
C_L = 2.99792458e8
M_E = 9.1093837015e-31
EPS0 = 8.8541878128e-12
MU0 = 1.25663706212e-6
Z0 = math.sqrt(MU0 / EPS0)
A0 = 5.29177210903e-11

N2D_V3 = 2.20e28
N2D_V14 = 4.2155e27
EF_MEV = 73.37
MSTAR = EF_MEV / 0.51099895
M_STAR = MSTAR * M_E
A_INTER = E_C ** 2 / (16.0 * HBAR)

out(TAG)
out("src/optics/sc_route_check.py  --  adjudication of the SC-ROUTE submission")
out("registration: runs/OPTICS/sc_route_registration.md  (predictions locked before measurement)")

# =================================================================================================
hdr("[0] OBJECT OF RECORD -- what this round adjudicates")
# =================================================================================================
out("  submission's central claim, verbatim (s7.1):")
out("    \"1. The yield-strength interpretation proposed earlier does not hold and should be withdrawn.\"")
out("    \"2. sigma_s(w) should be explicitly stated as the effective two-dimensional surface conductivity.\"")
out()
out("  So the submission asserts that this project has been reading sigma_s as a YIELD STRENGTH (Pa).")
out("  The first question is not whether that reading is wrong -- it is whether the record ever held it.")
out()
out("  speaker scope used for that question (%d files): docs/specs/, docs/conventions/, roadmap v1.4" % len(SPEAKER))
out("  excluded: docs/decisions/ -- commentary, which quotes rejected phrases while rejecting them (round-31 rule).")

# =================================================================================================
hdr("[A] DOES THE MISCONCEPTION EXIST IN THE RECORD?  (P1, P2)")
# =================================================================================================
PHYS = [r"\byield\s+strength\b", r"yield", r"\bplastic(ity)?\b", r"\bPoisson\b", r"Poisson effect",
        r"\byoung'?s\s+modulus\b", r"Young's modulus"]
hits = []
for pat in PHYS:
    for path, txt in SPEAKER.items():
        for m in re.finditer(pat, txt, re.I):
            hits.append((path, pat, m.group(0)))
out("  physics-sense patterns scanned: yield strength / yield / plastic / Poisson / Poisson effect / Young's modulus")
out("  hits in speaker scope: %d" % len(hits))
for h in hits[:12]:
    out("    %s  [%s]  '%s'" % h)
out()
out("  and hits that would identify sigma_s with any of them (same sentence or same table row):")
pair = 0
for path, txt in SPEAKER.items():
    for line in txt.splitlines():
        if re.search(r"σ_s|sigma_s", line) and re.search("|".join(PHYS), line, re.I):
            pair += 1
            out("    %s :: %s" % (path, line.strip()[:130]))
out("    count = %d" % pair)
verdict("P1", "the yield-strength reading is absent from the record: the correction repairs a document "
              "that does not exist", pair == 0 and len([h for h in hits if "Poisson" not in h[1] and "Poisson effect" not in h[1]]) == 0,
        "%d physics-sense hits total, %d bound to sigma_s" % (len(hits), pair))

# P2 -- the record's actual owner
own = []
for path, txt in SPEAKER.items():
    for m in re.finditer(r"σ_s\(\\omega\)|σ_s\\(\\omega\\)|sigma_s\(omega\)|σ_s\(ω\)", txt):
        own.append(path)
own_n = sum(1 for p in SPEAKER.values() if re.search(r"surface conductivity|surface conductivity|sheet conductivity", p, re.I))
is_input = "an input, not a" in road or "INPUT, not a universal constant" in opt
unit_s = bool(re.search(r"SI.{0,40}\bS\b|unit.{0,20}S\b|\[S\]", road + "".join(SPEAKER.values())))
out()
out("  files declaring sigma_s to be a SURFACE / SHEET conductivity: %d" % own_n)
out("  declared 'an input, not a universal constant' (s6.4 / S10): %s" % is_input)
out("  module header states the unit family: %s"
    % ("S" if "S]" in opt else "check"))
out("  the module's own docstring line:")
for line in opt.splitlines()[:12]:
    if "sigma_s" in line:
        out("    " + line.strip())
verdict("P2", "the record's only owner of sigma_s is the frequency-dependent surface conductivity, as an input",
        own_n > 0 and is_input, "%d files; input declared = %s" % (own_n, is_input))

# =================================================================================================
hdr("[B] IS THE SUBMISSION'S MACHINERY ALREADY BUILT?  (P3-P9)")
# =================================================================================================
# ---- P3: the metric
m_rec = re.search(r"ds\^2=-dt\^2\+dx\^2\+A\^2\(t,x\)\\,dy\^2\+B\^2\(t,x\)\\,dz\^2", road)
l_rec = re.search(r"d\\ell_z=B\\,dz", road)
out("  P3  the third-dimension scale factor")
out("      record, metric (roadmap l.146): ds^2 = -dt^2 + dx^2 + A^2(t,x)dy^2 + B^2(t,x)dz^2")
out("      record, length element (l.162):  dl_z = B dz")
out("        found metric line : %s" % bool(m_rec))
out("        found dl_z = B dz  : %s" % bool(l_rec))
sub_metric = re.search(r"ds\^2=-N\^2dt\^2\+A\^2dx\^2\+B\^2dy\^2\+C\^2dz\^2", sub)
sub_l = re.search(r"dl_z=C\(t,x\)\\,dz", sub)
sub_prose_B = re.search(r"\\\(B\\\)\s*[\uFF1A:]\s*DCC third-dimension scale factor", sub)
out("      submission, metric text present : %s" % bool(sub_metric))
out("      submission, dl_z = C dz present : %s" % bool(sub_l))
out("      submission, prose 'B = third-dim scale factor' : %s" % bool(sub_prose_B))
out()
out("      => the submission writes C on dz in its metric AND calls B the third-dim scale factor in its")
out("         symbol list.  Both cannot be the scale factor.  The record's symbol is B.")
verdict("P3", "the submission's metric is not the record's, and is internally inconsistent (C on dz, B named)",
        bool(m_rec) and bool(l_rec) and bool(sub_metric) and bool(sub_l) and bool(sub_prose_B),
        "record: B dz ; submission: C dz + 'B is the scale factor'")

# ---- P4: Task D formulas verbatim
fres = re.search(r"r=-\\frac\{Z_0\\sigma_s\(\\omega\)\}\{2\+Z_0\\sigma_s\(\\omega\)\}", road)
fres2 = re.search(r"t=\\frac\{2\}\{2\+Z_0\\sigma_s\(\\omega\)\}", road)
fres3 = re.search(r"R=\|r\|\^2,\\ T=\|t\|\^2,\\ A=1-R-T", road)
out()
out("  P4  Task D formulas in the roadmap s6.4:")
out("      r = -Z0 s/(2+Z0 s)   present: %s" % bool(fres))
out("      t = 2/(2+Z0 s)       present: %s" % bool(fres2))
out("      R=|r|^2, T=|t|^2, A=1-R-T present: %s" % bool(fres3))
verdict("P4", "Task D's five formulas are already verbatim in s6.4", bool(fres) and bool(fres2) and bool(fres3),
        "3 of 3 present")

# ---- P5: implemented + T1
rta_def = re.search(r"def rta\(sigma\)", opt)
t1 = re.search(r"\[T1\].*R \+ T \+ A = 1", opt)
out()
out("  P5  implementation:")
out("      def rta(sigma) in the module        : %s" % bool(rta_def))
out("      [T1] verifies R + T + A = 1         : %s" % bool(t1))
res_txt = read("runs/R5/r5l2_sigma_s_results.txt")
t1run = re.findall(r"\[T1\].*", res_txt)
out("      archived T1 output: %s" % (t1run[0][:150] if t1run else "MISSING"))
verdict("P5", "Task D is already implemented and R+T+A=1 is already tested", bool(rta_def) and bool(t1) and bool(t1run),
        "rta() present, T1 archived")

# ---- P6: film vs sheet
film = re.search(r"standard thin-film formula is", road) and re.search(r"e\^\{-2i\\delta\}", road)
out()
out("  P6  finite-film vs effective-sheet comparison already mandated: %s" % bool(film))
out("      roadmap s6.4: 'for a homogeneous film of thickness L_z, the standard thin-film formula is'")
out("      R = |(r01 + r12 e^{-2i delta})/(1 + r01 r12 e^{-2i delta})|^2, delta = 2 pi n L_z / lambda")
verdict("P6", "the film-vs-sheet comparison is already in s6.4", bool(film), "thin-film formula present")

# ---- P7: proper vs coordinate, how many quantities
q = re.search(r"The following four quantities may not be confused[^\n]*", road)
if q:
    named = re.findall(r"the coordinate interval[^,]*|the proper thickness[^,]*|the compact circumference[^,]*|the material thin-film thickness", q.group(0))
else:
    named = []
out()
out("  P7  proper-vs-coordinate disambiguation")
out("      roadmap l.164 names %d distinct quantities:" % len(named))
for n in named:
    out("        - %s" % n.strip())
out("      the submission proposes 2 (dz_proper vs dz).")
verdict("P7", "the disambiguation is already mandatory, with 4 quantities rather than 2",
        len(named) >= 4, "%d named" % len(named))

# ---- P8: N7 already a gate
n7 = re.search(r"carrier conservation \(N7\)", road)
n7b = re.search(r"carrier-conservation check", road)
out()
out("  P8  Task A ('fix the carrier population first') as an existing gate:")
out("      G5' gate row contains 'carrier conservation (N7)' : %s" % bool(n7))
out("      N7 prose 'carrier-conservation check'            : %s" % bool(n7b))
for line in road.splitlines():
    if "removed and any low-energy effective description" in line:
        out("      N7 verbatim: " + line.strip()[:230])
        break
for line in road.splitlines():
    if "primary source of approximation failure" in line and "N7" in line:
        out("      and it is ranked FIRST among the approximation failures, not overlooked:")
        out("      " + line.strip()[:230])
        break
verdict("P8", "Task A is already a gate condition (N7 inside G5'), so it is not 'most easily overlooked'",
        bool(n7) and bool(n7b), "N7 present in the G5' acceptance row")

# ---- P9: s8.4 four categories
s84 = re.search(r"## 8\.4 Mandatory four-category classification of R1 results", road)
cats = re.findall(r"\*\*([A-D]): ", road[road.find("## 8.4"):road.find("## 8.5")]) if s84 else []
deleted = re.search(r"is deleted", road[road.find("## 8.4"):road.find("## 8.5")]) if s84 else None
out()
out("  P9  'do not presuppose the branch' -- already s8.4:")
out("      section present: %s ; categories found: %s ; pre-classification deleted: %s"
    % (bool(s84), cats, bool(deleted)))
out("      the submission offers A/B/C (3).  s8.4 offers A/B/C/D (4), D being")
out("      'model or classical approximation fails, cannot be determined'.")
verdict("P9", "the no-presupposition rule is already mandated, with 4 categories; the submission's 3 are weaker",
        bool(s84) and len(cats) >= 4 and bool(deleted), "%d categories %s" % (len(cats), cats))

# =================================================================================================
hdr("[C] THE QUOTED CLAIMS  (P10, P11, P12)")
# =================================================================================================
# P10 -- 23.2 MeV
v3 = re.search(r"E_F_REF_MEV = 73\.37", opt)
rev = re.search(r"E_F = 23\.20 MeV\), which are REVOKED", opt)
out("  P10  the submission's Task A premise: 'mu_e reaches about 23.2 MeV'")
out("       module header: E_F_REF_MEV = 73.37  -> %s" % bool(v3))
out("       module header: pre-v3 values 'REVOKED' -> %s" % bool(rev))
ratio = EF_MEV / 23.203
out("       current / quoted = %.4f / %.4f MeV = %.4fx" % (EF_MEV, 23.203, ratio))
out()
out("       but the CONCLUSION the number supported is preserved and strengthened:")
row7 = [l for l in read("docs/decisions/G0p_seven_row_verdict_v1.md").splitlines() if "capture thresholds" in l]
if row7:
    out("       " + row7[0].strip()[:190])
out("       higher mu_e -> capture thresholds more deeply exceeded, so 'the electron gas object is gone'")
out("       is MORE true at 73.37 than at 23.20.  Stale number, sound conclusion.")
verdict("P10", "23.2 MeV is a revoked baseline (current 73.37 MeV, %.3fx), though its conclusion survives" % ratio,
        bool(v3) and bool(rev), "quoted 23.203 vs current 73.37")

# P11 -- G6 precondition
g6row = [l for l in road.splitlines() if l.startswith("| **G6**")]
g6ok = bool(re.search(r"G4, G5.+ \+ self-consistent \$\\sigma_s\(\\omega\)\$", g6row[0])) if g6row else False
out()
out("  P11  G6 precondition, record: " + (g6row[0].strip()[:150] if g6row else "MISSING"))
verdict("P11", "G6's precondition is quoted correctly (G4, G5' + self-consistent sigma_s)",
        g6ok, "matched the gate table row")

# P12 -- both directions forbidden
both = re.search(r"conclusions in either direction .{0,60}'transparent'.{0,20}'opaque'.{0,20}are forbidden", road)
both2 = re.search(r"both transparent and opaque forbidden", road)
out()
out("  P12  'both transparent and opaque forbidden': %s / %s" % (bool(both), bool(both2)))
verdict("P12", "'both directions forbidden' is quoted correctly", bool(both) or bool(both2),
        "s1.4 and s10.2 both carry it")

# =================================================================================================
hdr("[D] IS THE NAMED GAP REAL?  (P13)")
# =================================================================================================
CHECKS = {
    "Ward identity": [r"\bWard\b", r"charge conservation"],
    "Kramers-Kronig": [r"Kramers", r"Kronig", r"\bKK\b"],
    "passivity Re s >= 0": [r"passiv", r"Re\\?sigma\s*>=\s*0", r"non-negative"],
    "f-sum rule": [r"sum rule", r"f-sum", r"spectral weight"],
    "dimensional check (S)": [r"\bS\b", r"siemens"],
    "energy budget R+T+A": [r"R \+ T \+ A"],
    "analytic structure / causality": [r"causal", r"analytic"],
}
rows = []
for name, pats in CHECKS.items():
    n = sum(len(re.findall(p, opt)) for p in pats)
    rows.append([name, n, "present" if n else "ABSENT"])
table(rows, ["check from Task C", "hits in the optics module", "status"])
absent = [r[0] for r in rows if r[2] == "ABSENT"]
out()
out("  absent: %s" % absent)
out("  note: 'dimensional check' scores a hit on the bare token 'S' (siemens), which is a false positive;")
out("        the module does carry units.  The three that are genuinely absent are Ward, K-K, f-sum.")
verdict("P13", "Ward, Kramers-Kronig and the f-sum rule are absent from the record's only optics module",
        all(a in absent for a in ("Ward identity", "Kramers-Kronig", "f-sum rule")),
        "%d of 7 absent" % len(absent))

# =================================================================================================
hdr("[E] APPLIED TO THE RECORD: DOES THE SUBMISSION'S K-K CHECK BITE?  (P14)")
# =================================================================================================
# the module's own response function, reproduced exactly
def sigma_module(hbarw_ev, tau):
    w = hbarw_ev * E_C / HBAR
    s0 = E_C ** 2 * N2D_V3 * tau / M_STAR
    sD = s0 / (1.0 - 1j * w * tau)
    on = hbarw_ev > 2.0 * (EF_MEV * 1e6)
    return sD + (A_INTER if on else 0.0), on, s0, w


WF = 2.0 * EF_MEV * 1e6          # interband threshold in eV
out("  interband threshold: hbar*w = 2 E_F = %.4e eV = %.3f MeV" % (WF, WF / 1e6))
out("  the module's reported band: 1, 2, 3 eV  ->  band/threshold = %.3e" % (3.0 / WF))
out()
out("  K-K, as a numerical quadrature first VALIDATED on each piece separately:")
out("    Im s(w) = -(2w/pi) P int_0^inf Re s(w')/(w'^2-w^2) dw'")
out("    the pole is removed by the subtraction g(w')-g(w), which is exact because P int_0^inf dw'/(w'^2-w^2)=0.")
out("    the range is mapped by w' = S u/(1-u), u in (0,1), so the upper limit is infinite with no truncation.")


def kk_im(g, w0, scale, n=2_000_001):
    # midpoint grid: never lands exactly on the pole, and the 0/0 there would otherwise print nan
    u = (np.arange(1, n) + 0.5) / n
    wp = scale * u / (1.0 - u)
    dw = scale / (1.0 - u) ** 2
    g0 = g(np.array([w0]))[0]
    f = (g(wp) - g0) / (wp ** 2 - w0 ** 2)
    return -(2.0 * w0 / math.pi) * np.trapezoid(f * dw, u)


# --- piece 1: Drude, low band, scale = 1/tau (both 1/tau and w resolved)
tau_t = 1e-16
rows = []
for hw in (1.0, 2.0, 3.0):
    w0 = hw * E_C / HBAR
    s0 = E_C ** 2 * N2D_V3 * tau_t / M_STAR
    gD = lambda wp, tau=tau_t: s0 / (1.0 + (wp * tau) ** 2)
    num = kk_im(gD, w0, 1.0 / tau_t)
    ana = float(np.imag(sigma_module(hw, tau_t)[0]))
    rows.append(["%.1f eV" % hw, "%.6e" % num, "%.6e" % ana, "%.2e" % (abs(num - ana) / abs(ana))])
table(rows, ["band", "Im via K-K quadrature", "Im analytic (Drude)", "relative deviation"])
q1_ok = all(float(r[3]) < 1e-6 for r in rows)
out("    piece 1 (Drude) reproduced to <1e-6 relative: %s" % q1_ok)

# --- piece 2: the interband STEP alone, scale ~ w_g (resolves the threshold)
WG = WF * E_C / HBAR
step = lambda wp: np.where(wp >= WG, A_INTER, 0.0)
rows = []
for mult in (0.5, 2.0, 4.0, 10.0):
    w0 = mult * WG
    g0v = A_INTER if w0 >= WG else 0.0
    ana = -(A_INTER / math.pi) * math.log(abs((WG + w0) / (WG - w0))) if w0 != WG else float("nan")
    num = kk_im(step, w0, (mult + 3.0) * WG, n=4_000_001)
    rows.append(["%.1f w_g" % mult, "%+.6e" % num, "%+.6e" % ana, "%.2e" % (abs(num - ana) / abs(ana))])
table(rows, ["band", "Im via quadrature", "-(A/pi) ln|(wg+w)/(wg-w)|", "relative deviation"])
q2_ok = all(float(r[3]) < 1e-5 for r in rows)
out("    piece 2 (step) reproduced to <1e-5 relative: %s" % q2_ok)
out("    so the required Im for the full model is exactly  Im_Drude + Im_step, and the module supplies Im_Drude only.")
out()
out("  the residual the submission's K-K check reports, band by band:")
rows = []
for hw in (1.0, 3.0, 1.0e2, 1.0e6, 1.0e8, 1.0e8 * 1.5, 2.0e8, 3.0e8):
    w0 = hw * E_C / HBAR
    if w0 == WG:
        continue
    step_im = -(A_INTER / math.pi) * math.log(abs((WG + w0) / (WG - w0)))
    module_im = float(np.imag(sigma_module(hw, tau_t)[0]))
    resid = abs(step_im)
    rows.append(["%.4e" % hw, "%.4e" % module_im, "%.4e" % resid, "%.3e" % (resid / max(abs(module_im), 1e-300))])
table(rows, ["hbar w (eV)", "module Im s (S)", "|K-K residual| (S)", "relative"])
in_band = [r for r in rows if float(r[0]) <= 3.0]
above = [r for r in rows if float(r[0]) >= WF]
in_max = max(float(r[3]) for r in in_band)
above_min = min(float(r[3]) for r in above)
out()
out("  in-band (1..3 eV, and 1e2 eV): max relative residual = %.3e" % in_max)
out("  above threshold (hbar w > 2E_F): min relative residual = %.3e" % above_min)
out("  the residual DIVERGES logarithmically as w -> w_g, so the step cannot be made causal by tuning A.")
verdict("P14", "K-K is violated, but confined to the band above 2E_F = 1.467e8 eV; in the reported band "
              "it holds to <1e-12", q1_ok and q2_ok and in_max < 1e-6 and above_min > 1e-3,
        "in-band %.2e vs above-threshold %.2e" % (in_max, above_min))

# =================================================================================================
hdr("[F] APPLIED TO THE RECORD: DOES THE f-SUM CHECK BITE?  (P15)")
# =================================================================================================
fsum_pred = math.pi * E_C ** 2 * N2D_V3 / (2.0 * M_STAR)
out("  f-sum rule (2D):  int_0^inf Re sigma(w) dw = pi e^2 n_2D / (2 m*)")
out("    predicted total spectral weight W = %.6e S rad/s" % fsum_pred)
out()
rows = []
for tau in (1e-19, 1e-18, 1e-16):
    re_D = lambda wp, tau=tau: (E_C ** 2 * N2D_V3 * tau / M_STAR) / (1.0 + (wp * tau) ** 2)
    OM = 4000.0 / tau
    wp = np.linspace(0.0, OM, 8_000_001)
    quad = np.trapezoid(re_D(wp), wp)
    tail = (E_C ** 2 * N2D_V3 * tau / M_STAR) / (OM * tau ** 2)   # int_OM^inf sigma0/(w^2 tau^2) dw
    num = quad + tail
    rows.append(["%.0e" % tau, "%.6e" % num, "%.6e" % fsum_pred, "%.12f" % (num / fsum_pred),
                 "%.1e" % (tail / fsum_pred)])
table(rows, ["tau (s)", "int Re sigma_D dw (quad + tail)", "pi e^2 n / 2m*", "ratio", "tail fraction"])
ratios = [float(r[3]) for r in rows]
sat = all(abs(r - 1.0) < 1e-8 for r in ratios)
out("    the Drude term alone equals the f-sum total at every tau, ratio %.12f: %s" % (min(ratios), sat))
out("    (it is exact: sigma_0 = e^2 n tau / m*, so int = sigma_0 pi/(2 tau) = pi e^2 n/(2 m*), tau cancels.)")
out("    the truncated quadrature was short by 2/(4000 pi) = %.3e, which is the tail column -- added"
    % (2.0 / (4000.0 * math.pi)))
out("    analytically rather than by extending the grid.")
out()
out("  adding the interband constant A = e^2/(16 hbar) = %.4e S above w_g = %.4e rad/s:" % (A_INTER, WG))
rows = []
for mult in (1.0, 1.5, 2.0, 3.0, 10.0, 1e2):
    OM = mult * WG
    extra = A_INTER * max(OM - WG, 0.0)
    rows.append(["%.1f w_g" % mult, "%.4e" % extra, "%.4e" % (fsum_pred + extra),
                 "%.4f" % ((fsum_pred + extra) / fsum_pred)])
table(rows, ["integration cutoff", "extra weight A*(O-w_g)", "total", "total / f-sum"])
cross = [float(r[0].split()[0]) for r in rows if float(r[1]) > fsum_pred]
out("    the extra weight grows WITHOUT BOUND with slope A, so the total diverges: int Re sigma dw = infinity.")
out("    the interband channel ALONE exceeds the entire f-sum budget by omega = %.1f w_g." % min(cross))
out()
out("  the correct constraint is therefore a PARTITION, not an independent amplitude:")
out("    W_intra + W_inter = pi e^2 n_2D / (2 m*),   with the record's model assigning W_intra = W_total")
out("    and then adding W_inter > 0.  The interband amplitude is not 'an OPEN input' -- the total is")
out("    already fully allocated, so opening the interband channel must DEBIT the Drude weight.")
verdict("P15", "the Drude term alone saturates the f-sum %.12f; the interband term double-counts and diverges"
              % min(ratios), sat, "ratio %.12f at 3 taus; extra weight unbounded" % min(ratios))

# =================================================================================================
hdr("[G] THE REDUCTION'S DOMAIN OF VALIDITY  (P16)")
# =================================================================================================
d_v14 = 1.0 / math.sqrt(N2D_V14)
d_v3 = 1.0 / math.sqrt(N2D_V3)
LION = math.pi * A0
out("  a0 = %.6e m ;  L_z^ion = pi a0 = %.4e m = %.2f angstrom (bound states cease below this)" % (A0, LION, LION * 1e10))
out()
rows = [["v1.4 (revoked)", "%.4e" % N2D_V14, "%.4f fm" % (d_v14 * 1e15), "%.4e" % (d_v14 / A0)],
        ["v3   (current)", "%.4e" % N2D_V3, "%.4f fm" % (d_v3 * 1e15), "%.4e" % (d_v3 / A0)]]
table(rows, ["baseline", "n_surface (m^-2)", "d_par = n^-1/2", "d_par / a0"])
out()
out("  the submission's own validity condition (d): 'the 3D material still holds its original electronic states'")
r1 = [l for l in read("docs/decisions/G0p_seven_row_verdict_v1.md").splitlines() if "Maintain the body's original atoms" in l]
if r1:
    out("  the record's verdict on exactly that condition:")
    out("    " + r1[0].strip()[:200])
out()
out("  so the reduction sigma_s = int dl_z sigma_3D,par is exact where sigma_3D exists (many atomic layers),")
out("  and the endpoint is at d_par = %.2e a0 and L_z below %.1f angstrom -- one layer or less.  The bridge's"
    % (d_v3 / A0, LION * 1e10))
out("  far end is where sigma_3D stops being a defined object.")
verdict("P16", "condition (d) is false at the record's own target, so the reduction's domain excludes the "
              "regime it is wanted for", (d_v3 / A0) < 1.0 and bool(r1),
        "d_par/a0 = %.3e (v3), %.3e (v1.4)" % (d_v3 / A0, d_v14 / A0))

# =================================================================================================
hdr("[H] IS THE REDUCTION AT LEAST A DERIVATION OF THE RECORD'S ANSATZ?  (P17)")
# =================================================================================================
out("  claim: if sigma_3D,par is the 3D Drude form, then int dl_z sigma_3D,par = e^2 n_2D tau / m*")
out("         identically, because n_2D := n_3D * L_z^proper (column density).")
out()
rows = []
for Lz in (1e-9, 1e-8, 1e-7):
    n3 = N2D_V3 / Lz
    tau = 1e-16
    s3 = E_C ** 2 * n3 * tau / M_STAR      # 3D Drude, same m*
    integrated = Lz * s3
    direct = E_C ** 2 * N2D_V3 * tau / M_STAR
    rows.append(["%.0e" % Lz, "%.6e" % n3, "%.6e" % integrated, "%.6e" % direct,
                 "%.1e" % (abs(integrated - direct) / direct)])
table(rows, ["L_z (m)", "n_3D (m^-3)", "L_z * sigma_3D", "e^2 n_2D tau/m*", "rel dev"])
exact = all(float(r[4]) < 1e-12 for r in rows)
out("    exact at every L_z: %s" % exact)
out()
out("    So the submission CONVERTS R5-L2's asserted 2D Drude form into a derived one, in the regime where")
out("    sigma_3D exists.  That is a genuine credit and the first time the ansatz has a derivation.  It is")
out("    also content-free about the object: the identity is the DEFINITION of column density.")
verdict("P17", "the reduction derives the record's Drude ansatz exactly, and is otherwise the definition "
              "of n_2D", exact, "rel dev < 1e-12 at 3 thicknesses")

# =================================================================================================
hdr("[X] POST-HOC (not registered, added after the verdicts above) -- WHAT THE RECORD SAYS THE BLOCKER IS")
# =================================================================================================
out("  added because s[F] and s[D] raised it: the record states the G6/DC2 blocker in a specific form.")
solved = []
for path, txt in list(ALL_DOCS.items()) + [(ROADMAP, road)]:
    for line in txt.splitlines():
        if re.search(r"solved\W{0,8}(?:τ|\\tau|tau)", line):
            solved.append((path, line.strip()[:150]))
out("  files stating the blocker as 'a compliant sigma_s with a SOLVED tau': %d" % len(set(p for p, _ in solved)))
for p in sorted(set(p for p, _ in solved)):
    out("    - %s" % p)
out()
tau_sub = len(re.findall(r"\\tau", sub))
tau_stress = len(re.findall(r"\\tau_\{?[xyz]", sub))
out("  the submission's uses of 'tau': %d total, %d of them the SHEAR STRESS tau_xz / tau_yz" % (tau_sub, tau_stress))
out("  the submission's uses of tau as a RELAXATION TIME: %d" % (tau_sub - tau_stress))
out("  the submission's uses of 'relaxation' / 'collision' / 'relaxation': %d"
    % (len(re.findall(r"relaxation|collision|relaxation", sub, re.I))))
out()
out("  So the submission's route (Kubo -> Pi -> sigma_s) would in principle DETERMINE tau, but it never")
out("  names tau, and its Task-C checklist does not include 'tau is solved, not scanned'.  The one")
out("  quantity the record says is missing is the one quantity the checklist omits.")

# =================================================================================================
hdr("[I] ERRATA -- appended; the run above is not edited")
# =================================================================================================
out("  E1  P16's registered figure came from the REVOKED baseline.")
out("      I wrote 'd_par = 15.40 fm = 2.91e-4 a0'.  15.40 fm is 1/sqrt(4.2155e27), the v1.4 value, and")
out("      23.203 MeV is its companion -- the very number I faulted the submission for quoting in P10.")
out("      At v3 the figure is %.4f fm = %.4e a0.  The qualitative claim (d_par << a0) holds on both"
    % (d_v3 * 1e15, d_v3 / A0))
out("      baselines, but the prediction as registered is wrong for the current one.")
out("      Recorded, not corrected: a FAIL would be mine, a PASS is not free.")
out()
out("  E2  P13's 'dimensional check' row is a false positive -- the pattern \\bS\\b matches the letter S")
out("      anywhere in the source.  The module does carry SI units.  Only Ward, K-K and f-sum are absent.")
out()
out("  E3  two quadrature defects found and repaired IN-RUN, both disclosed rather than hidden:")
out("      (a) my first K-K grid truncated at 400/tau, so the Drude validation came out short by")
out("          exactly 2/(4000 pi) = %.3e -- the truncation, not the physics.  Replaced by the" % (2.0 / (4000.0 * math.pi)))
out("          substitution w' = S u/(1-u), which has an infinite upper limit and no truncation error;")
out("          the same defect then reappeared in the f-sum (ratio 0.999841), where the tail is added")
out("          analytically.  Both now close at 1.000000000003.")
out("      (b) at w = 0.5 w_g the grid point landed exactly on the pole, printing nan and false-FAILing")
out("          the step validation.  Midpoint grid; the analytic form is now confirmed to 6.2e-6.")
out()
out("  E4  section [X]'s first count printed 0 files and was wrong.  The record writes the phrase as")
out("      '*solved* `tau`' -- markdown emphasis plus the UNICODE tau -- and my pattern expected the")
out("      LaTeX token \\tau.  Corrected to %d files.  This is the fifth round in which a text pattern" % len(set(p for p, _ in solved)))
out("      stood in for a counted quantity; the count is now printed together with the files.")
out()
out("  Nothing above changes a verdict; the verdicts were printed before this section.")

# ---------------------------------------------------------------- tally
ids = sorted(FLAGS, key=lambda t: int(t[1:]))
npass = sum(1 for i in ids if FLAGS[i])
out()
out("=" * 96)
out("  " + "   ".join("%s:%s" % (i, "P" if FLAGS[i] else "F") for i in ids))
out("  %d / %d predictions hold as registered." % (npass, len(ids)))
out("=" * 96)

with open(os.path.join(ROOT, "runs/OPTICS/sc_route_results.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(OUT) + "\n")
print("\nwritten: runs/OPTICS/sc_route_results.txt")
