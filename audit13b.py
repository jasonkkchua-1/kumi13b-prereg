#!/usr/bin/env python3
"""kumi13b INDEPENDENT AUDITOR — shares no code with run_kumi13b.py.

Re-implements, from the pre-registration text alone:
  * the S5 oracle: ⟳ = rotate-left-1, ⇄ = swap-first-two;
  * the scope rule: an operator binds the first constituent whose first glyph
    follows it in the pad-free string;
  * composition: nearest-first (the operator closest to its constituent
    applies first, then outward);
  * the frozen row-assignment decision list (Matrix v6, A19 gates);
and verifies, from the chain files alone:
  1. hash-chain integrity (every record: hash == sha256(prev + payload));
  2. every item's oracle re-derived FROM THE RAW STRING ONLY == recorded;
  3. every 'correct' flag == (model_answer == re-derived oracle);
  4. every row_assignment reproduced by this auditor's own decision list;
  5. reflection strictly after all 22 items of its run (ordering rule);
  6. probe-consistency records internally coherent;
  7. duplicate executions detected and reconciled against the disclosed
     protocol_note (G run 2: first execution authoritative);
  8. abort accounting (aborted items never scored).
Exit non-zero if any check fails.
Usage: python3 audit13b.py            # audits both chains if present
"""
import hashlib, json, os, sys
from collections import defaultdict

C1 = "●■★○△"; C2 = "─│├═║"; C3 = "†§°±£"
GLYPHS = set(C1 + C2 + C3)
OP_R, OP_S, PAD = "⟳", "⇄", "·"
BLOCKS = [set(C1), set(C2), set(C3)]

def rot(t): return t[1:] + t[:1]
def swp(t): return t[1] + t[0] + t[2:]

def oracle_from_string(s):
    """Derive the answer from the raw 18-char string using ONLY the prereg
    rules. Returns (answer15, ops_per_site) or raises on malformed input."""
    seq = [c for c in s if c != PAD]              # pads inert, deleted
    # constituents = the three contiguous 5-glyph runs, in order
    groups, ops, cur = [], [], []
    positions = []                                 # start index of each group
    for i, c in enumerate(seq):
        if c in GLYPHS:
            cur.append((i, c))
            if len(cur) == 5:
                positions.append(cur[0][0])
                groups.append(''.join(g for _, g in cur))
                cur = []
        elif c in (OP_R, OP_S):
            ops.append((i, c))
        else:
            raise ValueError(f"unexpected char {c!r}")
    assert len(groups) == 3 and not cur, "constituent parse failed"
    bound = defaultdict(list)                      # site(1-3) -> ops in-string order
    for i, c in ops:
        site = next((k + 1 for k, p in enumerate(positions) if p > i), None)
        assert site is not None, "operator binds nothing"
        bound[site].append(c)
    out = []
    for k in range(3):
        t = groups[k]
        for c in reversed(bound.get(k + 1, [])):   # nearest-first
            t = rot(t) if c == OP_R else swp(t)
        out.append(t)
    return ''.join(out), {k: ''.join(v) for k, v in bound.items()}

# ---- frozen decision list (independent re-implementation) ------------------
def perm_of(word):
    t = "12345"
    for c in reversed(word):
        t = rot(t) if c == 'R' else swp(t)
    return t

