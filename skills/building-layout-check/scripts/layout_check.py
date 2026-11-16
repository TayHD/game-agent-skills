#!/usr/bin/env python3
"""layout_check.py: space-graph check for a building or enclosed environment.

Part of the building-layout-check skill. Python 3.8+, standard library only.

Usage:
  python3 -I layout_check.py GRAPH.json [--profile explore|contested]
                             [--site building|natural|ruin|vessel]
                             [--set NAME=VALUE ...] [--json OUT.json]

Settings are applied in this order, later wins: script defaults, the graph's
"settings", --profile and --site, then --set. Unknown setting names are an error.
The graph format is described in templates/space_graph.example.json.
Exit codes: 0 no blocker, 1 at least one blocker, 2 bad input or usage.
"""

import argparse
import json
import math
import sys
from collections import defaultdict, deque

DEFAULTS = {
    "PROFILE": "explore",            # explore | contested
    "SITE": "building",              # building | natural | ruin | vessel
    "RULES_OFF": "",                 # comma list of rule ids reported as NOTE only
    "PLAYER_RADIUS": 0.40,
    "CROUCH_HEIGHT": 1.10,
    "MIN_HEADROOM": 2.10,
    "MIN_DOOR_WIDTH": 0.90,
    "MIN_CORRIDOR_WIDTH": 1.20,
    "MIN_SPIRAL_WIDTH": 0.70,
    "MIN_CLIMB_WIDTH": 0.60,
    "LARGE_AGENT_DIAMETER": 0.0,
    "STAIR_RISER_MIN": 0.10,
    "STAIR_RISER_MAX": 0.20,
    "STAIR_TREAD_MIN": 0.22,
    "STAIR_TREAD_MAX": 0.40,
    "STAIR_PACE_MIN": 0.55,          # 2 x riser + tread, the stride rule
    "STAIR_PACE_MAX": 0.70,
    "MAX_RISERS_PER_FLIGHT": 16,
    "STEP_HEIGHT": 0.45,
    "GUARD_DROP": 1.00,
    "TUBE_LENGTH": 15.0,
    "DEAD_END_DEPTH": None,          # profile default: explore 20, contested 10
    "EXIT_SPACING": 10.0,
    "VERTICAL_SPACING": 15.0,
    "MAX_ROOM_OPENINGS": 4,
    "MIN_SPACE_AREA": 1.0,
}

LINK_KINDS = {"door", "opening", "stair", "ramp", "ladder", "hatch", "lift", "window",
              "drop", "climb", "swim", "squeeze"}
WIDTH_MIN_KEY = {"door": "MIN_DOOR_WIDTH", "opening": "MIN_DOOR_WIDTH", "stair": "MIN_DOOR_WIDTH",
                 "ramp": "MIN_DOOR_WIDTH", "ladder": "MIN_CLIMB_WIDTH", "climb": "MIN_CLIMB_WIDTH",
                 "hatch": "MIN_CLIMB_WIDTH", "swim": "MIN_CLIMB_WIDTH", "lift": "MIN_DOOR_WIDTH"}
LOW_LINKS = {"squeeze", "swim", "ladder", "climb", "hatch", "window"}   # headroom judged as crouch
ROOM_KINDS = {"room", "corridor", "landing", "chamber", "roof", "deck", "passage"}
OPENING_KINDS = {"room", "chamber"}
NOT_INTERIOR = {"exterior", "void"}
RULES = ["reach", "return", "sealed", "exits", "dead_end", "dead_share", "loop", "funnel", "vertical",
         "door_width", "corridor_width", "large_width", "headroom", "step", "guard", "stair", "tube",
         "small", "openings"]
# Rules a natural site or a ruin does not owe in explore (they come from how buildings are designed).
DESIGN_RULES = {"exits", "loop", "funnel", "dead_share", "tube"}


