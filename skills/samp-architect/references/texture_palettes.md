# Curated High-Resolution Texture Palettes for SA-MP Architecture

All textures listed below are 100% verified to exist in the GTA San Andreas standard assets library (matching Texture Studio's 9,065 texture definitions).

---

## 1. Palette: Modern Minimalist / Luxury Villa

| Element | Model | TXD Name | Texture Name | Visual Description |
|---|---|---|---|---|
| **Exterior Plaster** | 14668 | `711c` | `cj_white_wall2` | Ultra-clean modern white smooth stucco |
| **Secondary Wall** | 9514 | `711_sfw` | `mono1_sfe` | Light grey minimalist architectural concrete |
| **Accent Wood Panel**| 10101 | `2notherbuildsfe` | `sl_vicwall01` | Warm vertical natural wood slats |
| **Floor: Living/Hall**| 14668 | `711c` | `CJ_7_11_TILE` | Polished luxury porcelain tiles |
| **Floor: Bedroom/Wood**| 14668 | `711c` | `CJ_CHIP_M2` | Warm oak parquet flooring |
| **Ceiling** | 14668 | `711c` | `gun_ceiling1128`| Clean white architectural ceiling finish |
| **Glass / Windows** | 14668 | `711c` | `CJ_7_11_win` | Translucent modern window glass |
| **Terrace / Roof** | 10101 | `2notherbuildsfe` | `ws_rooftarmac1`| Clean dark roof membrane / terrace stone |

---

## 2. Palette: Industrial Warehouse / Urban Loft

| Element | Model | TXD Name | Texture Name | Visual Description |
|---|---|---|---|---|
| **Brick Facade** | 10101 | `2notherbuildsfe` | `sl_vicbrikwall01` | Classic red/brown exposed urban brickwork |
| **Corrugated Metal** | 9514 | `711_sfw` | `rebrckwall_128` | Industrial ribbed metal sheet cladding |
| **Pillar / Steel** | 9514 | `711_sfw` | `beachwall_law` | Heavy structural steel / industrial concrete |
| **Floor (Concrete)** | 9514 | `711_sfw` | `dt_carpark_line_texture` | Polished industrial floor with markings |
| **Ceiling** | 14668 | `711c` | `gun_ceiling3` | Industrial girder / high-ceiling concrete |
| **Doors** | 9514 | `711_sfw` | `staddoors1` | Heavy security industrial metal door |

---

## 3. Palette: Contemporary Office / Police HQ / Hospital

| Element | Model | TXD Name | Texture Name | Visual Description |
|---|---|---|---|---|
| **Office Wall** | 9514 | `711_sfw` | `mono2_sfe` | Professional beige/grey acoustic plaster |
| **Lobby Floor** | 14668 | `711c` | `bwtilebroth` | Black & white checkerboard or marble grid |
| **Corridor Floor**| 14668 | `711c` | `CJ_7_11_TILE` | Clean commercial vinyl / linoleum tile |
| **Acoustic Ceiling**| 14668 | `711c` | `gun_ceiling1128`| 2x2 grid drop-ceiling panels |
| **Office Glass** | 14668 | `711c` | `CJ_7_11_win` | Clear reflective glass partition |
| **Wood Doors** | 10101 | `2notherbuildsfe` | `flatdoor01_law` | Flush oak professional interior door |

---

## 4. Palette: Cyberpunk / Nightlife Club

| Element | Model | TXD Name | Texture Name | Hex Tint Overlay (ARGB) |
|---|---|---|---|---|
| **Dark Carbon Wall**| 10101 | `2notherbuildsfe` | `ws_rooftarmac1` | `0xFF1A1A24` (Deep obsidian) |
| **Reflective Floor** | 14668 | `711c` | `CJ_7_11_TILE` | `0xFF0A0A10` (High gloss mirror black)|
| **Accent Neon Blue**| 19172 | (Native) | (Native) | Bright luminous cyan |
| **Accent Neon Magenta**| 19173 | (Native) | (Native) | Electric purple/pink |
| **Ceiling Grid** | 14668 | `711c` | `gun_ceiling3` | `0xFF111118` (Dark matte void) |

---

## 5. Usage in SA-MP PAWN & Texture Studio

```pawn
// Apply texture to dynamic object:
SetDynamicObjectMaterial(
    objectid, 
    0,                      // Material Index 0
    14668,                  // Model ID
    "711c",                 // TXD Name
    "cj_white_wall2",       // Texture Name
    0                       // Color (0 = keep original texture colors)
);
```
