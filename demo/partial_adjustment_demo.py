"""Synthetic support-retention illustration; NOT an investment backtest.

New educational code for this portfolio. No institution code, market data,
production factor definitions, training arrays or model checkpoints are used.

Assumptions: n equal-weight old names and n disjoint equal-weight new names,
unit risky budget, exact execution, no price movement or eligibility changes.
Mix first, keep the largest n weights, then rescale to a unit budget. This is
NOT the complete risk/cap constrained pIVG/CAE/PA account implementation.
Equal weights are resolved by identifier, with old identifiers before new ones.
"""
from __future__ import annotations
import argparse
from dataclasses import asdict, dataclass
import json
import math


@dataclass(frozen=True)
class Outcome:
    half_life: float
    eta: float
    old_names: int
    new_names: int
    weights: dict[str, float]


def illustrate(half_life: float = 5.0, n: int = 100) -> Outcome:
    """Return a single synthetic update, with explicit deterministic tie handling."""
    if isinstance(half_life, bool) or not isinstance(half_life, (int, float)):
        raise TypeError('half_life must be a real number')
    if not math.isfinite(half_life) or half_life <= 0:
        raise ValueError('half_life must be finite and strictly positive')
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError('n must be a positive integer')
    eta = -math.expm1(-math.log(2.0) / half_life)
    candidates = [(f'A_old_{i:06d}', (1.0 - eta) / n) for i in range(n)]
    candidates += [(f'B_new_{i:06d}', eta / n) for i in range(n)]
    selected = sorted(candidates, key=lambda p: (-p[1], p[0]))[:n]
    total = math.fsum(weight for _, weight in selected)
    weights = {name: weight / total for name, weight in selected}
    old_count = sum(name.startswith('A_old_') for name in weights)
    return Outcome(float(half_life), eta, old_count, n-old_count, weights)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--half-life', type=float, default=5.0)
    parser.add_argument('--names', type=int, default=100)
    args = parser.parse_args()
    try:
        result = asdict(illustrate(args.half_life, args.names))
    except (TypeError, ValueError) as exc:
        parser.error(str(exc))
    result.pop('weights')
    print(json.dumps(result, ensure_ascii=False, indent=2))
