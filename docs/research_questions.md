# Research questions

Primary question (program):

> When a scientific system is only partially understood and experiments are expensive or limited, how should an AI decide what to investigate next?

This is a hypothesis, not a claim. The infrastructure must allow the answer to be yes, no, or "only under conditions X".

## Phase 1 questions (this version)

1. Under a hidden nonlinear response surface, a budget of 20, and 10,000 candidate experiments, which sequential acquisition strategy recovers the function and the oracle parameters most efficiently: random, uncertainty sampling, expected improvement, local information gain, or ECHO V0 (global expected knowledge change)?

2. For a homoscedastic Gaussian process, does local information gain select different experiments from uncertainty sampling? (The mathematics says no; the experiment checks the implementation.)

3. Does expected improvement, which seeks optima of y, recover a hidden mechanism worse than uncertainty-based design when the scientific target is the whole function rather than a minimum?

## Later questions (not answered in V0)

- Does hypothesis discrimination outperform generic uncertainty reduction?
- Does actively seeking falsifying experiments improve discovery?
- Does cost-aware scoring change the optimal policy?
- Do strategies transfer across unseen scientific systems?
- Can retrospective ocean sampling distinguish competing oceanographic hypotheses?

See `docs/research_log.md` for dated records of actual runs.
