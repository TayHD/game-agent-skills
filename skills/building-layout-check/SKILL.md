---
name: building-layout-check
description: Check that a generated or hand-built building, interior or enclosed environment (houses, offices, bunkers, ships, temples, ruins, caves, compounds, stations) is structurally sensible and properly walkable - load paths, walls that start and end at something, doors that lead somewhere, stairs with landings and headroom, no orphan rooms, no walls dropped into openings, enough exits, shallow dead ends, loops and two ways up where people fight or flee. Engine- and genre-neutral; ships a space-graph checker script. Use when reviewing a building or layout an agent or generator produced, before accepting a prefab, or when writing layout rules for a kit.
metadata:
  version: "0.1.0"
  updated: "2026-11-16"
---

# Building layout check

Modular kits make it easy to place a wall anywhere the grid allows, and generators and agents will do exactly that: walls that end in the middle of a room or run across a window, doors that open onto a blank wall or a drop, rooms nobody can reach, stairs that arrive facing a wall, one-door boxes and corridors that never branch. This skill is the check that catches them. It judges layout and structure, not finish or materials.

It works for any setting, period and art style, because it judges every space by **the world's own logic**, written down once in a world brief (below): a stone keep by how masons build and how a garrison lives, a starship by how its crew moves and what its hull carries, a cave by how water cut it and how its inhabitants use it, a cartoon village by the rules its style sets. Modern building codes are only the fallback when a project says nothing.

Three passes, in order, because each is cheaper than the next: the **space graph** (a script, seconds), the **geometric probes** (in the engine or modelling tool, minutes), and the **eye-height review** (a person or a fresh critic agent). A building passes when no blocker remains in any pass.

## The world brief (write it before the first check)

One short section in the project's environment docs, about half a page, that every check and every reviewer reads. Without it, reviewers fall back on their own era and style and flag the wrong things.

1. **Setting and period:** where and when (for example "late medieval river town", "orbital mining station, 2300s", "post-flood ruins of a 1970s suburb", "mushroom-folk burrows").
2. **Who built it, with what:** the builders' technology and materials, and what that allows: spans (timber 4 to 6 m, stone vaults, steel trusses, grown coral), wall thickness, how floors are carried, how vertical travel works (stairs, ladders, ramps, lifts, climbing, flight, teleport pads).
3. **What it is for, and what happened to it:** its original purpose, its use now (inhabited, abandoned, occupied by someone else, ruined) and the events that changed it (siege, flood, collapse, overgrowth). Damage needs a cause in this world.
4. **The art style's rules:** realistic, stylised, exaggerated, low-poly or toy-like, and what it does to proportion (oversized doors, chunky walls, wonky verticals) and to detail. A stylised world may bend real proportions on purpose; the brief says how far.
5. **Who moves through it:** the player's size and moves (walk, crouch, crawl, climb, jump, swim, fly), companions, creatures and vehicles that must fit, and whether spaces are explored, built in, fought through or fled through (this sets `PROFILE`).
6. **Deliberate exceptions:** what this world does that a modern building would not, so reviewers accept it (unguarded battlements, ladders instead of stairs, one-entrance fortifications, doorless huts, spiral stairs with steep risers, rooms reached only by climbing).

Rules below that say "sensible", "a builder", "a designer" or "a reason" mean: sensible for the builders, purpose and style in this brief.

## Settings the project supplies

Every setting has a default for a human-scale player, in metres, with modern proportions. A project with other proportions or another period (a small creature, a giant, a vehicle, steep medieval stairs, a different unit) sets the numbers from its world brief, not the method. In the script, settings come from the graph's `"settings"` object, then `--profile` and `--site`, then `--set NAME=VALUE` (later wins); an unknown name is an error, so a typo never passes silently.

**Site type and rules switched off.** Some rules come from how buildings are designed for people (exits by floor area, interior loops, no single funnel, the share of dead-end rooms, branching corridors). A cave, a ruin or a natural space does not owe them for exploration, so with `SITE` `natural` or `ruin` and `PROFILE` `explore` they are reported as notes; in `contested` they apply everywhere, because fights and chases need them wherever they happen. Any rule can also be switched off by the world brief with `RULES_OFF` (for example a fortress with one gate by design: `RULES_OFF=exits,funnel`), or accepted for one space in the graph's `accepted` list.

