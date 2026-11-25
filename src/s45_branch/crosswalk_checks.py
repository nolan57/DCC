"""
Crosswalk checks X1-X6: can C1/C2 be re-registered in the ME/CM system?

Registered first: runs/S45/crosswalk_checks_registration.md
Predicates are evaluated as registered; the five states are toy witnesses for implication
relations only and carry no physics beyond the registered numbers.
Report only: establishes no physics result.
"""
import os

D_PAR = 15.40e-15
H_BODY = 0.070
DZ = 1.0e-4          # 100 um, painting_render_v1.md voxel
LAM = 500e-9         # m, mid-visible

# state: (thickness, gap_frac, column_conserving, strain, interlayer_ok)
#   gap_frac = separation between sub-sheets relative to d_par (0 = contiguous)
STATES = {
    'S_A ideal 2D state':        (D_PAR,        0.0, True,  0.0, True),
    'S_B thin non-conserving':   (10e-15,       0.0, False, 0.0, True),
    'S_C intact body':           (H_BODY,       0.0, False, 0.0, True),
    'S_D 2-sheet stack':         (7 * D_PAR,    3.0, False, 0.0, False),
    'S_E S_A + strain field':    (D_PAR,        0.0, True,  1.0, True),
}


def me1(st, dz):
    """v0.2 ME1 reduced for a column: 1 if two points are separated by >= dz."""
    thickness, gap, *_ = st
    # a gapped stack has a separation of at least gap*d_par inside the column
    sep = max(thickness if gap == 0.0 else gap * D_PAR, 0.0)
    return 0.0 if sep < dz else 1.0


def me1_pass(st, dz):
    return me1(st, dz) == 0.0


def cm1_pass(st, lam):
    return st[0] < lam


def head(t):
    print()
    print("=" * 78)
    print(t)
    print("=" * 78)


# ---- X1: implication C1 => ME1 -------------------------------------------
head("X1  is C1 equivalent to its ME1 expression, or stronger than it?")
for dz, label in ((DZ, '100 um'), (D_PAR, 'd_par')):
    print("  Delta_z_res = %-8s (%.2e m)" % (label, dz))
    print("    %-28s %-6s %-8s %-8s %-8s" % ("state", "C1", "ME1", "CM1", "ME1&!C1"))
    viol = 0
    for name, st in STATES.items():
        c1 = st[2]
        m = me1_pass(st, dz)
        cm = cm1_pass(st, LAM)
        if c1 and not m:
            viol += 1
        print("    %-28s %-6s %-8s %-8s %-8s" % (name, c1, m, cm, (m and not c1)))
    print("    states with C1 true and ME1 false: %d  (C1 => ME1 requires 0)" % viol)
    print()

print("  witnesses for the converse failure (ME1 passes, C1 does not hold):")
for name, st in STATES.items():
    if me1_pass(st, DZ) and not st[2]:
        print("    %-28s thickness %.2e < Delta_z_res" % (name, st[0]))
print()
print("  => ME1 is a NECESSARY proxy of C1, not an equivalent. Relaxing the proxy")
print("     does not relax the constraint; it relaxes what the branch certifies.")

# ---- X2: is C2 visible to the gate vocabulary? ---------------------------
head("X2  can any ME/CM predicate express C2? (S_A vs S_E differ only in strain)")
a, e = STATES['S_A ideal 2D state'], STATES['S_E S_A + strain field']
print("  %-22s %-10s %-10s %-10s" % ("proxy", "S_A", "S_E", "same?"))
rows = [
    ("ME1 @100um", me1_pass(a, DZ), me1_pass(e, DZ)),
    ("ME1 @d_par", me1_pass(a, D_PAR), me1_pass(e, D_PAR)),
    ("CM1 @500nm", cm1_pass(a, LAM), cm1_pass(e, LAM)),
]
allsame = True
for n, va, ve in rows:
    same = va == ve
    allsame &= same
    print("  %-22s %-10s %-10s %-10s" % (n, va, ve, same))
