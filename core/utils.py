import bpy

def clean_scene():
    """清理场景中的所有物体、集合、材质等"""
    if bpy.context.active_object and bpy.context.active_object.mode == 'EDIT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    for col in bpy.data.collections: bpy.data.collections.remove(col)
    for b in bpy.data.meshes: bpy.data.meshes.remove(b)
    for b in bpy.data.curves: bpy.data.curves.remove(b)
    for b in bpy.data.materials: bpy.data.materials.remove(b)
    for b in bpy.data.lights: bpy.data.lights.remove(b)
    for b in bpy.data.cameras: bpy.data.cameras.remove(b)

def get_collection(name):
    """获取或新建集合"""
    if name in bpy.data.collections: return bpy.data.collections[name]
    new_col = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(new_col)
    return new_col