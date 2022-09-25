import bpy
import os
import glob
import bmesh
from bpy.types import Panel, Operator, PropertyGroup
from bpy.props import EnumProperty, PointerProperty
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty
import os.path

#__________________READ WINDOW DIRECTORY ________________

#Set the path of the folder (Library) we are working with and select only .fbx
#The path is set for the current older environement. Would need to be improve to be adaptable to any environement
#by setting a manual path for the library (would imply rework on the the BODY PART SELECTOR system)

path_to_fbx_dir = os.path.join("../ReadyPlayerMe/Library")
file_list = sorted(os.listdir(path_to_fbx_dir))
fbx_list = [item for item in file_list if item.endswith(".fbx")]


#check folder content
print(fbx_list)

#split files into list by cathegory (top/bottom/footwear) for latter
bottom_list = [item for item in fbx_list if item.endswith("bottom.fbx")]
top_list = [item for item in fbx_list if item.endswith("top.fbx")]
footwear_list = [item for item in fbx_list if item.endswith("footwear.fbx")]

#check separated list content
print(top_list)
print(bottom_list)
print(footwear_list)

#Set global variable
exportname = "default.fbx"

 
#___________________________________________________________________________ToolPanel N-tool__________________________________________________________________________
                          
#BODY PART SELECTORS_________________________________                             
class MyProperties(PropertyGroup):
    
    
#Create a Enum from the list of TopOutfit (top_list)
 
    my_enum : EnumProperty(
        name= "Top Outfit",
        description= "Pick a TopBody outfit",
        items= [('OP1', str(top_list[0]), ""),
                ('OP2', str(top_list[1]), ""),
                ('OP3', str(top_list[2]), "")
        ]
    )
    
#Create a Enum from the list of BottomOutfit (bottom_list)
 
    my_enum2 : EnumProperty(
        name= "Bottom Outfit",
        description= "Pick a TopBody outfit",
        items= [('OP1', str(bottom_list[0]), ""),
                ('OP2', str(bottom_list[1]), ""),
                ('OP3', str(bottom_list[2]), "")
        ]
    )    
    
#Create a Enum from the list of FootwearOutfit (footwear_list)
 
    my_enum3 : EnumProperty(
        name= "Footwear Outfit",
        description= "Pick a TopBody outfit",
        items= [('OP1', str(footwear_list[0]), ""),
                ('OP2', str(footwear_list[1]), ""),
                ('OP3', str(footwear_list[2]), "")
        ]
    )



#GENERATOR_________________________________________
#Set Outfit button function: Reading the Outfit choices and exporting them when clicking on it
class ADDONNAME_OT_my_op(Operator):
    bl_label = "Generate and Export Outfit"
    bl_idname = "addonname.myop_operator"



#Preparing a list of this elements to import when using the button. The current method is set for the specific list of asset we have in the folder and would need to be
#improved to works with any number of files. To do so and with more time I would probably try to update my lists/enums...etc by reading the content of my folder.


   
    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        
        
#CLEAR SCENE to generate a new outfit without overlapping

        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
             
        
        #Add Selected TopBody(my_enum) to the list
        if mytool.my_enum == 'OP1':
            result_enum = top_list[0]            
        if mytool.my_enum == 'OP2':
            result_enum = top_list[1]    
        if mytool.my_enum == 'OP3':
            result_enum = top_list[2]     
         #Add Selected BottomBody(my_enum2) to the list
        if mytool.my_enum2 == 'OP1':
            result_enum2 = bottom_list[0]            
        if mytool.my_enum2 == 'OP2':
            result_enum2 = bottom_list[1]    
        if mytool.my_enum2 == 'OP3':
            result_enum2 = bottom_list[2]     
         #Add Selected FootwearBody(my_enum3) to the list
        if mytool.my_enum3 == 'OP1':
            result_enum3 = footwear_list[0]            
        if mytool.my_enum3 == 'OP2':
            result_enum3 = footwear_list[1]    
        if mytool.my_enum3 == 'OP3':
            result_enum3 = footwear_list[2]
            
            
        imp_list = (result_enum, result_enum2, result_enum3)#Set the list to import
        print(imp_list, "<----- IMPORTED ELEMENTS")# print to check the list of element to import


