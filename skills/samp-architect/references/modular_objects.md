# Modular SA-MP Architecture Objects Reference

This reference catalogs the premier modular construction objects introduced in SA-MP 0.3c, 0.3d, and 0.3.7. These objects are designed specifically for precision building without gaps.

---

## 1. Modular Walls (0.3c / 0.3d Standard)

| Model ID | Object Name / Description | Dimensions (X x Y x Z) | Features |
|---|---|---|---|
| **19353** | Flat Wall Panel (Standard) | ~0.17m x 3.20m x 3.50m | Seamless retextureable wall. Primary building block. |
| **19354** | Wall with Window Opening | ~0.17m x 3.20m x 3.50m | Centered window cutout. Pair with glass `19379` or `19447`. |
| **19355** | Wall with Door Opening | ~0.17m x 3.20m x 3.50m | Centered doorway opening. Pair with door `1491` or `1495`. |
| **19356** | Corner Column Wall | ~0.35m x 0.35m x 3.50m | Clean 90-degree corner transition. Prevents seam gaps. |
| **19357** | Narrow Wall Panel (Half) | ~0.17m x 1.60m x 3.50m | Used for fitting remaining wall gaps. |
| **19358** | Very Narrow Wall Panel | ~0.17m x 0.80m x 3.50m | Precision filler panel. |
| **19445** | Modern Storefront Glass Wall | ~0.10m x 4.00m x 3.50m | Large glass frame with metal mullions. |
| **19447** | Seamless Tinted Glass Panel | ~0.05m x 3.00m x 3.00m | Ultra-clean reflective glass. Great for modern facades. |
| **19448** | Ultra-Wide Storefront Glass | ~0.10m x 9.63m x 3.50m | Premier pro choice for airport and commercial concourses. Zero tiling seams! |
| **19381** | Smooth Structural Panel | ~0.20m x 9.60m x 3.50m | Often rotated 90 deg for smooth road curbs and parking dividers. |
| **19816** | Ultra-Smooth Interior Wall | ~0.15m x 3.00m x 3.50m | High resolution clean interior wall for offices and houses. |

---

## 2. Floors, Ceilings & Foundations

| Model ID | Object Name / Description | Dimensions (X x Y x Z) | Features |
|---|---|---|---|
| **19359** | Floor / Ceiling Slab (Standard) | 3.20m x 3.20m x 0.20m | Perfectly matches `19353` wall grid. |
| **19360** | Medium Floor Slab | 5.00m x 5.00m x 0.20m | Fast floor coverage with collision. |
| **19361** | Large Floor / Foundation Slab | 10.00m x 10.00m x 0.25m | Ideal for base foundations and large warehouse floors. |
| **18344** | Giant Concrete Slab | 20.00m x 20.00m x 0.30m | Massive coverage for parking lots, plazas, and basements. |
| **19365** | Roof Cap / Trim | Various | Clean top edge finishing for walls and roof parapets. |

---

## 3. Structural Columns, Beams & Stairs

| Model ID | Object Name / Description | Dimensions / Specs | Best Use Case |
|---|---|---|---|
| **19362** | Cylindrical Round Pillar | Radius ~0.30m, Height 3.50m | Classic luxury columns, hotel lobbies, porch entrances. |
| **19363** | Square Structural Column | 0.40m x 0.40m x 3.50m | Modern architectural load-bearing columns. |
| **18762** | Steel Girder / Modular Truss | Length ~10.0m | Rotated 90 deg for horizontal roof trusses and canopy beams. |
| **18766** | Heavy Steel Girder / Truss | Length ~10.0m | Heavy load-bearing canopy frame and industrial girders. |
| **2512**  | Slanted Steel Pylon Strut | Height ~6.0m | Rotated at 70 deg for dramatic cantilevered modern airport canopies. |
| **3533**  | Pylon Base Support Column | Height ~5.0m | Anchors slanted structural canopy pylons. |
| **19364** | Modular Straight Staircase | Length 5.0m, Height 3.50m | Exact 1-floor rise staircase matching 3.5m wall height! |
| **19366** | Staircase Handrail / Railing | Length 5.0m | Safety railing for stairs and balconies. |
| **19367** | Balcony Railing Panel | Length 3.2m, Height 1.10m | Clean modern balcony and terrace safety barriers. |

---

## 4. Doors, Windows & Openings

| Model ID | Object Name / Description | Features |
|---|---|---|
| **1491** | Standard Wood / Glass Interior Door | Can be static or animated via MoveDynamicObject. |
| **1495** | Metal Security Door / Fire Door | For backdoors, server rooms, and utility exits. |
| **1497** | Glass Double Door | Modern entrance doors for offices, banks, and cafes. |
| **19379** | Modern Window Pane | Fits inside `19354` window cutout seamlessly. |
| **19856** | Sliding Modern Glass Door | Luxury patio / balcony transition door. |

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