class Report:
    def __init__(self, accepted, off, soft):
        self.items, self.accepted, self.off, self.soft = [], accepted, off, soft

    def add(self, level, rule, msg, where=None):
        if level in ("BLOCKER", "FINDING"):
            hits = [a for a in self.accepted if a.get("rule") == rule and
                    (a.get("space") is None and a.get("link") is None or where in (a.get("space"), a.get("link")))]
            if hits:
                r = hits[0].get("reason", "")
                level, msg = "ACCEPTED", f"{msg} (accepted: {r})" if r else f"{msg} (accepted)"
            elif rule in self.off:
                level, msg = "NOTE", f"{msg} (rule switched off)"
            elif rule in self.soft:
                level, msg = "NOTE", f"{msg} (not required for this site type)"
        self.items.append({"level": level, "rule": rule, "where": where, "message": msg})

    def count(self, level):
        return sum(1 for i in self.items if i["level"] == level)


def die(msg):
    print(f"layout_check: {msg}", file=sys.stderr)
    sys.exit(2)


def parse_value(text):
    for cast in (int, float):
        try:
            return cast(text)
        except ValueError:
            pass
    return text


def pos(obj):
    return (float(obj["x"]), float(obj["y"])) if "x" in obj and "y" in obj else None


def dist(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])


def node_disjoint_paths(adj, s, t, limit=3):
    """Number of internally node-disjoint paths s->t, capped at limit (unit node capacities)."""
    cap, graph = defaultdict(int), defaultdict(set)

    def add(u, v, c):
        cap[(u, v)] += c
        graph[u].add(v)
        graph[v].add(u)

    for v in adj:
        add((v, 0), (v, 1), limit if v in (s, t) else 1)
        for w in adj[v]:
            add((v, 1), (w, 0), limit)
    src, sink, flow = (s, 1), (t, 0), 0
    while flow < limit:
        parent, q = {src: None}, deque([src])
        while q and sink not in parent:
            u = q.popleft()
            for v in graph[u]:
                if v not in parent and cap[(u, v)] > 0:
                    parent[v] = u
                    q.append(v)
        if sink not in parent:
            break
        v = sink
        while parent[v] is not None:
            u = parent[v]
            cap[(u, v)] -= 1
            cap[(v, u)] += 1
            v = u
        flow += 1
    return flow


def bfs(start, graph):
    seen, q = {start}, deque([start])
    while q:
        u = q.popleft()
        for v in graph[u]:
            if v not in seen:
                seen.add(v)
                q.append(v)
    return seen


