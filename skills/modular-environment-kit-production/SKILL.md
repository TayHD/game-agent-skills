---
name: modular-environment-kit-production
description: Produce modular environment kits (buildings, interiors, fences, walls, ruins, stations, caves, props that snap together) for any setting, period or art style - a measured kit contract with one owner for every shared plane so nothing z-fights, overlaps or gaps, closure tested before polish, generators that emit the contract, scan-gated blind critics, a finish bar set by the art style, prefabs assembled from passed pieces and checked for layout. Use when starting or running an environment kit, writing its contract, building prefabs from kit pieces, or reviewing kit pieces.
metadata:
  version: "0.2.0"
  updated: "2026-11-16"
---

# Modular environment kit production

A kit is a set of pieces that must close into buildings at every corner, storey, roof and edge without z-fighting, overlaps, gaps, open backs or walls in places they make no sense, and must read as finished at the camera's working distance in the game's own style. This skill is the method and the standards; the numbers come from the project's world and art style.

Companion skills: `project-knowledge-system` (where the contract, decisions and lessons live) and `building-layout-check` (checks every prefab for structure and walkability, and defines the world brief this skill also reads).

## Settings the project supplies

| Setting | Meaning | Default |
|---|---|---|
| `WORLD_BRIEF` | Setting, period, builders and their materials, purpose and history, art style, who moves through it (defined in `building-layout-check`). | Required before the contract. |
| `KIT_CONTRACT` | The measured rules every piece obeys. Starter: `templates/KIT_CONTRACT.md`. | `Docs/Design/KitContract.md` |
| `FINISH_SPEC` | The finish bar for the art style (section "Finish follows the art style"). | Part of the contract |
| `CORE_LIBRARY` | Shared pieces every kit reuses before modelling anything. | Floors, roof slabs and edges, corners, partitions, vertical circulation, guards, columns |
| `PIECE_CAP` | Most new plus variant pieces per kit. | 200 |
| `CRITIC_TARGET` | The shipped game or games, of the same style, whose environments the critic compares against by name. | Named in the world brief |
| `CAMERA_RANGE` | The distances the camera usually sees pieces from. | 2 to 5 m first person; 5 to 15 m third person; per-game for top-down |
| `DCC`, `ENGINE` | The modelling tool, the engine and their import path. | Project's choice |

## Principles

1. **Closure before beauty.** Freeze the piece list by assembling the block-out into plans first.
2. **Reuse before rework.** Nothing is modelled that `CORE_LIBRARY` or a passed kit already does; a different look is a variant from the same generator.
3. **Every build is a new cycle folder;** nothing is overwritten.
4. **Evidence over claims:** scans and measurements decide; renders illustrate.
5. **Good is done:** majors and criticals block; minors go to a backlog.
6. **Decide, log, continue:** the lead decides parked items and logs them as contract rules.
7. **No new parts after the freeze;** gaps are solved by layout.
8. **Compliance by construction:** generators emit the contract (pivots, ends, joints, finish, UV channels, collision), so critics judge look, not rules.
9. **Scan-gated critics:** a cycle reaches a critic only after the numeric scans are clean.
10. **Does it make sense?** Never add, move or bend anything only to pass a scan or a rule. If a rule makes a piece worse in this world, ask for an exception and record it.

## The kit contract (written before any modelling)

Fill every item in `templates/KIT_CONTRACT.md`, log each value as a decision, and get the owner's yes on grid, storey and scale. The bracketed numbers there are proven defaults for human-scale realistic buildings; the world brief may change any of them (a hobbit hole, a cyclopean temple, a cramped submarine, a chunky cartoon town), never the rules themselves.

**Units and transforms.** One unit system, one up axis, one exterior direction, one run direction, one export script. Each export holds one render mesh at the origin with rotation 0 and **scale applied**, plus collision in the engine's convention. (Object-level scale left on a piece made it import 100 times too big wherever a step ignored it.)

