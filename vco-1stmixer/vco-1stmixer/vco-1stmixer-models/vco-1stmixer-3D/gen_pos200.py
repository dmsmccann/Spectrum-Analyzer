#!/usr/bin/env python3
"""
Generate STEP AP214 3D model for Mini-Circuits POS-200+ VCO.

Package dimensions from footprint & datasheet:
  Body: 20.32mm x 10.16mm x 5.59mm (0.800" x 0.400" x 0.220")
  8 through-hole pins in 2 rows of 4, 5.08mm (0.200") pitch
  Pin positions: X = -7.62, -2.54, 2.54, 7.62  /  Y = +2.54, -2.54
"""

import sys
import os

entities = {}   # id -> string
_id = [0]

def E(content):
    _id[0] += 1
    entities[_id[0]] = content
    return _id[0]

# ── Primitive geometry helpers ────────────────────────────────────────────────

def cp(x, y, z):
    return E(f"CARTESIAN_POINT('',({x:.6f},{y:.6f},{z:.6f}))")

def direction(dx, dy, dz):
    return E(f"DIRECTION('',({dx:.6f},{dy:.6f},{dz:.6f}))")

def vertex(cp_id):
    return E(f"VERTEX_POINT('',#{cp_id})")

def line(pt_id, dir_id):
    return E(f"LINE('',#{pt_id},VECTOR('',#{dir_id},1.0))")

def edge_curve(v1, v2, curve, same_sense=".T."):
    return E(f"EDGE_CURVE('',#{v1},#{v2},#{curve},{same_sense})")

def oriented_edge(ec, sense=".T."):
    return E(f"ORIENTED_EDGE('',*,*,#{ec},{sense})")

def edge_loop(oe_list):
    refs = ",".join(f"#{o}" for o in oe_list)
    return E(f"EDGE_LOOP('',({refs}))")

def face_outer_bound(el):
    return E(f"FACE_OUTER_BOUND('',#{el},.T.)")

def axis2(pt, norm, ref):
    return E(f"AXIS2_PLACEMENT_3D('',#{pt},#{norm},#{ref})")

def plane(ax):
    return E(f"PLANE('',#{ax})")

def advanced_face(fob, surf, sense=".T."):
    return E(f"ADVANCED_FACE('',(#{fob}),#{surf},{sense})")

def closed_shell(face_list):
    refs = ",".join(f"#{f}" for f in face_list)
    return E(f"CLOSED_SHELL('',({refs}))")

def manifold_solid_brep(name, shell):
    return E(f"MANIFOLD_SOLID_BREP('{name}',#{shell})")

# ── Box solid builder ─────────────────────────────────────────────────────────
# Vertices:  p0=(x0,y0,z0) p1=(x1,y0,z0) p2=(x1,y1,z0) p3=(x0,y1,z0)
#            p4=(x0,y0,z1) p5=(x1,y0,z1) p6=(x1,y1,z1) p7=(x0,y1,z1)
#
# Edge naming: e_b0..e_b3 (bottom ring), e_t0..e_t3 (top ring), e_v0..e_v3 (vertical)
# All normals verified with cross-product rule.

