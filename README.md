# 🏛️ SAMP Architect: AI 3D Mapping & Architectural Generator

[![Antigravity Plugin](https://img.shields.io/badge/Antigravity-Plugin-blue.svg)](https://github.com)
[![SA-MP / open.mp](https://img.shields.io/badge/SA--MP-0.3.7%20%7C%20open.mp-orange.svg)](https://open.mp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**SAMP Architect** is an official plugin and skill suite for **Google Antigravity (AGY)** and AI coding assistants. It turns the AI agent into an expert 3D architectural designer for **GTA San Andreas Multiplayer (SA-MP)** and **open.mp**.

It guarantees **mathematical precision, zero gaps, zero Z-fighting (overlapping texture flicker), proper human scale, and seamless Texture Studio BOBI v1 integration**.

---

## ✨ Features

- 📐 **Zero Z-Fighting & Gap Elimination**:
  Calculates automatic 0.005m – 0.010m normal offsets for overlapping surfaces, posters, carpets, and glass. Corner alignment formulas prevent light leaks and seam cracks.
- 🚶 **Human Ped Scale Compliance**:
  Enforces 3.2m – 3.8m standard single-story ceiling height, 2.2m – 2.5m doorframes, and realistic stair steps (~0.18m rise per ~0.28m tread) matching CJ's 1.8m ped model.
- 🎨 **Verified HD Texture Palettes**:
  Curated collection of 100% verified GTA SA textures matching Texture Studio's 9,065 database: Modern Plaster, Italian Marble, Polished Oak Parquet, Exposed Urban Brick, Corrugated Industrial Metal, and ARGB Color Tints.
- ⚡ **Direct Texture Studio BOBI Integration**:
  Exports directly into Texture Studio's SQLite `.db` map files in `SavedMaps/` AND `.pwn` scripts in `ImportMaps/` for instant live in-game preview (`/loadmap` or `/importmap`).
- 🤖 **Natural Language AI Prompts**:
  Tell Antigravity: *"Design a 2-story luxury modern glass villa at coordinates 1500, -1600, 15"* and it will generate all 3D coordinates, walls, floors, staircases, and textures automatically.

---

## 📦 Installation in Any Antigravity (AGY) Instance

You can install this plugin into any machine running Antigravity CLI or AGY IDE.

### Method 1: Global Plugin Installation (Recommended)
Clone directly into your global Antigravity plugins directory:
```bash
git clone https://github.com/jenniferhebertgqm277-create/samp-architect.git ~/.gemini/config/plugins/samp-architect
```
Antigravity will automatically discover and activate the plugin across all your projects.

---

### Method 2: Project-Specific Installation (Workspace)
If you want to keep the skill within a specific SA-MP server project repository:
```bash
cd /path/to/your/samp-project
mkdir -p .agents/plugins
git clone https://github.com/jenniferhebertgqm277-create/samp-architect.git .agents/plugins/samp-architect
```

---

### Method 3: Via Antigravity CLI
```bash
git clone https://github.com/jenniferhebertgqm277-create/samp-architect.git /tmp/samp-architect
agy plugin install /tmp/samp-architect
```

To verify the installation:
```bash
agy plugin validate ~/.gemini/config/plugins/samp-architect
```

---

## 🚀 Quick Start & CLI Usage

SAMP Architect includes a standalone high-precision procedural math engine:

### 1. Generating Architectural Templates via CLI:
```bash
# Modern 2-Story Luxury Villa (Balcony, glass facade, pool terrace, ambient neons)
python3 skills/samp-architect/scripts/samp_architect.py \
    --template villa --name MyModernVilla --x 1500.0 --y -1600.0 --z 15.0 --rot 0.0

# 3-Story Corporate Office HQ (Glass tower, reception, elevator shaft, downlights)
python3 skills/samp-architect/scripts/samp_architect.py \
    --template office --name CorporateHQ --x 1400.0 --y -1700.0 --z 14.0 --rot 90.0

# Industrial Logistics Warehouse / Hangar (Double height clearance, corrugated steel)
python3 skills/samp-architect/scripts/samp_architect.py \
    --template warehouse --name BigWarehouse --x 2000.0 --y -2200.0 --z 10.0

# Contemporary Coffee Shop / Cafe (Outdoor deck, storefront glass, warm downlights)
python3 skills/samp-architect/scripts/samp_architect.py \
    --template cafe --name CozyCafe --x 1100.0 --y -1450.0 --z 16.0
```

### 2. Output Locations:
When generated, SAMP Architect automatically creates:
- **Texture Studio DB**: `/root/texture-studio-bobi/scriptfiles/tstudio/SavedMaps/<Name>.db`
- **Texture Studio Import**: `/root/texture-studio-bobi/scriptfiles/tstudio/ImportMaps/<Name>.pwn`
- **Standalone PAWN Code**: Ready to paste into your gamemode or filterscript.

---

## 🎮 In-Game Testing (Texture Studio BOBI v1)

Connect to your SA-MP server and open the map in real time:
1. Load directly from SQLite:
   ```
   /loadmap MyModernVilla
   ```
2. Or import via `.pwn`:
   ```
   /importmap MyModernVilla.pwn
   ```
3. Use the on-screen **BOBI Touch Nudge Pad** or `/bobi` menu on mobile/PC to fine-tune any object.

---

## 🐍 Python Procedural Builder API

You can script custom structures in Python using the `Building` and `Vec3` classes:

```python
from skills.samp_architect.scripts.samp_architect import (
    Building, Vec3, MODULAR_WALL, MODULAR_SLAB, GLASS_PANEL,
    LIGHT_DOWNLIGHT, export_to_texture_studio_db, export_to_texture_studio_import
)

# Initialize building at target world coordinates and heading
b = Building("Custom_Penthouse", Vec3(1200.0, -1500.0, 25.0), heading=0.0, palette_name="modern_luxury")

# Build 16m x 12.8m room with 3.5m ceiling height
b.build_rectangular_room(
    Vec3(0, 0, 0),
    width=16.0, depth=12.8, height=3.50,
    ext_material="wall_ext", floor_material="floor", ceiling_material="ceiling"
)

# Add recessed downlight at ceiling center
b.add_object_local(LIGHT_DOWNLIGHT, Vec3(0, 0, 3.45), 0.0, 0.0, 0.0)

# Export directly to Texture Studio
export_to_texture_studio_db(b)
export_to_texture_studio_import(b)
```

---

## 📚 Architectural References Included

- [Modular Objects Reference](skills/samp-architect/references/modular_objects.md): Dimension specifications for modular building blocks (`19353` - `19367`).
- [Texture Palettes Reference](skills/samp-architect/references/texture_palettes.md): Curated HD material definitions with Model, TXD, and Texture Name.
- [Coordinate Math Guide](skills/samp-architect/references/coordinates_math.md): Trigonometric formulas for Euler rotations, local-to-world projection, and wall grid snapping.
- [AI Rules Guide](rules/AGENTS.md): Golden architectural design rules applied when Antigravity designs buildings.

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
Created with ❤️ by the Antigravity & BOBI Community.
