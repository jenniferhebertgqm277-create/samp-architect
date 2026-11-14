# 🏛️ SAMP Architect: Universal 3D Mapping & Architectural Generator

[![Antigravity Plugin](https://img.shields.io/badge/Antigravity-Plugin-blue.svg)](https://github.com/jenniferhebertgqm277-create/samp-architect)
[![SA-MP / open.mp](https://img.shields.io/badge/SA--MP-0.3.7%20%7C%20open.mp-orange.svg)](https://open.mp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**SAMP Architect** is an Antigravity (AGY) plugin and skill suite that empowers AI coding agents to design, generate, and calculate mathematically precise 3D structures for **GTA San Andreas Multiplayer (SA-MP)** and **open.mp**.

It works seamlessly across **ANY SA-MP gamemode** (Roleplay, Deathmatch, Freeroam, Cnr, Stunt, Racing) and generates clean, modular PAWN code (`.inc`, `.pwn`) with **zero Z-fighting**, **zero seam gaps**, and **strict human ped scale**.

---

## ✨ Core Features

- 📐 **Zero Z-Fighting & Gap Elimination**:
  Automatically calculates micro-offsets (0.005m – 0.010m) for coplanar elements (glass, floor overlays, wall posters). Geometric wall snapping eliminates seam gaps and texture glitching.
- 🚶 **Human Ped Scale Compliance**:
  Enforces 3.2m – 3.8m standard single-story ceiling height, 2.2m – 2.5m doorframes, and realistic stair steps matching CJ's 1.8m player model.
- 🎨 **Verified HD Texture Palettes**:
  Pre-configured with 100% verified GTA SA materials: Modern Plaster, Italian Marble, Polished Oak Parquet, Exposed Urban Brick, Corrugated Metal, Tinted Glass, and ARGB Color Tints.
- 📦 **Works with Any SA-MP Gamemode**:
  Generates production-ready PAWN includes (`.inc`) with `LoadMap_<Name>()` and `UnloadMap_<Name>()`, standalone filterscripts (`.pwn`), or raw code for `OnGameModeInit()`.
- 🤖 **Natural Language 3D Design**:
  Describe any building to Antigravity (e.g., *"Generate a modern 2-story glass villa at 1500, -1600, 15 with downlights and terrace"*), and the agent calculates all 3D transformations, rotations, materials, and code automatically.

---

## 📦 Installation in Any Antigravity (AGY) Instance

Install this plugin into any machine running Antigravity CLI or AGY IDE:

### 1. Global Installation (Recommended)
Clones into your global Antigravity plugins directory to be active across all projects:
```bash
git clone https://github.com/jenniferhebertgqm277-create/samp-architect.git ~/.gemini/config/plugins/samp-architect
```

### 2. Project-Specific Workspace Installation
If you want to keep the skill inside a specific server repository:
```bash
cd /path/to/your/samp-server
mkdir -p .agents/plugins
git clone https://github.com/jenniferhebertgqm277-create/samp-architect.git .agents/plugins/samp-architect
```

### 3. Via Antigravity CLI
```bash
git clone https://github.com/jenniferhebertgqm277-create/samp-architect.git /tmp/samp-architect
agy plugin install /tmp/samp-architect
```

Validate installation:
```bash
agy plugin validate ~/.gemini/config/plugins/samp-architect
```

---

## 🚀 Usage Guide

### 1. Generating Pre-built Architectural Templates
Use the built-in procedural generator:

```bash
# 1. Modern 2-Story Luxury Villa (Balcony, glass facade, pool terrace, ambient neons)
python3 skills/samp-architect/scripts/samp_architect.py \
    --template villa --name LuxuryVilla --x 1500.0 --y -1600.0 --z 15.0 --out-inc pawno/include/maps/villa.inc

# 2. 3-Story Corporate Office HQ (Glass curtain wall, lobby, stairwells, downlights)
python3 skills/samp-architect/scripts/samp_architect.py \
    --template office --name CorporateHQ --x 1400.0 --y -1700.0 --z 14.0 --out-inc pawno/include/maps/office.inc

# 3. Industrial Warehouse / Hangar (Double height clearance, corrugated steel)
python3 skills/samp-architect/scripts/samp_architect.py \
    --template warehouse --name BigWarehouse --x 2000.0 --y -2200.0 --z 10.0 --out-fs filterscripts/warehouse.pwn

# 4. Contemporary Coffee Shop / Cafe (Outdoor deck, storefront glass, warm downlights)
python3 skills/samp-architect/scripts/samp_architect.py \
    --template cafe --name DowntownCafe --x 1100.0 --y -1450.0 --z 16.0 --out-inc pawno/include/maps/cafe.inc
```

---

## 🔌 How to Load Generated Maps in Any Gamemode

### Method A: Modular PAWN Include (`.inc`)
Place the generated `.inc` file inside your server's `pawno/include/` directory and include it in your gamemode:

```pawn
#include <a_samp>
#include <streamer>
#include <maps/villa>

public OnGameModeInit()
{
    // Load the 3D mapping
    LoadMap_LuxuryVilla();
    return 1;
}

public OnGameModeExit()
{
    // Unload when gamemode shuts down
    UnloadMap_LuxuryVilla();
    return 1;
}
```

### Method B: Standalone Filterscript (`.pwn`)
Pass `--out-fs filterscripts/my_map.pwn` to generate a ready-to-compile filterscript:
```bash
# Compile using Pawn Compiler
pawncc filterscripts/my_map.pwn -i:pawno/include
```
Then add `my_map` to your `server.cfg` under `filterscripts`.

---

## 🐍 Python Procedural API for Custom Structures

You can script custom structures in Python using `Building` and `Vec3`:

```python
from skills.samp_architect.scripts.samp_architect import (
    Building, Vec3, MODULAR_WALL, MODULAR_SLAB, GLASS_PANEL,
    LIGHT_DOWNLIGHT, export_gamemode_include
)

# Initialize building at world coordinates and rotation
b = Building("Custom_Building", Vec3(1200.0, -1500.0, 20.0), heading=0.0, palette_name="modern_luxury")

# Build 16m x 12.8m room with 3.5m ceiling height
b.build_rectangular_room(
    Vec3(0, 0, 0),
    width=16.0, depth=12.8, height=3.50,
    ext_material="wall_ext", floor_material="floor", ceiling_material="ceiling"
)

# Add recessed downlight at ceiling center
b.add_object_local(LIGHT_DOWNLIGHT, Vec3(0, 0, 3.45), 0.0, 0.0, 0.0)

# Export to clean PAWN include
with open("custom_building.inc", "w") as f:
    f.write(export_gamemode_include(b))
```

---

## 📚 Technical References Included

- [Modular Construction Objects](skills/samp-architect/references/modular_objects.md): Dimension specifications for modular building blocks (`19353` - `19367`).
- [Texture Palettes Reference](skills/samp-architect/references/texture_palettes.md): Curated HD material definitions with Model, TXD, and Texture Name.
- [3D Coordinate Math Guide](skills/samp-architect/references/coordinates_math.md): Trigonometric formulas for Euler rotations, local-to-world projection, and wall grid snapping.
- [AI Rules Guide](rules/AGENTS.md): Architectural design standards applied when Antigravity designs buildings.

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
Created with ❤️ for the SA-MP and open.mp developer community.
