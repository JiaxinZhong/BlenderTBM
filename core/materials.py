import bpy

class HoppingStyle:
    """封装 Hopping 的视觉属性"""
    def __init__(self, material, has_arrow=True, thickness=0.12):
        self.mat = material
        self.arrow = has_arrow
        self.thickness = thickness

def create_material(name, color, roughness=0.3, metallic=0.0):
    """创建 Cycles 材质"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Metallic'].default_value = metallic
    return mat

def init_materials(config):
    """根据配置初始化所有材质，返回字典"""
    # 1. Site 材质
    mat_site = create_material("Site", config.color_site, roughness=0.3, metallic=1.0)
    
    # 2. Hopping 材质 (从配置的颜色列表中生成)
    # 假设配置里有 color_NPG 或 hop_colors
    mat_hops = []
    colors = getattr(config, 'hop_colors', [])
    for i, col in enumerate(colors):
        mat_hops.append(create_material(f"HopMat{i}", col, roughness=0.2, metallic=0.0))
        
    return {
        'site': mat_site,
        'hops': mat_hops
    }