"""
algorithms.py
─────────────
Two shortest-path algorithms:
  1. Dijkstra        — classical O(E + V log V), always optimal.
  2. Grover Search   — proper quantum amplitude-amplification simulation
                       over the discrete path search space.
                       Uses a numpy state-vector that is iteratively
                       phase-flipped (oracle) and diffused (inversion
                       about the mean), then sampled.
"""

import time
import math
import random
import numpy as np
import networkx as nx


# ─────────────────────────────────────────────────────────────────────────────
# 1. DIJKSTRA (classical)
# ─────────────────────────────────────────────────────────────────────────────

def run_dijkstra(G: nx.Graph, source: str, target: str) -> dict:
    """
    Standard Dijkstra via NetworkX.
    Returns a result dict with path, cost, time_ms, and step log.
    """
    t0 = time.perf_counter()

    try:
        path = nx.dijkstra_path(G, source, target, weight="weight")
        cost = nx.dijkstra_path_length(G, source, target, weight="weight")
    except nx.NetworkXNoPath:
        return {"path": [], "cost": None, "time_ms": 0,
                "error": "No path found", "steps": []}
    except nx.NodeNotFound as e:
        return {"path": [], "cost": None, "time_ms": 0,
                "error": str(e), "steps": []}

    elapsed = (time.perf_counter() - t0) * 1000

    # Build a human-readable relaxation log (simulated from the final path)
    steps = []
    running = 0
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        w = G[u][v]["weight"]
        running += w
        steps.append({
            "step": i + 1,
            "edge": f"{u} → {v}",
            "edge_km": w,
            "cumulative_km": round(running, 1),
        })

    return {
        "path": path,
        "cost": round(cost, 1),
        "time_ms": round(elapsed, 3),
        "error": None,
        "steps": steps,
        "complexity": "O(E + V log V)",
    }


# ─────────────────────────────────────────────────────────────────────────────
# 2. GROVER QUANTUM SEARCH SIMULATION
# ─────────────────────────────────────────────────────────────────────────────

def _collect_paths(G: nx.Graph, source: str, target: str,
                   max_paths: int = 512):
    """
    Enumerate simple paths (DFS).  Capped at max_paths to keep the
    state-vector tractable; shortest paths are prepended so quality
    solutions are always in the search space.
    """
    try:
        optimal = nx.dijkstra_path(G, source, target, weight="weight")
    except Exception:
        optimal = None

    paths = []
    gen = nx.all_simple_paths(G, source, target, cutoff=8)
    for p in gen:
        paths.append(p)
        if len(paths) >= max_paths:
            break

    if optimal and optimal not in paths:
        paths.insert(0, optimal)

    return paths


def _path_cost(G: nx.Graph, path) -> float:
    return sum(G[path[i]][path[i + 1]]["weight"]
               for i in range(len(path) - 1))


def _grover_iterations(N: int) -> int:
    """Optimal Grover iterations ≈ π/4 · √N."""
    return max(1, round((math.pi / 4) * math.sqrt(N)))


def run_grover(G: nx.Graph, source: str, target: str,
               max_paths: int = 256) -> dict:
    """
    Grover Amplitude Amplification over the path search space.

    State vector:
      |ψ⟩ = Σ αᵢ |pathᵢ⟩   (complex amplitudes, Σ|αᵢ|² = 1)

    Oracle:
      Flips the sign of all "good" states — i.e., paths whose cost
      is at most (1 + ε) × optimal cost.  A 10 % margin is used so
      near-optimal paths are also marked.

    Diffuser (inversion about the mean):
      αᵢ ← 2·μ − αᵢ   where μ = mean amplitude.

    After ⌊π/4 · √N⌋ iterations the amplitude of good states is
    amplified from O(1/√N) to O(1), so a single measurement (sample)
    finds a good path with high probability.
    """

    t0 = time.perf_counter()

    paths = _collect_paths(G, source, target, max_paths=max_paths)
    N = len(paths)

    if N == 0:
        return {"path": [], "cost": None, "time_ms": 0,
                "error": "No paths found", "iterations": 0,
                "history": [], "N": 0}

    # ── cost vector ──────────────────────────────────────────────────────────
    costs = np.array([_path_cost(G, p) for p in paths], dtype=np.float64)
    optimal_cost = costs.min()

    # Mark "good" states: cost ≤ optimal × 1.10  (10 % tolerance)
    threshold = optimal_cost * 1.10
    oracle_mask = (costs <= threshold).astype(np.float64)

    # ── initial uniform superposition ────────────────────────────────────────
    amplitudes = np.ones(N, dtype=np.float64) / math.sqrt(N)

    num_iter = _grover_iterations(N)
    history = []
    oracle_calls = 0
    

    for it in range(num_iter):
        oracle_calls += 1
        # Oracle: flip sign of good states
        amplitudes = amplitudes * (1 - 2 * oracle_mask)

        # Diffuser: inversion about the mean
        mean_amp = amplitudes.mean()
        amplitudes = 2 * mean_amp - amplitudes

        # Renormalise (floating-point safety)
        norm = np.linalg.norm(amplitudes)
        if norm > 1e-12:
            amplitudes /= norm

        # Probability distribution from amplitudes
        probs = amplitudes ** 2
        probs = np.clip(probs, 0, None)
        probs /= probs.sum()

        # Most-probable path at this iteration
        best_idx = int(np.argmax(probs))
        history.append({
            "iteration": it + 1,
            "best_path": paths[best_idx],
            "best_cost": round(costs[best_idx], 1),
            "prob_best": round(float(probs[best_idx]), 4),
            "good_prob_total": round(float(probs[oracle_mask == 1].sum()), 4),
        })

    # ── Final measurement: sample according to probability ───────────────────
    probs = amplitudes ** 2
    probs = np.clip(probs, 0, None)
    probs /= probs.sum()

    sampled_idx = int(np.random.choice(N, p=probs))
    sampled_path = paths[sampled_idx]
    sampled_cost = round(costs[sampled_idx], 1)

    elapsed = (time.perf_counter() - t0) * 1000

    return {
        "path": sampled_path,
        "cost": sampled_cost,
        "time_ms": round(elapsed, 3),
        "error": None,
        "iterations": num_iter,
        "N": N,
        "history": history,
        "complexity": f"O(√N) ≈ {num_iter} Grover iterations for N={N} paths",
        "optimal_cost": round(optimal_cost, 1),
    }