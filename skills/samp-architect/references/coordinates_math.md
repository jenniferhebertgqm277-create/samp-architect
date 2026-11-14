# 3D Coordinate Math & Snapping Algorithms for SA-MP Architecture

In SA-MP, objects are placed via world coordinates `(x, y, z)` and Euler rotations `(rx, ry, rz)` in degrees:
- `rx`: Pitch (rotation around X axis)
- `ry`: Roll (rotation around Y axis)
- `rz`: Yaw (rotation around Z axis / compass heading)

---

## 1. Local-to-World Coordinate Transformation

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

## 2. Wall Segment Snapping Formulas

Standard modular wall `19353` has length `L = 3.20m` along its local Y-axis and thickness `T = 0.17m` along its local X-axis.

### Placing a Straight Wall of Length `TotalLength`:
To span a distance `TotalLength` along direction angle `θ`:
1. Number of full panels: `N = int(TotalLength / 3.20)`
2. Remainder distance: `Rem = TotalLength - (N * 3.20)`
3. For each panel `i` from `0` to `N-1`:
   - Offset along wall line: `s = (i + 0.5) * 3.20`
   - Position:
     `px = start_x + s * cos(θ)`
     `py = start_y + s * sin(θ)`
     `pz = floor_z + (WallHeight / 2.0)`
     `rot_z = math.degrees(θ)`

### Seamless 90-Degree Corner Joints:
To avoid gaps or overlapping glitching textures (Z-fighting) at corners:
- Outer corner offset adjustment:
  `Corner_X = Outer_Boundary - (Wall_Thickness / 2.0)`
- Or place modular corner column `19356` or square pillar `19363` centered at the exact vertex `(Corner_X, Corner_Y)` with dimension `0.40m x 0.40m`.

---

## 3. Floor and Ceiling Slab Grid Calculation

For a room of width `W` and depth `D`:
- Grid step for `19359` (standard slab): `Step = 3.20m`
- Grid step for `19360` (large slab): `Step = 5.00m`
- For floor: `Z = Base_Z + 0.10m`
- For ceiling: `Z = Base_Z + Story_Height - 0.10m`
- Upper floor: `Z = Base_Z + Story_Height + 0.10m`

---

## 4. Staircase Rise & Run Calculation

Modular staircase `19364` is designed for:
- Standard floor rise: `ΔZ = 3.50m`
- Horizontal run: `ΔY = 5.00m`
- Width: `1.80m`

Placement:
- Place base at bottom floor edge `(X_stair, Y_stair, Base_Z)`.
- Center point of staircase:
  `Z_center = Base_Z + (3.50 / 2.0) = Base_Z + 1.75m`
  `Y_center = Y_stair + (5.00 / 2.0) = Y_stair + 2.50m`
- Cut an opening in the upper ceiling slab of at least `2.0m x 4.0m` directly above the staircase so the player ped's head does not collide with the ceiling while walking up.
