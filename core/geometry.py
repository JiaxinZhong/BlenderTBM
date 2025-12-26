import bpy
from mathutils import Vector
from .utils import get_collection

def create_arrow(location, direction, size, material, collection):
    bpy.ops.mesh.primitive_cone_add(radius1=size*0.3, radius2=0, depth=size, location=location, vertices=64)
    arrow = bpy.context.active_object
    arrow.data.materials.append(material)
    arrow.rotation_euler = direction.to_track_quat('Z', 'Y').to_euler()
    for coll in arrow.users_collection: coll.objects.unlink(arrow)
    collection.objects.link(arrow)
    bpy.ops.object.shade_smooth()

def create_hopping(p_start, p_end, h, style, col, bend_axis=Vector((0, 1, 0)), arrow_size=0.8):
    if not isinstance(bend_axis, Vector): bend_axis = Vector(bend_axis)
    
    mat = style.mat
    rad = style.thickness
    en_arrow = style.arrow

    p1, p2 = Vector(p_start), Vector(p_end)
    mid = (p1 + p2) / 2

    if bend_axis.length > 0:
        ctrl = mid + h * bend_axis.normalized()
    else:
        ctrl = mid 
    
    curve_data = bpy.data.curves.new('Hop', 'CURVE')
    curve_data.dimensions = '3D'; curve_data.resolution_u = 64; curve_data.bevel_depth = rad
    spline = curve_data.splines.new('BEZIER')
    spline.bezier_points.add(1)
    
    pt0, pt1 = spline.bezier_points[0], spline.bezier_points[1]
    pt0.co, pt0.handle_right = p1, ctrl
    pt0.handle_right_type = pt0.handle_left_type = 'FREE'
    pt1.co, pt1.handle_left = p2, ctrl
    pt1.handle_left_type = pt1.handle_right_type = 'FREE'
    
    obj = bpy.data.objects.new('HopObj', curve_data)
    col.objects.link(obj); obj.data.materials.append(mat)
    
    pos = (p1 + p2 + 6 * ctrl) / 8
    tan = p2 - p1
    
    if en_arrow:
        create_arrow(pos, tan, arrow_size, mat, col)

def create_ground(width_coverage, y_level):
    """创建地面"""
    bpy.ops.mesh.primitive_plane_add(size=1000, location=(0, 0, y_level))
    ground = bpy.context.active_object
    ground.name = "Ground_Table"
    
    mat = bpy.data.materials.new(name="Mat_Table")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = (0.9, 0.9, 0.9, 1)
    bsdf.inputs['Roughness'].default_value = 0.1
    bsdf.inputs['Specular IOR Level'].default_value = 0.5
    
    ground.data.materials.append(mat)
    return ground

def generate_sites(config, mat_site):
    """生成所有格点，返回位置字典"""
    col_lattice = get_collection("Lattice")
    positions = {}
    
    Nx, Ny, Nz = config.Nx, config.Ny, config.Nz
    dx, dy, dz = config.dx, config.dy, config.dz
    
    for iz in range(Nz):     
        for iy in range(Ny):
            for ix in range(Nx):
                pos = Vector((ix * dx, iy * dy, iz * dz))
                positions[(ix, iy, iz)] = pos 
                
                bpy.ops.mesh.primitive_uv_sphere_add(radius=config.site_rad, location=pos, segments=64, ring_count=32)
                site = bpy.context.active_object
                site.data.materials.append(mat_site)
                bpy.ops.object.shade_smooth()
                for c in site.users_collection: c.objects.unlink(site)
                col_lattice.objects.link(site)
    return positions

def generate_hoppings(config, positions):
    """生成所有 Hopping"""
    col_lattice = get_collection("Lattice")
    Nx, Ny, Nz = config.Nx, config.Ny, config.Nz
    
    for iz in range(Nz):
        for iy in range(Ny):
            for ix in range(Nx):
                curr_idx = (ix, iy, iz)
                if curr_idx not in positions: continue
                p_curr = positions[curr_idx]
                
                for rule in config.hopping_rules:
                    d_vec, bend_axis, h_scale, hop_style = rule
                    
                    tx, ty, tz = ix + d_vec[0], iy + d_vec[1], iz + d_vec[2]
                    
                    if 0 <= tx < Nx and 0 <= ty < Ny and 0 <= tz < Nz:
                        p_target = positions[(tx, ty, tz)]
                        geom_dist = (p_target - p_curr).length
                        h = geom_dist * config.arc_height_scale * h_scale
                        
                        create_hopping(p_curr, p_target, h, hop_style, col_lattice, 
                                     bend_axis=bend_axis, arrow_size=config.arrow_size)