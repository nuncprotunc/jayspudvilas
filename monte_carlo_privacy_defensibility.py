"""Heuristic Monte Carlo model for how defensible the current privacy / analytics notice
on jayspudvilas.com is under Victorian and ACT privacy regimes.

IMPORTANT: This is a conceptual risk-stress test only. It is NOT legal advice.
The probabilities and thresholds below are judgement calls, not statements about
actual law or regulator behaviour.
"""

from __future__ import annotations

import random
from collections import Counter, defaultdict
from typing import Dict, Tuple


# Outcome buckets for a regulator looking at the current notice and practices.
OUTCOMES = [
    "no_issue",          # Compliant / low concern
    "minor_guidance",    # Essentially fine but guidance / small improvement suggested
    "moderate_risk",      # Some non-trivial concerns, might require changes
    "adverse_finding",    # Material non-compliance / enforcement-style outcome
]

# Key dimensions for privacy defensibility in this context.
DIMENSIONS = [
    "transparency",           # How clear and plain-English the notice is
    "consent_and_control",    # How much real choice/control users have (cookies, opt-out)
    "third_party_overseas",   # Handling of third-party analytics and cross-border issues
    "small_site_context",     # Context: personal site, limited data use, proportionality
]

DIM_WEIGHTS: Dict[str, float] = {
    "transparency": 0.35,
    "consent_and_control": 0.25,
    "third_party_overseas": 0.25,
    "small_site_context": 0.15,
}

# Relative frequency / weighting of each regulator when thinking about combined risk.
REGIMES = {
    "vic": {"weight": 0.6},  # Site operated from Victoria
    "act": {"weight": 0.4},  # ACT added to stress-test combined view
}

# Heuristic mean scores per dimension (0–1) by regime for the current notice.
# These are subjective, not empirical.
BASE_MEANS: Dict[str, Dict[str, float]] = {
    "vic": {
        "transparency": 0.90,
        "consent_and_control": 0.72,
        "third_party_overseas": 0.68,
        "small_site_context": 0.83,
    },
    "act": {
        # Assume broadly similar posture, with slightly different emphasis.
        "transparency": 0.88,
        "consent_and_control": 0.70,
        "third_party_overseas": 0.66,
        "small_site_context": 0.81,
    },
}

# Standard deviations for each dimension (same across regimes for simplicity).
BASE_STDS: Dict[str, float] = {
    "transparency": 0.07,
    "consent_and_control": 0.10,
    "third_party_overseas": 0.12,
    "small_site_context": 0.08,
}

# Scrutiny scenarios: different contexts in which the notice might be assessed.
# Thresholds are (no_issue, minor_guidance, moderate_risk) for the overall score.
SCENARIOS: Dict[str, Dict[str, object]] = {
    "normal_use": {
        "weight": 0.65,
        "thresholds": (0.75, 0.60, 0.45),
    },
    "privacy_savvy_visitor": {
        "weight": 0.20,
        "thresholds": (0.80, 0.65, 0.50),
    },
    "regulatory_complaint": {
        "weight": 0.10,
        "thresholds": (0.82, 0.68, 0.54),
    },
    "data_incident": {
        "weight": 0.05,
        "thresholds": (0.86, 0.72, 0.58),
    },
}


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    """Clamp scores into the 0–1 range."""

    return max(lo, min(hi, x))


def sample_dimension_scores(regime: str) -> Dict[str, float]:
    """Sample a defensibility score per dimension for the given regime."""

    means = BASE_MEANS[regime]
    scores: Dict[str, float] = {}
    for dim in DIMENSIONS:
        mean = means[dim]
        std = BASE_STDS[dim]
        scores[dim] = clamp(random.gauss(mean, std))
    return scores


def overall_index(scores: Dict[str, float]) -> float:
    """Weighted overall defensibility index in [0, 1]."""

    return sum(scores[d] * DIM_WEIGHTS[d] for d in DIMENSIONS)


def classify_outcome(idx: float, thresholds: Tuple[float, float, float]) -> str:
    """Map an overall index to an outcome bucket using scenario-specific thresholds."""

    no_issue, minor_guidance, moderate_risk = thresholds
    if idx >= no_issue:
        return "no_issue"
    if idx >= minor_guidance:
        return "minor_guidance"
    if idx >= moderate_risk:
        return "moderate_risk"
    return "adverse_finding"