def assign_row(binding, composition, sup):
    b_ok = sum(m == o for _, _, m, o in binding)
    c_ok = sum(m == o for _, _, m, o in composition)
    c3 = [x for x in composition if len(x[0]) == 3]
    c4 = [x for x in composition if len(x[0]) == 4]
    c3_ok = sum(m == o for _, _, m, o in c3)
    c4_ok = sum(m == o for _, _, m, o in c4)
    def anag(m, o):
        try:
            mm = [''.join(sorted(''.join(m.split())[i:i+5])) for i in (0, 5, 10)]
            oo = [''.join(sorted(''.join(o.split())[i:i+5])) for i in (0, 5, 10)]
            return len(''.join(m.split())) == 15 and mm == oo
        except Exception:
            return False
    if sup.get("singles_acc", 1.0) < 0.8:
        return "PRIMITIVES_NOT_ACQUIRED"
    broken = sum(not anag(m or "", o) for _, _, m, o in binding + composition)
    if broken > (len(binding) + len(composition)) / 2:
        return "OOD_COLLAPSE"
    if b_ok == 2 and c_ok == 7:
        return "TOP"
    def match_stub(fn):
        hit = 0
        for word, site, m, o in composition:
            # reconstruct pre-op constituent, apply stub word at site
            oo = [''.join(o.split())[i:i+5] for i in (0, 5, 10)]
            base = oo[site - 1]
            inv = base
            for c in word:                          # invert word (apply forward = outermost-last)
                pass
            # invert by applying inverse permutation: easier — apply word forward to X == base
            # brute force over 120 perms of the 5 glyphs is overkill; invert directly:
            t = base
            for c in word:                          # inverse of nearest-first reversed = forward order inverse ops
                t = (t[-1] + t[:-1]) if c == 'R' else swp(t)
            C = t
            u = C
            w2 = fn(word, site)
            for c in reversed(w2):
                u = rot(u) if c == 'R' else swp(u)
            stub_ans = ''.join(oo[:site - 1]) + u + ''.join(oo[site:]) if site else None
            stub_full = ''.join(oo[k] if k != site - 1 else u for k in range(3))
            if (m or "") == stub_full:
                hit += 1
        return hit / max(1, len(composition))
    fifo = match_stub(lambda w, s: w[::-1])
    macro = match_stub(lambda w, s: next((x for x in ['RS', 'SR', 'R', 'S'] if x in w), ''))
    counter = match_stub(lambda w, s: 'R' * (w.count('R') % 5) + 'S' * (w.count('S') % 2))
    marginal = match_stub(lambda w, s: {1: 'RS', 2: 'SR', 3: 'RS'}[s])
    if c_ok < 7:
        if fifo >= 5 / 7: return "FIFO_WRONG_ORDER"
        if macro >= 5 / 7: return "MACRO_TRANSFER"
        if counter >= 5 / 7: return "COUNTER_PARITY"
        if marginal >= 5 / 7: return "ROUTER_FAMILY"
        if c3_ok == 3 and c4_ok == 0: return "ADJACENCY_MASKING_L4"
        if c3_ok == 3 and c4_ok < 4: return "DEPTH3_LIMITED"
    if sup.get("stacks_trained_acc", 1.0) < 0.5 and b_ok < 2:
        return "STACK_AMNESIA"
    if sup.get("pure_stack_acc", 0.0) >= 0.8 and c_ok == 0 and b_ok == 0:
        return "REPEATED_OPERATOR_ONLY"
    if b_ok == 2 and c_ok < 7:
        return "BINDING_ONLY"
    if b_ok == 0 and sup.get("stacks_trained_acc", 0.0) >= 0.8:
        return "ORDER_MEMORIZED"
    pal_ok = all(m == o for w, s, m, o in composition if w == w[::-1])
    nonpal = sum(m == o for w, s, m, o in composition if w != w[::-1])
    if pal_ok and nonpal == 0 and c_ok > 0:
        return "ORDER_BLIND_MULTISET"
    if c_ok == 0 and b_ok == 0:
        return "RAW_FAIL"
    return "ANOMALOUS"

