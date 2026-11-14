# 3D Coordinate Math & Snapping Algorithms for SA-MP Architecture

In SA-MP, objects are placed via world coordinates `(x, y, z)` and Euler rotations `(rx, ry, rz)` in degrees:
- `rx`: Pitch (rotation around X axis)
- `ry`: Roll (rotation around Y axis)
- `rz`: Yaw (rotation around Z axis / compass heading)

---

## 1. The Golden SA-MP Modular Grid Standards

Extracted directly from collision bounding boxes in `modelsizes.db`:
- **Single-Bay Unit**: `3.211m` width, `3.500m` height, `0.172m` thickness (`19353`)
- **Half-Bay Unit**: `1.601m` width (`19426`)
- **Triple-Bay Unit**: `9.633m` width (`19445`, `19448`)
- **Triple-Height 3-Story Unit**: `10.500m` height (`19377`)
- **Structural Concrete Grid**:
  - `18762` (`Concrete1mx1mx5m`): 1.0m x 1.0m x 5.0m
  - `18766` (`Concrete10mx1mx5m`): 10.0m x 1.0m x 5.0m
  - `18765` (`Concrete10mx10mx5m`): 10.0m x 10.0m x 5.0m

All building layouts should snap to multiples of **`3.211m`** (or `1.601m` for tight rooms) and vertical story heights of **`3.500m`**. This guarantees 100% airtight seams and mathematically zero Z-fighting.

---

## 2. Local-to-World Coordinate Transformation

When designing a room or building, it is vastly easier to design in **Local Space** (where `(0, 0, 0)` is the center or corner of the building and `+Y` is forward) and then project every object into **World Space** with arbitrary position `(WX, WY, WZ)` and rotation `Heading` (degrees).

### 2D Rotation (Yaw around Z):
Given local coordinates `(lx, ly)` and world heading `θ` (in radians):
```text
world_x = WX + (lx * cos(θ) - ly * sin(θ))
world_y = WY + (lx * sin(θ) + ly * cos(θ))
world_z = WZ + lz
world_rz = (local_rz + heading_deg) % 360.0
```

> **IMPORTANT**: SA-MP uses a counter-clockwise coordinate rotation. In Python:
> `rad = math.radians(heading_deg)`
> `cos_a = math.cos(rad)`
> `sin_a = math.sin(rad)`

---

## 3. Wall Segment Snapping Formulas

### Placing a Straight Wall of Length `TotalLength`:
To span a distance `TotalLength` along direction angle `θ`:
1. Use triple-bay panels `19445` (9.633m) for long spans: `N_triple = int(TotalLength / 9.633)`
2. Remainder is filled with single-bay `19353` (3.211m): `N_single = int((TotalLength % 9.633) / 3.211)`
3. Any small remaining fraction is closed with half-bay `19426` (1.601m).

### Airtight 90-Degree Corner Joints:
To avoid gaps or overlapping glitching textures (Z-fighting) at corners:
- Outer corner offset adjustment:
  `Corner_X = Outer_Boundary - (Wall_Thickness / 2.0)` where `Wall_Thickness = 0.172m`.
- Or place corner wall `19356` or structural column `18762` (`1.0m x 1.0m`) centered at the vertex.

---

## 4. Normal Offset Rule for Zero Z-Fighting Overlays

When applying wainscoting, wall slat screens (`19939`), signboards (`19482`), or poster decals (`18066`) over solid walls or floors:
- **Surface Normal Vector**: `n = (cos(θ + 90°), sin(θ + 90°))`
- **Offset Distance**: `d = +0.025m` to `+0.035m` (Never place at `0.000m` offset, which produces flickering Z-fighting).
- Position of overlay object:
  `overlay_x = wall_x + d * cos(rad + π/2)`
  `overlay_y = wall_y + d * sin(rad + π/2)`
  `overlay_z = wall_z`

---

## 5. Staircase Rise & Run Calculation

Modular staircase `19364` is designed for:
- Standard floor rise: `ΔZ = 3.500m` (exact match to `19353` wall height!)
- Horizontal run: `ΔY = 5.000m`
- Width: `1.800m`

Placement:
- Place base at bottom floor edge `(X_stair, Y_stair, Base_Z)`.
- Center point of staircase:
  `Z_center = Base_Z + (3.500 / 2.0) = Base_Z + 1.750m`
  `Y_center = Y_stair + (5.000 / 2.0) = Y_stair + 2.500m`
- Cut an opening in the upper ceiling slab of at least `2.0m x 4.0m` directly above the staircase so the player ped's head does not collide with the ceiling while walking up.

