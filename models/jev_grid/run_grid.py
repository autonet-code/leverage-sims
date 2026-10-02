import json, sys, time, urllib.request, threading
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, __import__("os").path.dirname(__file__))
from grid_def import cells, state, QUESTIONS, PROTOCOL, FACTORS

URL = "http://127.0.0.1:9117/mcp"
H = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
QJSON = json.dumps({k: {"type": "noul", "instructions": v} for k, v in QUESTIONS.items()})
_loc = threading.local()


def post(body, sid=None):
    h = dict(H)
    if sid:
        h["Mcp-Session-Id"] = sid
    r = urllib.request.urlopen(urllib.request.Request(URL, json.dumps(body).encode(), h), timeout=120)
    return r.headers.get("Mcp-Session-Id"), r.read().decode()


def session():
    if not getattr(_loc, "ok", False):
        sid, _ = post({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "grid", "version": "1"}}})
        post({"jsonrpc": "2.0", "method": "notifications/initialized"}, sid)
        _loc.sid = sid; _loc.ok = True
    return _loc.sid


def ask(st):
    for attempt in range(5):
        try:
            sid = session()
            _, b = post({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "jev", "arguments": {"state": st, "questions": QJSON}}}, sid)
            res = json.loads(b)["result"]
            if res.get("isError"):
                raise RuntimeError(res["content"][0]["text"][:300])
            d = json.loads(res["content"][0]["text"])
            return {k: v["noul"] for k, v in d["answers"].items()}, d.get("model")
        except Exception as e:
            err = e; _loc.ok = False; time.sleep(1 + attempt)
    raise err


def main(out):
    jobs = []
    for arm in ["closed", "control"]:
        for ci, c in enumerate(cells()):
            for k in range(3):
                jobs.append((arm, ci, k))
    t0 = time.time()
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(lambda j: ask(state(cells()[j[1]], j[2], j[0])), jobs))
    rows = []
    for (arm, ci, k), (ans, model) in zip(jobs, res):
        rows.append(dict(arm=arm, cell=ci, para=k, **cells()[ci], **ans))
    json.dump(dict(protocol=PROTOCOL, factors=FACTORS, model=res[0][1], n_calls=len(jobs), seconds=round(time.time() - t0, 1),
                   rows=rows), open(out, "w"), indent=0)
    print(len(rows), time.time() - t0, res[0][1])


if __name__ == "__main__":
    main(sys.argv[1])