#check naming to set the future naming convention        
#check name information for top outfit        
        if "office" in result_enum:
            name_ref_top = "off"
        if "casual" in result_enum:
            name_ref_top = "cas"
        if "cyberpunk" in result_enum:
            name_ref_top = "cyb"
            
#check name information for bottom outfit            
        if "office" in result_enum2:
            name_ref_bottom = "off"
        if "casual" in result_enum2:
            name_ref_bottom = "cas"
        if "cyberpunk" in result_enum2:
            name_ref_bottom = "cyb"
            
#check name information for footwear outfit        
        if "office" in result_enum3:
            name_ref_footwear = "off"
        if "casual" in result_enum3:
            name_ref_footwear = "cas"
        if "cyberpunk" in result_enum3:
            name_ref_footwear = "cyb"
            
            
#get the complete file name depending of the imported elements and print it            
        filename = "outfit-f" + "-" + name_ref_top + "-" + name_ref_bottom + "-" + name_ref_footwear       
        exportname = (filename + ".fbx")
        
        
        print(exportname + "THIS IS MY FILE NAME")#check print
        
        
#Importing the elements of the list in the scene to generate the Outfit
        for item in imp_list:
            path_to_file = os.path.join(path_to_fbx_dir, item)
            bpy.ops.import_scene.fbx(filepath = path_to_file, axis_forward="-Z", axis_up="Y")

#Deselect all scene elements to clean the hierarchy                
        bpy.ops.object.select_all(action='DESELECT')
         
        if bpy.context.object.mode == 'EDIT':
           bpy.ops.object.mode_set(mode='OBJECT')

#Clean for Armature.001            
        bpy.data.objects['Armature.001'].select_set(True)
        for child in bpy.data.objects["Armature.001"].children:
            if child.type != 'MESH':
                child.select_set(True)
        
#Clean for Armature.002        
        bpy.data.objects['Armature.002'].select_set(True)
        for child in bpy.data.objects["Armature.002"].children:
            if child.type != 'MESH':
                child.select_set(True)
                
        bpy.ops.object.delete()

#Set hierarchy with one Armature Parent
        
         
        object_parent =  bpy.data.objects['Armature']
        object_bottom =  bpy.data.objects['Wolf3D_Outfit_Bottom']
        
        #Cyberpunk-Footwear content issue / engine naming different (code could be improve
        #or naming of asset more consistent to use the same in-engine collection naming)
        
        cyb_footwear = bpy.context.scene.objects.get('Wolf3D_Footwear_Cyberpunk')
        if cyb_footwear:
            object_footwear =  bpy.data.objects['Wolf3D_Footwear_Cyberpunk']
        else:
            object_footwear =  bpy.data.objects['Wolf3D_Outfit_Footwear']   
              
              
            
        #Set Armature as parent     
        object_bottom.parent = object_parent
        object_footwear.parent = object_parent
        
#Export the generated model with a proper naming convention base on his sub-elements        
        def execute(self, context):
            scene = context.scene
         
       
        bpy.ops.export_scene.fbx(filepath = "../ReadyPlayerMe/Library/CustomOutfits/" + exportname, use_active_collection=True, embed_textures=True, path_mode='COPY')    
        
        return {'FINISHED'}
           

     
    
#________________________________________________UI content_________________________________________________________


#Draw Panel in N-panel with DropDown Menu from Enums for each cathegory
    
    
class ADDONNAME_PT_main_panel(Panel):
    bl_label = "Outfit Generator"
    bl_idname = "ADDONNAME_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "BodyGen"
 
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        
        row = layout.row()
        row.prop(mytool, "my_enum")
        
        row = layout.row()
        row.prop(mytool, "my_enum2")
        
        row = layout.row()
        row.prop(mytool, "my_enum3")
        
        
        layout.operator("addonname.myop_operator")#Generator Button
        

 
 
 
classes = [MyProperties, ADDONNAME_PT_main_panel, ADDONNAME_OT_my_op]

 
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.my_tool = PointerProperty(type= MyProperties)
 
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.my_tool
 
 
 
if __name__ == "__main__":
    register()




