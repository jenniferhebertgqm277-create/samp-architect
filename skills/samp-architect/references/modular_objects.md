# Modular SA-MP Architecture Objects Reference

This reference catalogs the premier modular construction objects in SA-MP and open.mp, complete with exact bounding box dimensions (X, Y, Z) extracted from the game engine collision geometry.

---

## 1. Modular Walls (0.3c / 0.3d / 0.3.7 Standard)

Every modular wall follows the **Golden SA-MP Modular Grid**:
- Standard Height: **3.500m**
- Standard Wall Thickness: **0.172m**
- Base Unit Width: **3.211m** (`19353`)
- Half-Bay Width: **1.601m** (`19426`)
- Triple-Bay Width: **9.633m** (`19445`, `19448`)
- Continuous 3-Story Height: **10.500m** (`19377`)

| Model ID | Object Name / Description | Dimensions (X x Y x Z) | Features & Pro Usage |
|---|---|---|---|
| **19353** | Flat Wall Panel (Standard) | 0.172m x 3.211m x 3.500m | Seamless retextureable wall. The primary single-bay building block. |
| **19354** | Wall with Window Opening | 0.172m x 3.211m x 3.500m | Centered window cutout. Fits glass pane `19379` or `19447`. |
| **19355** | Wall with Door Opening | 0.172m x 3.211m x 3.500m | Centered doorway opening. Fits door `1491` or `1495`. |
| **19356** | Corner Column Wall | 0.172m x 3.211m x 3.500m | Clean 90-degree corner transition. Eliminates seam gaps. |
| **19426** | Narrow Wall Panel (Half-Bay) | 0.172m x 1.601m x 3.500m | Exactly half width (1.601m). Used as mullions and gap closers. |
| **19445** | Large Modular Wall / Glass Panel | 0.172m x 9.633m x 3.500m | Exactly 3x width (9.633m). High-speed seamless wall coverage. |
| **19448** | Ultra-Wide Storefront Glass | 0.172m x 9.633m x 3.500m | Commercial and airport curtain wall standard. Zero tiling seams! |
| **19377** | Continuous 3-Story Wall | 0.172m x 9.633m x 10.500m| Exactly 3 bays wide and 3 stories high (10.5m). Eliminates horizontal floor seams. |
| **19447** | Seamless Tinted Glass Panel | ~0.05m x 3.00m x 3.00m | Ultra-clean reflective glass. Great for modern facades. |
| **18066** | Poster Decal / Panel (`posterv`) | ~0.02m x 1.50m x 2.00m | Placed with +0.03m normal offset to create trims, wainscoting, and accent slats with 0 Z-fighting! |

---

## 2. Floors, Ceilings & Foundations

| Model ID | Object Name / Description | Dimensions (X x Y x Z) | Features |
|---|---|---|---|
| **19359** | Floor / Ceiling Slab (Standard) | 3.211m x 3.211m x 0.20m | Perfectly matches single-bay `19353` wall grid. |
| **19360** | Medium Floor Slab | 5.00m x 5.00m x 0.20m | Fast floor coverage with collision. |
| **19361** | Large Floor Slab | 10.00m x 10.00m x 0.25m | Ideal for base foundations and large warehouse floors. |
| **18765** | Concrete Foundation Block | 10.00m x 10.00m x 5.00m | Massive 5m deep subterranean foundation block. Guarantees building never floats on hills! |
| **18344** | Giant Concrete Slab | 196.8m x 254.2m x 22.5m | Massive coverage for parking lots, runways, and concourses. |
| **19365** | Roof Cap / Fascia Trim | 3.211m x 0.35m x 0.35m | Clean top edge finishing for walls and roof parapets. |

---

## 3. Structural Columns, Beams & Framing

| Model ID | Object Name / Description | Dimensions (X x Y x Z) | Best Use Case |
|---|---|---|---|
| **18762** | Concrete / Steel Pillar (`Concrete1mx1mx5m`)| 1.00m x 1.00m x 5.00m | Standard 1m x 1m column. When rotated 90 deg, serves as a 5m horizontal beam! |
| **18766** | Heavy Concrete Beam (`Concrete10mx1mx5m`)| 10.00m x 1.00m x 5.00m | 10m long beam / curb / lintel. The #1 framing object in elite Indonesian mapping. |
| **19363** | Square Structural Pillar | 0.40m x 0.40m x 3.50m | Clean interior column matching standard 3.5m ceiling height. |
| **19362** | Cylindrical Round Column | Radius ~0.30m, Height 3.50m | Classic luxury columns, hotel lobbies, porch entrances. |
| **2512**  | Slanted Steel Pylon Strut | Height ~6.0m | Rotated at 70 deg for dramatic cantilevered modern airport canopies. |
| **3533**  | Pylon Base Support Column | Height ~5.0m | Anchors slanted structural canopy pylons. |
| **19364** | Modular Straight Staircase | Length 5.00m, Height 3.50m | Exact 1-floor rise staircase matching 3.5m wall height! |
| **19939** | Stair Step / Slat Tread | 0.437m x 1.000m x 0.031m | Custom architectural floating stairs, louvers, and wood slat screens. |
| **19367** | Balcony Railing Panel | Length 3.21m, Height 1.10m | Clean modern balcony and terrace safety barriers. |

---

## 4. Doors, Signs & Commercial Counters

| Model ID | Object Name / Description | Dimensions / Features |
|---|---|---|
| **1491** | Standard Wood / Glass Interior Door | 1.0m width, 2.2m height. Can be animated with MoveDynamicObject. |
| **1495** | Metal Security Door / Fire Door | Heavy back exit door. |
| **1497** | Glass Double Door | Modern entrance doors for offices, banks, and cafes. |
| **19856** | Sliding Modern Glass Door | Luxury patio / showroom transition door. |
| **19482** | Illuminated Signboard Surface | Flat box surface for crisp dynamic `SetDynamicObjectMaterialText`. |
| **18980** | Modern Reception / Office Counter | Commercial reception desks, police booking desks, hotel check-in. |
| **18981** | Modern Retail Display Shelf / Partition | 1.0m x 25.0m x 25.0m partition wall / retail shelf backplate. |

---

## 5. Architectural Lighting & Visual Effects

| Model ID | Light Type | Visual Style | Notes |
|---|---|---|---|
| **19894** | Recessed Downlight / Spot | Warm white downlight spot | Place on ceiling slab (Z - 0.05m). Realistic interior lighting. |
| **19896** | Fluorescent Tube Lamp | Cool white industrial light | Perfect for garages, offices, and kitchens. |
| **19172** | Neon Tube Light (Blue) | Glow effect | High-tech, nightlife, cyber, modern edge trim. |
| **19173** | Neon Tube Light (Red) | Glow effect | Accent lighting and warnings. |
| **19174** | Neon Tube Light (Green) | Glow effect | Modern futuristic accents. |
| **18646** | Pure White Omnilight Flare | Ambient light sphere | Illuminates surrounding surfaces realistically. |
| **19897** | Modern Wall Sconce | Up & down wall wash | Exterior facade illumination. |

