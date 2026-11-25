# Submission verbatim — `MR2-D` + truncated Morse interface potential

**Received**: 2026-11-22.
**Status**: **`PROPOSED` — governs nothing.** Registered for adjudication only.
**Provenance**: `NEITHER`.

---

## Physics-Self-Consistency Correction and Simulation Scheme for the 3D-to-2D Space (DCC) Model

### I. Background and Core Contradictions

In advancing the theoretical derivation of smooth 2D projection for macroscopic 3D objects, the earlier review of the
mathematical framework exposed severe physical distortions. The originally relied-upon ARAP (As-Rigid-As-Possible)
algorithm and the global statistic (MR2) suffer from fundamental flaws in discrete physical models:

- **The fatal flaw of topological rupture**: The disjointness of internal supports causes the 3D and 2D distance
  distributions to be completely non-overlapping, making the KL divergence diverge and leading to the outright
  rejection of the MR2 statistic.
- **Misalignment between mathematical constraints and physical reality**: The original framework treated "not
  cutting interfaces" as a rigid mathematical topological requirement (preserving homeomorphism), forcibly
  maintaining connecting edges in vacuum regions or between voxels without physical contact, thereby generating
  spurious stresses during dimensionality reduction.
- **Mismatch of objects and dimensions**: The ARAP algorithm requires a continuous vertex set, whereas the current
  physical records contain only discrete "extended annular plate" voxels, and the local rotation matrices cannot
  act directly across dimensions on 3D edge vectors.

### II. Core Theoretical Correction: From Mathematical Topology to Physical Energy

To resolve the aforementioned contradictions, "not cutting interfaces" must be transformed from a purely
mathematical topological constraint into a physical energy constraint, ensuring that the dimensionality-reduction
mapping strictly adheres to the boundaries of real interaction forces.

**Introduction of the Physical Interface Potential Term**

The ARAP energy functional is reconstructed by introducing a truncated potential term based on real physical
interaction forces. The total energy functional is revised as:

```
E_total(X) = E_ARAP(X) + λ Σ_{(i,j) ∈ N_phys} Ψ(d_2D(i,j))
```

Here, the physical potential term Ψ(d) adopts a smoothly truncated Morse potential variant:

```
Ψ(d) = D_e ( e^{−2α(d−d₀)} − 2e^{−α(d−d₀)} )   if d ≤ r_cut
Ψ(d) = 0                                        if d > r_cut
```

- **r_cut (physical cutoff radius)**: The key threshold distinguishing "true physical interfaces" from "purely
  mathematical connections". When the 2D unfolding distance exceeds this value, the potential drops to zero, and the
  algorithm voluntarily abandons maintaining the connection, permitting the "rupture" of mathematical topology to
  avoid spurious stresses.
- **N_phys**: Contains only voxel pairs with genuine short-range physical interactions, excluding vacuum regions or
  purely geometrically adjacent edges lacking physical contact.

**The Sole Surviving Diagnostic Metric: MR2-D**

Abandoning the global KL divergence, we adopt the threshold-free local diagnostic metric MR2-D. This metric
disregards global distance distributions and strictly verifies:

- Whether axial neighbors remain at a distance of one pitch after dimensionality reduction.
- Whether physical interface distances are compromised.

MR2-D is the only formulation capable of clearly distinguishing "smooth unfolding" from "brute-force destruction",
proving that as long as true physical interfaces are not severed, local weak-force relationships can be perfectly
preserved.

### III. Repositioning of Space-Filling Curves (SFC)

Experiments confirm that SFC can indeed distinguish sediments from random shuffles, but 99.2% of this discriminative
ability stems from partitioning data into contiguous blocks rather than a genuine understanding of physical
structure. Therefore, SFC cannot replace ARAP as the physical dimensionality-reduction algorithm; its true role is
repositioned as an underlying data indexing and serialization accelerator, used to improve cache hit rates during
neighborhood searches and covariance matrix computations.

### IV. Simulation Strategy: Scale Gradually from Small to Large

In the current phase of theoretical derivation and physical self-consistency review, there is no need to pursue the
extreme engineering scale of over 4 billion voxels. A "small-to-large" strategy should be adopted, using minimal
data volumes to validate the physical logic and mathematical pipeline.

**Proof of Concept (POC) Phase.** Data volume: a micro test case of 500 to 1000 voxels representing an "extended
annular plate". Objective: verify whether the algorithm, after introducing the physical cutoff potential Ψ(d), can
correctly identify "true physical interfaces" and avoid spurious stresses during 2D unfolding. This allows intuitive
observation of the stress distribution on the post-reduction 2D canvas (high stress in red, natural ruptures).

**Local Physical Field Verification Phase.** Data volume: tens of thousands to hundreds of thousands of voxels.
Objective: observe stress distributions at the junctions of multiple "extended annular plates", verify the
convergence stability of the Conjugate Gradient (CG) method when solving large-scale sparse matrices, and tune the
parameters of the physical potential function (D_e, α, r_cut).

### V. Engineering Implementation under Current Hardware Constraints (Windows / 32GB RAM / No GPU)

Given the hardware limitations of the current Windows platform, 32GB pure RAM, and lack of a GPU, extreme low-level
optimizations are required:

- **Memory and Data Structure Optimization.** Sparse Voxel Octrees and Chunking: partition the global space into
  fixed-size blocks, allocating memory only for blocks containing entities and skipping vacuum regions, compressing
  memory footprint to 1%–5%. Bit-packing: discard redundant floating-point numbers; use 6 bits for local
  coordinates, 3 bits for normals, and 7 bits for material IDs, compressing per-vertex data to 32 bits (4 bytes).
  Memory-Mapped Files: utilize Windows memory mapping to map disk data directly into virtual memory space, loading
  pages on demand to prevent physical memory overflow.
- **CPU Parallel Computing and Instruction Set Optimization.** Multithreading (OpenMP / TBB): distribute chunked
  voxel grid computations across all physical cores to independently calculate gradients for local rigidity terms
  and physical potential terms. SIMD Vectorization (AVX2): through 32-byte memory alignment, use AVX2 instruction
  sets to process 8 floating-point numbers per cycle, improving cache hit rates and accelerating inner-loop
  mathematical operations.
- **Energy Minimization Solver Selection.** Conjugate Gradient (CG) Method: discard Newton's method, which requires
  storing an (3N)² Hessian matrix, in favor of the CG method, which only requires storing 3N-sized vectors,
  resulting in an extremely low memory footprint. Truncated Line Search: after determining the search direction,
  perform only 1-2 evaluations before pivoting, drastically reducing total execution time.
- **Windows System-Level Tuning.** Disable Memory Compression and Page Combining: execute
  `Disable-MMAgent -MemoryCompression` and `Disable-MMAgent -PageCombining` to reduce CPU overhead. Optimize Virtual
  Memory: move the paging file to a non-system NVMe SSD and set a fixed size (32GB-48GB). Disable Kernel Code
  Paging: modify the registry key `DisablePagingExecutive` to 1, ensuring ultra-low latency for underlying
  scheduling.

### VI. Next Steps

This scheme establishes the core approach of substituting physical energy constraints for mathematical topological
constraints, and outlines the complete pathway from micro-scale proof of concept to large-scale engineering
implementation. The next step is to prioritize building a 500-1000 voxel micro test case, writing the core data
structure code, and demonstrating how to compute its initial stress distribution under the new energy functional,
thereby fully validating the physical self-consistency logic.

---

*End of submission. Content generated by AI.*