def main():
    ap = argparse.ArgumentParser(description="Space-graph layout check (building-layout-check skill).")
    ap.add_argument("graph")
    ap.add_argument("--profile", choices=["explore", "contested"])
    ap.add_argument("--site", choices=["building", "natural", "ruin", "vessel"])
    ap.add_argument("--set", action="append", default=[], metavar="NAME=VALUE")
    ap.add_argument("--json", metavar="OUT")
    args = ap.parse_args()

    try:
        with open(args.graph, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        die(f"cannot read {args.graph}: {exc}")

    st = dict(DEFAULTS)
    overrides = [(k.upper(), v) for k, v in data.get("settings", {}).items()]
    if args.profile:
        overrides.append(("PROFILE", args.profile))
    if args.site:
        overrides.append(("SITE", args.site))
    for item in args.set:
        if "=" not in item:
            die(f"--set needs NAME=VALUE, got {item!r}")
        k, v = item.split("=", 1)
        overrides.append((k.strip().upper(), parse_value(v.strip())))
    for k, v in overrides:
        if k not in DEFAULTS:
            die(f"unknown setting {k!r}; known settings: {', '.join(sorted(DEFAULTS))}")
        st[k] = v
    if st["PROFILE"] not in ("explore", "contested"):
        die("PROFILE must be explore or contested")
    if st["SITE"] not in ("building", "natural", "ruin", "vessel"):
        die("SITE must be building, natural, ruin or vessel")
    contested = st["PROFILE"] == "contested"
    if st["DEAD_END_DEPTH"] is None:
        st["DEAD_END_DEPTH"] = 10.0 if contested else 20.0
    off = {r.strip() for r in str(st["RULES_OFF"]).split(",") if r.strip()}
    bad = off - set(RULES)
    if bad:
        die(f"RULES_OFF names unknown rule(s) {sorted(bad)}; rule ids: {', '.join(RULES)}")
    soft = DESIGN_RULES if (st["SITE"] in ("natural", "ruin") and not contested) else set()

    spaces = {}
    for s in data.get("spaces", []):
        if "id" not in s:
            die("a space has no id")
        if s["id"] in spaces:
            die(f"duplicate space id {s['id']!r}")
        spaces[s["id"]] = s
    ext = [k for k, s in spaces.items() if s.get("kind") == "exterior"]
    if not ext:
        die("the graph needs one space with kind 'exterior' (the outside world)")
    links = data.get("links", [])
    for n, l in enumerate(links):
        l.setdefault("id", f"link{n + 1}")
        l.setdefault("kind", "door")
        for end in ("a", "b"):
            if l.get(end) not in spaces:
                die(f"link {l['id']} refers to unknown space {l.get(end)!r}")
        if l["kind"] not in LINK_KINDS:
            die(f"link {l['id']} has unknown kind {l['kind']!r}; use one of {sorted(LINK_KINDS)}")
    for a in data.get("accepted", []):
        if a.get("rule") not in RULES:
            die(f"accepted entry names unknown rule {a.get('rule')!r}; rule ids: {', '.join(RULES)}")

    rep = Report(data.get("accepted", []), off, soft)
    EXT = "__exterior__"
    notes = []

    def node(sid):
        return EXT if sid in ext else sid

    def is_interior(sid):
        s = spaces[sid]
        return s.get("kind") not in NOT_INTERIOR and not s.get("sealed")

    def storey(sid):
        return 0 if sid in ext else spaces[sid].get("storey", 0)

    fwd, back, und = defaultdict(set), defaultdict(set), defaultdict(set)
    for l in links:
        a, b = node(l["a"]), node(l["b"])
        if a == b:
            continue
        fwd[a].add(b)
        back[b].add(a)
        if l["kind"] != "drop":
            fwd[b].add(a)
            back[a].add(b)
            und[a].add(b)
            und[b].add(a)

    interior = [k for k in spaces if is_interior(k)]
    area_total = sum(float(spaces[k].get("area", 0)) for k in interior if spaces[k].get("kind") != "yard")

    # 1. Reachability and return.
    reach, can_return = bfs(EXT, fwd), bfs(EXT, back)
    for k in interior:
        if k not in reach:
            rep.add("BLOCKER", "reach", f"space {k} cannot be reached from outside with the moves in the graph", k)
        elif k not in can_return:
            rep.add("BLOCKER", "return", f"space {k} can be entered but there is no way back out (one-way drops only)", k)
    for k, s in spaces.items():
        if s.get("sealed") and any(k in (l["a"], l["b"]) for l in links):
            rep.add("FINDING", "sealed", f"sealed space {k} has a link; a sealed void should have none", k)

    # 2. Exits (drops to the outside are escapes, not exits).
    exits = [l for l in links if (l["a"] in ext) != (l["b"] in ext) and l["kind"] != "drop"]
    escapes = [l for l in links if l["kind"] == "drop" and l["b"] in ext and l["a"] not in ext]
    faces = {l.get("face") for l in exits if l.get("face")}
    if area_total < 100:
        need, need_faces = (2, 2) if contested else (1, 1)
    elif area_total <= 400:
        need, need_faces = (3, 2) if contested else (2, 2)
    else:
        need, need_faces = (4, 3) if contested else (3, 2)
    counted = []
    for l in sorted(exits, key=lambda e: e["kind"] == "window"):
        p = pos(l)
        if p and any(pos(c) and dist(p, pos(c)) < st["EXIT_SPACING"] and l.get("face") == c.get("face")
                     for c in counted):
            continue
        counted.append(l)
    value = sum(0.5 if l["kind"] == "window" else 1.0 for l in counted)
    msg = (f"{len(exits)} exit(s), worth {value:g} after spacing, on {len(faces) or 'unrecorded'} face(s); "
           f"{area_total:g} m2 needs {need} on {need_faces} face(s)")
    if escapes:
        msg += f"; plus {len(escapes)} one-way escape(s) not counted"
    if value < 1:
        rep.add("BLOCKER", "exits", msg + ": no way in or out")
    elif value < need or (faces and len(faces) < need_faces):
        rep.add("BLOCKER" if contested else "FINDING", "exits", msg)
    else:
        rep.add("OK", "exits", msg)
    if len(exits) > 1 and not faces:
        notes.append("exits carry no 'face', so their spread over faces was not checked")
    if len(exits) > 1 and not all(pos(l) for l in exits):
        notes.append("some exits carry no x, y, so exits closer than EXIT_SPACING were not merged")

    # 3. Dead ends.
    rooms = [k for k in interior if spaces[k].get("kind") in ROOM_KINDS]
    dead = [k for k in rooms if len(und[k]) == 1]
    guessed = []

    def size_of(k):
        s = spaces[k]
        if s.get("length"):
            return float(s["length"])
        if s.get("area"):
            return math.sqrt(float(s["area"]))
        guessed.append(k)
        return 3.0

    for k in dead:
        depth, chain, prev, cur = size_of(k), [k], None, k
        while True:
            nxt = [v for v in und[cur] if v != prev]
            if len(nxt) != 1 or nxt[0] == EXT:
                break
            prev, cur = cur, nxt[0]
            if len(und[cur]) != 2 or spaces[cur].get("kind") not in ROOM_KINDS:
                break
            chain.append(cur)
            depth += size_of(cur)
        if depth > st["DEAD_END_DEPTH"] or len(chain) > 1:
            level = "BLOCKER" if contested and depth > st["DEAD_END_DEPTH"] else "FINDING"
            rep.add(level, "dead_end", f"dead end at {k}: {len(chain)} space(s) deep, about {depth:.0f} m "
                    f"(limit {st['DEAD_END_DEPTH']:g} m): {' <- '.join(chain)}", k)
    if guessed:
        notes.append(f"no area or length on {', '.join(sorted(set(guessed)))}; dead-end depth assumed 3 m each")
    room_only = [k for k in rooms if spaces[k].get("kind") in OPENING_KINDS]
    if contested and room_only:
        share = sum(1 for k in dead if k in room_only) / len(room_only)
        if share > 0.25:
            rep.add("FINDING", "dead_share", f"{share:.0%} of rooms are dead ends (limit 25% when contested)")

    # 4. Loops and funnel.
    inner = {k: {v for v in und[k] if v != EXT and v in interior} for k in interior}
    edges = sum(len(v) for v in inner.values()) // 2
    comps, seen = 0, set()
    for k in inner:
        if k not in seen:
            comps += 1
            seen |= bfs(k, inner)
    cycles = edges - len(inner) + comps
    lvl, q = {EXT: 0}, deque([EXT])
    while q:
        u = q.popleft()
        for v in und[u]:
            if v not in lvl:
                lvl[v] = lvl[u] + 1
                q.append(v)
    depth_rooms = max([lvl.get(k, 0) for k in interior] or [0])
    if (area_total > 400 or depth_rooms > 2) and cycles < 1:
        rep.add("BLOCKER" if contested else "FINDING", "loop",
                f"no loop inside ({area_total:g} m2, {depth_rooms} spaces deep): one route between rooms")
    else:
        rep.add("OK", "loop", f"{cycles} independent interior loop(s)")

    anchors = [k for k in interior if spaces[k].get("anchor")]
    if not anchors and room_only:
        reachable_rooms = [k for k in room_only if k in lvl]
        if reachable_rooms:
            anchors = [max(reachable_rooms, key=lambda k: (lvl[k], float(spaces[k].get("area", 0))))]
            notes.append(f"no anchor marked; funnel measured to the deepest room, {anchors[0]}")
    full = defaultdict(set)
    for k, vs in und.items():
        for v in vs:
            full[k].add(v)
            full[v].add(k)
    for a in anchors:
        if a not in reach:
            continue
        paths = node_disjoint_paths(full, EXT, a)
        msg = f"{paths} separate route(s) from outside to {a}"
        if paths < 2 and area_total > (100 if contested else 400):
            rep.add("BLOCKER" if contested else "FINDING", "funnel", msg + "; one space cuts it off", a)
        else:
            rep.add("OK", "funnel", msg, a)

    # 5. Vertical routes: any non-drop link joining two storeys, toward the entry storey.
    storeys = sorted({storey(k) for k in interior})
    entry = {storey(l["b"] if l["a"] in ext else l["a"]) for l in exits} or ({storeys[0]} if storeys else {0})
    spacing_unchecked = []
    for s in storeys:
        if s in entry:
            continue
        toward = min(entry, key=lambda e: abs(e - s))

        def joins(l, s=s, toward=toward):
            sa, sb = storey(l["a"]), storey(l["b"])
            if s not in (sa, sb) or sa == sb:
                return False
            other = sb if sa == s else sa
            return other < s if toward < s else other > s

        routes = [l for l in links if l["kind"] != "drop" and joins(l)]
        s_area = sum(float(spaces[k].get("area", 0)) for k in interior if storey(k) == s)
        need_two = s_area > 200 or (contested and s_area > 100)
        pts = [pos(l) for l in routes if pos(l)]
        spread = max((dist(p, q) for p in pts for q in pts), default=0.0)
        msg = f"storey {s}: {len(routes)} route(s) toward the entry storey, {s_area:g} m2"
        if len(pts) == len(routes) > 1:
            msg += f", furthest apart {spread:.1f} m"
        if not routes:
            if any(storey(k) == s and k in reach for k in interior):
                rep.add("NOTE", "vertical", msg + " (reached by another path)")
            else:
                rep.add("BLOCKER", "vertical", msg + ": no way there")
        elif need_two and len(routes) < 2:
            rep.add("BLOCKER" if contested else "FINDING", "vertical", msg + "; needs 2")
        elif need_two and len(pts) == len(routes) and spread < st["VERTICAL_SPACING"]:
            rep.add("FINDING", "vertical", msg + f"; needs {st['VERTICAL_SPACING']:g} m apart")
        else:
            rep.add("OK", "vertical", msg)
            if need_two and len(pts) < len(routes):
                spacing_unchecked.append(str(s))
    if spacing_unchecked:
        notes.append(f"vertical routes without x, y on storey {', '.join(spacing_unchecked)}; spacing not checked")

    # 6. Sizes, steps, guards and stairs.
    large = float(st["LARGE_AGENT_DIAMETER"] or 0)
    risers = set()
    for l in links:
        w, h, lid, kind = l.get("width"), l.get("headroom"), l["id"], l["kind"]
        where = f"{l['a']}-{l['b']}"
        min_w = st["MIN_SPIRAL_WIDTH"] if (kind == "stair" and l.get("spiral")) else st.get(WIDTH_MIN_KEY.get(kind, ""), None)
        if kind == "squeeze":
            min_w = 2 * st["PLAYER_RADIUS"]
        if min_w is not None and w is not None and float(w) < min_w:
            rep.add("BLOCKER", "door_width", f"{kind} {where} is {w} m wide (min {min_w:g})", lid)
        if l.get("large_route") and large and (w is None or float(w) < 1.5 * large):
            rep.add("BLOCKER", "large_width", f"large route {where} is {w} m wide (min {1.5 * large:g})", lid)
        if h is not None:
            low = l.get("crawl") or kind in LOW_LINKS
            min_h = st["CROUCH_HEIGHT"] if low else st["MIN_HEADROOM"]
            if float(h) < min_h:
                rep.add("BLOCKER", "headroom", f"{kind} {where} has {h} m headroom (min {min_h:g})", lid)
        if l.get("step") is not None and kind in ("door", "opening") and float(l["step"]) > st["STEP_HEIGHT"]:
            rep.add("BLOCKER", "step", f"{kind} {where} has a {l['step']} m step with no stair "
                    f"(max {st['STEP_HEIGHT']:g})", lid)
        if kind == "stair":
            r, t, n = l.get("riser"), l.get("tread"), l.get("risers")
            if r is not None:
                risers.add(round(float(r), 3))
                if not st["STAIR_RISER_MIN"] <= float(r) <= st["STAIR_RISER_MAX"]:
                    rep.add("FINDING", "stair", f"stair {where} riser {r} m outside "
                            f"{st['STAIR_RISER_MIN']:g}-{st['STAIR_RISER_MAX']:g}", lid)
            if t is not None and not st["STAIR_TREAD_MIN"] <= float(t) <= st["STAIR_TREAD_MAX"]:
                rep.add("FINDING", "stair", f"stair {where} tread {t} m outside "
                        f"{st['STAIR_TREAD_MIN']:g}-{st['STAIR_TREAD_MAX']:g}", lid)
            if r is not None and t is not None and not l.get("spiral"):
                pace = 2 * float(r) + float(t)
                if not st["STAIR_PACE_MIN"] <= pace <= st["STAIR_PACE_MAX"]:
                    rep.add("FINDING", "stair", f"stair {where} stride 2R+T = {pace:.2f} m outside "
                            f"{st['STAIR_PACE_MIN']:g}-{st['STAIR_PACE_MAX']:g} (too steep or too shallow)", lid)
            if n is not None and int(n) > st["MAX_RISERS_PER_FLIGHT"] and not l.get("spiral"):
                rep.add("FINDING", "stair", f"stair {where} has {n} risers in one flight "
                        f"(landing every {st['MAX_RISERS_PER_FLIGHT']})", lid)
    if len(risers) > 1:
        rep.add("FINDING", "stair", f"mixed riser heights in one building: {sorted(risers)}")

    for k in interior:
        s, w, area = spaces[k], spaces[k].get("width"), spaces[k].get("area")
        crawl = s.get("crawl")
        if s.get("kind") in ("corridor", "passage") and w is not None and not crawl \
                and float(w) < st["MIN_CORRIDOR_WIDTH"]:
            rep.add("BLOCKER", "corridor_width", f"{s['kind']} {k} is {w} m wide (min {st['MIN_CORRIDOR_WIDTH']:g})", k)
        if s.get("large_route") and large and (w is None or float(w) < 1.5 * large):
            rep.add("BLOCKER", "large_width", f"large route {k} is {w} m wide (min {1.5 * large:g})", k)
        if w is not None and float(w) < 2 * st["PLAYER_RADIUS"]:
            rep.add("BLOCKER", "small", f"{k} is {w} m wide: narrower than the player", k)
        if area is not None and float(area) < st["MIN_SPACE_AREA"]:
            rep.add("FINDING", "small", f"{k} is {area} m2: too small to use", k)
        if s.get("headroom") is not None:
            min_h = st["CROUCH_HEIGHT"] if crawl else st["MIN_HEADROOM"]
            if float(s["headroom"]) < min_h:
                rep.add("BLOCKER", "headroom", f"{k} has {s['headroom']} m headroom (min {min_h:g})", k)
        if s.get("edge_drop") is not None and float(s["edge_drop"]) > st["GUARD_DROP"] and not s.get("guarded"):
            rep.add("FINDING", "guard", f"{k} has an unguarded {s['edge_drop']} m drop "
                    f"(guard above {st['GUARD_DROP']:g} m, or accept it as deliberate)", k)
        if s.get("kind") in ("corridor", "passage") and s.get("length") \
                and float(s["length"]) > st["TUBE_LENGTH"] and len(und[k]) <= 2:
            rep.add("BLOCKER" if contested else "FINDING", "tube",
                    f"{s['kind']} {k} runs {s['length']} m without a branch (limit {st['TUBE_LENGTH']:g})", k)
        if contested and s.get("kind") in OPENING_KINDS:
            n_open = sum(1 for l in links if k in (l["a"], l["b"]))
            if n_open > st["MAX_ROOM_OPENINGS"]:
                rep.add("FINDING", "openings", f"{k} has {n_open} openings (max {st['MAX_ROOM_OPENINGS']})", k)

    for n in notes:
        rep.add("NOTE", "input", n)

    name = data.get("name", args.graph)
    print(f"Layout check: {name}\n  profile {st['PROFILE']}, site {st['SITE']}, {len(interior)} spaces, "
          f"{len(links)} links, {area_total:g} m2")
    order = {"BLOCKER": 0, "FINDING": 1, "ACCEPTED": 2, "NOTE": 3, "OK": 4}
    for it in sorted(rep.items, key=lambda i: order[i["level"]]):
        print(f"  {it['level']:<8} [{it['rule']}] {it['message']}")
    b, f = rep.count("BLOCKER"), rep.count("FINDING")
    print(f"\n{b} blocker(s), {f} finding(s), {rep.count('ACCEPTED')} accepted")
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"name": name, "settings": st, "items": rep.items, "blockers": b, "findings": f}, fh, indent=2)
    sys.exit(1 if b else 0)


if __name__ == "__main__":
    main()
