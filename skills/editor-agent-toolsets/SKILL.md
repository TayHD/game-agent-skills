---
name: editor-agent-toolsets
description: Enable and use the Unreal Engine 5.9 editor's built-in MCP server and agent toolsets safely - editor-only plugins, loopback only, the four meta-tools (list_toolsets, describe_toolsets, describe_tools, call_tool), the stdio proxy, the shipping-receipt gate and the acceptance calls. Use when turning on editor toolsets, calling editor tools from an agent, or checking that none reach a shipped build.
metadata:
  version: "0.1.0"
  updated: "2026-11-15"
---

# Editor agent toolsets (UE 5.9)

## Settings the project supplies

| Setting | Meaning |
|---|---|
| `ENGINE_ROOT` | The engine root (for the proxy executable path). |
| `UPROJECT` | The project file where plugins are enabled. |
| `MCP_JSON` | The client MCP configuration file to install the proxy into. |
| `TOOLSET_LIST` | The toolset plugins the project enables, by name. |
| `SLOT_RULES` | The exclusive engine slot; a running editor holds it. |
| `INSTRUCTIONS_TEXT` | The short project rules sent to every MCP client on connect. |

## What the engine provides

- Plugin `ModelContextProtocol` serves `http://localhost:8000/mcp` (defaults). `bAutoStartServer` defaults to false; set it true in the editor per-project user settings. Commandlets skip the configured auto-start, so only an interactive editor binds the port.
- With tool search on, a client sees four meta-tools and discovers the rest on demand:
  - `list_toolsets` - every registered toolset;
  - `describe_toolsets` with `toolset_names` - the tools in each;
  - `describe_tools` with `tool_names` (`<Toolset>.<Tool>`) - parameters;
  - `call_tool` with `toolset_name`, `tool_name`, `arguments`.
- Toolsets are separate experimental plugins registered through `ToolsetRegistry`; enabling them needs an editor rebuild.
- A stdio proxy (`Engine/Plugins/Experimental/ModelContextProtocol/Extras/Proxy/Bin/Win64/unreal_mcp_proxy.exe`) keeps the client connected across editor restarts. Install it with `unreal_mcp_proxy.exe --mcp-json <MCP_JSON> install`; the flag goes before the subcommand.

## Enabling safely

1. Enable each plugin in `TOOLSET_LIST` by name in `UPROJECT` with `"Enabled": true, "TargetAllowList": ["Editor"]`. Add the same editor-only entry for `ModelContextProtocol`, `ToolsetRegistry` and `AIAssistant`, which are on by default and have runtime modules. Avoid an all-toolsets aggregator; it enables engine plugins the project does not use.
2. Server settings: port 8000, tool search on, allowed origins empty (loopback only), optionally dump captured media to disk and prune that folder.
3. Put `INSTRUCTIONS_TEXT` in the project's game config: hold the slot before any call, back up before changing assets, never edit imported art.
4. Rebuild the editor. Test whether a commandlet binds the port before turning auto-start on.
5. **Shipping gate:** the server and shipping client target receipts list no module whose name contains `Toolset`, `ModelContextProtocol`, `AgentLook`, `WidgetFinder` or `AIAssistant`. Check after every package.

## Using the tools

- A call needs a running editor, which holds the engine slot: take the slot first.
- List, describe, then call. Read a tool's parameters before its first call.
- Input and cheat tools need a PIE session. Live Coding is disabled in an `-unattended` editor until `EnableLiveCoding` is called; then `CompileLiveCoding` works.
- A server added to the MCP config during a session does not reach that session; call it with raw JSON-RPC over HTTP instead (`scripts/mcp_call.py`).
- Tools can save assets: the backup and imported-art rules apply to every write.

## Acceptance calls (one per group)

Initialize and list the four meta-tools; `list_toolsets`; then one read-only call per enabled group (for example list Blueprint graphs, check Live Coding readiness, list automation tests, search console variables, list stat groups, query navigation info, list State Tree states, describe a widget, list knowledge bases). Keep each request and response as evidence. The proxy's reconnect across an editor restart is checked from a fresh client session.

## Done when

The editor builds with the toolsets, every group answers a call, the shipping receipts pass the gate, and no existing harness is retired until a call-by-call mapping shows a tool replaces it.
