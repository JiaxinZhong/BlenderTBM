from mathutils import Vector
from core.materials import HoppingStyle

color_site = (0.3, 0.3, 0.3, 1)
hop_colors = [
    (230/255, 75/255, 53/255, 1), 
    (77/255, 187/255, 213/255, 1)
]

Nx, Ny, Nz = 3, 3, 1
dx, dy, dz = 5.0, 5.0, 5.0
site_rad = 0.5
hop_thickness = 0.12
arrow_size = 1.0
arc_height_scale = 1.5

def get_rules_and_legend(materials):
    hops = materials['hops']
    s_x = HoppingStyle(hops[0], False, hop_thickness)
    s_y = HoppingStyle(hops[1], False, hop_thickness)
    
    rules = [
        ((1,0,0), Vector((0,0,1)), 0.0, s_x),
        ((1,1,0), Vector((0,0,1)), 0.0, s_y),
    ]
    
    shift = Vector((0.1, 0.1, 0))
    legend = [
        (r"\kappa_x", s_x, shift),
        (r"\kappa_y", s_y, shift),
    ]
    return rules, legend

legend_settings = {
    'start_pos': Vector((0.5, -2, 0)),
    'cols': 2, 'row_spacing': 2.0, 'col_spacing': 5.0, 'line_length': 3.0,
    'text_orient': (0, 0, 1), # Direction the text faces
}

camera_settings = {
    'scale': 1.25, # Control the orthogonal scale of the camera
    'shift': Vector((-1, 0, 0)), # Optional shift of the target point
}

axis_settings = {
    'show': True,           # Turn on/off
    'location': (-3, -3, 0),# Position (Left-Bottom corner usually looks best)
    'length': 2.5,          # Length of the axis
    'thickness': 0.08,       # Thickness of the shaft
    'text_orient': (0, 0, 1), # Direction the text faces
    'show_axes': ['x', 'y'],          # <--- 关键修改，不写 'z'
}

scale = 2
output_res = (900*scale, 900*scale)
output_name = "2D_Reciprocal"