| Setting | Default | Meaning | Used by |
|---|---|---|---|
| `WORLD_BRIEF` | none (modern, realistic, human-scale assumed, and the report should say so) | The half page above. | All passes |
| `PROFILE` | `explore` | `explore` (exploration, story, building, survival without indoor fights) or `contested` (players fight, chase or flee here). `contested` turns on the rules marked (C). | Script |
| `SITE` | `building` | `building`, `vessel` (ships, stations, vehicles: treated as a building), `natural` (caves, canyons, groves, ice, reefs) or `ruin`. | Script |
| `RULES_OFF` | none | Comma list of rule ids reported as notes only. | Script |
| `PLAYER_RADIUS` | 0.40 | Half the walking capsule's width. | Script |
| `CROUCH_HEIGHT` | 1.10 | Headroom needed on crawl spaces, squeezes, swims, ladders, climbs, hatches and windows. | Script |
| `MIN_HEADROOM` | 2.10 | Clear height over every walkable surface that is not a crawl space. | Script |
| `MIN_DOOR_WIDTH` | 0.90 | Clear width of a door, opening, stair, ramp or lift. | Script |
| `MIN_CORRIDOR_WIDTH` | 1.20 | Clear width of a corridor or passage. | Script |
| `MIN_SPIRAL_WIDTH` | 0.70 | Clear width of a stair marked `"spiral": true`. | Script |
| `MIN_CLIMB_WIDTH` | 0.60 | Clear width of a ladder, climb, hatch or swim. | Script |
| `LARGE_AGENT_DIAMETER` | 0 (none) | Diameter of the largest creature or vehicle that must pass; routes marked `large_route` are at least 1.5 times this wide. | Script |
| `STAIR_RISER_MIN`, `STAIR_RISER_MAX` | 0.10, 0.20 | Riser range. A medieval or cramped world raises the maximum. | Script |
| `STAIR_TREAD_MIN`, `STAIR_TREAD_MAX` | 0.22, 0.40 | Tread range. | Script |
| `STAIR_PACE_MIN`, `STAIR_PACE_MAX` | 0.55, 0.70 | The stride rule: twice the riser plus the tread. It holds across periods and catches stairs that are steep for their tread. Not applied to spirals. | Script |
| `MAX_RISERS_PER_FLIGHT` | 16 | A landing at least this often (not applied to spirals). | Script |
| `STEP_HEIGHT` | 0.45 | The tallest step the character climbs without a stair; a door or opening with a larger `step` is a blocker. | Script |
| `GUARD_DROP` | 1.00 | A walkable space with an `edge_drop` greater than this needs `"guarded": true` (rail, parapet, wall, or whatever this world uses), or an accepted condition saying the drop is deliberate and reads as one. | Script, probe |
| `TUBE_LENGTH` | 15 | Longest corridor or passage without a branch. | Script |
| `DEAD_END_DEPTH` | explore 20, contested 10 | Deepest dead end from its last junction, in metres. | Script |
| `EXIT_SPACING`, `VERTICAL_SPACING` | 10, 15 | Exits closer than this on one face count once; two vertical routes must be at least this far apart. | Script |
| `MAX_ROOM_OPENINGS` | 4 | (C) Most openings into one room or chamber. | Script |
| `MIN_SPACE_AREA` | 1.0 | Smallest usable space. | Script |
| `GUARD_HEIGHT` | 1.00 to 1.10 | Height of a guard where one is needed. | Probe |
| `LAYOUT_SOURCE` | the project's layout data | Where the plan comes from: a recipe or manifest, a level export, or a plan drawn by hand. | Pass 1 input |

Exits by floor area (all walkable interior storeys together). Exits closer than `EXIT_SPACING` on the same face count once; a window a player can climb through counts as half; a one-way drop to the outside is an escape, listed but not counted.

| Floor area | `explore` | `contested` |
|---|---|---|
| Under 100 m² | 1 | 2, on 2 faces |
| 100 to 400 m² | 2, on 2 faces | 3, on at least 2 faces |
| Over 400 m² | 3, on at least 2 faces | 4, on at least 3 faces |

## Pass 1: the space graph (script)

Describe the place as spaces and links in JSON (format and every field in `templates/space_graph.example.json`) and run:

```
python3 -I scripts/layout_check.py <graph.json> [--profile explore|contested] [--site building|natural|ruin|vessel] [--set NAME=VALUE ...] [--json out.json]
```