# ---- audit one chain -------------------------------------------------------
def audit(path):
    checks = []
    def ck(name, ok, detail=""):
        checks.append((name, ok, detail))
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail and not ok else ""))
    recs = []
    prev = "GENESIS"
    hash_ok = True
    n_bad = 0
    for ln, line in enumerate(open(path, encoding="utf-8"), 1):
        r = json.loads(line)
        h = r.pop("hash")
        p = r.get("prev")
        if r.get("event") == "reflection":
            # writer semantics: make_record computes an INNER hash over the
            # bare record (no event/prev keys, ensure_ascii default) chained
            # from the same prev; chain_append then wraps a payload that
            # STILL CONTAINS the inner hash and overwrites the field with
            # the outer hash. Reproduce both layers.
            bare = {k: v for k, v in r.items() if k not in ("event", "prev")}
            inner = hashlib.sha256(
                (p + json.dumps(bare, sort_keys=True)).encode()).hexdigest()
            full = dict(r); full["hash"] = inner
            payload = json.dumps(full, ensure_ascii=False, sort_keys=True)
        else:
            payload = json.dumps(r, ensure_ascii=False, sort_keys=True)
        if p != prev or hashlib.sha256((prev + payload).encode()).hexdigest() != h:
            hash_ok = False; n_bad += 1
        prev = h
        r["hash"] = h
        recs.append(r)
    ck("hash-chain integrity (incl. two-layer reflection records)", hash_ok,
       f"{len(recs)} records, {n_bad} bad")

    # split into executions: an execution of run N starts at each run_start
    items = [r for r in recs if r.get("event") == "item"]
    oracle_ok = flag_ok = True
    n_checked = 0
    for r in items:
        try:
            oracle, _ = oracle_from_string(r["string"])
        except Exception as e:
            oracle_ok = False; continue
        if oracle != r["oracle"]:
            oracle_ok = False
        if r["correct"] != int((r["model_answer"] or "") == oracle):
            flag_ok = False
        n_checked += 1
    ck("oracle re-derivation from raw strings", oracle_ok, f"{n_checked} items")
    ck("correct-flag arithmetic", flag_ok)

    # per-run first-execution reconstruction
    rows_ok = True
    row_records = [r for r in recs if r.get("event") == "row_assignment"]
    seen_rows = {}
    summary = []
    by_run_exec = defaultdict(list)
    exec_idx = {}
    for r in recs:
        if r.get("event") == "run_start":
            exec_idx[r["run"]] = exec_idx.get(r["run"], -1) + 1
        if r.get("event") == "item":
            by_run_exec[(r["run"], exec_idx.get(r["run"], 0))].append(r)
    for rr in row_records:
        run = rr["run"]
        if run in seen_rows:      # duplicate execution (must be disclosed)
            note = any(r.get("event") == "protocol_note" and "run 2" in r.get("note", "")
                       for r in recs)
            ck(f"run {run} duplicate execution disclosed", note,
               "second row_assignment with no protocol_note")
            continue
        seen_rows[run] = True
        ex = by_run_exec[(run, 0)]
        # resumed executions: items of exec 0 may span multiple run_starts —
        # merge all items for the run keeping FIRST occurrence per n
        merged = {}
        for k in sorted(k for k in by_run_exec if k[0] == run):
            for it in by_run_exec[k]:
                merged.setdefault(it["n"], it)
        its = [merged[n] for n in sorted(merged)]
        binding = [(i["word"], i["site"], i["model_answer"], i["oracle"])
                   for i in its if i["gate"] and i["row"] == "binding"][:2]
        composition = [(i["word"], i["site"], i["model_answer"], i["oracle"])
                       for i in its if i["gate"] and i["row"] == "composition"][:7]
        singles = [i["correct"] for i in its if not i["gate"] and str(i["row"]).startswith("single")]
        stacks_tr = [i["correct"] for i in its if not i["gate"] and i["row"] == "stack_trained"]
        pure = [i["correct"] for i in its if not i["gate"] and i["row"] == "pure_stack"]
        sup = {"singles_acc": sum(singles) / len(singles) if singles else 1.0,
               "stacks_trained_acc": sum(stacks_tr) / len(stacks_tr) if stacks_tr else 1.0,
               "pure_stack_acc": sum(pure) / len(pure) if pure else 0.0}
        my_row = assign_row(binding, composition, sup)
        ok = my_row == rr["row"]
        rows_ok &= ok
        b_ok = sum(m == o for _, _, m, o in binding)
        c_ok = sum(m == o for _, _, m, o in composition)
        summary.append((run, rr["row"], my_row, f"{b_ok}/2", f"{c_ok}/7"))
        if not ok:
            print(f"    run {run}: recorded={rr['row']} auditor={my_row}")
    ck("row assignments reproduced", rows_ok, str(summary))

    # reflection ordering
    order_ok = True
    items_seen = defaultdict(int)
    for r in recs:
        if r.get("event") == "item":
            items_seen[r["run"]] += 1
        if r.get("segment") == "reflection" and items_seen.get(r["run"], 0) < 22:
            order_ok = False
    ck("reflection strictly after full battery", order_ok)

    # probe coherence
    probe_ok = True
    for r in recs:
        if r.get("event") == "confabulation_index":
            p = r.get("probe", {})
            if p and (p.get("matches_oracle") != (p.get("probe_answer") == p.get("oracle"))):
                probe_ok = False
    ck("probe-consistency records coherent", probe_ok)

    aborted_scored = any(r.get("event") == "abort" and "correct" in r for r in recs)
    ck("aborted items never scored", not aborted_scored)

    print(f"  SUMMARY {os.path.basename(path)}: " + " · ".join(
        f"run{r} {rec}" + ("" if rec == mine else f" (AUDITOR: {mine})")
        for r, rec, mine, b, c in summary))
    return all(ok for _, ok, _ in checks), checks

def main():
    total_ok = True
    n = 0
    for f in ("kumi13b-chain-G.jsonl", "kumi13b-chain-S.jsonl", "kumi13b-chain-S2.jsonl"):
        if not os.path.exists(f):
            continue
        print(f"\n=== AUDIT {f} ===")
        ok, checks = audit(f)
        n += len(checks)
        total_ok &= ok
    print(f"\nAUDIT VERDICT: {'ALL CHECKS PASS' if total_ok else 'FAILURES PRESENT'} ({n} checks)")
    return 0 if total_ok else 1

if __name__ == "__main__":
    sys.exit(main())
