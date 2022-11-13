import bpy
import math

#True for flood, False for fire

flood = True
anim_len = 60
flood_height = 0.5
flood_width = 0.25
file = "C:\\Down\\S131Table.ply"

for obj in bpy.context.scene.objects:
    obj.select_set(True)
bpy.ops.object.delete()
            
bpy.data.scenes[0].frame_end = anim_len

bpy.ops.import_mesh.ply(filepath = file)
obj_object = bpy.context.selected_objects[0]
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

bpy.ops.mesh.primitive_cube_add(location = (0, 0, obj_object.dimensions.z), scale = (1, 1, obj_object.dimensions.z))

domain = bpy.context.selected_objects[0]

mesh = domain.data
for f in mesh.polygons:
    f.use_smooth = True
    
domain_fluid_modifier = domain.modifiers.new('domain modifier', 'FLUID')

domain_fluid_modifier.fluid_type = 'DOMAIN'

domain_fluid_modifier.domain_settings.domain_type = 'LIQUID' if flood else 'GAS'

domain_fluid_modifier.domain_settings.cache_type = 'ALL'

domain_fluid_modifier.domain_settings.resolution_max = 64

domain_fluid_modifier.domain_settings.cache_frame_end = anim_len

domain_fluid_modifier.domain_settings.use_mesh = True

bpy.ops.mesh.primitive_cube_add(location = (1 - flood_width * 0.5, 0, obj_object.dimensions.z * flood_height * 0.5), scale = (flood_width * 0.5, 1, obj_object.dimensions.z * flood_height * 0.5))

source = bpy.context.selected_objects[0]

source_fluid_modifier = source.modifiers.new('domain modifier', 'FLUID')

source_fluid_modifier.fluid_type = 'FLOW'

source_fluid_modifier.flow_settings.flow_behavior = 'INFLOW'

source_fluid_modifier.flow_settings.flow_type = 'LIQUID' if flood else 'SMOKE'

domain.select_set(True)

bpy.context.view_layer.objects.active = domain

bpy.ops.fluid.bake_all()

bpy.ops.object.camera_add(location = (2, 2, 2), rotation = (math.atan(math.sqrt(2)), 0, math.pi * 3 /4))

camera = bpy.context.selected_objects[0]

bpy.ops.object.light_add(location = (0, 0, 2))

bpy.ops.object.select_all(action='DESELECT')

source.select_set(True)

bpy.ops.object.delete()

bpy.context.scene.eevee.use_ssr = True

bpy.context.scene.eevee.use_ssr_refraction = True

water_material = bpy.data.materials.new(name = 'Water')

water_material.use_nodes = True

glass_bsdf = water_material.node_tree.nodes.new('ShaderNodeBsdfGlass')

glass_bsdf.color = (0.5,0.5,0.5)

output = water_material.node_tree.nodes['Material Output']

water_material.node_tree.links.new(glass_bsdf.outputs['BSDF'], output.inputs['Surface'])

water_material.use_screen_refraction = True

domain.data.materials.append(water_material)