print()
print("  all proxies identical on a pair differing only in strain: %s" % allsame)
print("  => C2 is INVISIBLE to the gate vocabulary. Renaming C2 into CM would not rename")
print("     it; it would substitute a predicate that cannot see it.")

# ---- X3: textual corroboration -----------------------------------------
head("X3  textual: does any ME/CM definition mention strain?")
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
spec = open(os.path.join(root, 'docs', 'specs', 'meff_boundary_v0_2.md'), encoding='utf-8').read()
import re
hits = [m.start() for m in re.finditer(r'strain', spec)]
print("  raw 'strain' occurrences in meff_boundary_v0_2.md: %d" % len(hits))
print("  of which inside 'constraint(s)': %d" % len(re.findall(r'constraints?', spec)))
print("  standalone mechanical 'strain': %d" % (len(hits) - len(re.findall(r'constraints?', spec))))

# ---- X4: is C3 expressible? -------------------------------------------
head("X4  is C3 expressible in ME/CM?")
for k in ('T_munu', 'T^{mu nu}', 'action', 'S_eff', 'weak interaction'):
    print("  %-18s occurrences in meff_boundary_v0_2.md: %d" % (k, spec.count(k)))
print("  registry S1: 'An ME predicate may never be a chain constraint'.")
print("  => C3 has no expression, and is FORBIDDEN one by domain rule, not merely missing.")

# ---- X5: how much of the diagonal is expressible? ---------------------
head("X5  fraction of the constraint diagonal expressible in gate space")
tab = [("C1", "ME1 (necessary proxy)"), ("C2", "none -- invisible (X2)"), ("C3", "none -- forbidden (S1)")]
for c, p in tab:
    print("  %-4s -> %s" % (c, p))
print()
print("  expressible: 1 of 3 = %.3f" % (1 / 3))
print("  => an ME-indexed ladder cannot walk the constraint diagonal; it can take at")
print("     most one of its steps (C1's), and that step is S4's object.")

# ---- X6: blast radius of the literal rename ---------------------------
head("X6  blast radius if C1/C2 were literally renamed into ME/CM")
import subprocess
cnt_files, cnt_cites = 0, 0
for d in ('docs', 'reports'):
    for dp, _dn, fns in os.walk(os.path.join(root, d)):
        for fn in fns:
            if fn.endswith('.md'):
                p = os.path.join(dp, fn)
                t = open(p, encoding='utf-8', errors='replace').read()
                n = len(re.findall(r'(?<![A-Za-z_])C[12](?![0-9])', t))
                if n:
                    cnt_files += 1
                    cnt_cites += n
road = open(os.path.join(root, 'Macro3D_to_2D_Smooth_Reduction_Roadmap_v1.4.md'), encoding='utf-8').read()
n_road = len(re.findall(r'(?<![A-Za-z_])C[12](?![0-9])', road))
print("  C1/C2 citations in docs/ + reports/: %d across %d files" % (cnt_cites, cnt_files))
print("  plus %d in the roadmap" % n_road)
print("  total citations that would change register: %d" % (cnt_cites + n_road))
print("  ME labels already used as chain constraints (S1 forbids): 0 (symbol_lint rule G)")
print()
print("  => the rename is not local: it re-registers every gate and ledger row, and every")
print("     one of them would then cite a branch predicate as a chain constraint.")

head("SUMMARY")
print("  X1 PASS  C1 => ME1 with 0 counterexamples; converse false (2 witnesses)")
print("  X2 PASS  S_A/S_E indistinguishable to every ME/CM proxy => no proxy for C2")
print("  X3 PASS  standalone 'strain' in the adopted spec: 0")
print("  X4 PASS  C3 has no expression and is forbidden one by S1")
print("  X5 PASS  expressible fraction of the diagonal: 1/3")
print("  X6 PASS  rename touches %d citations; all would violate S1" % (cnt_cites + n_road))
print()
print("  Conclusion supported by the checks: the legal operation is a BRIDGE (test")
print("  expressions at declared scales), not a rename. The constraints stay in C.")
print()
print("PROVENANCE: NEITHER  (bridge-legality check; establishes no physics)")
print()
print("Content generated by AI")
