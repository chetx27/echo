from __future__ import annotations

import numpy as np


def rng_for(seed: int, stream: int) -> np.random.Generator:
    """Independent RNG stream derived from an experiment seed."""
    return np.random.default_rng([int(seed), int(stream)])
