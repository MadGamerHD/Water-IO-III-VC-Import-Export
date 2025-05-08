bl_info = {
    "name": "Water IO III/VC",
    "author": "MadGamerHD",
    "version": (1, 4, 1),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Water IO III/VC",
    "description": "Import, visualize, and export GTA III/VC waterpro.dat (64×64 visual grid)",
    "category": "Import-Export",
}

import bpy
import struct

# --------- Constants ---------
MAX_LEVELS = 48
GRID_SIZE = 64
CELL_SIZE = 64.0
OFFSET = CELL_SIZE * GRID_SIZE / 2

# --------- State ---------
_imported_heights = []
_imported_vis_map = []

# --------- File I/O ---------

def read_waterpro(filepath):
    global _imported_heights, _imported_vis_map
    with open(filepath, 'rb') as f:
        data = f.read()
    num_levels = struct.unpack_from('<I', data, 0)[0]
    heights = list(struct.unpack_from(f'<{MAX_LEVELS}f', data, 4))[:num_levels]

    # visibility map begins at offset 0x03C4
    start = 0x03C4
    vis_map = [
        list(data[offset:offset + GRID_SIZE])
        for offset in range(start, start + GRID_SIZE * GRID_SIZE, GRID_SIZE)
    ]

    _imported_heights = heights
    _imported_vis_map = vis_map
    return heights, vis_map


def write_waterpro(filepath):
    if not _imported_heights or not _imported_vis_map:
        raise RuntimeError("No data to export. Please import a waterpro.dat first.")
    # header + heights
    header = struct.pack('<I', len(_imported_heights))
    heights_padded = _imported_heights + [0.0] * (MAX_LEVELS - len(_imported_heights))
    heights_bytes = struct.pack(f'<{MAX_LEVELS}f', *heights_padded)

    # zone data is empty from 0x00C4 to 0x03C4
    zone_bytes = b'\x00' * (0x03C4 - (4 + MAX_LEVELS * 4))
    vis_bytes = b''.join(bytes(row) for row in _imported_vis_map)
    # phys data is empty from end of vis to 0x53C0
    phys_start = 0x03C4 + GRID_SIZE * GRID_SIZE
    phys_bytes = b'\x00' * (0x53C0 - phys_start)

    with open(filepath, 'wb') as f:
        f.write(header + heights_bytes + zone_bytes + vis_bytes + phys_bytes)
    print(f"Exported waterpro.dat with {len(_imported_heights)} levels to {filepath}")

# --------- Blender Helpers ---------

def clear_water_collection():
    name = 'Water IO III/VC'
    if name in bpy.data.collections:
        col = bpy.data.collections[name]
        for obj in list(col.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(col)
    col = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(col)
    return col


def create_cell(col, x, y, height, mat, idx):
    xmin = x * CELL_SIZE - OFFSET
    ymin = y * CELL_SIZE - OFFSET
    verts = [
        (xmin, ymin, height),
        (xmin + CELL_SIZE, ymin, height),
        (xmin + CELL_SIZE, ymin + CELL_SIZE, height),
        (xmin, ymin + CELL_SIZE, height)
    ]
    mesh = bpy.data.meshes.new(f"Cell_{x}_{y}")
    mesh.from_pydata(verts, [], [(0,1,2,3)])
    obj = bpy.data.objects.new(f"Water_{x}_{y}", mesh)
    obj.data.materials.append(mat)
    obj["water_index"] = idx
    col.objects.link(obj)

# --------- Core Logic ---------

def import_waterpro(filepath):
    heights, vis_map = read_waterpro(filepath)
    col = clear_water_collection()
    # prepare materials
    mats = []
    for i in range(len(heights)):
        name = f"WLevel_{i}"
        mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
        mat.blend_method = 'BLEND'
        mat.diffuse_color = (0.0, 0.2 + i / max(1,len(heights)) * 0.8, 1.0, 0.5)
        mats.append(mat)

    count = 0
    for y, row in enumerate(vis_map):
        for x, idx in enumerate(row):
            if idx < len(heights):
                create_cell(col, x, y, heights[idx], mats[idx], idx)
                count += 1
    print(f"Imported {count} water cells.")

# --------- UI ---------

class IMPORT_OT(bpy.types.Operator):
    bl_idname = "waterio.import_dat"
    bl_label = "Import waterpro.dat"
    bl_options = {'REGISTER', 'UNDO'}
    filepath: bpy.props.StringProperty(
        subtype='FILE_PATH',
        default="",
        options={'HIDDEN'}
    )
    filter_glob: bpy.props.StringProperty(
        default="*.dat", options={'HIDDEN'}
    )

    def execute(self, context):
        try:
            import_waterpro(self.filepath)
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class EXPORT_OT(bpy.types.Operator):
    bl_idname = "waterio.export_dat"
    bl_label = "Export waterpro.dat"
    bl_options = {'REGISTER'}
    filepath: bpy.props.StringProperty(
        subtype='FILE_PATH',
        default="waterpro.dat",
        options={'HIDDEN'}
    )
    filter_glob: bpy.props.StringProperty(
        default="*.dat", options={'HIDDEN'}
    )

    def execute(self, context):
        try:
            write_waterpro(self.filepath)
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class WATERIO_PT_panel(bpy.types.Panel):
    bl_label = "Water IO III/VC"
    bl_idname = "WATERIO_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Water IO III/VC'

    def draw(self, context):
        layout = self.layout
        layout.operator(IMPORT_OT.bl_idname, text="Import waterpro.dat")
        layout.operator(EXPORT_OT.bl_idname, text="Export waterpro.dat")

# --------- Registration ---------

def register():
    for cls in (IMPORT_OT, EXPORT_OT, WATERIO_PT_panel):
        bpy.utils.register_class(cls)


def unregister():
    for cls in (IMPORT_OT, EXPORT_OT, WATERIO_PT_panel):
        bpy.utils.unregister_class(cls)

if __name__ == '__main__':
    register()