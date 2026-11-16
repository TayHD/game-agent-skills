# <Project> kit contract

Status: draft. Owner: <owner>. Kept by: <lead>. Last updated: <date>.
World brief: <path to the world brief>. Decisions: the decisions log, area "Environment".

Every number in this file is the one place that number lives; other docs cite rules by their id (U1, G2, O3...). A change is a new dated row in the change log at the bottom, never a silent edit. Bracketed values are proven defaults for human-scale realistic buildings in metres; replace them from the world brief and delete the brackets. Items marked (owner) need the owner's yes.

## U. Units and transforms

| Id | Rule | Value |
|---|---|---|
| U1 | Units in the modelling tool and the engine; export scale | [metres in the modelling tool; engine native; scale applied at export] |
| U2 | Up axis, exterior direction, run direction | [Z up; exterior faces -Y; pieces run along +X] |
| U3 | One mesh per export at the origin, rotation 0, scale 1 applied, plus collision in the engine's convention | required |
| U4 | The one export script every piece uses, and its settings | <path> |

## G. Grid and datums (owner)

| Id | Rule | Value |
|---|---|---|
| G1 | Planning grid; every footprint a multiple of the base unit | [2 / 4 / 8 m] |
| G2 | Engine snapping | [grid unit, 90 degrees; radial families their own angle step] |
| G3 | Storey height; datums at its multiples | [4.00 m] |
| G4 | Wall core thickness | [0.30 m] |
| G5 | Floor and roof slab thickness; the slab top sits on the datum | [0.40 m] |
| G6 | Snapping uses pivot and logical footprint, never visual bounds | required |
| G7 | Trim projection past the footprint: outward / past the ends; never into a neighbour's core | [0.20 m / 0.11 m] |
| G8 | Hung pieces (canopies, balconies, porches, signs) and their maximum projection, each with its own pivot on the host | [about 2 m] |

## P. Pivots

| Id | Piece type | Pivot |
|---|---|---|
| P1 | Walls | [start corner of the exterior face, at the floor top] |
| P2 | Floors and roofs | [a slab corner on the top surface] |
| P3 | Corners | [the corner point on the grid] |
| P4 | Freestanding pieces (fences, screens) | [panel centred on its line, base at ground] |
| P5 | Radial pieces | [the ring centre at the floor top] |

## O. Ownership (one owner for every shared plane or band)

| Id | Rule | Value |
|---|---|---|
| O1 | Primary floor scheme: grid on the interior faces of outer walls; walls stack at full storey height; inset slabs fill the bays | required |
| O2 | Slab over a wall line: receiver walls of this height stop under it; an edge piece covers the slab edge | [3.60 m receiver] |
| O3 | Never mix O1 and O2 along one edge; switch only at a corner or movement joint | required |
| O4 | Roof surface offset above its datum | [+0.015 m] |
| O5 | Corner pieces own the corner square; face-length formulas (outside-outside, outside-inside, inside-inside) | [n x grid + 2 x core / n x grid / n x grid - 2 x core] |
| O6 | Partitions: T and X butt the through-run; L corners and free ends use a post; never overlap | required |
| O7 | Guards and fences are post-and-panel; each post owns this distance either side; turns are rotations | [±0.10 m] |
| O8 | Hung-piece end caps set inside the host by | [5 mm] |

## J. Joints and ends

| Id | Rule | Value |
|---|---|---|
| J1 | Butt joints are designed: groove per mating edge, or recess, or set-back | [2 mm half-groove each side; 1 mm recess; 3 to 5 mm set-back] |
| J2 | Coincident faces allowed only on a covered mating plane; scans list them apart | required |
| J3 | End types: open (must meet a neighbour) and finished (exposed free end); a finished end is never butted | names: <open suffix>, <finished suffix> |

## H. Geometry hygiene

| Id | Rule | Value |
|---|---|---|
| H1 | Every piece a closed shell except declared open ends | required |
| H2 | No n-gons in exports, no zero-area faces, no duplicated shells, consistent winding | required |
| H3 | Collision to the mating planes; collision outside the visible surface at most | [0.01 m at the 95th percentile, 0.02 m max] |
| H4 | Openings fixed in modules; doors and moving parts are separate actors from sockets | required |

## T. Texturing and materials

| Id | Rule | Value |
|---|---|---|
| T1 | Texturing scheme and density | [world-scale tiling, 1 UV unit per metre ±1%] |
| T2 | Channel list, authored on every piece from its first cycle | [0 tiling, 1 lightmap, then any layer or bake channels] |
| T3 | Shared material slots by name; a new slot is a contract change | <slot list> |

## F. Finish (from the art style in the world brief)

| Id | Rule | Value |
|---|---|---|
| F1 | Style row (realistic, stylised, low-poly, toy-like, or the project's own) | <style> |
| F2 | Edge treatment by material class | <table or rule> |
| F3 | Normals | <rule> |
| F4 | Detail and silhouette rules; largest plain area allowed in camera range | <rule> |
| F5 | Surface wear and decay, and what may cause it in this world | <rule> |
| F6 | Triangle budgets per piece type | <table> |
| F7 | A finish step never changes bounds, pivot or a mating plane | required |

## N. Naming and budget

| Id | Rule | Value |
|---|---|---|
| N1 | Name pattern, sizes in centimetres | [<prefix>_<KitCode>_<Family>_<Width>[x<Depth>]_<Variant>] |
| N2 | Family vocabulary | <list> |
| N3 | Pieces per kit (own new plus variants; core reuse free) | [200] |
| N4 | A passed piece is never renamed; a rename is a new piece | required |

## A. Accepted conditions

Deliberate conditions critics must not flag (covered mating planes, finished ends by design, world-brief exceptions).

- 

## Change log

- <date> · <lead> · Created from the world brief.
