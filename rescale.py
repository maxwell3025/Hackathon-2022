import bpy
import math

#True for flood, False for fire

flood = False

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

obj_object.location.z = obj_object.dimensions.z / 2

scene_fluid_modifier = obj_object.modifiers.new('scene modifier', 'FLUID')

scene_fluid_modifier.fluid_type = 'EFFECTOR'

scene_fluid_modifier.effector_settings.use_plane_init = True

bpy.ops.mesh.primitive_cube_add(location = (0, 0, 1))

domain = bpy.context.selected_objects[0]

domain_fluid_modifier = domain.modifiers.new('domain modifier', 'FLUID')

domain_fluid_modifier.fluid_type = 'DOMAIN'

domain_fluid_modifier.domain_settings.domain_type = 'LIQUID' if flood else 'GAS'

domain_fluid_modifier.domain_settings.cache_type = 'ALL'

domain_fluid_modifier.domain_settings.cache_frame_end = 60

domain_fluid_modifier.domain_settings.use_mesh = True

bpy.ops.mesh.primitive_cube_add(location = (0.75, 0, 0.25), scale = (0.25, 1, 0.25))

source = bpy.context.selected_objects[0]

source_fluid_modifier = source.modifiers.new('domain modifier', 'FLUID')

source_fluid_modifier.fluid_type = 'FLOW'

source_fluid_modifier.flow_settings.flow_behavior = 'INFLOW'

source_fluid_modifier.flow_settings.flow_type = 'LIQUID' if flood else 'SMOKE'

domain.select_set(True)

bpy.context.view_layer.objects.active = domain

bpy.ops.fluid.bake_all()