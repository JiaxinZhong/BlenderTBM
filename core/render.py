import bpy
import os
from mathutils import Vector

def enable_gpu():
    prefs = bpy.context.preferences
    cprefs = prefs.addons['cycles'].preferences
    for device_type in ['OPTIX', 'CUDA', 'METAL']:
        try:
            cprefs.compute_device_type = device_type
            cprefs.get_devices()
            for device in cprefs.devices: device.use = True
            break
        except: pass

def setup_cycles():
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'GPU'
    enable_gpu()
    scene.cycles.samples = 128
    scene.cycles.use_denoising = True
    scene.view_settings.view_transform = 'Standard'
    scene.view_settings.look = 'Medium High Contrast'
    scene.view_settings.exposure = 0.0

def setup_lighting(target_center):
    from .utils import get_collection
    col_light = get_collection("Lighting")
    
    # Key Light
    light = bpy.data.lights.new(name="Key_Light", type='AREA')
    light.energy = 1000.0; light.size = 20.0
    key = bpy.data.objects.new(name="Key_Light", object_data=light)
    col_light.objects.link(key)
    key.location = (target_center[0], -20, 30)
    key.rotation_euler = (Vector(target_center) - key.location).to_track_quat('-Z', 'Y').to_euler()

    # Fill Light
    light2 = bpy.data.lights.new(name="Fill_Light", type='AREA')
    light2.energy = 600.0; light2.size = 15.0
    fill = bpy.data.objects.new(name="Fill_Light", object_data=light2)
    col_light.objects.link(fill)
    fill.location = (target_center[0], 10, 20)
    fill.rotation_euler = (Vector(target_center) - fill.location).to_track_quat('-Z', 'Y').to_euler()

def setup_camera(config, center_x, total_width):
    cam_data = bpy.data.cameras.new("MainCamera")
    cam_obj = bpy.data.objects.new("MainCamera", cam_data)
    bpy.context.scene.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj
    cam_obj.data.type = 'ORTHO'
    
    lattice_max_y = (config.Ny - 1) * config.dy
    legend_pos_y = config.legend_settings['start_pos'][1]
    
    scene_center_y = (lattice_max_y + legend_pos_y) / 2.0
    target_vec = Vector((center_x, scene_center_y, 0))
    
    scene_h = lattice_max_y - legend_pos_y
    cam_obj.data.ortho_scale = max(total_width, scene_h) * 1.05
    
    cam_obj.location = target_vec + Vector((0, -20, 30))
    cam_obj.rotation_euler = (target_vec - cam_obj.location).to_track_quat('-Z', 'Y').to_euler()

def output_image(filename_suffix, width, height, folder="output"):
    scene = bpy.context.scene
    blend_path = bpy.data.filepath
    if not blend_path: print("Save blend file first!"); return
    
    dir_path = os.path.dirname(blend_path)
    out_dir = os.path.join(dir_path, folder)
    if not os.path.exists(out_dir): os.makedirs(out_dir)
    
    base_name = os.path.splitext(os.path.basename(blend_path))[0]
    final_filename = f"{base_name}_{filename_suffix}.png"
    
    scene.render.resolution_x = width
    scene.render.resolution_y = height
    scene.render.filepath = os.path.join(out_dir, final_filename)
    bpy.ops.render.render(write_still=True)
    print(f"Rendered: {scene.render.filepath}")