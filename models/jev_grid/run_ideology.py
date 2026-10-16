"""Run the pre-registered ideology elicitation (ideology_def.py) against the Jev HTTPS API."""
import json, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
from ideology_def import cells, state, QUESTIONS, PROTOCOL, FACTORS

URL = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-latest"
KEY = next(l.split("=", 1)[1].strip() for l in open("C:/code/jev/.env", encoding="utf-8") if l.startswith("jev_api="))
QS = {k: {"type": "noul", "instructions": v} for k, v in QUESTIONS.items()}


def ask(st):
    for attempt in range(5):
        try:
            body = json.dumps({"model": MODEL, "state": st, "questions": QS}).encode()
            req = urllib.request.Request(URL, body, {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as r:
                d = json.load(r)
            return {k: v["noul"] for k, v in d["answers"].items()}, d.get("model", MODEL)
        except Exception as e:
            err = e; time.sleep(1 + attempt)
    raise err


def main(out):
    cs = cells(); jobs = [(ci, k) for ci in range(len(cs)) for k in range(3)]
    t0 = time.time()
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(lambda j: ask(state(cs[j[0]], j[1])), jobs))
    rows = [dict(cell=ci, para=k, **cs[ci], **a) for (ci, k), (a, m) in zip(jobs, res)]
    json.dump(dict(protocol=PROTOCOL, factors=FACTORS, model=res[0][1], n_calls=len(jobs), seconds=round(time.time() - t0, 1),
                   rows=rows), open(out, "w"), indent=0)
    print(len(rows), round(time.time() - t0, 1), res[0][1])


if __name__ == "__main__":
    main(sys.argv[1])
