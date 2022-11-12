import bpy
import math

#'LIQUID' for flood, 'GAS' for fire

mode = 'LIQUID'
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

scene_fluid_modifier = obj_object.modifiers.new('scene modifier', 'FLUID')

scene_fluid_modifier.fluid_type = 'EFFECTOR'

bpy.ops.mesh.primitive_cube_add()

domain = bpy.context.selected_objects[0]

domain_fluid_modifier = domain.modifiers.new('domain modifier', 'FLUID')

domain_fluid_modifier.fluid_type = 'DOMAIN'

domain_fluid_modifier.domain_settings.domain_type = mode

domain_fluid_modifier.domain_settings.cache_type = 'ALL'

bpy.ops.mesh.primitive_cube_add(location = (1, 0, 0), scale = (0.5, 1, 1))

source = bpy.context.selected_objects[0]

source_fluid_modifier = source.modifiers.new('domain modifier', 'FLUID')

source_fluid_modifier.fluid_type = 'FLOW'

source_fluid_modifier.flow_settings.flow_behavior = 'INFLOW'

source_fluid_modifier.flow_settings.flow_type = 'LIQUID'