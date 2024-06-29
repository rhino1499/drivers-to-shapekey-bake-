bl_info = {
    "name": "Bake Shapekeys from Driver",
    "blender": (3, 0, 0),
    "category": "Animation",
}

import bpy

class BakeShapekeysOperator(bpy.types.Operator):
    bl_idname = "object.bake_shapekeys"
    bl_label = "Bake Shapekeys from Driver"
    bl_options = {'REGISTER', 'UNDO'}

    source_shapekey_name: bpy.props.StringProperty(
        name="Source Shapekey",
        description="Name of the source shapekey",
        default="Key 2"
    )

    target_shapekey_name: bpy.props.StringProperty(
        name="Target Shapekey",
        description="Name of the target shapekey",
        default="Key 1"
    )

    start_frame: bpy.props.IntProperty(
        name="Start Frame",
        description="Start frame of the animation",
        default=1
    )

    end_frame: bpy.props.IntProperty(
        name="End Frame",
        description="End frame of the animation",
        default=250
    )

    def execute(self, context):
        obj = context.active_object

        def keyframe_shapekeys(scene):
            current_frame = scene.frame_current
            if current_frame <= self.end_frame:
                source_value = obj.data.shape_keys.key_blocks[self.source_shapekey_name].value
                obj.data.shape_keys.key_blocks[self.target_shapekey_name].value = source_value
                obj.data.shape_keys.key_blocks[self.target_shapekey_name].keyframe_insert(data_path="value")
                scene.frame_set(current_frame + 1)
            else:
                bpy.app.handlers.frame_change_post.remove(keyframe_shapekeys)
                bpy.ops.screen.animation_play()  # Stop the animation

        # Set the scene to the start frame
        context.scene.frame_set(self.start_frame)

        # Add the keyframing function to the frame change handler
        bpy.app.handlers.frame_change_post.append(keyframe_shapekeys)

        # Play the animation
        bpy.ops.screen.animation_play()

        return {'FINISHED'}

class BakeShapekeysPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_bake_shapekeys"
    bl_label = "Bake Shapekeys from Driver"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Animation'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.operator("object.bake_shapekeys")
        layout.prop(scene, "source_shapekey_name")
        layout.prop(scene, "target_shapekey_name")
        layout.prop(scene, "start_frame")
        layout.prop(scene, "end_frame")

def register():
    bpy.utils.register_class(BakeShapekeysOperator)
    bpy.utils.register_class(BakeShapekeysPanel)
    bpy.types.Scene.source_shapekey_name = bpy.props.StringProperty(
        name="Source Shapekey",
        description="Name of the source shapekey",
        default="Key 2"
    )
    bpy.types.Scene.target_shapekey_name = bpy.props.StringProperty(
        name="Target Shapekey",
        description="Name of the target shapekey",
        default="Key 1"
    )
    bpy.types.Scene.start_frame = bpy.props.IntProperty(
        name="Start Frame",
        description="Start frame of the animation",
        default=1
    )
    bpy.types.Scene.end_frame = bpy.props.IntProperty(
        name="End Frame",
        description="End frame of the animation",
        default=250
    )

def unregister():
    bpy.utils.unregister_class(BakeShapekeysOperator)
    bpy.utils.unregister_class(BakeShapekeysPanel)
    del bpy.types.Scene.source_shapekey_name
    del bpy.types.Scene.target_shapekey_name
    del bpy.types.Scene.start_frame
    del bpy.types.Scene.end_frame

if __name__ == "__main__":
    register()
