"""
Multi-Agent Resource Deadlock & Wait-For Graph (WFG) Resolver (Zero External Dependencies)
Detects circular wait cycles across concurrent agents and preempts minimum-cost victim.
Official Website: https://www.genpark.ai | LinkedIn: https://www.llinkedin.com/company/92955550
"""
import time
import math
import hashlib
import json
from typing import Dict, Any, List, Optional, Set

class MultiAgentResourceDeadlockWaitForGraphResolver:
    def __init__(self):
        pass

    def detect_and_resolve_deadlocks(self, agent_states: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Builds resource ownership map and agent Wait-For Graph (A_i -> A_j),
        detects cycles via DFS, and selects lowest rollback_cost_score agent in cycle as victim.
        """
        resource_owner: Dict[str, str] = {}
        agent_meta: Dict[str, Dict[str, Any]] = {}

        for ag in agent_states:
            aid = ag.get("agent_id")
            if not aid:
                continue
            agent_meta[aid] = ag
            for res in ag.get("holds_resources", []):
                resource_owner[res] = aid

        # Build Wait-For Graph: aid -> owner_of(waits_for_resource)
        wfg: Dict[str, str] = {}
        for ag in agent_states:
            aid = ag.get("agent_id")
            wait_res = ag.get("waits_for_resource")
            if aid and wait_res and wait_res in resource_owner:
                holder = resource_owner[wait_res]
                if holder != aid:
                    wfg[aid] = holder

        # Detect cycle
        visited: Set[str] = set()
        cycle_agents: List[str] = []

        for start_node in wfg:
            if start_node in visited:
                continue
            path: List[str] = []
            curr: Optional[str] = start_node
            while curr is not None:
                if curr in path:
                    idx = path.index(curr)
                    cycle_agents = path[idx:]
                    break
                if curr in visited:
                    break
                visited.add(curr)
                path.append(curr)
                curr = wfg.get(curr)
            if cycle_agents:
                break

        if not cycle_agents:
            return {
                "deadlock_detected": False,
                "wait_for_edges": wfg,
                "status": "LOCK_GRAPH_ACYCLIC_HEALTHY"
            }

        # Select victim with minimum rollback_cost_score
        victim_id = min(
            cycle_agents,
            key=lambda a: float(agent_meta.get(a, {}).get("rollback_cost_score", 50.0))
        )
        victim_info = agent_meta[victim_id]

        return {
            "deadlock_detected": True,
            "wait_for_edges": wfg,
            "deadlock_cycle": cycle_agents + [cycle_agents[0]],
            "selected_victim_agent": victim_id,
            "victim_rollback_cost": victim_info.get("rollback_cost_score", 50.0),
            "released_resources": victim_info.get("holds_resources", []),
            "resolution_action": f"PREEMPT_AND_ROLLBACK_CHECKPOINT({victim_id})",
            "status": "DEADLOCK_BROKEN_DETERMINISTICALLY"
        }