- A **space** is anywhere a player can stand that reads as one place. Kinds: `exterior` (the outside world, exactly one), `room`, `chamber` (natural or irregular rooms), `corridor`, `passage` (natural corridors), `landing`, `stair` (a stairwell space), `roof`, `deck`, `yard`, `void` (sealed). Rooms, chambers, corridors, passages, landings, roofs and decks count for dead ends; rooms and chambers count for openings and the dead-end share. Give each an id, storey, area, and where you can: position (x, y), length and width (corridors and passages), headroom, `edge_drop` and `guarded`, `crawl`, `anchor` (the main space), `sealed`.
- A **link** is any way between two spaces. Kinds: `door`, `opening`, `stair`, `ramp`, `lift`, `ladder`, `hatch`, `climb`, `swim`, `squeeze` (crawl-through), `window` (one a player climbs through) and `drop` (one-way, from a to b). Give it its clear width and headroom where known, `face` and x, y for links to the outside, `step` for a level change at a door, and riser, tread, risers and `spiral` for stairs. Model each stair flight as a stair link between the spaces it joins; any non-drop link between two storeys counts as a vertical route.

Rule ids, used in reports, `accepted` and `RULES_OFF`: `reach`, `return`, `sealed`, `exits`, `dead_end`, `dead_share`, `loop`, `funnel`, `vertical`, `door_width`, `corridor_width`, `large_width`, `headroom`, `step`, `guard`, `stair`, `tube`, `small`, `openings`. An `accepted` entry is `{"rule": "...", "space": "..."}` (or `"link"`), or just a rule and a reason to accept it everywhere.

The script reports BLOCKER, FINDING, ACCEPTED, NOTE (including what it could not check from the data given) and OK:
- **Reachability** (`reach`, `return`): every non-sealed space reachable from outside with the moves in the graph, and a way back from each (drops are one-way).
- **Exits** (`exits`): count, faces and spacing against the table.
- **Dead ends** (`dead_end`, `dead_share`): spaces with one way in, the chain depth from the last junction, and (C) the share of dead-end rooms.
- **Loops** (`loop`): at least one interior loop where the place is over 400 m² or more than two spaces deep.
- **Funnel** (`funnel`): separate routes (sharing no space) from outside to the anchor, or to the deepest room if none is marked; one route is a blocker in (C) over 100 m² and a finding over 400 m².
- **Vertical routes** (`vertical`): routes from each storey toward the entry storey, up or down; two, at least `VERTICAL_SPACING` apart, on storeys over 200 m², or over 100 m² in (C).
- **Sizes and levels** (`door_width`, `corridor_width`, `large_width`, `headroom`, `small`, `step`): widths and headroom by link kind, spaces narrower than the player, steps with no stair.
- **Stairs** (`stair`): riser, tread, stride and flight length; mixed risers in one building.
- **Edges** (`guard`): unguarded drops over `GUARD_DROP`.
- **Tubes and openings** (`tube`, `openings`): corridors over `TUBE_LENGTH` with no branch; (C) rooms with too many openings.

## Pass 2: geometric probes (in the engine or modelling tool)

The graph cannot see geometry. Run these on the assembled building with the project's own tools; each must produce a number or a list, not a screenshot.

| Probe | Measures | Fails when |
|---|---|---|
| Walk flood | A capsule of the player's size walks from every exterior door with gravity, treating walls as solid (a navigation mesh build is acceptable). | A space the graph calls reachable is not reached, or the walk reaches a place the graph does not have (a gap, a wall top, a roof with no route). |
| Support | For every floor, roof, stair, beam and upper wall: the element below it in its footprint. | Anything rests on nothing (more than 1 cm of air), a column or wall above lands on a floor span with no beam or wall under it, or a cantilever exceeds about a third of its back span without a visible bracket or brace. |
| Wall ends | Each end of every wall and partition. | An end touches nothing (and is not a finished free end), lands inside a door or window opening, or stops short of a wall by less than the player's width. |
| Openings | Floor height on both sides of each door, a ray through each window. | A door opens onto a wall, a drop, a sealed void or a step taller than `STEP_HEIGHT`; a window is blocked within 1 m behind it by a wall, floor slab, stair or tall prop; a floor or interior wall crosses a window on the facade. |
| Clearance | Swept capsule along each route, door swing areas, stair landings. | Headroom or width falls under the settings; a prop, column or partition stands in a door path, on a landing or in a corridor's clear width. |
| Edges | Every walkable edge and its fall. | A fall over `GUARD_DROP` has no guard and is not marked deliberate. |
| Overlap | Wall-in-wall, wall-in-floor and prop-in-wall intersections. | Any intersection over a few millimetres that a player can see. |

## Pass 3: eye-height review

