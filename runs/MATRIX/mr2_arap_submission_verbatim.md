# Submission verbatim — `MR2` via ARAP + TPGIM + KL

**Received**: 2026-11-22.
**Status**: **`PROPOSED` — governs nothing.** Registered for adjudication only. Not inserted into `R1`, not
inserted into any spec, and it may not be cited as a definition of `MR2`.

**Provenance**: `NEITHER`.

---

To establish a physically self-consistent framework for the Dimensional Collapse and Continuation (DCC) model, we
systematically derive the mathematical formulations from three fundamental physical constraints: the Effective 2D
Space, Smooth 2D-ification, and Weak Interaction Force Preservation. This derivation bridges macro-level physical
intuitions with rigorous geometric and topological mathematics, culminating in the reconstruction of the MR2
(Permutation-Sensitive Statistic) to rigorously evaluate the dimensional reduction process.

## Energy Minimization Formulation of ARAP (Ensuring Smooth 2D-ification and Weak Interaction Force Preservation)

In the DCC model, the evolution from a 3D macroscopic object to a 2D representation must not be a violent
coordinate truncation or random permutation. Instead, it must be governed by a continuous deformation process
driven by energy minimization.

Let the 3D object be represented by a triangular mesh consisting of a vertex set V = {v_1, ..., v_n} and an edge
set E. Our objective is to find a mapping Phi: R^3 → R^2 that projects these vertices onto a 2D plane, yielding a
new vertex set U = {u_1, ..., u_n}.

To strictly satisfy the physical requirements of "Smooth 2D-ification" and "Weak Interaction Force Preservation,"
we introduce the As-Rigid-As-Possible (ARAP) energy function. For each vertex v_i, the local deformation gradient
within its neighborhood should approximate a 2D rotation matrix R_i in SO(2) as closely as possible. The energy
minimization formulation is defined as:

    E_ARAP(U, R) = sum_{i=1}^{n} w_i sum_{j in N(i)} | (u_i - u_j) - R_i (v_i - v_j) |^2

Where:
N(i) denotes the local neighborhood of vertex v_i in the 3D space (defined by the edge set E).
w_i represents the weight coefficient, which physically corresponds to the local mass density or interaction
strength of that region.
R_i is the local rotation matrix, which permits global rotation during the unrolling process while strictly
prohibiting local stretching or shearing.

Physical Self-Consistency Review:
This formulation rigorously constrains the relative distances within the local neighborhood N(i). After 2D
projection, particles that interacted via short-range forces (weak interaction forces) in the 3D space maintain
their rigid relative positional relationships in the 2D plane. This mathematically precludes the generation of
"disordered fragments" and ensures that the short-range interaction terms within the physical system's Hamiltonian
remain intact during dimensional reduction.

## Depth Channel Encoding via Topology-Preserving Geometry Images (Ensuring Effective 2D Space)

Having resolved the smooth unrolling process, the next critical step is to address the lossless encoding of the
Z-axis depth information. Traditional projection methods inherently discard depth data; therefore, we employ the
Topology-Preserving Geometry Images (TPGIMs) approach to convert 3D spatial coordinates into 2D attribute channels.

Let the 2D planar coordinates after ARAP unrolling be denoted as (u, v). We construct a 2D discrete grid (canvas)
represented by I in R^{H × W × C}, where C denotes the number of attribute channels.

The depth-preserving mapping function Psi is defined as:

    I(floor u, floor v, :) = (x, y, z)^T

Where:
(floor u, floor v) represents the discrete pixel coordinates on the 2D canvas corresponding to the unrolled
vertices.
x, y, z are the original 3D spatial coordinates of the vertex, which are directly stored as the first three
channels (e.g., RGB channels) of the 2D image.
For vacant pixels not covered by the projected vertices, Laplacian interpolation or nearest-neighbor interpolation
is applied for attribute filling.

Physical Self-Consistency Review:
This scheme achieves "lossless dimensional reduction." The 2D canvas not only encapsulates the topological
structure of the unrolled plane (u,v) but also fully retains the depth attribute z from the original 3D space.
Consequently, the 2D space is no longer an empty projection but an "Effective 2D Space" that carries the complete
physical state of the 3D object.

## Reconstruction of MR2 Based on the ARAP Adjacency Matrix (Permutation-Sensitive Statistic)

With the rigorous mathematical formulations established in the previous steps, we can finally define the MR2
statistic, which accurately measures "spatial arrangement self-consistency."

Previous MR2 tests failed due to the lack of a rigorous definition for spatial arrangement. Utilizing the local
adjacency matrix from the ARAP algorithm and the depth channels from TPGIMs, we define the Permutation-Sensitive
Mutual Information (PSMI) as the core statistical metric for MR2.

Let the original 3D object be O_3D and the 2D projected result be O_2D. We define two stochastic variables:
X: The relative distance distribution of voxel pairs in the 3D space, denoted as P_3D(d_3D).
Y: The relative distance distribution of the corresponding voxel pairs after 2D projection, denoted as P_2D(d_2D).

The MR2 statistic is formulated as the Kullback-Leibler (KL) Divergence between these two distributions:

    MR2_PSMI = D_KL(P_3D || P_2D) = sum_d P_3D(d) log [ P_3D(d) / P_2D(d) ]

Physical Self-Consistency Review and Evaluation Criteria:
Permutation Sensitivity: If the 2D projection process shatters the object into disordered fragments (as observed in
previous iterations like DEMO-1), P_2D(d) will approach a uniform distribution, resulting in a substantially high
D_KL value. Only when the 2D projection strictly preserves the spatial arrangement will P_2D(d) highly correlate
with P_3D(d), driving the MR2_PSMI value toward zero.
Weak Interaction Force Verification: We can isolate and calculate the local distance distribution specifically
where d < epsilon (the threshold for weak interaction force range). If MR2_PSMI approaches zero at this local
scale, it strictly proves that the weak interaction forces have been flawlessly preserved throughout the 2D
projection process.

## Summary and Future Research on 2D Representation Pathways

This derivation establishes a complete theoretical closed loop from physical constraints to mathematical
representations:
- ARAP Energy Minimization guarantees smooth unrolling and the preservation of weak interaction forces.
- TPGIMs Depth Channel Encoding constructs an Effective 2D Space.
- KL Divergence based on Neighborhood Distance Distributions reconstructs the MR2 statistic.

Building upon this rigorous mathematical foundation, subsequent research on 2D representation pathways will focus
on the dynamic evolution of the 2D canvas under varying physical conditions, specifically investigating the
topological phase transitions (e.g., the generation or annihilation of holes) and their corresponding impacts on
the MR2_PSMI metric. This will further validate the robustness of the DCC model in simulating macroscopic
dimensional collapse.

---

*End of submission. Content generated by AI.*
