"""
Generate T-30-6 toroid core with 17-turn #28 enameled wire winding.

T-30-6 standard dimensions:
  Outer diameter: 7.62 mm (0.300")
  Inner hole diameter: 4.06 mm (0.160")
  Height (thickness): 5.08 mm (0.200")
  Material: Permalloy 6 (yellow)

#28 enameled wire: ~0.32 mm diameter

Modeled as:
  - Toroid solid (yellow)
  - 17 turns of #28 wire wound around the toroid (red, swept circle along helical path)
"""

import FreeCAD
import Part
import math
import sys
import os

OUT_CORE = "/home/dmsmccann/Documents/ham_radio/Spectrum-Analyzer/vco-1stmixer/vco-1stmixer/vco-1stmixer-models/vco-1stmixer-3D/T-30-6.step"
OUT_WOUND = "/home/dmsmccann/Documents/ham_radio/Spectrum-Analyzer/vco-1stmixer/vco-1stmixer/vco-1stmixer-models/vco-1stmixer-3D/T-30-6-wound.step"

doc = FreeCAD.newDocument("Toroid")

# ── T-30-6 Toroid Core ────────────────────────────────────────────────────────
# Standard dimensions
MAJOR_RADIUS = (7.62 / 2)  # outer D / 2 = 3.81 mm center-to-center
MINOR_RADIUS = 2.54        # (7.62 - 4.06) / 2 = cross-section radius

# Torus with minor radius 2.54 mm and major radius 3.81 mm
# FreeCAD Part.makeTorus(radius1, radius2, pnt, dir, angle)
# where radius1 is major (distance to center of tube), radius2 is minor (tube radius)
toroid = Part.makeTorus(MAJOR_RADIUS, MINOR_RADIUS)

obj_core = doc.addObject("Part::Feature", "ToroidCore")
obj_core.Shape = toroid
doc.recompute()

# Export core only
Part.export([obj_core], OUT_CORE)
print(f"Written (core only): {OUT_CORE}")

# ── Wire Winding: 17 turns of #28 wire ────────────────────────────────────────
# Wire diameter approximated as swept cylinder around toroid
wire_radius = 0.32 / 2  # #28 wire is ~0.32 mm diameter, so 0.16 mm radius

# Build 17 circular cross-sections positioned along a helix on the toroid surface
turns = 17
num_points = turns * 32  # ~32 points per turn for smooth spiral

wire_shapes = []

for i in range(num_points):
    # Parameter along the helix: goes from 0 to turns*2*pi
    theta = (i / num_points) * turns * 2 * math.pi  # angle around toroid center
    # Height variation creates the 17-turn pitch
    z_offset = (i / num_points) * MINOR_RADIUS * 2  # spread across toroid height
    # Clamp to prevent overshoot
    z_offset = max(-MINOR_RADIUS, min(MINOR_RADIUS, z_offset - MINOR_RADIUS))
    
    # Center of this wire cross-section on the toroid surface
    # Torus surface point: major circle + minor circle offset
    major_x = (MAJOR_RADIUS + MINOR_RADIUS * math.cos(z_offset / MINOR_RADIUS)) * math.cos(theta)
    major_y = (MAJOR_RADIUS + MINOR_RADIUS * math.cos(z_offset / MINOR_RADIUS)) * math.sin(theta)
    major_z = MINOR_RADIUS * math.sin(z_offset / MINOR_RADIUS)
    
    pt = FreeCAD.Vector(major_x, major_y, major_z)
    
    # Create a small sphere at this position (represents wire cross-section)
    sphere = Part.makeSphere(wire_radius, pt)
    wire_shapes.append(sphere)

# Fuse all wire segments into continuous winding
if wire_shapes:
    wire_compound = Part.makeCompound(wire_shapes)
    # Try to fuse for visual continuity (slow, but looks better)
    try:
        wire_solid = wire_shapes[0]
        for s in wire_shapes[1:]:
            wire_solid = wire_solid.fuse(s)
    except:
        wire_solid = wire_compound

    obj_wire = doc.addObject("Part::Feature", "Wire")
    obj_wire.Shape = wire_solid
    doc.recompute()

# ── Combined model: toroid + wire ─────────────────────────────────────────────
combined = Part.makeCompound([toroid, wire_solid])
obj_combined = doc.addObject("Part::Feature", "ToroidWound")
obj_combined.Shape = combined
doc.recompute()

Part.export([obj_combined], OUT_WOUND)
print(f"Written (toroid + 17-turn wire): {OUT_WOUND}")

# ── Variant: export core and wire separately (for coloring in KiCad) ──────────
# Compound with both shapes
Part.export([obj_core, obj_wire], OUT_WOUND)
print(f"Exported as compound: {OUT_WOUND}")

print("Done.")