A fresh reviewer (person or critic agent who has not seen the build) walks it at eye height and looks at a plan and a section of each storey. They are given the world brief, the building's purpose ("a two-family farmhouse", "a flooded research bunker", "a collapsed temple", "a crew deck on a cargo hauler") and the accepted conditions (deliberate dead ends, locked doors, collapsed sections, crawl spaces), and answer:

1. **Does every wall have a reason?** It encloses a room, carries something, guards an edge, screens a view, or (in a ruin) is what is left of one of those. A wall that does none of these is removed.
2. **Does every room have a purpose and a way in that suits it?** A wash room off a passage, not off the kitchen through a bedroom; a storeroom near what it stores; a guard post where it can see what it guards; an airlock between pressure and vacuum.
3. **Does the structure read, by this world's means?** Upper walls over lower walls or beams; columns over columns; a roof that bears on walls; spans and overhangs the builders in the brief could make (or, for a natural space, that the rock, ice or growth could hold). A stylised world may exaggerate, but consistently.
4. **Would the people who built and use this place have put this door, stair and window here?** Entrances face the approach; stairs start from a hall or landing, not from inside a closet; windows light rooms, not walls; defensive buildings defend their entrances; a ruin's damage follows its cause.
5. **Can a player find the way on?** At every junction at least two ways on are visible without turning around; the way out is findable without a map.
6. **Does the outside match the inside?** Storey lines, windows and doors seen outside correspond to floors, rooms and doors inside.
7. **(C) Where would a fight go?** No single spot covers every way in; an indoor dead end is one room deep at most; a stair can be bypassed; a player can break line of sight within a few metres.

## Failure patterns and their fixes

| Pattern | Seen | Fix |
|---|---|---|
| Wall to nowhere | A wall or partition that ends mid-room, or stops a hand's width short of another wall | Extend it to a wall or column, finish it as a deliberate free end, or remove it |
| Wall through an opening | A partition landing on a window or door, or a floor slab crossing a window | Move the partition to a solid section of wall; move the floor or the window |
| Door to nowhere | A door onto a blank wall, a drop, a void or a cupboard-sized slot | Remove the door, or give it a room, landing or balcony |
| Orphan room | A room with no way in, or seen through a window with nothing behind it | Add a door from a sensible neighbour, or seal it as a closed void with no visible interior |
| Floating floor | A floor, stair or upper wall with nothing under it | Add the wall, column or beam that would carry it, or move it onto structure |
| Stair into a wall | A flight that arrives facing a wall closer than its own width, or has no landing | Turn the stair, add a landing at least the stair's width deep, or move it |
| Stair trap (C) | The only way up or down, watched from one spot | A second route at the other end or on another face (outside stair, ladder, hatch) |
| One-door box | A building or large room with one exit, or all exits on one face | A door on another face; more by floor area (exit table) |
| Dead-end chain | Rooms reachable only through other dead-end rooms | Join the far room back to the circulation, or shorten the chain |
| Tube | A corridor longer than `TUBE_LENGTH` with no branch | A side opening, a widening or a cross corridor every 10 to 15 m |
| Sliver | A space narrower than the capsule, or a gap between walls a player can see but not enter | Close it up, or widen it into a usable space |
| Blocked path | A column, prop, partition or door swing in a doorway, landing or corridor | Move the object; keep the clear width |
| Guess room (C) | A room with more than four openings | Merge or close openings until the main way reads |
| Maze | Interior walls that force long detours between rooms that sit side by side | Cut the openings the desire lines want; remove walls that serve no room |
| Missing guard | A walkable edge with a dangerous fall and no rail or parapet | Add the guard, or make the drop clearly deliberate |
| Inside-outside mismatch | Facade storey lines, windows or doors that do not match the floors and rooms inside | Move the interior to suit the facade, or the facade to suit the interior |

## Rules for fixing

- **Fixes are layout changes first:** move, remove or swap pieces. A new piece is the last resort, and only when the kit genuinely lacks a role (log it as a kit gap).
- **Never add a piece only to satisfy a check.** If a rule makes this building worse (a deliberate one-door vault, a ruin with a collapsed stair), record it as an accepted condition with the reason, and the reviewer stops flagging it.
- Re-run all three passes after a fix; the probe that found the fault must still contain the original failing point.
- Record new failure patterns and project thresholds in the project's own layout rules, so the next building is checked against them.

## Done when

The space-graph script reports no blocker, every probe returns its number within the settings, the eye-height reviewer finds nothing above a minor that is not an accepted condition, and the report lists the graph file, the probe outputs and the review notes.
