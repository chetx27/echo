# ECHO

Research infrastructure for **sequential experiment selection** under uncertainty and limited experimental budgets.

**Status:** prototype / experimental research code (Phase 1).

This is not a product, not an LLM agent, and not a claim that an AI can do science. It is a computational laboratory for asking a precise question:

> When a scientific system is only partially understood and experiments are expensive, how should an algorithm decide what to measure next?

The conceptual loop is:

```text
experiment → observation → belief update → next experiment
```

## Problem

Scientific work often involves incomplete models, competing explanations, noisy measurements, and a small number of affordable experiments. Standard machine-learning evaluation (accuracy, a single benchmark score, or black-box optimization of a scalar) does not automatically answer:

> What should I measure next so that I understand the system better?

That decision problem is the object of study.

## Question

Can an experiment-selection policy recover a hidden scientific mechanism more efficiently than existing acquisition strategies, under a fixed budget — and under which conditions does it fail?

The answer is not assumed to be yes.

## Approach (V0)

1. Represent unknown systems as synthetic scientific environments with hidden laws.
2. Give the agent candidate experiments, noisy observations, and a budget. Ground truth is reserved for evaluation.
3. Maintain a Gaussian process posterior over the unknown function.
4. Select experiments **sequentially**, updating after every observation.
5. Compare policies on **several** discovery metrics, not one.

V0 does not use a language model.

## What is implemented

| Component | V0 status |
| --- | --- |
| Environment interface | implemented |
| Linear synthetic world | implemented |
| Nonlinear synthetic world | implemented (first experiment) |
| Exact Gaussian process | implemented |
| Random, uncertainty, EI, local information gain | implemented |
| ECHO V0 (global expected knowledge change) | implemented |
| Sequential loop, multi-metric evaluation, failure reports | implemented |
| Competing hypotheses, causal graphs, cost-aware design, real data | not implemented |

## Reproduce the first experiment

The Unix command `echo` is a shell builtin, so the CLI is `python -m echo` (or `echolab` after install).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
python -m echo compare --config configs/first_experiment.yaml
python -m echo analyze --run results/first_experiment
```

A faster correctness check:

```bash
python -m echo compare --config configs/smoke.yaml
```

The first experiment (see `configs/first_experiment.yaml`) uses the nonlinear hidden system, 10,000 candidates, budget 20, noise 0.1, and 30 seeds. It compares random sampling, uncertainty sampling, expected improvement, local information gain, and ECHO V0.

Results live in `results/first_experiment/` and are interpreted in `docs/reports/first_experiment.md`. They are not hardcoded in this README.

Short version of that run: expected improvement recovered the hidden surface much worse than uncertainty-style design; ECHO V0 was not distinguishable from uncertainty sampling on function RMSE.

## How to read claims

Do not treat this repository as evidence that ECHO is a better scientist. Treat a result as research only if it has a stated question, baselines, multiple seeds, uncertainty, failure cases, and limitations. See `docs/`.

## Citation

There is no paper yet. Use `CITATION.cff` to cite the software version. When a preprint exists, that file will be updated.

## License

MIT. See `LICENSE`.
