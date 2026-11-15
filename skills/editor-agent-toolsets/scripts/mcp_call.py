"""Minimal raw JSON-RPC client for an editor MCP server (loopback only).

Usage (engine or system Python 3.9+):
  python -I mcp_call.py list
  python -I mcp_call.py describe <Toolset.Name> [...]
  python -I mcp_call.py tools <Toolset.Name.Tool> [...]
  python -I mcp_call.py call <Toolset.Name> <Tool> '<json arguments>'
Environment: MCP_URL (default http://127.0.0.1:8000/mcp), MCP_OUT (folder for one JSON file per call).
"""
import json
import os
import sys
import urllib.error
import urllib.request

URL = os.environ.get('MCP_URL', 'http://127.0.0.1:8000/mcp')
OUT = os.environ.get('MCP_OUT')
if not URL.startswith(('http://127.0.0.1', 'http://localhost')):
    sys.exit('refusing a non-loopback MCP_URL')

_session = None
_next_id = 0


def rpc(method, params=None, notify=False, tag=None):
    global _session, _next_id
    body = {'jsonrpc': '2.0', 'method': method}
    if params is not None:
        body['params'] = params
    if not notify:
        _next_id += 1
        body['id'] = _next_id
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream'}
    if _session:
        headers['Mcp-Session-Id'] = _session
    request = urllib.request.Request(URL, json.dumps(body).encode(), headers)
    try:
        response = urllib.request.urlopen(request, timeout=120)
        text, status = response.read().decode(), response.status
        _session = response.headers.get('Mcp-Session-Id') or _session
    except urllib.error.HTTPError as error:
        text, status = error.read().decode(), error.code
    if OUT and tag:
        os.makedirs(OUT, exist_ok=True)
        with open(os.path.join(OUT, tag + '.json'), 'w', encoding='utf-8') as f:
            json.dump({'request': body, 'status': status, 'response': text}, f, indent=1)
    for line in [text] + [l[5:] for l in text.splitlines() if l.startswith('data:')]:
        try:
            return json.loads(line)
        except ValueError:
            continue
    return {'status': status, 'raw': text}


def main(argv):
    rpc('initialize', {'protocolVersion': '2025-03-26', 'capabilities': {},
                       'clientInfo': {'name': 'mcp_call', 'version': '0.1'}}, tag='initialize')
    rpc('notifications/initialized', notify=True)
    if not argv or argv[0] == 'list':
        result = rpc('tools/call', {'name': 'list_toolsets', 'arguments': {}}, tag='list_toolsets')
    elif argv[0] == 'describe':
        result = rpc('tools/call', {'name': 'describe_toolsets', 'arguments': {'toolset_names': argv[1:]}}, tag='describe_toolsets')
    elif argv[0] == 'tools':
        result = rpc('tools/call', {'name': 'describe_tools', 'arguments': {'tool_names': argv[1:]}}, tag='describe_tools')
    elif argv[0] == 'call' and len(argv) >= 3:
        arguments = json.loads(argv[3]) if len(argv) > 3 else {}
        result = rpc('tools/call', {'name': 'call_tool', 'arguments': {
            'toolset_name': argv[1], 'tool_name': argv[2], 'arguments': arguments}}, tag='call_' + argv[2])
    else:
        sys.exit(__doc__)
    print(json.dumps(result, indent=1)[:20000])


if __name__ == '__main__':
    main(sys.argv[1:])