**Grid and datums.** A planning grid, engine snapping that matches it, a storey height with datums at its multiples, wall core and floor thickness, and **the floor's top on the datum**. Snapping uses the pivot and the logical footprint, never visual bounds. Trim may project past the footprint by a fixed allowance and never into a neighbour's core; larger projections (canopies, balconies, signs, porches) are separate hung pieces with their own pivot on the host.

**Ownership: every shared plane or band has exactly one owner.** This is what prevents z-fighting.
- **Floors versus walls:** one primary scheme by default. The grid is referenced to the interior faces of outer walls; walls stack wall on wall at full storey height; floor and roof slabs are inset pieces that fill the bays exactly, so wall tops and slab tops meet edge to edge. Where a slab must run over a wall line, shorter receiver walls stop under it and an edge piece covers the slab edge. **Never mix the two schemes along one edge;** switch only at a corner or a movement joint. (A wall top and the next floor's top in the same plane z-fought wherever a slab covered a wall.)
- **Roofs versus floors:** the roof surface sits a small fixed offset above its datum so it never shares a plane with a floor.
- **Corners:** dedicated outside and inside corner pieces own the corner square; walls never overlap to make a corner. Write the face-length formulas so every interior face is a whole number of bays.
- **Partitions:** T and X junctions butt the through-run's face; L corners and free ends use a post that hides the open ends; partitions never overlap.
- **Guards, rails and fences:** post-and-panel. Every post is a node owning a fixed distance either side; panels span node to node; turns are rotations only; a corner piece owns the corner square. (Case-by-case railings grew to more than fifty pieces; post-and-panel did the same work with about twenty.)
- **Hung pieces** share end planes with their host only where a neighbour or an end cap covers them; their own end caps sit a few millimetres inside the host.

**Joints.** Where two pieces butt, the joint is designed: a small groove on each mating edge, a recess, or an end set back by a few millimetres. A visible coincident face is a defect. Faces that coincide exactly on a mating plane are accepted only where a neighbour is placed against them; scans list them separately. Ends are named: open ends that must meet a neighbour, and finished ends for exposed free ends; a finished end is never butted.

**Geometry hygiene.** Every piece is a closed shell (no open bottom, back or inner face except a declared open end). No n-gons in exports, no zero-area faces, no duplicated shells, consistent winding. Collision runs exactly to the mating planes; collision outside the visible surface stays within a centimetre or two. Openings are fixed in modules; door leaves and other moving parts are separate actors placed from sockets.

**UV and material channels** are decided before the first piece and authored on every piece from its first cycle: world-scale tiling at a fixed density (or the style's own texturing scheme), trim-sheet bands, lightmap if the engine needs one, any material-layer or bake channels. Shared material slots by name. (Channels decided after the geometry passed cost every finished piece four extra cycles.)

**Naming and budget.** A fixed name pattern with sizes, a fixed family vocabulary, no renames of passed pieces, a piece cap per kit, triangle budgets per piece type.

## Finish follows the art style

The finish bar is written in the contract from the world brief, measured where possible, and checked at `CAMERA_RANGE`. The critic's standing line is always: **anything that reads as unintended or unfinished at working distance is a major**, which in a realistic style means primitive geometry and razor edges, and in a low-poly style means accidental smoothing or noisy detail.

| Style | Edges | Normals | Detail and silhouette | Surfaces |
|---|---|---|---|---|
| Realistic | Bevel every visible convex edge by material class, wide enough to catch light at working distance, 2 or more segments (concrete about 4% of the section, 1.5 to 8 cm; masonry 1 to 3 cm; heavy steel 0.6 to 1.5 cm; timber and box sections 0.3 to 1.5 cm; thin trim a 1.5 to 3 mm micro-bevel); coverage of visible convex edge length at least 90% | Smooth, face-weighted custom normals; hard splits only at sharp dihedrals; import keeps them | Real profiles where they read (round rails, real steel sections, built joints, no open tube ends); no flat region over about 3 x 3 m in eye range without a reveal, rib or trim | Wear and decay with a physical cause in this world |
| Stylised or painterly | Exaggerated, chunky bevels or deliberately uneven edges, consistent across the kit | Soft, sometimes hand-tuned | Exaggerated proportions and silhouettes as the brief allows, consistent across the kit | Hand-painted or stylised wear only where the style uses it |
| Low-poly or faceted | Hard, intentional facets; no accidental bevels | Flat or deliberately split | Silhouette carries the read; detail budget kept low and even | Flat or gradient colour; no realistic grime |
| Toy-like or miniature | Rounded, soft, uniform radii | Smooth | Simple readable forms, scaled-up details | Clean, saturated; damage only if the style asks |

Whatever the style: **a finish step never changes bounds, pivot or a mating plane;** mating edges and faces inside a core stay as the contract sets them.

## Stages

1. **World brief and contract:** write the brief, measure any baseline, tag every piece reuse, variant, new or withdraw within `PIECE_CAP`, write the contract.
2. **Closure test on the block-out:** assemble a two-storey rectangle, an L with outside and inside corners, a setback with a terrace, the kit's signature form, a **loopback** (the kit doubling back round a courtyard), a **stack** (three storeys with a void, a stair and a hatch through them) and a **hall room** (a corridor one bay wide and three long). Run every assembly scan; every gap becomes a piece or a layout rule; then freeze the piece list.
3. **Archetype loop,** per family in parallel: one parameterised generator per family, one parameter file per kit; build into a scratch folder, pass the scan gate, then write the cycle; critic A, then a blind critic B who never reads A, both given the contract, the accepted conditions and the piece's intended neighbours. Pass on two consecutive clean critics plus zero coplanar overlap, or one clean blind critic for a mechanical fix. Budget three cycles; question the archetype at five.
4. **Variants** from passed archetypes, one batched spot-check per family.
5. **Assembly:** rebuild the closure plans from passed pieces; all assembly scans clean.
6. **Kit gate:** three prefabs that exercise the kit's main systems the way a level designer of this world would (shell, interior, vertical circulation, roof), each through `building-layout-check`, walked at eye height and orbited, with a fresh critic.
7. **Building set** at small, medium and large scale with a variety critic (no two share plan and roof type; heights and ground-floor uses vary; larger buildings carry a landmark element).
8. **Finish stage** on every piece against `FINISH_SPEC`, inside the generators, never by hand per piece.
9. **Materials** at the style's bar; decay and damage only where the world brief gives them a cause; review renders use real materials.
10. **Import,** verify counts against the export stats, one play check, the owner's stamp.
11. **Condition variants** (damaged, overgrown, ruined) after the kit ships, each keeping its base piece's socket and footprint, if the world needs them.

## Scans (numbers decide)

Built before the first piece loop; a kit does not start until each runs on its block-out.

- **Per piece:** measurement (bounds against pivot, triangles, collision, UV channels and density, slots, n-gons, zero-area faces, applied scale); **coplanar overlap** (visible same-facing faces within about 0.5 mm and 1 degree with overlapping area: must be 0, with duplicated shells detected as duplicates); **triangle intersection** between separate parts; open boundary loops; collision outside the surface; UV stretch and seams; the finish report for the style.
- **Per assembly:** coplanar 0 across pieces (mating-plane hits listed apart), intersections 0, gaps 0, exposed open ends, a gravity walk that treats walls as solid, a sphere flood at every junction, every free end and foot on ground or a host, the largest gap through every grille or railing.
- **Place both legs at every corner and host face before the first critic;** single-leg tests hide crossings. **Coplanar 0 does not prove no interpenetration;** run the intersection check too.

## Prefabs

A prefab is a recipe of passed pieces assembled by a script. Fixes are layout changes; no hand-building in the engine and no new pieces for a prefab. Every prefab passes `building-layout-check` before review. Large buildings export as merged sections under a triangle cap, split by wing and storey, collision kept.

## Done when

The kit is stamped; its pieces pass the scans and the style's finish bar; its gate prefabs and building set pass the layout check and their critics; and the completion report lists the measurements, critic paths, accepted conditions and parked items. Every problem a review found is a lesson line in the kit playbook, and every rule it changed is a dated contract row.
