# Using ECHO as a laboratory

ECHO is a sequential experiment-selection lab. You give it a hidden system, a budget, and a list of policies. It runs paired seeds, writes metrics, figures, failure records, and a markdown report.

It is not a product, not an LLM agent, and not a claim that an AI can do science.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

The Unix command `echo` is a shell builtin. Use `python -m echo` or `echolab`.

## The loop

```text
candidates → policy picks x → noisy y → GP (and optional hypothesis) update → next x
```

Ground truth is evaluator-only. Policies receive `DecisionState` (candidates, observations, costs, GP, optional hypothesis posterior). They never receive the hidden formula.

## Built-in worlds

`python -m echo list environments`

| Name | Hidden law (evaluator-only) |
| --- | --- |
| `linear` | \(3x_1+2x_2-4x_3\) |
| `nonlinear` | \(3x_1+2x_2^2-4\sin(x_3)\) |
| `interaction` | \(2x_1+3x_2+5 x_1 x_3\) |
| `competing_hypotheses` | quadratic vs linear/sin vocabulary |
| `causal` | SCM \(A\to C\to D\), \(B\to C\); query \(\mathrm{do}(A,B)\) |
| `multimodal` | three mechanisms in \(x_1\) |
| `anomaly` | linear background + compact +4 box |
| `unseen` | \(\exp\), product, \(\tanh\) |

## Built-in policies

`python -m echo list algorithms`

Random, greedy, uncertainty, diversity, expected improvement, GP-UCB, Thompson, local information gain, ECHO V0 (global knowledge change), hypothesis discrimination, falsification, cost wrappers, open-loop ECHO.

## Fastest path: a Python function

```python
from echo.lab import compare_policies

def f(X):
    return X[:, 0] ** 2 + 0.3 * X[:, 1]

summary = compare_policies(
    f,
    dim=2,
    algorithms=["random", "uncertainty", "echo_v0"],
    budget=15,
    n_candidates=400,
    n_seeds=5,
    name="my_system",
)
```

Results: `results/my_system/summary.json`, `metrics.csv`, `table.tex`, `report.md`, `failures/`. Figures: `figures/my_system/` when `output_dir` is `results`.

## YAML + plugin (repeatable)

`examples/oscillator.py` registers a named world. Then:

```bash
python -m echo compare --config configs/example_oscillator.yaml --jobs 4
python -m echo analyze --run results/example_oscillator
python -m echo report --run results/example_oscillator
```

`--jobs` uses processes. Custom worlds used with `--jobs > 1` must live in a plugin file so workers can import them. Interrupted runs resume matching trajectories (`--no-resume` to force a rerun).

## CSV / lookup table

When you have rows instead of a formula:

```python
from echo.lab import TabularWorld, tabular_from_csv, compare
from echo.utils.io import ExperimentConfig
from echo.environments import register_environment

env_factory = lambda **kw: tabular_from_csv(
    "data/my_table.csv",
    x_columns=["temp", "pressure"],
    y_column="yield",
    f_column="yield_noiseless",  # optional
    n_test=kw.get("n_test", 50),
)
register_environment("my_table", env_factory)
```

Each seed holds out a test slice for evaluation and treats the rest as queryable candidates.

## Custom acquisition

```python
from echo.lab import register_acquisition

def prefer_cheap(state):
    return -state.costs

register_acquisition("cheap", prefer_cheap)
```

`state` is `echo.policies.state.DecisionState`. Score every candidate; unavailable rows are masked for you.

To register a full `Policy` subclass, use `register_policy(name, factory)`.

## Paper-scale experiments in this repo

```bash
python -m echo compare --config configs/first_experiment.yaml
python -m echo compare --config configs/experiment2_hypotheses.yaml --jobs 4
python -m echo compare --config configs/experiment3_falsification.yaml --jobs 4
python -m echo compare --config configs/experiment4_cost.yaml --jobs 4
python -m echo compare --config configs/experiment5_generalization.yaml --jobs 4
python -m echo compare --config configs/experiment_causal.yaml --jobs 4
python -m echo compare --config configs/experiment6_multimodal.yaml --jobs 4
python -m echo compare --config configs/experiment7_anomaly.yaml --jobs 4
python -m echo bench
```

Smoke configs (`configs/smoke*.yaml`) are for CI, not claims.

## How to read an output

- `summary.json` is the record. Reports copy numbers from it.
- Pairwise tests are seed-paired. A tiny mean difference with \(p > 0.05\) is a tie.
- Failure JSON files are seeds where the primary method lost to the comparator on the configured metric. Keep them.
- Do not write that ECHO is a better scientist. Write the question, the metric, the seeds, and the failures.

## What this lab is not

- Not real-time laboratory hardware control.
- Not an LLM planner.
- Not a published community benchmark (`echo.bench` is a local index).
- Not a trained policy: nothing here is optimized across environments.
