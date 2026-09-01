from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


@dataclass
class ExperimentConfig:
    name: str = "experiment"
    environment: str = "nonlinear"
    algorithms: List[str] = field(default_factory=lambda: ["random", "echo_v0"])
    n_candidates: int = 10000
    budget: int = 20
    n_init: int = 3
    noise: float = 0.1
    n_test: int = 1000
    n_probe: int = 256
    domain_low: float = -2.0
    domain_high: float = 2.0
    n_seeds: int = 30
    seed_start: int = 0
    output_dir: str = "results"
    n_restarts: int = 1
    cost_mode: str = "uniform"
    primary_algorithm: str = "echo_v0"
    comparator: str = "uncertainty"
    failure_metric: str = "function_recovery_rmse"
    failure_higher_is_better: bool = False
    plot_metrics: List[str] = field(
        default_factory=lambda: [
            "function_recovery_rmse",
            "parameter_recovery_rmse",
            "probe_entropy",
            "mean_predictive_std",
        ]
    )
    plugin: Optional[str] = None
    question: Optional[str] = None

    def seed_list(self) -> List[int]:
        return list(range(self.seed_start, self.seed_start + self.n_seeds))

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def _hash_dict(self) -> Dict[str, Any]:
        """Scientific fields only.

        Empty plugin/question fields are omitted. V1+ defaults that match the
        original V0 implicit config are omitted so ``first_experiment.yaml``
        keeps hash ``6ffdacd9e99772df``.
        """
        d = self.to_dict()
        for key in ("plugin", "question"):
            if not d.get(key):
                d.pop(key, None)
        implicit_v0 = {
            "cost_mode": "uniform",
            "primary_algorithm": "echo_v0",
            "comparator": "uncertainty",
            "failure_metric": "function_recovery_rmse",
            "failure_higher_is_better": False,
            "plot_metrics": [
                "function_recovery_rmse",
                "parameter_recovery_rmse",
                "probe_entropy",
                "mean_predictive_std",
            ],
        }
        for key, value in implicit_v0.items():
            if d.get(key) == value:
                d.pop(key, None)
        return d

    def config_hash(self) -> str:
        payload = json.dumps(self._hash_dict(), sort_keys=True, default=str)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def load_config(path: str | Path) -> ExperimentConfig:
    path = Path(path)
    with path.open() as f:
        raw = yaml.safe_load(f) or {}
    known = {k: v for k, v in raw.items() if k in ExperimentConfig.__dataclass_fields__}
    config = ExperimentConfig(**known)
    if config.plugin:
        from echo.plugins import load_plugin

        load_plugin(config.plugin, search_from=path.parent)
    return config


def save_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        json.dump(payload, f, indent=2, default=_json_default)


def load_json(path: Path) -> Any:
    with path.open() as f:
        return json.load(f)


def _json_default(obj: Any) -> Any:
    if hasattr(obj, "tolist"):
        return obj.tolist()
    raise TypeError(f"not JSON serializable: {type(obj)}")