def make_box(x0, y0, z0, x1, y1, z1, name="box"):
    c = [cp(x0,y0,z0), cp(x1,y0,z0), cp(x1,y1,z0), cp(x0,y1,z0),
         cp(x0,y0,z1), cp(x1,y0,z1), cp(x1,y1,z1), cp(x0,y1,z1)]
    v = [vertex(c[i]) for i in range(8)]

    # Reusable directions
    dx = direction(1,0,0); dy = direction(0,1,0); dz = direction(0,0,1)

    # Bottom ring edges
    e_b0 = edge_curve(v[0],v[1], line(c[0],dx))  # p0→p1 +X
    e_b1 = edge_curve(v[1],v[2], line(c[1],dy))  # p1→p2 +Y
    e_b2 = edge_curve(v[3],v[2], line(c[3],dx))  # p3→p2 +X
    e_b3 = edge_curve(v[0],v[3], line(c[0],dy))  # p0→p3 +Y
    # Top ring edges
    e_t0 = edge_curve(v[4],v[5], line(c[4],dx))  # p4→p5 +X
    e_t1 = edge_curve(v[5],v[6], line(c[5],dy))  # p5→p6 +Y
    e_t2 = edge_curve(v[7],v[6], line(c[7],dx))  # p7→p6 +X
    e_t3 = edge_curve(v[4],v[7], line(c[4],dy))  # p4→p7 +Y
    # Vertical edges
    e_v0 = edge_curve(v[0],v[4], line(c[0],dz))  # p0→p4 +Z
    e_v1 = edge_curve(v[1],v[5], line(c[1],dz))  # p1→p5 +Z
    e_v2 = edge_curve(v[2],v[6], line(c[2],dz))  # p2→p6 +Z
    e_v3 = edge_curve(v[3],v[7], line(c[3],dz))  # p3→p7 +Z

    face_ids = []

    # Bottom (z=z0, normal -Z): loop p0→p3→p2→p1
    el = edge_loop([oriented_edge(e_b3,".T."), oriented_edge(e_b2,".T."),
                    oriented_edge(e_b1,".F."), oriented_edge(e_b0,".F.")])
    face_ids.append(advanced_face(face_outer_bound(el),
                                  plane(axis2(c[0], direction(0,0,-1), direction(1,0,0)))))

    # Top (z=z1, normal +Z): loop p4→p5→p6→p7
    el = edge_loop([oriented_edge(e_t0,".T."), oriented_edge(e_t1,".T."),
                    oriented_edge(e_t2,".F."), oriented_edge(e_t3,".F.")])
    face_ids.append(advanced_face(face_outer_bound(el),
                                  plane(axis2(c[4], direction(0,0,1), direction(1,0,0)))))

    # Front (y=y0, normal -Y): loop p0→p1→p5→p4
    el = edge_loop([oriented_edge(e_b0,".T."), oriented_edge(e_v1,".T."),
                    oriented_edge(e_t0,".F."), oriented_edge(e_v0,".F.")])
    face_ids.append(advanced_face(face_outer_bound(el),
                                  plane(axis2(c[0], direction(0,-1,0), direction(1,0,0)))))

    # Back (y=y1, normal +Y): loop p2→p3→p7→p6
    el = edge_loop([oriented_edge(e_b2,".F."), oriented_edge(e_v3,".T."),
                    oriented_edge(e_t2,".T."), oriented_edge(e_v2,".F.")])
    face_ids.append(advanced_face(face_outer_bound(el),
                                  plane(axis2(c[3], direction(0,1,0), direction(-1,0,0)))))

    # Left (x=x0, normal -X): loop p0→p4→p7→p3
    el = edge_loop([oriented_edge(e_v0,".T."), oriented_edge(e_t3,".T."),
                    oriented_edge(e_v3,".F."), oriented_edge(e_b3,".F.")])
    face_ids.append(advanced_face(face_outer_bound(el),
                                  plane(axis2(c[0], direction(-1,0,0), direction(0,1,0)))))

    # Right (x=x1, normal +X): loop p1→p2→p6→p5
    el = edge_loop([oriented_edge(e_b1,".T."), oriented_edge(e_v2,".T."),
                    oriented_edge(e_t1,".F."), oriented_edge(e_v1,".F.")])
    face_ids.append(advanced_face(face_outer_bound(el),
                                  plane(axis2(c[1], direction(1,0,0), direction(0,1,0)))))

    shell = closed_shell(face_ids)
    brep  = manifold_solid_brep(name, shell)
    return brep, face_ids

# ── Build model geometry ──────────────────────────────────────────────────────

# POS-200+ body: 20.32 x 10.16 x 5.59 mm, centered at (0,0), Z from 0 to 5.59
body_brep, body_faces = make_box(-10.16, -5.08, 0.0,  10.16,  5.08, 5.59, "body")

