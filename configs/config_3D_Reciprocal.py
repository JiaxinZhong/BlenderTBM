from mathutils import Vector
from core.materials import HoppingStyle

color_site = (0.3, 0.3, 0.3, 1)
hop_colors = [
    (230/255, 75/255, 53/255, 1),             # 1. 朱红 (Red) - 强调色
    (77/255, 187/255, 213/255, 1),            # 2. 湖蓝 (Blue) - 强调色
    (0/255, 160/255, 135/255, 1),             # 3. 翠绿 (Green) - 常用对比
    (60/255, 84/255, 136/255, 1),             # 4. 深蓝 (Dark Blue)
    (243/255, 155/255, 127/255, 1),           # 5. 浅鲑红 (Light Red)
]

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
    
    # rules = [
    #     ((1,0,0), Vector((0,0,1)), 0.0, s_x),
    #     ((1,1,0), Vector((0,0,1)), 0.0, s_y),
    # ]
    hopping_rules = [
        # Rules: (Direction vector, Bending axis, Height scale, Material, Has arrow)
        ( (1, 0, 0), Vector((0, 0, 1)), 0.0, hop_style[0] ),
        ( (0, 1, 0), Vector((0, 0, 1)), 0.0, hop_style[1] ),
        ( (0, 0, 1), Vector((0, 0, 1)), 0.0, hop_style[2] ),
        ( (1, 1, 1), Vector((0, 0, 1)), 0.0, hop_style[3] ),
        ( (1, -1, 1), Vector((0, 0, 1)), 0.0, hop_style[4] ),
    ]
    
    legend_latex_shift = Vector((0.1, 0.1, 0))
    # legend = [
    #     (r"\kappa_x", s_x, shift),
    #     (r"\kappa_y", s_y, shift),
    # ]
    legend = [
        (r"\kappa_x", hop_style[0], legend_latex_shift),
        (r"\kappa_y", hop_style[1], legend_latex_shift),
        (r"\kappa_z", hop_style[2], legend_latex_shift),
        (r"\kappa_\mathrm{d}", hop_style[3], legend_latex_shift),
        (r"\kappa_\mathrm{a}", hop_style[4], legend_latex_shift),
    ]
    return hopping_rules, legend

# legend_settings = {
#     'start_pos': Vector((0.5, -2, 0)),
#     'cols': 2, 'row_spacing': 2.0, 'col_spacing': 5.0, 'line_length': 3.0
# }
legend_settings = {
    'start_pos': Vector((0.5, -2, 0)),
    'cols': 3, # Number of columns
    'row_spacing': 2.0,
    'col_spacing': 5.0,
    'line_length': 3.0,
}
output_res = (900, 900)
output_name = "3D_Reciprocal"