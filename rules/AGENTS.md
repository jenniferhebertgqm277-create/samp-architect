# SA-MP 3D Architectural Mapping Rules

These rules govern how the agent designs, calculates coordinates, and generates 3D mappings for SA-MP and open.mp.

## 0. Autonomous Bespoke Design (Strictly No Pre-baked Templates)
- **Zero Static Template Restriction**: The agent MUST NEVER force or restrict mappings into rigid, canned templates (e.g. static "villa" or "office" presets). All uploaded sample mappings and training files exist purely for the AI to **learn** architectural principles, modular dimensions, texture combinations, and framing techniques.
- **Bespoke Generation From Scratch**: When a user requests any building (e.g. a beachfront cafe in Santa Maria Beach, a drift garage in Las Venturas, a police precinct, a modern villa, or a cartel compound), the agent acts as an autonomous master architect:
  1. **Site & Context Analysis**: Determine target world coordinates `(X, Y, Z, Heading)` and remove overlapping default GTA SA objects via `RemoveBuildingForPlayer`.
  2. **Parametric Space Planning**: Compute custom room sizes, floor heights, entrance portals, outdoor patios, and window bay distributions.
  3. **Precision Mathematical Assembly**: Snap walls and structural frames using the learned modular grid (`3.211m`, `1.601m`, `9.633m`, `3.500m`, `18762`, `18766`).
  4. **Dynamic Detailing**: Generate unique furniture layouts, customized 3D signage text (`SetDynamicObjectMaterialText`), and realistic lighting.
  5. **Material Harmonization**: Apply verified, theme-appropriate textures from the learned palette database.

## 1. Dimensional Standards & Human Scale
- **Player Scale**: In SA-MP, CJ / human ped height is ~1.8 units.
- **Floor-to-Ceiling Height**: Standard single-story ceiling height MUST be between **3.2m and 3.8m**. Never make ceilings lower than 2.8m (feels claustrophobic in third-person camera) or higher than 5.0m for normal residential rooms.
- **Doorways**: Width 1.0m to 1.5m, Height 2.2m to 2.5m. Clear clearance on both sides.
- **Window Sills**: 0.8m to 1.0m above floor level.
- **Staircases**: Use modular staircase `19364` or steps with ~0.18m rise and ~0.28m tread.
- **Wall Thickness**: Standard modular walls (e.g. `19353`) have ~0.17m to 0.20m thickness.

## 2. Zero Z-Fighting & Gap Elimination
- **Never place two coplanar surfaces on the exact same plane**: When placing interior wallpaper, posters, carpets, or glass over solid walls/floors, ALWAYS apply an offset of **`0.005m to 0.010m`** in the normal direction.
- **Corner Joint Alignment**:
  - For 90-degree corners, align wall edges considering the wall thickness:
    `Offset = (Width / 2.0) - (Thickness / 2.0)`
  - Use modular corner column `19356` or structural pillar `19363` at intersections to guarantee seamless, airtight connections.
- **Terrain Foundation Snap**:
  - Always extend foundation slabs or basement perimeter walls at least **0.5m - 1.5m below ground level** (Z minus) so the building never appears to "float" over uneven or sloping terrain.

## 3. Structural Integrity & Architectural Completeness
Every realistic building must contain the following core architectural layers:
1. **Foundation Slab**: Base plate leveling the uneven ground.
2. **Structural Columns**: Load-bearing pillars (`19362` or `19363`) at corners and every 5m - 10m span.
3. **Perimeter Enclosure**: External walls with deliberate door and window cutouts.
4. **Intermediate Floors & Ceilings**: Slabs separating floors with openings for stairwells or elevators.
5. **Roof & Parapet**: Finished top surface with protective parapet walls (0.8m - 1.2m high) or slanted roof shingles.
6. **Architectural Lighting**:
   - Downlights / Spotlights (`19894`) centered in rooms.
   - Ambient strip neons (`19172`-`19174`) for modern/cyber accents.
   - Exterior wall sconces or floodlights for entrance facades.

