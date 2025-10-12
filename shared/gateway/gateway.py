from time import perf_counter
from typing import Dict, Any, List, Callable

Processor = Callable[[Dict[str, Any]], Dict[str, Any]]

class Chain:
    def __init__(self, pre: List[Processor], post: List[Processor], llm_call: Callable):
        self.pre = pre
        self.post = post
        self.llm_call = llm_call

    def run(self, req: Dict[str, Any]) -> Dict[str, Any]:
        meta = {"stages": [], "p95_hint_ms": None}
        x = req
        for p in self.pre:
            t0 = perf_counter()
            x = p(x)
            meta["stages"].append({"name": p.__name__, "latency_ms": round((perf_counter()-t0)*1000, 1)})
            if x.get("_blocked"):
                return {"blocked": True, "reason": x.get("_reason"), "meta": meta}
        t0 = perf_counter()
        y = self.llm_call(x)
        meta["stages"].append({"name": "llm_call", "latency_ms": round((perf_counter()-t0)*1000, 1)})
        for p in self.post:
            t0 = perf_counter()
            y = p({**x, **y})
            meta["stages"].append({"name": p.__name__, "latency_ms": round((perf_counter()-t0)*1000, 1)})
        y["meta"] = meta
        return y