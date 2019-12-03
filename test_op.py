import bpy
from bpy.types import Operator

class Test_OT_Operator(Operator):
    bl_idname = "view3d.curvestobone"
    bl_label = "Simple operator"
    bl_description = "Add bones to curves with parent"

    # Gray out if not a curve
    @classmethod
    def poll(cls, context):
        return (len(bpy.context.selected_objects) != 0 and context.object.type is not None and
                context.object.type == 'CURVE')

    def execute(self, context):
        collection = context.collection
        scene = context.scene

        curve_objs = bpy.context.selected_objects

        for curve_obj in curve_objs:
        # curve_obj = context.object
            curve = curve_obj.data


            # Check if curve
            if (curve_obj.type != 'CURVE'):
                self.report({'WARNING'}, 'Object must be a curve')
                return {'CANCELLED'}

            # Create new armature
            arm = bpy.data.armatures.new("BezArmature")
            arm_obj = bpy.data.objects.new("BezArmature", arm)
            collection.objects.link(arm_obj)

            # Add bones at spline points
            context.view_layer.objects.active = arm_obj
            bpy.ops.object.mode_set(mode='EDIT')
            mw = curve_obj.matrix_world
            arm_obj.matrix_world = mw
            
            for spline in curve.splines:   
                points = [bp.co for bp in spline.points]
                if len(points) < 2:
                    self.report({'WARNING'}, 'Curve must be a path with at least 2 points')
                    return {'CANCELLED'}

                if spline.use_cyclic_u:
                    points.append(points[0])
                parent = None    
                for i in range(len(points)-1):
                    bone = arm.edit_bones.new("Bone")
                    
                    bone.head = points[i][0:3]
                    bone.tail = points[i+1][0:3]
                    bone.parent = parent
                    if i > 0: # Don't connect masterbone
                        bone.use_connect = True
                    parent = bone
            bpy.ops.object.mode_set(mode='OBJECT')

            # Add modifier to curve 
            bpy.ops.object.select_all(action='DESELECT') #deselect all object
            curve_obj.select_set(state=True)
            arm_obj.select_set(state=True)
            context.view_layer.objects.active = arm_obj
            bpy.ops.object.parent_set(type='ARMATURE_ENVELOPE')
            curve_obj.modifiers["Armature"].use_bone_envelopes = True
            curve_obj.modifiers["Armature"].use_apply_on_spline = True

            context.view_layer.objects.active = arm_obj
            obj = bpy.context.object.data.bones[1:]
            if (scene.add_jiggle_bool):
                try:
                    bpy.context.scene.jiggle.test_mode = True
                except AttributeError:
                    print("Jiggle Addon not installed") 
                bpy.ops.object.mode_set(mode='POSE')    
                for bone in obj:
                    bone.select = True
                    try:
                        bone.jiggle.enabled = True
                    except AttributeError:
                        print("Jiggle Addon not installed")            
            bpy.context.object.data.bones.active = obj[0]

        return {'FINISHED'}