# 8 through-hole pins: 0.7 x 0.7 mm cross-section, 3mm below board
# Positions match footprint pad centres
PIN_XS = 0.35   # half side of pin cross-section
PIN_Z  = -3.0   # how far pins extend below PCB

pin_positions = [
    (-7.62,  2.54), (-2.54,  2.54), ( 2.54,  2.54), ( 7.62,  2.54),
    (-7.62, -2.54), (-2.54, -2.54), ( 2.54, -2.54), ( 7.62, -2.54),
]

pin_breps = []
pin_face_lists = []
for i, (px, py) in enumerate(pin_positions):
    b, f = make_box(px-PIN_XS, py-PIN_XS, PIN_Z,
                    px+PIN_XS, py+PIN_XS, 0.0, f"pin{i+1}")
    pin_breps.append(b)
    pin_face_lists.append(f)

geometry_done_at = _id[0]   # last entity ID used for geometry

# ── Presentation / colour ─────────────────────────────────────────────────────

def colour_rgb(name, r, g, b):
    return E(f"COLOUR_RGB('{name}',{r},{g},{b})")

def psa(surface_style_usage_id, curve_style_id):
    return E(f"PRESENTATION_STYLE_ASSIGNMENT(({surface_style_usage_id},{curve_style_id}))")

def make_colour_style(name, r, g, b):
    """Return (PRESENTATION_STYLE_ASSIGNMENT id, COLOUR_RGB id)."""
    col       = colour_rgb(name, r, g, b)
    font      = E("DRAUGHTING_PRE_DEFINED_CURVE_FONT('continuous')")
    fill_col  = E(f"FILL_AREA_STYLE_COLOUR('',#{col})")
    fill_area = E(f"FILL_AREA_STYLE('',(#{fill_col}))")
    sfa       = E(f"SURFACE_STYLE_FILL_AREA(#{fill_area})")
    side_sty  = E(f"SURFACE_SIDE_STYLE('',(#{sfa}))")
    ssu       = E(f"SURFACE_STYLE_USAGE(.BOTH.,#{side_sty})")
    crv_sty   = E(f"CURVE_STYLE('',#{font},POSITIVE_LENGTH_MEASURE(0.1),#{col})")
    return E(f"PRESENTATION_STYLE_ASSIGNMENT((#{ssu},#{crv_sty}))"), col

# Body colour: dark charcoal / near-black (Mini-Circuits black moulded body)
body_psa, _ = make_colour_style("Body", 0.15, 0.15, 0.15)

# Pin colour: tin/silver
pin_psa, _  = make_colour_style("Pin", 0.85, 0.85, 0.90)

# STYLED_ITEM for each face
styled_items = []

for fid in body_faces:
    sid = E(f"STYLED_ITEM('',(#{body_psa}),#{fid})")
    styled_items.append(sid)

for flist in pin_face_lists:
    for fid in flist:
        sid = E(f"STYLED_ITEM('',(#{pin_psa}),#{fid})")
        styled_items.append(sid)

# ── AP214 boilerplate ─────────────────────────────────────────────────────────

app_ctx  = E("APPLICATION_CONTEXT('Core Data for Automotive Mechanical Design Process')")
_        = E(f"APPLICATION_PROTOCOL_DEFINITION('international standard','automotive_design',2003,#{app_ctx})")
prod_ctx = E(f"PRODUCT_CONTEXT('3D Mechanical Parts',#{app_ctx},'mechanical')")
prod     = E(f"PRODUCT('POS-200','POS-200 VCO','',(#{prod_ctx}))")
_        = E("PRODUCT_CATEGORY('part','')")
_        = E(f"PRODUCT_RELATED_PRODUCT_CATEGORY('','',(#{prod}))")
pdef_ctx = E(f"PRODUCT_DEFINITION_CONTEXT('3D Mechanical Parts',#{app_ctx},'design')")
pdef_frm = E(f"PRODUCT_DEFINITION_FORMATION('1.0','first version',#{prod})")
pdef     = E(f"PRODUCT_DEFINITION('design','',#{pdef_frm},#{pdef_ctx})")
pdef_shp = E(f"PRODUCT_DEFINITION_SHAPE('','',#{pdef})")

