"""
Generate POS-200.step using FreeCAD/OCCT.
Body: 20.32 x 10.16 x 5.59 mm, centred at (0,0), Z from 0 to 5.59 mm
8 pins: 0.7 x 0.7 mm square, 3 mm below board
Pin positions from footprint pad centres.
"""

import sys
import os

# FreeCAD console mode imports
import FreeCAD
import Part

OUT = "/home/dmsmccann/Documents/ham_radio/Spectrum-Analyzer/vco-1stmixer/vco-1stmixer/vco-1stmixer-models/vco-1stmixer-3D/POS-200.step"

doc = FreeCAD.newDocument("POS200")

shapes = []

# ── Body ──────────────────────────────────────────────────────────────────────
# Body centred at X=0, Y=0; half-dimensions: 10.16, 5.08
body = Part.makeBox(20.32, 10.16, 5.59,
                    FreeCAD.Vector(-10.16, -5.08, 0.0))
shapes.append(body)

# ── Pins ──────────────────────────────────────────────────────────────────────
# 8 through-hole pins, 0.7 x 0.7 mm cross-section, from Z=-3.0 to Z=0
PIN_HALF = 0.35
PIN_BOT  = -3.0
PIN_TOP  =  0.0

pin_positions = [
    (-7.62,  2.54), (-2.54,  2.54), ( 2.54,  2.54), ( 7.62,  2.54),
    (-7.62, -2.54), (-2.54, -2.54), ( 2.54, -2.54), ( 7.62, -2.54),
]

for px, py in pin_positions:
    pin = Part.makeBox(
        2 * PIN_HALF, 2 * PIN_HALF, PIN_TOP - PIN_BOT,
        FreeCAD.Vector(px - PIN_HALF, py - PIN_HALF, PIN_BOT)
    )
    shapes.append(pin)

# ── Merge all into a compound and export ─────────────────────────────────────
compound = Part.makeCompound(shapes)

obj = doc.addObject("Part::Feature", "POS200")
obj.Shape = compound
doc.recompute()

Part.export([obj], OUT)

print("Written:", OUT)
