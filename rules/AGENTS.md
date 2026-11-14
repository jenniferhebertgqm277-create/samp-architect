# SA-MP 3D Architectural Mapping Rules

These rules govern how the agent designs, calculates coordinates, and generates 3D mappings for SA-MP and open.mp.

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
