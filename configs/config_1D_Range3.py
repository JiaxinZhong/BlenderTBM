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
hop_colors = [colors.NPG[0], colors.NPG[1], colors.NPG[2], colors.NPG[3]]

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
    # 定义样式
    s1 = HoppingStyle(hops[0], True, hop_thickness) # Red
    s2 = HoppingStyle(hops[1], True, hop_thickness) # Blue
    s3 = HoppingStyle(hops[2], True, hop_thickness) # Green
    s4 = HoppingStyle(hops[3], True, hop_thickness) # DarkBlue
    
    rules = [
        ((1,0,0), Vector((0,1,0)), 0.08, s1),
        ((2,0,0), Vector((0,1,0)), 0.15, s2),
        ((3,0,0), Vector((0,1,0)), 0.2, s3),
        ((-1,0,0), Vector((0,-1,0)), 0.08, s3),
        ((-2,0,0), Vector((0,-1,0)), 0.15, s4),
        ((-3,0,0), Vector((0,-1,0)), 0.2, s1),
    ]
    
    shift = Vector((0.1, 0.1, 0))
    legend = [
        (r"2\alpha(1+\gamma)", s1, shift),
        (r"(1-\gamma)^2", s2, shift + Vector((0.3,0,0))),
        (r"2\alpha(1-\gamma)", s3, shift),
        (r"(1+\gamma)^2", s4, shift + Vector((0.3,0,0)))
    ]
    return rules, legend

legend_settings = {
    'start_pos': Vector((2.5, -5, 0)),
    'cols': 2, 'row_spacing': 2.0, 'col_spacing': 8.5, 'line_length': 3.0
}
output_res = (2000, 900)
output_name = "1D_Range3"

camera_settings = {
    'scale': 1.2, # Control the orthogonal scale of the camera
}