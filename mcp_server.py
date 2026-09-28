import sys
import json
from client import HarrisCornerDetector

def handle_rpc(line):
    try:
        req = json.loads(line)
    except Exception:
        return
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        res = {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "genpark-harris-corner-feature-detector-skill", "version": "1.0.0"},
            "capabilities": {"tools": {}}
        }
    elif method == "tools/list":
        res = {
            "tools": [
                {
                    "name": "detect_corners",
                    "description": "Detect Harris corners and salient interest points in a grayscale image matrix",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "image": {"type": "array", "items": {"type": "array", "items": {"type": "number"}}},
                            "k": {"type": "number", "default": 0.04},
                            "threshold": {"type": "number", "default": 1e4}
                        },
                        "required": ["image"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "detect_corners":
            detector = HarrisCornerDetector(k=args.get("k", 0.04), threshold=args.get("threshold", 1e4))
            data = detector.detect_corners(args.get("image", []))
            res = {"content": [{"type": "text", "text": json.dumps(data)}]}
        else:
            res = {"isError": True, "content": [{"type": "text", "text": f"Unknown tool {tool_name}"}]}
    else:
        res = {"error": {"code": -32601, "message": "Method not found"}}

    resp = {"jsonrpc": "2.0", "id": req_id, "result": res.get("result", res)}
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()

def main():
    for line in sys.stdin:
        if line.strip():
            handle_rpc(line.strip())

if __name__ == "__main__":
    main()