## 4. Texture & Material Harmony
- **Material Slot Matching**: Always apply textures to slot `0` (or the appropriate material index) using verified SA-MP textures.
- **Texture Theme Consistency**:
  - *Modern*: Smooth plaster (`cj_white_wall2`, `mono1_sfe`), tinted glass (`19447`), polished tile (`CJ_7_11_TILE`), dark oak.
  - *Industrial*: Corrugated steel (`rebrckwall_128`), exposed brick (`sl_vicbrikwall01`), concrete tarmac (`ws_rooftarmac1`).
  - *Luxury*: Polished marble (`bwtilebroth`), gold/brass accents, rich velvet, mahogany.
- **Scale and Grain**: Never stretch textures inappropriately; maintain realistic aspect ratios.

## 5. Performance & Streamer Optimization
- Use large modular units (e.g. 10m x 10m slabs or walls) wherever long flat spans exist, rather than assembling dozens of tiny pieces.
- Target dynamic object stream distance between 200.0m and 300.0m for optimal client FPS on mobile and low-end PCs.

## 6. Anti-Looping & Architectural Composition Directives
- **Strictly Prohibit Naive Tile Loops**: NEVER generate mapping by mindlessly looping dozens of small floor/ceiling tiles (`19360` 5x5m) or repetitive identical wall segments. This produces ugly "tiled matrix" slop with visible seams.
- **Large-Format Structural Slabs**: Use 10m x 10m (`19361`) or 20m x 20m (`18344`) plates for concourses, roadways, and foundations to ensure silky smooth surfaces with minimum object count.
- **Architectural Rhythm & Hierarchy**:
  - Break long facades into deliberate bays using structural columns (`19363`) every 6m to 10m.
  - Crown the top of all curtain walls and facades with horizontal fascia trim (`19365`) or parapet railings (`19367`).
  - Feature dedicated, distinct entrance portals with sliding glass doors (`19856`) and crisp dynamic signage (`19475`), not endless uniform glass sheets.
- **Authentic Streetscape & Human Scale Detailing**:
  - Elevate sidewalks +0.10m to +0.25m above roadways to form realistic street curbs.
  - Add realistic functional amenities: stainless steel bollards (`1237`), stylish benches (`1280`), luggage trolleys (`14576`), designer palm planter boxes, and live Flight/Transit Information Display Systems (FIDS).

## 7. GTA World Context & Default Building Removal
- **Zero Collision with GTA World**: When mapping at real GTA SA landmarks (e.g. LS Airport, Vinewood, Santa Maria Beach, Idlewood), ALWAYS inspect and remove overlapping default GTA SA buildings, lampposts, and clutter using `RemoveBuildingForPlayer`.
- **Integrated Include & Script Removal**: Always export removals via `RemoveBuildings_<Name>(playerid)` so that both modular includes and standalone filterscripts cleanly clear conflicting default objects upon player connection.

## 8. The Modular Grid Standards (Precision Snapping)
- All structural walls and rooms MUST snap to multiples of the standard modular unit:
  - **Single Bay**: `3.211m` (`19353`, `19354`, `19355`)
  - **Half Bay**: `1.601m` (`19426`)
  - **Triple Bay**: `9.633m` (`19445`, `19448`)
  - **Single Story Height**: `3.500m`
  - **Triple Story Continuous Height**: `10.500m` (`19377`)
- Use structural framing models `18762` (1m x 1m x 5m) and `18766` (10m x 1m x 5m) for crisp pilasters, canopies, roof trims, and curbs.

## 9. Dynamic Signage & MaterialText Best Practices
- Place signboards using flat signage model `19482` or structural plate `18066`.
- Use clean modern fonts: `Arial`, `Calibri`, or `Arial Black`.
- Apply appropriate font sizes:
  - Room / Door signs: Size `20` to `28`
  - Department / Zone signs: Size `50` to `80`
  - Exterior Building Facades: Size `100` to `180`
- Use hex formatting e.g. `{ffffff}EMERGENCY` or `{ffcc00}DEALERSHIP` for clean visual pop.


