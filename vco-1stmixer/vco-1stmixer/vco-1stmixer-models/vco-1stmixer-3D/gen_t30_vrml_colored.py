"""
Generate T-30-6 toroid with 17-turn wire as VRML with embedded colors.

T-30-6 actual dimensions:
  Outer diameter: 6/16" = 9.525 mm
  Inner hole diameter: 4/16" = 6.35 mm
  Height: 5/16" ≈ 7.94 mm

VRML allows material properties (including RGB colors) to be embedded in the file.
- Toroid core: Yellow (1.0, 0.9, 0.0)
- Wire: Red (1.0, 0.0, 0.0)

This ensures colors are preserved when imported into KiCad.
"""

import FreeCAD
import Part
import math

OUT_VRML = "/home/dmsmccann/Documents/ham_radio/Spectrum-Analyzer/vco-1stmixer/vco-1stmixer/vco-1stmixer-models/vco-1stmixer-3D/T-30-6-wound-colored.wrl"

doc = FreeCAD.newDocument("ToroidColored")

# ── Toroid Core ───────────────────────────────────────────────────────────────
# Previous size was still too large, so shrink all dimensions to 25%.
# Original toroid: OD 9.525 mm, ID 6.35 mm
# New toroid: OD 2.38125 mm, ID 1.5875 mm
# Major radius R + minor radius r = 1.190625 mm
# Major radius R - minor radius r = 0.79375 mm
MAJOR_RADIUS = 0.9921875   # mm (center of tube to toroid center)
MINOR_RADIUS = 0.1984375   # mm (tube cross-section radius)

toroid = Part.makeTorus(MAJOR_RADIUS, MINOR_RADIUS)
obj_core = doc.addObject("Part::Feature", "ToroidCore")
obj_core.Shape = toroid

# ── Wire Winding: 17 turns of #28 wire ─────────────────────────────────────────
# Keep the winding visually slimmer so it does not overpower the toroid core.
wire_radius = 0.025

turns = 17
num_points = turns * 32  # points per turn

wire_shapes = []

for i in range(num_points):
    theta = (i / num_points) * turns * 2 * math.pi
    z_offset = (i / num_points) * MINOR_RADIUS * 1.2
    z_offset = max(-MINOR_RADIUS, min(MINOR_RADIUS, z_offset - MINOR_RADIUS))
    
    major_x = (MAJOR_RADIUS + MINOR_RADIUS * math.cos(z_offset / MINOR_RADIUS)) * math.cos(theta)
    major_y = (MAJOR_RADIUS + MINOR_RADIUS * math.cos(z_offset / MINOR_RADIUS)) * math.sin(theta)
    major_z = MINOR_RADIUS * math.sin(z_offset / MINOR_RADIUS)
    
    pt = FreeCAD.Vector(major_x, major_y, major_z)
    sphere = Part.makeSphere(wire_radius, pt)
    wire_shapes.append(sphere)

# Fuse wire segments
wire_solid = wire_shapes[0]
for s in wire_shapes[1:]:
    try:
        wire_solid = wire_solid.fuse(s)
    except:
        pass

obj_wire = doc.addObject("Part::Feature", "Wire")
obj_wire.Shape = wire_solid

doc.recompute()

# ── Export as VRML with manual color injection ─────────────────────────────────
# Convert shapes to meshes directly
obj_core.Shape.tessellate(0.1)
obj_wire.Shape.tessellate(0.1)

# Write VRML manually with color nodes
with open(OUT_VRML, 'w') as f:
    f.write("#VRML V2.0 utf8\n\n")
    f.write("# T-30-6 Toroid with 17-turn wire winding\n")
    f.write("# Yellow toroid core, Red wire\n\n")
    
    # ── Toroid Core (Yellow) ──────────────────────────────────────────────────
    f.write("Shape {\n")
    f.write("  appearance Appearance {\n")
    f.write("    material Material {\n")
    f.write("      ambientIntensity 0.3\n")
    f.write("      diffuseColor 1.0 0.9 0.0\n")  # Yellow
    f.write("      specularColor 0.8 0.8 0.8\n")
    f.write("      shininess 0.2\n")
    f.write("      transparency 0.0\n")
    f.write("    }\n")
    f.write("  }\n")
    f.write("  geometry IndexedFaceSet {\n")
    f.write("    coord Coordinate {\n")
    f.write("      point [\n")
    
    facets = obj_core.Shape.tessellate(0.1)
    vertices_core = []
    for vert in facets[0]:
        f.write(f"        {vert[0]} {vert[1]} {vert[2]},\n")
        vertices_core.append(vert)
    
    f.write("      ]\n")
    f.write("    }\n")
    f.write("    coordIndex [\n")
    
    for tri in facets[1]:
        if len(tri) == 3:
            f.write(f"      {tri[0]} {tri[1]} {tri[2]} -1,\n")
    
    f.write("    ]\n")
    f.write("  }\n")
    f.write("}\n\n")
    
    # ── Wire (Red) ────────────────────────────────────────────────────────────
    f.write("Shape {\n")
    f.write("  appearance Appearance {\n")
    f.write("    material Material {\n")
    f.write("      ambientIntensity 0.3\n")
    f.write("      diffuseColor 1.0 0.0 0.0\n")  # Red
    f.write("      specularColor 0.8 0.8 0.8\n")
    f.write("      shininess 0.2\n")
    f.write("      transparency 0.0\n")
    f.write("    }\n")
    f.write("  }\n")
    f.write("  geometry IndexedFaceSet {\n")
    f.write("    coord Coordinate {\n")
    f.write("      point [\n")
    
    facets_wire = obj_wire.Shape.tessellate(0.1)
    for vert in facets_wire[0]:
        f.write(f"        {vert[0]} {vert[1]} {vert[2]},\n")
    
    f.write("      ]\n")
    f.write("    }\n")
    f.write("    coordIndex [\n")
    
    for tri in facets_wire[1]:
        if len(tri) == 3:
            f.write(f"      {tri[0]} {tri[1]} {tri[2]} -1,\n")
    
    f.write("    ]\n")
    f.write("  }\n")
    f.write("}\n")

print(f"Written VRML with colors: {OUT_VRML}")
print(f"Toroid core: Yellow (RGB 1.0, 0.9, 0.0)")
print(f"Wire: Red (RGB 1.0, 0.0, 0.0)")

