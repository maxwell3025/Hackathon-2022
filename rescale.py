import bpy
import math
file = "C:\\Down\\neucon-scene1.obj"
bpy.ops.import_scene.obj(filepath = file)
obj_object = bpy.context.selected_objects[0]
bpy.ops.transform.rotate(value = math.pi/2.0, orient_axis='X')
scale = 2.0 / max(
obj_object.dimensions.x,
obj_object.dimensions.y,
obj_object.dimensions.z
)
bpy.ops.transform.resize(value = (scale, scale, scale))

obj_object.select_set(True)

bpy.ops.object.origin_set(center = 'BOUNDS')