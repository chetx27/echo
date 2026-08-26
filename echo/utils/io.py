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

    def seed_list(self) -> List[int]:
        return list(range(self.seed_start, self.seed_start + self.n_seeds))

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def config_hash(self) -> str:
        payload = json.dumps(self.to_dict(), sort_keys=True, default=str)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def load_config(path: str | Path) -> ExperimentConfig:
    path = Path(path)
    with path.open() as f:
        raw = yaml.safe_load(f) or {}
    known = {k: v for k, v in raw.items() if k in ExperimentConfig.__dataclass_fields__}
    return ExperimentConfig(**known)


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
