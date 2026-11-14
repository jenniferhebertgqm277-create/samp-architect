---
name: samp-architect
description: >-
  Use this skill whenever the user asks to design, generate, or create 3D mappings,
  buildings, houses, villas, offices, warehouses, cafes, interiors, or architectural
  structures for GTA SA-MP or open.mp with high resolution, mathematical precision,
  zero Z-fighting, and universal PAWN gamemode export.
---

# SAMP Architect: Universal 3D Mapping & Architectural Generator

SAMP Architect enables Antigravity to act as an expert 3D architectural designer for SA-MP and open.mp. It enforces strict coordinate math, modular building dimensions, human ped scale, zero Z-fighting, and professional texture palettes compatible with **any SA-MP gamemode**.

---

## 1. Core Architectural Workflow

When the user asks you to design or build a mapping:

```
[User Request]
       │
       ▼
[1. Requirement Gathering]
   - Building function (Villa, Office, Shop, Base, Police HQ, Cafe, Airport, etc.)
   - Dimensions & Story count (e.g. 16m x 12m, 2 floors)
   - Aesthetic Palette (Modern Luxury, Industrial, Office HQ, Cyberpunk)
   - Target Location (World Coordinates X, Y, Z, and Heading Rotation)
   - Context Check: If located at an existing GTA SA landmark, query and remove overlapping default buildings via `remove_buildings_in_box`
       │
       ▼
[2. Geometry & Anti-Looping Architectural Design]
   - NEVER generate repetitive naive slab grids (`19360` 5x5m loops).
   - Use large-format structural plates (`19361` 10x10m or `18344` 20x20m).
   - Establish architectural rhythm: columns (`19363`) at 6m - 10m intervals, glass panels (`19447`), and roof fascia (`19365`).
   - Create distinct entrance portals with sliding doors (`19856`) and dynamic text signage (`19475`).
   - Floor-to-ceiling clearance: 3.2m to 3.8m (or 7.0m for double-height terminals).
   - Offset coplanar surfaces by 0.005m - 0.010m to prevent Z-fighting.
   - Raised pedestrian sidewalk curbs (+0.10m to +0.25m) with safety bollards (`1237`).
       │
       ▼
[3. Texture & Material Mapping]
   - Select verified textures from [texture_palettes.md](./references/texture_palettes.md).
   - Apply `SetDynamicObjectMaterial` with slot, model, txd, and texture name.
   - Add ambient and architectural lighting (`19894` downlights, `19172` neons).
       │
       ▼
[4. Generation & Universal PAWN Export]
   - Run the generator script:
     `python3 scripts/samp_architect.py --template <villa|office|warehouse|cafe|dealership|police|hospital> --name <Name> --x <X> --y <Y> --z <Z> --rot <Rot> --out-inc <path.inc> --out-fs <path.pwn>`
   - Outputs:
     - Modular Include (`.inc`) with `LoadMap_<Name>()` and `UnloadMap_<Name>()`.
     - Standalone Filterscript (`.pwn`) ready to compile with pawncc.
       │
       ▼
[5. Gamemode Integration]
   - Include in gamemode via `#include <maps/name>` and call `LoadMap_Name()`.
```

---

## 2. Universal PAWN Integration Patterns

### Pattern A: Modular Include (`#include <maps/name>`)
```pawn
#include <a_samp>
#include <streamer>
#include <maps/my_building>

public OnGameModeInit()
{
    LoadMap_MyBuilding();
    return 1;
}

public OnGameModeExit()
{
    UnloadMap_MyBuilding();
    return 1;
}
```

### Pattern B: Standalone Filterscript
```bash
python3 scripts/samp_architect.py --template villa --name LuxuryVilla --x 1500.0 --y -1600.0 --z 15.0 --out-fs filterscripts/villa.pwn
```

---

## 3. Key References for Detailed Specs

- [Modular Construction Objects](./references/modular_objects.md): Dimension and collision reference for modular blocks (`19353`-`19367`).
- [Texture Palettes](./references/texture_palettes.md): Verified TXD names, texture names, and color tint values for luxury, modern, industrial, and cyber themes.
- [3D Coordinate Math](./references/coordinates_math.md): Trigonometric rotation matrices and wall snapping formulas.
- [Architectural Rules](../../rules/AGENTS.md): Design rules for scale, structural completeness, and zero Z-fighting.
