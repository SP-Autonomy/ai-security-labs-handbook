import re
MASKS = [
  (re.compile(r"\b\d{16}\b"), "****-****-****-****"),     # naive card
  (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "***-**-****"),   # US SSN-ish
  (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "<email>"),
]

def dlp_pre(req):
    original_txt = req.get("prompt","")  # ← Save original
    txt = original_txt
    for rx, rep in MASKS:
        txt = rx.sub(rep, txt)
    req["prompt"] = txt
    # simple sensitivity hint
    req["contains_sensitive"] = txt != original_txt  # ← Compare to original
    return req

def dlp_post(res):
    out = res.get("answer", "")
    for rx, rep in MASKS:
        out = rx.sub(rep, out)
    res["answer"] = out
    return res
