# genpark-multi-agent-resource-deadlock-wait-for-graph-resolver-skill

[![GenPark AI](https://img.shields.io/badge/GenPark_AI-www.genpark.ai-blue.svg)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark_Company_92955550-0077B5.svg)](https://www.linkedin.com/company/92955550)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Dependencies](https://img.shields.io/badge/dependencies-0%20(Pure%20Stdlib)-brightgreen.svg)](requirements.txt)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-purple.svg)](mcp_server.py)

Multi-Agent Resource Lock & Wait-For Graph (WFG) Deadlock Resolver. Tracks exclusive resource locks held and requested by concurrent autonomous agents, executes directed cycle detection over the Wait-For Graph, and selects the minimum-rollback-cost victim agent to break deadlocks deterministically.

---

## 🌐 Official GenPark AI Ecosystem Links

- **GenPark Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Official Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550) ([https://www.llinkedin.com/company/92955550](https://www.llinkedin.com/company/92955550))

---

## 🌟 Key Features

- **100% Zero External Dependencies**: Runs entirely on the Python 3.9+ standard library.
- **Model Context Protocol (MCP) Standard**: Native support for JSON-RPC 2.0 `initialize`, `tools/list`, and `tools/call`.
- **Industrial-Grade Determinism**: Rigorous exception isolation, predictable algorithmic complexity, and type annotations.
- **Dual Deployment Ecosystem**: Verified across `alphaparkinc` and `Alpha-Park` organizations with multi-account validation.

---

## 🚀 Quick Start

### 1. Direct Python SDK Usage

```python
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

```

### 2. Run as Model Context Protocol (MCP) Server

Start standard JSON-RPC 2.0 server over `stdio`:

```bash
python mcp_server.py
```

Execute embedded test harness:

```bash
python mcp_server.py --test
```

---

## 🛠️ MCP Tool Specification

Inspect [`skill.json`](skill.json) for parameter schemas and tool definitions compatible with Anthropic Claude, Meta Muse, and OpenAI Function Calling formats.

---

## 📜 License & Community

Licensed under the [MIT License](LICENSE). Copyright © 2026 [GenPark AI](https://www.genpark.ai).
Follow us on LinkedIn: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550) | [https://www.llinkedin.com/company/92955550](https://www.llinkedin.com/company/92955550)
