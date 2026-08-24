"""Deterministic radio-noise and attenuation helpers."""
from __future__ import annotations

import math
import random


def attenuation(distance: float, reference_distance: float = 1.0, exponent: float = 2.0) -> float:
    """Return inverse-power signal factor for a non-negative distance."""
    if distance < 0 or reference_distance <= 0 or exponent <= 0:
        raise ValueError("distance/reference_distance/exponent must be positive")
    return min(1.0, (reference_distance / max(distance, reference_distance)) ** exponent)


def noise_channels(count: int, blocked: int, rng: random.Random | None = None) -> set[int]:
    """Choose up to *blocked* unique channel indexes using a supplied RNG."""
    if count < 0 or blocked < 0:
        raise ValueError("counts must be non-negative")
    return set((rng or random).sample(range(count), min(blocked, count)))


def rssi_from_distance(distance: float, tx_dbm: float = -30.0, path_loss_exponent: float = 2.0) -> float:
    """Simple educational log-distance RSSI model."""
    if distance < 0 or path_loss_exponent <= 0:
        raise ValueError("invalid radio parameters")
    return tx_dbm - 10.0 * path_loss_exponent * math.log10(max(distance, 1.0))