def simulate_defensibility(n_runs: int = 1_000_000, seed: int | None = 42) -> None:
    """Run the Monte Carlo stress test and print summary metrics.

    n_runs: number of simulated scenarios.
    seed:  random seed (set to None for nondeterministic runs).
    """

    if seed is not None:
        random.seed(seed)

    regime_names = list(REGIMES.keys())
    regime_weights = [REGIMES[r]["weight"] for r in regime_names]

    scenario_names = list(SCENARIOS.keys())
    scenario_weights = [SCENARIOS[s]["weight"] for s in scenario_names]

    overall_outcomes = Counter()
    outcomes_by_regime: Dict[str, Counter] = {r: Counter() for r in regime_names}
    outcomes_by_scenario: Dict[str, Counter] = {s: Counter() for s in scenario_names}

    # Aggregate scores for reporting mean defensibility indices.
    agg_scores_overall: defaultdict[str, float] = defaultdict(float)
    agg_scores_by_regime: Dict[str, defaultdict[str, float]] = {
        r: defaultdict(float) for r in regime_names
    }

    for _ in range(n_runs):
        regime = random.choices(regime_names, weights=regime_weights, k=1)[0]
        scenario = random.choices(scenario_names, weights=scenario_weights, k=1)[0]
        thresholds = SCENARIOS[scenario]["thresholds"]  # type: ignore[assignment]

        scores = sample_dimension_scores(regime)
        idx = overall_index(scores)
        outcome = classify_outcome(idx, thresholds)  # type: ignore[arg-type]

        overall_outcomes[outcome] += 1
        outcomes_by_regime[regime][outcome] += 1
        outcomes_by_scenario[scenario][outcome] += 1

        agg_scores_overall["overall"] += idx
        for dim, value in scores.items():
            agg_scores_overall[dim] += value
            agg_scores_by_regime[regime][dim] += value

    def pct(count: int) -> float:
        return (count / n_runs) * 100.0

    print("\n=== Monte Carlo stress test: privacy defensibility (VIC + ACT) ===")
    print(f"Simulated runs: {n_runs:,}")
    print("Note: heuristic model only – this is NOT legal advice.\n")

    print("Overall outcome probabilities (combined regimes & scenarios):")
    for outcome in OUTCOMES:
        print(f"  {outcome:15s}: {pct(overall_outcomes[outcome]):5.2f}%")

    print("\nOutcome probabilities by regime:")
    for regime in regime_names:
        total_r = sum(outcomes_by_regime[regime].values()) or 1
        print(f"- {regime.upper()} (weight {REGIMES[regime]['weight']:.2f}, {total_r:,} runs):")
        for outcome in OUTCOMES:
            share = (outcomes_by_regime[regime][outcome] / total_r) * 100.0
            print(f"    {outcome:15s}: {share:5.2f}%")

    print("\nOutcome probabilities by scrutiny scenario:")
    for scenario in scenario_names:
        total_s = sum(outcomes_by_scenario[scenario].values()) or 1
        print(f"- {scenario.replace('_', ' ').title()} (weight {SCENARIOS[scenario]['weight']:.2f}, {total_s:,} runs):")
        for outcome in OUTCOMES:
            share = (outcomes_by_scenario[scenario][outcome] / total_s) * 100.0
            print(f"    {outcome:15s}: {share:5.2f}%")

    print("\nMean defensibility scores (0–100 scale, combined):")
    for key in ["overall"] + DIMENSIONS:
        mean_score = agg_scores_overall[key] / n_runs
        print(f"  {key:22s}: {mean_score * 100:5.1f}")

    print("\nMean defensibility scores by regime (0–100 scale):")
    for regime in regime_names:
        total_r = sum(outcomes_by_regime[regime].values()) or 1
        print(f"- {regime.upper()}:")
        # Use total_r as denominator because each run for that regime contributed one score.
        for key in DIMENSIONS:
            mean_score = agg_scores_by_regime[regime][key] / total_r
            print(f"    {key:22s}: {mean_score * 100:5.1f}")


if __name__ == "__main__":  # pragma: no cover - script entrypoint
    simulate_defensibility()
