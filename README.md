# ECHO

Research laboratory for **sequential experiment selection** under uncertainty and limited experimental budgets.

**Status:** usable research lab (V0–V2 worlds, plugin API, resume/parallel compare). Prototype science, not a product.

This is not an LLM agent and not a claim that an AI can do science. It is a computational laboratory for a precise question:

> When a scientific system is only partially understood and experiments are expensive, how should an algorithm decide what to measure next?

The conceptual loop is:

```text
experiment → observation → belief update → next experiment
```

## Use it on your own system

Install, then either pass a Python function or a YAML config. Full guide: [`docs/using_echo.md`](docs/using_echo.md).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

```python
from echo.lab import compare_policies

def f(X):
    return X[:, 0] ** 2 + 0.3 * X[:, 1]

compare_policies(
    f,
    dim=2,
    algorithms=["random", "uncertainty", "echo_v0"],
    budget=15,
    n_candidates=400,
    n_seeds=5,
    name="my_system",
)
```

The Unix command `echo` is a shell builtin, so the CLI is `python -m echo` (or `echolab` after install).

```bash
python -m echo list
python -m echo compare --config configs/example_oscillator.yaml --jobs 4
python -m echo analyze --run results/example_oscillator
```

## Problem

Scientific work often involves incomplete models, competing explanations, noisy measurements, and a small number of affordable experiments. Standard machine-learning evaluation (accuracy, a single benchmark score, or black-box optimization of a scalar) does not automatically answer:

> What should I measure next so that I understand the system better?

That decision problem is the object of study.

## Question

Can an experiment-selection policy recover a hidden scientific mechanism more efficiently than existing acquisition strategies, under a fixed budget — and under which conditions does it fail?

The answer is not assumed to be yes.

## Approach

1. Represent unknown systems as environments with hidden laws (built-in, a Python function, or a CSV lookup table).
2. Give the agent candidate experiments, noisy observations, and a budget. Ground truth is reserved for evaluation.
3. Maintain a Gaussian process posterior over the unknown function, and a posterior over parametric hypotheses when the environment provides a candidate class list.
4. Select experiments **sequentially**, updating after every observation. An open-loop ablation scores once and does not re-rank.
5. Compare policies on **several** discovery metrics, not one.

No language model is used.

## What is implemented

| Component | Status |
| --- | --- |
| Environment interface | implemented |
| Linear, nonlinear, interaction worlds | implemented |
| Competing-hypotheses world | implemented |
| Causal SCM, multimodal, anomaly, unseen worlds | implemented |
| Function / CSV plugin worlds | implemented |
| Exact Gaussian process | implemented |
| Random, greedy, uncertainty, diversity, EI, UCB, Thompson, local IG | implemented |
| ECHO V0 (global expected knowledge change) | implemented |
| ECHO hypothesis / falsify / cost / penalty / open-loop | implemented |
| Sequential loop, multi-metric evaluation, failure reports | implemented |
| Resume + parallel `compare`, auto markdown reports | implemented |
| ECHO-Bench task registry | local index only; not a published benchmark |
| Real data, LLM layer | CSV/tabular interface implemented; no published dataset. No LLM. |

## Reproduce the first experiment

```bash
python -m echo compare --config configs/first_experiment.yaml
python -m echo analyze --run results/first_experiment
```

A faster correctness check:

```bash
pytest
python -m echo compare --config configs/smoke.yaml
python -m echo compare --config configs/smoke_hypotheses.yaml
python -m echo bench
```

The first experiment (see `configs/first_experiment.yaml`) uses the nonlinear hidden system, 10,000 candidates, budget 20, noise 0.1, and 30 seeds. It compares random sampling, uncertainty sampling, expected improvement, local information gain, and ECHO V0.

Results live in `results/first_experiment/` and are interpreted in `docs/reports/first_experiment.md`. They are not hardcoded in this README.

Short version of that run: expected improvement recovered the hidden surface much worse than uncertainty-style design; ECHO V0 was not distinguishable from uncertainty sampling on function RMSE.

Paper configs 2–7 and the causal comparison now have 30-seed summaries under `results/` and write-ups in `docs/reports/`. Re-run with `--jobs N`; matching trajectories resume. The example plugin is `configs/example_oscillator.yaml`.

## How to read claims

Do not treat this repository as evidence that ECHO is a better scientist. Treat a result as research only if it has a stated question, baselines, multiple seeds, uncertainty, failure cases, and limitations. See `docs/`.

## Citation

There is no paper yet. Use `CITATION.cff` to cite the software version. When a preprint exists, that file will be updated.

## License

MIT. See `LICENSE`.
