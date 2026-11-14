---
name: samp-architect
description: >-
  Use this skill whenever the user asks to design, generate, or create 3D mappings,
  buildings, houses, villas, offices, warehouses, cafes, interiors, or architectural
  structures for GTA SA-MP or open.mp with high resolution, mathematical precision,
  zero Z-fighting, and universal PAWN gamemode export.
---

# SAMP Architect: Universal 3D Mapping & Autonomous Architectural Generator

SAMP Architect enables Antigravity to act as an expert, autonomous 3D architectural designer for SA-MP and open.mp. It designs every structure **from scratch** based on the user's specific request—enforcing strict coordinate math, modular building dimensions, human ped scale, zero Z-fighting, and professional texture palettes compatible with **any SA-MP gamemode**.

> [!IMPORTANT]
> **Strictly No Rigid Templates**: The AI never relies on fixed, pre-baked building templates. Uploaded mapping files and server archives serve as **training & learning references** from which the AI extracts exact collision dimensions, model synergies, texture palettes, and pro architectural techniques.

---

## 1. Autonomous Architectural Generation Pipeline

When the user asks you to design or build any mapping (e.g. a beach club at Santa Maria, an auto repair shop in Blueberry, a luxury penthouse in Rodeo, or a police precinct):

```
[User Request]
       │
       ▼
[1. Architectural Conception & Spatial Planning]
   - Determine Building Function, Footprint, and Story Count.
   - Plan Functional Zones: Entrances, main lobby/hall, private rooms, outdoor patios, driveways.
   - Select Aesthetic Palette: Modern luxury, automotive showroom, government limestone, industrial steel, etc.
   - Target Coordinates: Origin (X, Y, Z) and Facing Rotation (degrees).
       │
       ▼
[2. Site Context & World Clearance]
   - Inspect surrounding GTA SA world coordinates.
   - Automatically register overlapping default GTA SA buildings, lampposts, or props for removal via `remove_buildings_in_radius` or `remove_buildings_in_box`.
       │
       ▼
[3. Precision 3D Mathematical Assembly (Grid Snapping)]
   - Snap structural elements to the **Golden Modular Grid**:
     * Single-Bay: 3.211m (`19353`, `19354`, `19355`)
     * Half-Bay: 1.601m (`19426`)
     * Triple-Bay: 9.633m (`19445`, `19448`)
     * Story Height: 3.500m (or 7.000m for double-height concourses)
   - Anchor the structure with subterranean concrete foundation plates (`18765` or `19361`).
   - Frame long spans with structural columns (`18762` / `19363`) and horizontal beams (`18766`).
   - Offset all overlay panels / posters (`18066`) by +0.025m to +0.035m normal to prevent Z-fighting.
       │
       ▼
[4. Architectural Detailing, Lighting & Dynamic Signage]
   - Install entrance portals with sliding glass doors (`19856`) or commercial glass double doors (`1497`).
   - Add custom 3D illuminated signboards (`19482` / `SetDynamicObjectMaterialText`) with proper font sizes (20-28 for doors, 36-50 for headers, 80-130 for exterior building facades).
   - Distribute recessed ceiling downlights (`19894`), fluorescent tubes (`19896`), or neon accent tubes (`19172`).
   - Add appropriate furniture, desks (`18980`), counters, railings (`19367`), and outdoor sidewalk curbs.
       │
       ▼
[5. Dynamic Script Synthesis & Universal PAWN Export]
   - Write a custom Python script using the `samp_architect` toolkit to synthesize the custom geometry.
   - Export directly to:
     * Modular Include (`.inc`) with `LoadMap_<Name>()` and `UnloadMap_<Name>()`.
     * Standalone Filterscript (`.pwn`) ready to compile with pawncc and test via `/loadmap <Name>`.
```

---

## 2. Dynamic Bespoke Architecture Example

When building custom architecture, the agent writes a concise Python script using the `samp_architect` engine:

```python
from samp_architect import Building, Vec3

# 1. Initialize Bespoke Building at Target Location
b = Building(name="SMB_Beach_Club", origin=Vec3(380.0, -1880.0, 8.0), heading=0.0, palette_name="modern_luxury")

# 2. Clear Overlapping Default GTA SA World Objects
b.remove_buildings_in_radius(380.0, -1880.0, radius=50.0)

# 3. Build Raised Foundation & Beach Deck
b.build_slab_grid(Vec3(0, 0, 0), width=28.899, depth=19.266, z_offset=0.0, material_key="floor_wood")

# 4. Construct Glass Curtain Facade Facing Ocean
b.build_curtain_wall_facade(
    start_pos=Vec3(-14.45, -9.63, 0), length=28.899, height=3.5, heading_deg=0.0,
    column_span=9.633, column_model=18762, glass_model=19448
)

# 5. Add Custom Dynamic Signage & Downlights
sign = b.add_object_local(19482, Vec3(0, -9.8, 3.2), 0.0, 0.0, 0.0)
sign.set_material_text(0, "{00ffff}OCEAN BREEZE {ffffff}| BEACH CLUB", material_size=130, font="Arial Black", font_size=36)

# 6. Export to Universal Include and Standalone Filterscript
with open("SMB_Beach_Club.inc", "w") as f:
    f.write(export_gamemode_include(b))
```

---

## 3. Universal PAWN Integration Patterns

### Pattern A: Modular Include (`#include <maps/name>`)
```pawn
#include <a_samp>
#include <streamer>
#include <maps/SMB_Beach_Club>

public OnGameModeInit()
{
    LoadMap_SMB_Beach_Club();
    return 1;
}

public OnGameModeExit()
{
    UnloadMap_SMB_Beach_Club();
    return 1;
}
```

### Pattern B: Standalone Filterscript / Texture Studio
Place `.pwn` in `scriptfiles/tstudio/ImportMaps/` to load instantly in-game via `/loadmap <Name>`, or compile directly into `filterscripts/<Name>.amx`.

---

## 3. Key References for Detailed Specs

- [Modular Construction Objects](./references/modular_objects.md): Dimension and collision reference for modular blocks (`19353`-`19367`).
- [Texture Palettes](./references/texture_palettes.md): Verified TXD names, texture names, and color tint values for luxury, modern, industrial, and cyber themes.
- [3D Coordinate Math](./references/coordinates_math.md): Trigonometric rotation matrices and wall snapping formulas.
- [Architectural Rules](../../rules/AGENTS.md): Design rules for scale, structural completeness, and zero Z-fighting.
