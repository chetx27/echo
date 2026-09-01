# Research questions

Primary question (program):

> When a scientific system is only partially understood and experiments are expensive or limited, how should an AI decide what to investigate next?

This is a hypothesis, not a claim. The infrastructure must allow the answer to be yes, no, or "only under conditions X".

## Phase 1 questions (this version)

1. Under a hidden nonlinear response surface, a budget of 20, and 10,000 candidate experiments, which sequential acquisition strategy recovers the function and the oracle parameters most efficiently: random, uncertainty sampling, expected improvement, local information gain, or ECHO V0 (global expected knowledge change)?

2. For a homoscedastic Gaussian process, does local information gain select different experiments from uncertainty sampling? (The mathematics says no; the experiment checks the implementation.)

3. Does expected improvement, which seeks optima of y, recover a hidden mechanism worse than uncertainty-based design when the scientific target is the whole function rather than a minimum?

## Later questions (Experiment 2+)

4. Does hypothesis discrimination outperform generic uncertainty reduction on \(P(H_{\mathrm{true}}\mid D)\) and posterior entropy of \(H\)?
5. Does a falsification-driven score (disagreement with the leading hypothesis) identify the true class faster or slower than discrimination?
6. Does dividing discrimination by experimental cost change the selected sequence when costs are heterogeneous?

## Phase 3–5 questions (infrastructure ready; claims wait on summaries)

7. Under a hidden four-node linear Gaussian SCM and hard \(\mathrm{do}(A,B)\) experiments, which sequential policy recovers the graph (structural Hamming distance) more efficiently?
8. On a landscape with three distinct mechanisms, does uncertainty-style design visit all regions or lock onto one?
9. When most of the domain obeys a linear law but a compact box does not, does sequential design find that structured violation?
10. Do the Phase-1 policy rankings hold on an unused functional form?
11. Does open-loop scoring (no sequential re-ranking) match sequential ECHO V0 under the same budget?

Answers as of 2026-09-01 (see `docs/reports/` and `docs/research_log.md`): (7) SHD does not stably rank policies; (8) all methods visit all three regions; (9) random finds the box more than uncertainty/ECHO V0; (10) EI/random ranking held, ECHO vs uncertainty is no longer a tie; (11) open-loop wrecks surface RMSE on the hypothesis world (0.64 vs ~0.07).

Ocean retrospective sampling remains later. No policy in this repository is trained across environments.

See `docs/research_log.md` for dated records of actual runs.
