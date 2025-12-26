import bpy
import importlib
import sys
import os

# --- 动态重载模块 (开发必备) ---
def reload_modules():
    # 确保当前目录在 sys.path
    blend_path = bpy.data.filepath
    if blend_path:
        d = os.path.dirname(blend_path)
        if d not in sys.path: sys.path.append(d)

    import core.utils as utils
    import core.materials as mat
    import core.geometry as geo
    import core.legend as leg
    import core.render as ren
    
    # 强制重载
    importlib.reload(utils)
    importlib.reload(mat)
    importlib.reload(geo)
    importlib.reload(leg)
    importlib.reload(ren)
    return utils, mat, geo, leg, ren

def run():
    # 1. Load core modules
    utils, mat, geo, leg, ren = reload_modules()
    
    # ------------------------------------------------------------
    # Select Configuration File here.
    #   - The configuration file is located in the "configs" folder.
    # ------------------------------------------------------------
    
    # ==========================================
    # 2. Safely Load Configuration
    # ==========================================
    
    # The configuration name to load (corresponds to the filename in 'configs/')
    # DO NOT add .py extension here.
    TARGET_CONFIG = "config_1D_Range2" 
    # TARGET_CONFIG = "config_1D_Range3" 
    # TARGET_CONFIG = "config_2D_Reciprocal" 
    # TARGET_CONFIG = "config_3D_Reciprocal" 
    
    try:
        # Attempt to dynamically import the module
        cfg = importlib.import_module(f"configs.{TARGET_CONFIG}")
        
        # Force reload config (Essential for Blender development)
        # This prevents Blender from remembering old parameters after you edit the config file.
        importlib.reload(cfg)
        
        print(f"Configuration loaded successfully: {TARGET_CONFIG}")

    except ModuleNotFoundError:
        print("\n" + "="*50)
        print(f"!!! [Error] Configuration file not found: configs/{TARGET_CONFIG}.py")
        print(f"   Please check if the file exists in the 'configs/' folder")
        print(f"   and ensure the filename is spelled correctly.")
        print("="*50 + "\n")
        return # Stop execution

    except Exception as e:
        # Catch syntax errors within the config file itself (e.g., missing commas, colons)
        print(f"!!! [Error] Syntax error in configuration file '{TARGET_CONFIG}': {e}")
        traceback.print_exc()
        return

    # ==========================================
    # 3. Start Building 
    # ==========================================
    
    # Use 'getattr' to avoid errors if 'output_name' is missing in the config
    print(f"--- Building Config: {getattr(cfg, 'output_name', 'Unknown')} ---")
    
    utils.clean_scene()
    ren.setup_cycles()
    
    # Initialize materials
    materials_dict = mat.init_materials(cfg)
    
    # Get rules (inject materials)
    # The trick here is to pass materials back to the config script, allowing it to assemble the Style
    cfg.hopping_rules, cfg.legend_data = cfg.get_rules_and_legend(materials_dict)
    
    # Generate geometry
    positions = geo.generate_sites(cfg, materials_dict['site'])
    geo.generate_hoppings(cfg, positions)
    
    # ==========================================
    # 5. Create Axis Gizmo (New Feature)
    # ==========================================
    # Safe access: If 'axis_settings' is missing, do nothing.
    axis_cfg = getattr(cfg, 'axis_settings', {})
    if axis_cfg.get('show', False):
        print("--- Generating Axis Gizmo ---")
        loc = axis_cfg.get('location', (-2, -2, 0)) # Default position
        ln  = axis_cfg.get('length', 2.0)
        th  = axis_cfg.get('thickness', 0.06)
        
        geo.create_axis_gizmo(axis_cfg, loc, length=ln, thickness=th)
    # ==========================================
    
    # Ground
    total_width = (cfg.Nx - 1) * cfg.dx
    geo.create_ground(total_width, -cfg.site_rad - 0.05)
    
    # Legend
    leg.create_system(cfg.legend_data, **cfg.legend_settings, arrow_size=cfg.arrow_size)
    
    # Scene setup
    ren.setup_lighting((total_width/2, 0, 0))
    ren.setup_camera(cfg, total_width/2, total_width)
    
    # Rendering
    res = getattr(cfg, 'output_res', (1920, 1080))
    ren.output_image(getattr(cfg, 'output_name', 'render'), res[0], res[1])

if __name__ == "__main__":
    run()