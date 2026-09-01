Notebooks are optional. The research engine is the CLI and `echo.lab`.

```bash
python -m echo compare --config configs/example_oscillator.yaml
```

```python
from echo.lab import compare_policies

compare_policies(lambda X: X[:, 0] ** 2, dim=1, n_seeds=3, budget=8, name="notebook_demo")
```

See `docs/using_echo.md`.
