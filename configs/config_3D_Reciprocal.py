from mathutils import Vector
from core.materials import HoppingStyle
import core.colors as colors

color_site = (0.3, 0.3, 0.3, 1)
hop_colors = [colors.NPG[i] for i in range(5)]

Nx, Ny, Nz = 3, 3, 3  # Number of sites in x, y, z directions
dx, dy, dz = 5.0, 5.0, 5.0
site_rad = 0.5
hop_thickness = 0.12
arrow_size = 1.0
arc_height_scale = 1.5

def get_rules_and_legend(materials):
    hop_mat = materials['hops']
    hop_style = [
        HoppingStyle(hop_mat[0], has_arrow=False, thickness=hop_thickness),
        HoppingStyle(hop_mat[1], has_arrow=False, thickness=hop_thickness),
        HoppingStyle(hop_mat[2], has_arrow=False, thickness=hop_thickness),
        HoppingStyle(hop_mat[3], has_arrow=False, thickness=hop_thickness),
        HoppingStyle(hop_mat[4], has_arrow=False, thickness=hop_thickness),
    ]
    
    hopping_rules = [
        # Rules: (Direction vector, Bending axis, Height scale, style)
        ( (1, 0, 0), Vector((0, 0, 1)), 0.0, hop_style[0] ),
        ( (0, 1, 0), Vector((0, 0, 1)), 0.0, hop_style[1] ),
        ( (0, 0, 1), Vector((0, 0, 1)), 0.0, hop_style[2] ),
        ( (1, 1, 1), Vector((0, 0, 1)), 0.0, hop_style[3] ),
        ( (1, -1, 1), Vector((0, 0, 1)), 0.0, hop_style[4] ),
    ]
    
    legend_latex_shift = Vector((-0.2, 0.1, 0))
    legend = [
        (r"\kappa_x", hop_style[0], legend_latex_shift),
        (r"\kappa_y", hop_style[1], legend_latex_shift),
        (r"\kappa_z", hop_style[2], legend_latex_shift),
        (r"\kappa_\mathrm{d}", hop_style[3], legend_latex_shift),
        (r"\kappa_\mathrm{a}", hop_style[4], legend_latex_shift),
    ]
    return hopping_rules, legend

legend_settings = {
    'start_pos': Vector((0.5, -2, 0)),
    'cols': 2, # Number of columns
    'row_spacing': 2.0, # Vertical spacing between rows
    'col_spacing': 5.2, # Horizontal spacing between columns
    'text_orient': (0, -1, 0), # Direction the text faces
    'line_length': 3.0, # Length of the line in each legend entry
}

camera_settings = {
    'scale': 1.6, # Control the orthogonal scale of the camera
    'cam_loc': Vector((10.17,-21.3,18.87)), # Custom camera location
    'shift': Vector((0,-0.5,-0.5)), # Optional shift of the target point
}

axis_settings = {
    'show': True,           # Turn on/off
    'location': (-3, -3, 0),# Position (Left-Bottom corner usually looks best)
    'length': 2.5,          # Length of the axis
    'thickness': 0.08,       # Thickness of the shaft
    'text_orient': (0, -1, 0), # Direction the text faces
    'show_axes': ['x', 'y', 'z'],          # <--- 关键修改，不写 'z'
}

scale = 2
output_res = (900*scale, 900*scale)
output_name = "3D_Reciprocal"
