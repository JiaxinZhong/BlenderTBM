from mathutils import Vector
from core.materials import HoppingStyle
import core.colors as colors

# --- 配色 ---
color_site = (0.3, 0.3, 0.3, 1)

# Defined colors by hand
# c_red = (230/255, 75/255, 53/255, 1)
# c_blue = (77/255, 187/255, 213/255, 1)
# c_green = (0/255, 160/255, 135/255, 1)
# c_darkblue = (60/255, 84/255, 136/255, 1)
# hop_colors = [c_red, c_blue, c_green, c_darkblue]

# Define colors using color.py
hop_colors = [colors.NPG[0], colors.NPG[1], colors.NPG[2]]

# --- 晶格参数 ---
Nx, Ny, Nz = 5, 1, 1
dx, dy, dz = 5.0, 5.0, 5.0
site_rad = 0.5
hop_thickness = 0.12
arrow_size = 1.0
arc_height_scale = 1.5

# --- 规则生成函数 (因为需要引用材质) ---
def get_rules_and_legend(materials):
    hops = materials['hops'] # 这是一个材质列表
    # define styles
    hop_style = [
        HoppingStyle(hops[0], has_arrow=False, thickness=hop_thickness), 
        HoppingStyle(hops[1], has_arrow=True, thickness=hop_thickness),
        HoppingStyle(hops[2], has_arrow=True, thickness=hop_thickness),
    ]
    
    hop_rules = [
        # Rules: (Direction vector, Bending axis, Height scale, Material, Style)
        ((1,0,0), Vector((0,1,0)), 0, hop_style[0]),
        ((2,0,0), Vector((0,1,0)), 0.15, hop_style[1]),
        ((-2,0,0), Vector((0,-1,0)), 0.15, hop_style[2]),
    ]
    
    shift = Vector((0.1, 0.1, 0))
    legend = [
        (r"\kappa", hop_style[0], shift),
        (r"\kappa_+", hop_style[1], shift + Vector((0.3,0,0))),
        (r"\kappa_-", hop_style[2], shift),
    ]
    return hop_rules, legend

legend_settings = {
    'start_pos': Vector((1.5, -3.5, 0)),
    'cols': 3, 
    'row_spacing': 2.0,
    'col_spacing': 6,
    'line_length': 3.0
}
output_res_scale = 2
output_res = (1000*output_res_scale, 260*output_res_scale)
output_name = "1D_Range2"

camera_settings = {
    'scale': 1.15, # Control the orthogonal scale of the camera
    'shift': Vector((0,0.5,0)), # Optional shift of the target point
}