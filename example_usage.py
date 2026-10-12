"""Example usage for MultiAgentResourceDeadlockWaitForGraphResolver."""
import sys
import json
from client import MultiAgentResourceDeadlockWaitForGraphResolver

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("=== Multi-Agent Resource Lock & Wait-For Graph (WFG) Deadlock Resolver Demo ===")
    resolver = MultiAgentResourceDeadlockWaitForGraphResolver()

    concurrent_agents = [
        {
            "agent_id": "workbuddy_finance_agent",
            "holds_resources": ["tencent_sheet_q4_budget"],
            "waits_for_resource": "erp_sql_settlement_table",
            "rollback_cost_score": 90.0
        },
        {
            "agent_id": "workbuddy_erp_sync_agent",
            "holds_resources": ["erp_sql_settlement_table"],
            "waits_for_resource": "tencent_sheet_q4_budget",
            "rollback_cost_score": 20.0
        }
    ]

    print("\n--- 1. Scanning Wait-For Graph (WFG) for Circular Lock Contention ---")
    outcome = resolver.detect_and_resolve_deadlocks(concurrent_agents)
    print(f"Deadlock Detected: {outcome['deadlock_detected']}")
    print(f"Circular Wait Cycle: {' -> '.join(outcome['deadlock_cycle'])}")
    print(f"Selected Minimum-Cost Victim: {outcome['selected_victim_agent']} (Rollback Cost: {outcome['victim_rollback_cost']})")
    print(f"Released Resources: {outcome['released_resources']}")
    print(f"Resolution Action: {outcome['resolution_action']}")

if __name__ == "__main__":
    main()
