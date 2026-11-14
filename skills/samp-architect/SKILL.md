---
name: samp-architect
description: >-
  Use this skill whenever the user asks to design, generate, or create 3D mappings,
  buildings, houses, villas, offices, warehouses, cafes, interiors, or architectural
  structures for GTA SA-MP (San Andreas Multiplayer) or open.mp with high resolution,
  mathematical precision, zero Z-fighting, and direct Texture Studio BOBI integration.
---

# SAMP Architect: 3D Mapping & Architectural Generator

SAMP Architect enables Antigravity to act as an expert 3D architectural designer for SA-MP and open.mp. It enforces strict coordinate math, modular building dimensions, human ped scale, zero Z-fighting, and professional texture palettes.

---

## 1. Core Architectural Workflow

When the user asks you to design or build a mapping:

```
[User Request]
       │
       ▼
[1. Requirement Gathering]
   - Building function (Villa, Office, Shop, Base, Police HQ, Cafe, etc.)
   - Dimensions & Story count (e.g. 16m x 12m, 2 floors)
   - Aesthetic Palette (Modern Luxury, Industrial, Office HQ, Cyberpunk)
   - Location (Target World Coordinates X, Y, Z, and Heading Rotation)
       │
       ▼
[2. Geometry & 3D Math Calculation]
   - Snap modular walls (`19353`) and slabs (`19359`/`19360`) without gaps.
   - Floor-to-ceiling clearance: 3.2m to 3.8m.
   - Offset coplanar surfaces by 0.005m - 0.010m to prevent Z-fighting.
   - Corner joins using structural square pillars (`19363`) or corner units (`19356`).
       │
       ▼
[3. Texture & Material Mapping]
   - Select verified textures from [texture_palettes.md](./references/texture_palettes.md).
   - Apply `SetDynamicObjectMaterial` with slot, model, txd, and texture name.
   - Add ambient and architectural lighting (`19894` downlights, `19172` neons).
       │
       ▼
[4. Generation & Export]
   - Run the generator script:
     `python3 scripts/samp_architect.py --template <template> --name <Name> --x <X> --y <Y> --z <Z> --rot <Rot>`
   - Direct export to `/root/texture-studio-bobi/scriptfiles/tstudio/SavedMaps/<Name>.db`
   - Direct export to `/root/texture-studio-bobi/scriptfiles/tstudio/ImportMaps/<Name>.pwn`
       │
       ▼
[5. In-Game Testing]
   - Player can immediately test in Texture Studio BOBI using:
     `/loadmap <Name>` or `/importmap <Name>.pwn`
```

---

## 2. Using the Procedural Generator Script

The built-in engine at `scripts/samp_architect.py` provides pre-engineered, mathematically flawless templates:

### Generating Pre-built Architectural Templates:
```bash
# 1. Luxury Modern Villa (2-Story with balcony, glass facade, pool deck)
python3 /root/.gemini/config/plugins/samp-architect/skills/samp-architect/scripts/samp_architect.py \
    --template villa --name LuxuryVilla --x 1500.0 --y -1600.0 --z 15.0 --rot 0.0

# 2. Corporate Office HQ (3-Story commercial building with stairwell)
python3 /root/.gemini/config/plugins/samp-architect/skills/samp-architect/scripts/samp_architect.py \
    --template office --name CorporateHQ --x 1400.0 --y -1700.0 --z 14.0 --rot 90.0

# 3. Industrial Warehouse / Hangar (High-clearance double height)
python3 /root/.gemini/config/plugins/samp-architect/skills/samp-architect/scripts/samp_architect.py \
    --template warehouse --name AirCargoHangar --x 2000.0 --y -2200.0 --z 10.0

# 4. Contemporary Coffee Shop / Cafe (Front patio, storefront glass, bar)
python3 /root/.gemini/config/plugins/samp-architect/skills/samp-architect/scripts/samp_architect.py \
    --template cafe --name DowntownCafe --x 1100.0 --y -1450.0 --z 16.0
```

---

## 3. Custom Procedural Code Example in Python

For custom architectural designs, import `Building` and `Vec3` from `scripts.samp_architect`:

```python
from scripts.samp_architect import Building, Vec3, MODULAR_WALL, MODULAR_SLAB, GLASS_PANEL, LIGHT_DOWNLIGHT

# Create a building at Las Venturas (2000.0, 1500.0, 12.0) with heading 45.0 degrees
b = Building("CustomHQ", Vec3(2000.0, 1500.0, 12.0), heading=45.0, palette_name="modern_luxury")

# Build foundation & floor slab (16m x 16m)
b.build_slab_grid(Vec3(0, 0, 0), width=16.0, depth=16.0, z_offset=0.0, material_key="floor")

# Build perimeter walls
b.build_straight_wall(Vec3(-8.0, -8.0, 1.75), length=16.0, heading_deg=0.0, material_key="wall_ext", window_interval=2)
b.build_straight_wall(Vec3(8.0, 8.0, 1.75), length=16.0, heading_deg=180.0, material_key="wall_ext", window_interval=2)

# Build ceiling
b.build_slab_grid(Vec3(0, 0, 3.5), width=16.0, depth=16.0, z_offset=0.0, material_key="ceiling")

# Add ceiling downlights
b.add_object_local(LIGHT_DOWNLIGHT, Vec3(0, 0, 3.45), 0.0, 0.0, 0.0)

# Export directly to Texture Studio
from scripts.samp_architect import export_to_texture_studio_db, export_to_texture_studio_import
export_to_texture_studio_db(b)
export_to_texture_studio_import(b)
```

---

## 4. Key References for Detailed Specs

- [Modular Construction Objects](./references/modular_objects.md): Complete dimension and collision reference for modular blocks (`19353`-`19367`).
- [Texture Palettes](./references/texture_palettes.md): Verified TXD names, texture names, and color tint values for luxury, modern, industrial, and cyber themes.
- [3D Coordinate Math](./references/coordinates_math.md): Trigonometric rotation matrices and wall snapping formulas.