# Geometric context (millimetres, degrees)
uncert   = E("UNCERTAINTY_MEASURE_WITH_UNIT(LENGTH_MEASURE(1.E-005),#mm_unit_placeholder,'DISTANCE_ACCURACY_VALUE','Maximum model space distance between geometric entities at asserted connectivities')")
mm_unit  = E("(LENGTH_UNIT() NAMED_UNIT(*) SI_UNIT(.MILLI.,.METRE.))")
dim_exp  = E("DIMENSIONAL_EXPONENTS(0.,0.,0.,0.,0.,0.,0.)")
rad_unit = E("(NAMED_UNIT(*) PLANE_ANGLE_UNIT() SI_UNIT($,.RADIAN.))")
deg_meas = E(f"MEASURE_WITH_UNIT(PLANE_ANGLE_MEASURE(0.01745329252),#{rad_unit})")
ang_unit = E(f"(CONVERSION_BASED_UNIT('degree',#{deg_meas}) NAMED_UNIT(#{dim_exp}) PLANE_ANGLE_UNIT())")
sol_unit = E("(NAMED_UNIT(*) SI_UNIT($,.STERADIAN.) SOLID_ANGLE_UNIT())")
uncert2  = E(f"UNCERTAINTY_MEASURE_WITH_UNIT(LENGTH_MEASURE(1.E-005),#{mm_unit},'DISTANCE_ACCURACY_VALUE','Maximum model space distance between geometric entities at asserted connectivities')")

geom_ctx_str = (
    f"(GEOMETRIC_REPRESENTATION_CONTEXT(3) "
    f"GLOBAL_UNCERTAINTY_ASSIGNED_CONTEXT((#{uncert2})) "
    f"GLOBAL_UNIT_ASSIGNED_CONTEXT((#{mm_unit},#{ang_unit},#{sol_unit})) "
    f"REPRESENTATION_CONTEXT('ID1','3D'))"
)
geom_ctx = E(geom_ctx_str)

# All solid items in shape representation
all_brep_refs = ",".join(f"#{b}" for b in [body_brep] + pin_breps)
shape_repr = E(f"SHAPE_REPRESENTATION('',({all_brep_refs}),#{geom_ctx})")

shape_def_repr = E(f"SHAPE_DEFINITION_REPRESENTATION(#{pdef_shp},#{shape_repr})")

# Mechanical design geometric presentation representation
all_styled_refs = ",".join(f"#{s}" for s in styled_items)
mech_pres = E(f"MECHANICAL_DESIGN_GEOMETRIC_PRESENTATION_REPRESENTATION($,({all_styled_refs}),#{geom_ctx})")

# ── Write output file ─────────────────────────────────────────────────────────

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "POS-200.step")

with open(out_path, "w") as f:
    f.write("ISO-10303-21;\n")
    f.write("HEADER;\n")
    f.write("FILE_DESCRIPTION(('STEP AP214 - Mini-Circuits POS-200+ VCO'),'1');\n")
    f.write("FILE_NAME('POS-200','2026-05-10T00:00:00',(''),(''),'gen_pos200.py','','');\n")
    f.write("FILE_SCHEMA(('AUTOMOTIVE_DESIGN'));\n")
    f.write("ENDSEC;\n")
    f.write("DATA;\n")

    for eid in sorted(entities.keys()):
        content = entities[eid]
        # Fix up placeholder
        content = content.replace("#mm_unit_placeholder", f"#{mm_unit}")
        f.write(f"#{eid}={content};\n")

    f.write("ENDSEC;\n")
    f.write("END-ISO-10303-21;\n")

print(f"Written: {out_path}")
print(f"Total entities: {_id[0]}")
