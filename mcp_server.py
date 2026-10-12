"""MCP Server for Multi-Agent Resource Deadlock Wait-For Graph Resolver."""
import sys
import json
import time
from client import MultiAgentResourceDeadlockWaitForGraphResolver

resolver = MultiAgentResourceDeadlockWaitForGraphResolver()

def handle_call_tool(params):
    name = params.get("name")
    args = params.get("arguments", {})
    if name != "resolve_multi_agent_deadlock":
        raise ValueError(f"Unknown tool: {name}")

    action = args.get("action", "detect_and_resolve_deadlocks")
    if action == "detect_and_resolve_deadlocks":
        return resolver.detect_and_resolve_deadlocks(args.get("agent_states", []))
    else:
        raise ValueError(f"Invalid action: {action}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Running self-test...")
        states = [
            {"agent_id": "agent_excel_writer", "holds_resources": ["lock_sheet_A"], "waits_for_resource": "lock_db_ledger", "rollback_cost_score": 85.0},
            {"agent_id": "agent_sql_auditor", "holds_resources": ["lock_db_ledger"], "waits_for_resource": "lock_ppt_deck", "rollback_cost_score": 40.0},
            {"agent_id": "agent_slide_compiler", "holds_resources": ["lock_ppt_deck"], "waits_for_resource": "lock_sheet_A", "rollback_cost_score": 15.0}
        ]
        res = resolver.detect_and_resolve_deadlocks(states)
        assert res["deadlock_detected"] is True
        assert res["selected_victim_agent"] == "agent_slide_compiler"
        assert "lock_ppt_deck" in res["released_resources"]
        print("Self-test PASSED!")
        sys.exit(0)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            msg_id = req.get("id")
            method = req.get("method")
            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {"name": "MultiAgentResourceDeadlockWaitForGraphResolver", "version": "1.0.0"},
                        "capabilities": {"tools": {}}
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [{
                            "name": "resolve_multi_agent_deadlock",
                            "description": "Construct Wait-For Graph from agent lock allocations, detect circular wait cycles, and preempt minimum-cost victim agent.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "action": {"type": "string", "enum": ["detect_and_resolve_deadlocks"]},
                                    "agent_states": {"type": "array"}
                                },
                                "required": ["action"]
                            }
                        }]
                    }
                }
            elif method == "tools/call":
                res = handle_call_tool(req.get("params", {}))
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {}}
            print(json.dumps(resp), flush=True)
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err_resp), flush=True)

if __name__ == "__main__":
    main()
