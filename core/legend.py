import bpy
import math
from mathutils import Vector
from .utils import get_collection
from .materials import create_material
from .geometry import create_arrow

def generate_latex_mesh(latex_code, location, scale=1.0, material=None, collection=None, thickness=0.05, offset=(0,0,0), orientation=(0, 0, 1)):
    """
    Generates a 3D mesh from LaTeX code using the 'latex2blender' addon logic.
    """
    scene = bpy.context.scene
    try: 
        settings = scene.my_tool
    except: 
        print("Error: No latex2blender addon found")
        return None

    settings.latex_code = f"${latex_code}$"
    try: 
        bpy.ops.wm.compile_as_mesh()
    except: 
        return None
    
    obj = bpy.context.active_object
    if obj and "LaTeX" in obj.name:
        # Rename object to avoid conflicts
        # obj.name = f"LatexFormula_{int(time.time()*1000)}"
        clean_name = latex_code.replace("\\", "").replace("{", "").replace("}", "")
        obj.name = f"Latex_{clean_name}"
        obj.scale = (scale, scale, scale)
        
        # Force update to get correct dimensions before positioning
        bpy.context.view_layer.update()
        
        # Calculate Position
        # Note: Adjusting x based on dimensions helps center the text anchor
        final_pos = Vector(location)
        final_pos.x += obj.dimensions.x / 2.0 + offset[0]
        final_pos.y += offset[1]
        final_pos.z += offset[2]
        obj.location = final_pos
        
        # --- [NEW] Apply Orientation ---
        # Convert orientation tuple to Vector
        target_vec = Vector(orientation)
        
        print(f"Orienting LaTeX mesh '{obj.name}' to direction: {target_vec}")
        # Only rotate if the target vector is valid (non-zero length)
        if target_vec.length_squared > 0:
            # If the target vector is (0,0,1), use '-Z' to avoid gimbal lock
            if target_vec.x == 0 and target_vec.y == 0:
                target_vec.z = -1 # todo: Here is to fix to positive Z direction
                obj.rotation_euler = target_vec.to_track_quat('-Z', 'Y').to_euler()
            else:
                obj.rotation_euler = target_vec.to_track_quat('Z', 'Y').to_euler()
        # -------------------------------
        
        # Add Thickness (Solidify Modifier)
        if thickness > 0:
            mod = obj.modifiers.new(name="Thickness", type='SOLIDIFY')
            mod.thickness = thickness
            mod.offset = 0
            
        # Assign Material
        if material:
            obj.data.materials.clear()
            obj.data.materials.append(material)
        
        # Link to correct collection
        if collection:
            for c in obj.users_collection: 
                c.objects.unlink(obj)
            collection.objects.link(obj)
            
        return obj
        
    return None

def create_legend_row(pos, length, latex_str, hop_style, col, arrow_size=1.0, offset=(0,0,0), orientation=(0, 0, 1)):
    x, y, z = pos
    # Line
    mid_x = x + length / 2
    bpy.ops.mesh.primitive_cylinder_add(radius=hop_style.thickness, depth=length, location=(mid_x, y, z), vertices=32)
    line = bpy.context.active_object
    line.data.materials.append(hop_style.mat)
    line.rotation_euler = (0, math.radians(90), 0)
    for c in line.users_collection: c.objects.unlink(line)
    col.objects.link(line)
    bpy.ops.object.shade_smooth()
    
    # Arrow
    if hop_style.arrow:
        create_arrow(Vector((x + length, y, z)), Vector((1, 0, 0)), arrow_size, hop_style.mat, col)
    
    # Text
    text_pos = Vector((x + length + 0.5, y - 0.2, z))
    mat_text = bpy.data.materials.get("Mat_Formula_Black")
    if not mat_text: mat_text = create_material("Mat_Formula_Black", (0.05, 0.05, 0.05, 1))
    
    latex_scale = 1.5 # Control the size of the LaTeX text
    generate_latex_mesh(latex_str, text_pos, latex_scale, mat_text, col, thickness=0.05, offset=offset, orientation=orientation)

def create_system(legend_data_list, start_pos, arrow_size=1.0, line_length=3.0, cols=1, row_spacing=2.0, col_spacing=4.0, text_orient=(0,0,1)):
    col_legend = get_collection("Legend")
    start_x, start_y, start_z = start_pos
    
    for i, item in enumerate(legend_data_list):
        label, hop_style = item[0], item[1]
        shift = item[2] if len(item) > 2 else (0, 0, 0)
        
        col_idx = i % cols      
        row_idx = i // cols     
        
        cur_x = start_x + (col_idx * col_spacing)
        cur_y = start_y - (row_idx * row_spacing)
        
        create_legend_row((cur_x, cur_y, start_z), line_length, label, hop_style, col_legend, arrow_size=arrow_size, offset=shift, orientation=text_orient)