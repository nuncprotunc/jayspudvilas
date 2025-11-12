import argparse
import os
import math
import json
from dataclasses import dataclass
from typing import Optional, List, Dict
import numpy as np
import pandas as pd


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def _normal_pos(mu: float, sigma: float, size=None):
    # Draw from Normal, clamp at zero
    arr = np.random.normal(mu, sigma, size=size)
    if size is None:
        return max(0.0, float(arr))
    return np.maximum(0.0, arr)


@dataclass
class SimConfig:
    days: int = 90
    iters: int = 20000
    invites_per_day: float = 10
    posts_per_week: float = 2
    comments_per_day: float = 1

    accept_mu: float = 0.38
    accept_sigma: float = 0.08

    views_per_post_mu: float = 900
    views_per_post_sigma: float = 300

    views_per_comment_mu: float = 120
    views_per_comment_sigma: float = 60

    follow_conv_mu: float = 0.018
    follow_conv_sigma: float = 0.008

    carryover_decay: float = 0.85
    weekend_drop: float = 0.7

    seed: Optional[int] = None


def simulate(cfg: SimConfig) -> pd.DataFrame:
    if cfg.seed is not None:
        np.random.seed(cfg.seed)

    D = cfg.days
    N = cfg.iters

    # Prepare per-day content schedule
    posts_per_day = cfg.posts_per_week / 7.0
    # Expected posts each day ~ Poisson around rate; allow fractional with Poisson
    post_counts = np.random.poisson(lam=posts_per_day, size=(N, D))
    comment_counts = np.random.poisson(lam=cfg.comments_per_day, size=(N, D))

    # Views per post/comment
    views_per_post = np.maximum(0.0, np.random.normal(cfg.views_per_post_mu, cfg.views_per_post_sigma, size=(N, D)))
    views_per_comment = np.maximum(0.0, np.random.normal(cfg.views_per_comment_mu, cfg.views_per_comment_sigma, size=(N, D)))

    # Acceptance and conversion rates
    accept_rates = np.clip(np.random.normal(cfg.accept_mu, cfg.accept_sigma, size=(N, D)), 0.0, 1.0)
    follow_conv = np.clip(np.random.normal(cfg.follow_conv_mu, cfg.follow_conv_sigma, size=(N, D)), 0.0, 1.0)

    # Weekend mask
    days_idx = np.arange(D)
    is_weekend = (days_idx % 7 >= 5).astype(float)  # Sat=5, Sun=6
    weekend_multiplier = np.where(is_weekend > 0, cfg.weekend_drop, 1.0)

    followers = np.zeros((N, D), dtype=float)

    for t in range(D):
        # Content views today
        views_today = post_counts[:, t] * views_per_post[:, t] + comment_counts[:, t] * views_per_comment[:, t]
        # Carryover from previous day attention
        if t > 0:
            views_today = views_today + cfg.carryover_decay * followers[:, t-1] * 10.0  # heuristic carryover → more visibility

        # Convert views to follows
        follows_from_content = views_today * follow_conv[:, t]

        # Invites → accepted connections (treated as followers for growth proxy)
        invites_today = np.full(N, cfg.invites_per_day, dtype=float)
        accepted = invites_today * accept_rates[:, t]

        gain = (follows_from_content + accepted) * weekend_multiplier[t]
        followers[:, t] = followers[:, t-1] + gain if t > 0 else gain

    # Summaries per day
    df = pd.DataFrame({
        'day': days_idx + 1,
        'mean_followers': followers.mean(axis=0),
        'p10': np.percentile(followers, 10, axis=0),
        'p50': np.percentile(followers, 50, axis=0),
        'p90': np.percentile(followers, 90, axis=0),
    })
    return df


def save_outputs(df: pd.DataFrame, outdir: str):
    os.makedirs(outdir, exist_ok=True)
    csv_path = os.path.join(outdir, 'linkedin_mc_summary.csv')
    df.to_csv(csv_path, index=False)
    return csv_path


def run_from_args(args) -> int:
    cfg = SimConfig(
        days=args.days,
        iters=args.iters,
        invites_per_day=args.invites_per_day,
        posts_per_week=args.posts_per_week,
        comments_per_day=args.comments_per_day,
        accept_mu=args.accept_mu,
        accept_sigma=args.accept_sigma,
        views_per_post_mu=args.views_per_post_mu,
        views_per_post_sigma=args.views_per_post_sigma,
        views_per_comment_mu=args.views_per_comment_mu,
        views_per_comment_sigma=args.views_per_comment_sigma,
        follow_conv_mu=args.follow_conv_mu,
        follow_conv_sigma=args.follow_conv_sigma,
        carryover_decay=args.carryover_decay,
        weekend_drop=args.weekend_drop,
        seed=args.seed,
    )
    df = simulate(cfg)
    outdir = args.outdir or './sim_out'
    csv_path = save_outputs(df, outdir)
    print(f"Saved summary: {csv_path}")
    print(df.tail(5).to_string(index=False))
    return 0


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description='LinkedIn growth Monte Carlo simulator')
    p.add_argument('--days', type=int, default=90)
    p.add_argument('--iters', type=int, default=20000)
    p.add_argument('--invites_per_day', type=float, default=10)
    p.add_argument('--posts_per_week', type=float, default=2)
    p.add_argument('--comments_per_day', type=float, default=1)
    p.add_argument('--accept_mu', type=float, default=0.38)
    p.add_argument('--accept_sigma', type=float, default=0.08)
    p.add_argument('--views_per_post_mu', type=float, default=900)
    p.add_argument('--views_per_post_sigma', type=float, default=300)
    p.add_argument('--views_per_comment_mu', type=float, default=120)
    p.add_argument('--views_per_comment_sigma', type=float, default=60)
    p.add_argument('--follow_conv_mu', type=float, default=0.018)
    p.add_argument('--follow_conv_sigma', type=float, default=0.008)
    p.add_argument('--carryover_decay', type=float, default=0.85)
    p.add_argument('--weekend_drop', type=float, default=0.7)
    p.add_argument('--seed', type=int, default=None)
    p.add_argument('--outdir', type=str, default='./sim_out')
    return p


if __name__ == '__main__':
    parser = build_arg_parser()
    args = parser.parse_args()
    raise SystemExit(run_from_args(args))
