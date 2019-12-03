import bpy

class TEST_PT_Panel(bpy.types.Panel):
    bl_idname = "TEST_PT_Panel"
    bl_label = "Curvebones"
    bl_category = "Rigging"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI" 

    # Gray out if not a curve
    @classmethod
    def poll(cls, context):
        return (len(bpy.context.selected_objects) != 0 and context.object.type is not None and
                context.object.type == 'CURVE')

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        row = layout.row()
        row.operator("view3d.curvestobone", text="Add curvebones")

        row = layout.row(align=False)
        row.prop(scene, "add_jiggle_bool", text="Add jiggle to bones")

