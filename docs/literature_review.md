# Literature review (Phase 0, incomplete)

This file is a working review, not a claim of completeness. Novelty is **not** established. Do not write "nobody has done this before."

ECHO's V0 question sits at the intersection of active learning, Bayesian experimental design, Bayesian optimization, and "AI for science." Those communities already contain strong methods for choosing \(x\) under uncertainty. What is not assumed, and what V0 tests, is whether conventional acquisition objectives coincide with recovering a hidden scientific mechanism under a tiny budget.

Working contrast (to be revised as the review grows):

> Existing literature appears to emphasize predictive accuracy, entropy of a model posterior, or location of an optimum. ECHO investigates whether those scores agree with mechanism recovery, hypothesis discrimination, and related discovery metrics when experiments are sequential and scarce.

## Areas in scope

- Active learning
- Bayesian / optimal experimental design
- Bayesian optimization
- Information-theoretic exploration
- Autonomous experimentation / robot scientists
- Causal experimental design (later)
- Learned acquisition functions / adaptive design (later)
- Scientific discovery benchmarks (later)
- Ocean adaptive sampling (later; no ocean prototype was present in this repository)

## Notes already filed

See `docs/literature/` for structured notes. The following papers are recorded because they constrain V0, not because they are an exhaustive canon.

| Note | Why it matters for ECHO |
| --- | --- |
| Lindley 1956 | Information provided by an experiment as expected utility of belief change |
| MacKay 1992 | Information-based active selection for models with posterior uncertainty |
| Chaloner & Verdinelli 1995 | Bayesian experimental design review |
| Jones, Schonlau & Welch 1998 | Expected improvement (EGO); V0 BO baseline |
| Krause, Singh & Guestrin 2008 | GP mutual information for sensor placement; closest math to ECHO V0 |
| Settles 2009 | Active learning survey; uncertainty sampling |
| Srinivas et al. 2010 | GP-UCB; optimization under uncertainty |
| Houlsby et al. 2011 | BALD; local information gain |
| King et al. 2004, 2009 | Closed-loop robot scientist; hypothesis-driven wet-lab experiments |
| Foster et al. 2021 | Amortized sequential Bayesian experimental design |
| Wang et al. 2023 | Broad AI-for-science review; ECHO is not this paper |

## Gaps to investigate (not assumed empty)

1. Do uncertainty-based strategies select scientifically useful experiments, or only high-variance locations?
2. Does local information gain differ from uncertainty sampling in the model classes used for science (V0: it should not, for a homoscedastic GP)?
3. Does global entropy reduction recover mechanisms better than optimum-seeking (EI)?
4. When do these objectives disagree?

Hypothesis-aware policies, falsification, cost, causal worlds, and real data are out of scope for this review's experimental claims until those experiments exist.

## Citation practice

Citations below were entered from standard bibliographic knowledge of well-known papers. Page-level quotes are not used. A later pass should verify every reference against the PDF or a library record before any submission.
