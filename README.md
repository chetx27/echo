# ECHO

**Sequential experiment selection under uncertainty and limited budgets.**

[![License: MIT](https://img.shields.io/badge/license-MIT-0B6E4F.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-3776AB.svg)](pyproject.toml)
[![Tests](https://img.shields.io/badge/tests-37%20passed-0B6E4F.svg)](tests)
[![No LLM](https://img.shields.io/badge/LLM-not%20used-4D4D4D.svg)](#scope)

ECHO is a computational laboratory for one decision problem:

> Given what I already measured, **what experiment should I run next?**

It is research software, not a product and not an autonomous scientist. Policies never see the hidden law. Evaluation is multi-metric, multi-seed, and records failures. The answer is allowed to be *no*, or *only under conditions X*.

```text
experiment  →  observation  →  belief update  →  next experiment
```

---

## Why it exists

Accuracy on a held-out set, a single benchmark score, or Bayesian optimization of a scalar do not automatically answer a scientific design question. ECHO isolates that question: under a **fixed budget**, which sequential policy recovers a hidden mechanism — and where does it fail?

The same loop runs on built-in synthetic worlds or on **your** function / CSV table.

| You bring | ECHO provides |
| --- | --- |
| A hidden response \(f(x)\), or a table of candidate experiments | Paired-seed comparison of policies |
| A budget and a noise level | GP posterior (+ optional hypothesis posterior) |
| Optional custom acquisition | RMSE, \(P(H_{\mathrm{true}})\), SHD, coverage, cost, failures, figures, LaTeX |

Full laboratory guide: [`docs/using_echo.md`](docs/using_echo.md).

---

## Install

The Unix command `echo` is a shell builtin. Use `python -m echo` or `echolab`.

```bash
git clone https://github.com/chetx27/echo.git
cd echo
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
```

Requires Python 3.9+ · NumPy · SciPy · scikit-learn · Matplotlib · PyYAML.

---

## Thirty-second example

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

```bash
python -m echo list
python -m echo compare --config configs/example_oscillator.yaml --jobs 4
python -m echo analyze --run results/example_oscillator
python -m echo bench
```

Outputs (per run): `results/<name>/summary.json`, `metrics.csv`, `table.tex`, `report.md`, `failures/`, and figures under `figures/<name>/`. Interrupted runs **resume**. `--jobs N` parallelizes seeds.

---

## Method, in one page

1. **Worlds.** Hidden synthetic laws, a Python callable, or a CSV lookup table. Candidates are finite. Noise is seed-paired so two policies querying the same index see the same \(y\).
2. **Belief.** Exact RBF Gaussian process (misspecified for most worlds). When the world exposes a model class list, a posterior over parametric hypotheses is maintained from Gaussian marginal likelihoods.
3. **Policies.** Random, greedy, uncertainty, diversity, expected improvement, GP-UCB, Thompson, local information gain, ECHO V0 (global expected knowledge change on a probe set), hypothesis discrimination, falsification, cost wrappers, open-loop ECHO.
4. **Isolation.** `DecisionState` has no hidden formula, no \(\theta\), no test set. Ground truth is evaluator-only.
5. **Claims protocol.** Pre-specified question, paired Wilcoxon tests, 95% CIs, seed-level failure files. `summary.json` is the record; prose reports copy it.

No language model is used at any layer.

---

## Built-in worlds and tasks

| World | Scientific target | Config |
| --- | --- | --- |
| Nonlinear surface | Reconstruct \(3x_1 + 2x_2^2 - 4\sin(x_3)\) | `configs/first_experiment.yaml` |
| Competing hypotheses | Identify quadratic vs linear / sinusoid | `configs/experiment2_hypotheses.yaml` |
| Falsification | Disagreement with the leading class | `configs/experiment3_falsification.yaml` |
| Cost-aware design | Heterogeneous \(x_1\) costs | `configs/experiment4_cost.yaml` |
| Unseen form | Same policies, unused \(f\) | `configs/experiment5_generalization.yaml` |
| Causal SCM | Graph recovery after \(\mathrm{do}(A,B)\) | `configs/experiment_causal.yaml` |
| Multimodal | Three mechanisms in \(x_1\) | `configs/experiment6_multimodal.yaml` |
| Anomaly box | Compact structured violation of a linear law | `configs/experiment7_anomaly.yaml` |

`python -m echo list environments` · `python -m echo list algorithms` · `python -m echo bench`

ECHO-Bench is a **local task index**, not a community leaderboard.

---

## Results snapshot (30 seeds)

Numbers are from `results/*/summary.json`. If this table disagrees with the JSON, the JSON wins. Full write-ups: [`docs/reports/`](docs/reports/).

| Study | Primary finding |
| --- | --- |
| [Nonlinear](docs/reports/first_experiment.md) | Expected improvement is the wrong objective for reconstructing \(f\). ECHO V0 **ties** uncertainty on RMSE (\(p=0.52\)). |
| [Hypotheses](docs/reports/experiment2_hypotheses.md) | \(P(H_{\mathrm{true}})\) saturates for **every** policy, including random. The class list is too easy at this budget. |
| [Falsification](docs/reports/experiment3_falsification.md) | Same ceiling. Open-loop ECHO wrecks surface RMSE (0.64 vs ~0.07). |
| [Cost](docs/reports/experiment4_cost.md) | Cost wrappers change **spend**, not identification. |
| [Unseen form](docs/reports/experiment5_generalization.md) | EI/random ranking holds. ECHO V0 vs uncertainty is no longer a tie (\(p=0.036\), 19/30). One environment — not a general win. |
| [Causal](docs/reports/experiment_causal.md) | Structural Hamming distance does not stably rank sequential designs. |
| [Multimodal](docs/reports/experiment6_multimodal.md) | All methods visit all three regions. Diversity is best on region RMSE. |
| [Anomaly](docs/reports/experiment7_anomaly.md) | Random finds the box more often than uncertainty / ECHO V0. Method-class failure for structured incompleteness. |

Reproduce a paper config (resumes completed trajectories):

```bash
python -m echo compare --config configs/first_experiment.yaml --jobs 8
python -m echo analyze --run results/first_experiment
```

Smoke (CI, not claims): `configs/smoke.yaml`, `configs/smoke_hypotheses.yaml`.

---

## Documentation

| Document | Contents |
| --- | --- |
| [`docs/using_echo.md`](docs/using_echo.md) | Plug in a function, CSV, or custom acquisition |
| [`docs/methodology.md`](docs/methodology.md) | Estimators, metrics, statistics, limitations |
| [`docs/experiments.md`](docs/experiments.md) | Configs, commands, how to read outputs |
| [`docs/research_questions.md`](docs/research_questions.md) | Pre-specified questions |
| [`docs/research_log.md`](docs/research_log.md) | Dated runs, including failures |
| [`docs/literature_review.md`](docs/literature_review.md) | Working bibliography |
| [`docs/decisions/`](docs/decisions/) | Design decisions |
| [`papers/draft/`](papers/draft/) | No manuscript yet — do not invent one |

---

## Scope

**In scope.** Sequential design, Gaussian-process and hypothesis-aware acquisition, synthetic and user-supplied systems, honest multi-seed evaluation.

**Out of scope.** Language models, wet-lab hardware control, a published community benchmark, a claim that ECHO is a better scientist.

A result in this repository is research only if it has a stated question, baselines, seeds, uncertainty, failure cases, and limitations.

---

## Citation

There is no paper yet. Cite **software version 0.2.0**. Metadata: [`CITATION.cff`](CITATION.cff). When a preprint exists, that file will be updated.

**BibTeX**

```bibtex
@software{echo2026,
  title     = {ECHO: sequential experiment selection under uncertainty},
  author    = {Chethana, G.},
  year      = {2026},
  version   = {0.2.0},
  url       = {https://github.com/chetx27/echo},
  note      = {Research software. No peer-reviewed publication at this version.}
}
```

**APA**

Chethana, G. (2026). *ECHO: sequential experiment selection under uncertainty* (Version 0.2.0) [Computer software]. https://github.com/chetx27/echo

---

## License

MIT. See [`LICENSE`](LICENSE).
