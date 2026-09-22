import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# Verified mapping keys that safely replace layout strings without breaking parentheses
TRANSLATION_MAP = {
     # Interface Text Swaps (Protects Parentheses Structure)
    'warning_msg = "SciPyが利用できません。NumPy・SciPy再インストールボタンを使用してください"': 'warning_msg = "SciPy is unavailable. Please use the NumPy/SciPy reinstall button below."',
    'warning_msg = "ソースアバター名を設定してください"': 'warning_msg = "Please configure the Source Avatar Name [Set_Src]"',
    'text="アバター設定"': 'text="Avatar Settings [Avatar_Set]"',
    'text="アバターデータファイル:"': 'text="Avatar Data Files:"',
    'box.label(text="NumPy・SciPy マルチスレッド対応", icon=\'LIBRARY_DATA_DIRECT\')': 'box.label(text="NumPy & SciPy Multi-Thread Optimization Hub [Lib_Hub]", icon=\'LIBRARY_DATA_DIRECT\')',
    'col.label(text=f"現在のNumPy: {numpy_version}", icon=\'CHECKMARK\')': 'col.label(text=f"Active NumPy Version: {numpy_version} [NumPy_Ver]", icon=\'CHECKMARK\')',
    'col.label(text="SciPy が見つかりません（新規インストールされます）", icon=\'INFO\')': 'col.label(text="SciPy environment missing (Fresh install will trigger) [SciPy_Miss]", icon=\'INFO\')',
    'row.operator("rbf.reinstall_numpy_scipy_multithreaded", text="NumPy・SciPy マルチスレッド版 再インストール", icon=\'FILE_REFRESH\')': 'row.operator("rbf.reinstall_numpy_scipy_multithreaded", text="Reinstall NumPy & SciPy (Multi-Thread Optimized) [Reinstall_Lib]", icon=\'FILE_REFRESH\')',
    'box.label(text="デバッグ・トラブルシューティング", icon=\'CONSOLE\')': 'box.label(text="Debug & Diagnostic Troubleshooting Hub [Debug_Hub]", icon=\'CONSOLE\')',
    
    # Shapekey
    'row.prop(scene, "rbf_apply_shape_key_name", text="シェイプキー名")': 'row.prop(scene, "rbf_apply_shape_key_name", text="Shape Key Name [Key_Label]")',

    # System Properties & Core Fields
    'name="Source Mesh"': 'name="Source Mesh [Source]"',
    'name="Source Shape Key"': 'name="Source Shape Key [Shape_Key]"',
    'name="Shape Key Start Value"': 'name="Shape Key Start Value [Start]"',
    'name="Shape Key End Value"': 'name="Shape Key End Value [End]"',
    'name="Selected Vertices Only"': 'name="Selected Vertices Only [Selected_Only]"',
    'name="Save Self Shape Key Transform"': 'name="Save Shape Transform [Save_Self]"',
    'name="Keep First Field for Debug"': 'name="Keep First Field [Debug_Keep]"',
    'name="Epsilon"': 'name="Epsilon [Eps]"',
    'name="Number of Steps"': 'name="Number of Steps [Steps]"',
    'name="Source Avatar Name"': 'name="Source Avatar Name [Src_Name]"',
    'name="Target Avatar Name"': 'name="Target Avatar Name [Tgt_Name]"',
    'name="Source Avatar Data"': 'name="Source Avatar Data [Src_Data]"',
    'name="Target Avatar Data"': 'name="Target Avatar Data [Tgt_Data]"',
    'name="Add Normal Control Points"': 'name="Add Normal Control Points [Add_Norm]"',
    'name="Normal Distance"': 'name="Normal Distance [Norm_Dist]"',
    'name="Enable X Mirror"': 'name="Enable X Mirror [X_Mirror]"',
    'name="Apply Shape Key Name"': 'name="Apply Shape Key Name [Key_Name]"',
    'name="Base Grid Spacing"': 'name="Base Grid Spacing [Grid_Space]"',
    'name="Surface Distance"': 'name="Surface Distance [Surf_Dist]"',
    'name="Max Distance"': 'name="Max Distance [Max_Dist]"',
    'name="Min Distance"': 'name="Min Distance [Min_Dist]"',
    'name="Density Falloff"': 'name="Density Falloff [Falloff]"',
    'name="BBox Scale Factor"': 'name="BBox Scale Factor [BBox_Scale]"',
    'name="Invert Pose"': 'name="Invert Pose [Inv_Pose]"',
    'name="Show Debug Info"': 'name="Show Debug Info [Debug_Info]"',
    'name="Field Step"': 'name="Field Step [Field_Step]"',
    'name="Use Inverse Data"': 'name="Use Inverse Data [Inv_Data]"',
    'name="Field Object Name"': 'name="Field Object Name [Obj_Name]"',
    
    # Interface Text Swaps
    'text="アバター設定"': 'text="Avatar Settings [Avatar_Set]"',
    'text="アバターデータファイル:"': 'text="Avatar Data Files:"',
    'text="ソース⇄ターゲット入れ替え"': 'text="Swap Source ⇄ Target [Swap_Obj]"',
    'text="Armatureオブジェクトを選択してください"': 'text="Please select an Armature object [Err_Arm]"',
    'text="ソースアバターデータファイルを設定してください"': 'text="Please set the source avatar data file [Err_Src]"',
    'text="ベースポーズ差分"': 'text="Base Pose Difference [Base_Pose]"',
    'text="ベースポーズを保存"': 'text="Save Base Pose [Save_Base]"',
    'text=f"保存先: {base_pose_filename}"': 'text=f"Saved To: {base_pose_filename}"',
    'text="ソースアバターを指定"': 'text="Assign source avatar data file [Assign_Src]"',
    'text="ソースアバター名を設定"': 'text="Set Source Avatar Name [Set_Src]"',
    'text="設定を完了してください"': 'text="Please complete the settings [Incomplete]"',
    'text="ベースポーズを適用"': 'text="Apply Base Pose [Apply_Base]"',
    'text="ポーズ差分"': 'text="Pose Difference [Pose_Diff]"',
    'text="ポーズを保存"': 'text="Save Pose [Save_Pose]"',
    'text=f"保存先: {pose_filename}"': 'text=f"Saved To: {pose_filename}"',
    'text="アバター名を設定してください"': 'text="Please set the Avatar name [Err_Name]"',
    'text="ポーズを適用"': 'text="Apply Pose [Apply_Pose]"',
    'text="ターゲットアバターデータファイルを指定"': 'text="Assign target avatar data file [Assign_Tgt]"',
    'text="変形フィールド設定"': 'text="Deformation Field Settings [Deform_Set]"',
    'text="シェイプキーを選択"': 'text="Select Shape Key [Sel_Key]"',
    'text="有効なシェイプキーがありません"': 'text="No valid shape keys found [No_Keys]"',
    'text="ソースオブジェクトにシェイプキーがありません"': 'text="Source mesh has no shape keys [Mesh_No_Keys]"',
    'text="開始値"': 'text="Start"',
    'text="終了値"': 'text="End"',
    'text="開始値と終了値は異なる値を設定してください"': 'text="Start and End values must be different [Val_Err]"',
    'text="RBF変形設定:"': 'text="RBF Deformation Settings:"',
    'text="法線制御点設定:"': 'text="Normal Control Point Settings:"',
    'text="グリッド設定:"': 'text="Grid Settings:"',
    'text="距離減衰設定:"': 'text="Distance Attenuation Settings:"',
    'text="変形を保存（シングルスレッド）"': 'text="Save (Single-Thread) [Save_Single]"',
    'text="一時データエクスポート＆マルチスレッド処理"': 'text="Export Temp & Process (Multi-Thread) [Run_Multi]"',
    'text="※ rbf_multithread_processor.pyが同じフォルダに必要です"': 'text="* rbf_multithread_processor.py must be in the same directory"',
    'text="保存した変形データを適用"': 'text="Apply Saved Deformation Data [Apply_Saved]"',
    'text="変形データ適用"': 'text="Apply Data [Apply_Data]"',
    'text="逆変形データ適用"': 'text="Apply Inverse [Apply_Inv]"',
    'text="フィールド可視化"': 'text="Field Visualization [Field_Vis]"',
    'text="フィールドを可視化"': 'text="Visualize Field [Run_Vis]"'
}

def browse_folder():
    folder = filedialog.askdirectory(title="Select MochiFitter Addon Folder")
    if folder:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, folder)

def clear_cache(addon_folder):
    cache_folder = os.path.join(addon_folder, "__pycache__")
    if os.path.exists(cache_folder):
        shutil.rmtree(cache_folder)

def run_patch():
    addon_folder = path_entry.get().strip()
    if not addon_folder or not os.path.exists(addon_folder):
        messagebox.showerror("Error", "Please select a valid folder path!")
        return

    patched_files = 0
    try:
        has_backups = any(f.endswith('.bak') for root, _, files in os.walk(addon_folder) for f in files)
        if has_backups:
            restore_backups_silently(addon_folder)

        for root, dirs, files in os.walk(addon_folder):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    backup_path = file_path + '.bak'
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    modified = False
                    for jp_code, en_code in TRANSLATION_MAP.items():
                        if jp_code in content:
                            content = content.replace(jp_code, en_code)
                            modified = True
                    
                    if modified:
                        if not os.path.exists(backup_path):
                            shutil.copy2(file_path, backup_path)
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        patched_files += 1

        clear_cache(addon_folder)

        if patched_files > 0:
            messagebox.showinfo("Success", f"Successfully translated {patched_files} files!\nRestart Blender to view.")
        else:
            messagebox.showwarning("Notice", "No Japanese MochiFitter UI strings found.")
            
    except Exception as e:
        messagebox.showerror("Execution Error", f"An error occurred: {str(e)}")

def restore_backups_silently(addon_folder):
    for root, dirs, files in os.walk(addon_folder):
        for file in files:
            if file.endswith('.py.bak'):
                backup_path = os.path.join(root, file)
                original_path = backup_path[:-4]
                shutil.move(backup_path, original_path)

def run_revert():
    addon_folder = path_entry.get().strip()
    if not addon_folder or not os.path.exists(addon_folder):
        messagebox.showerror("Error", "Please select a valid folder path!")
        return

    reverted_files = 0
    try:
        for root, dirs, files in os.walk(addon_folder):
            for file in files:
                if file.endswith('.py.bak'):
                    backup_path = os.path.join(root, file)
                    original_path = backup_path[:-4]
                    shutil.move(backup_path, original_path)
                    reverted_files += 1
        
        clear_cache(addon_folder)

        if reverted_files > 0:
            messagebox.showinfo("Revert Complete", f"Successfully restored {reverted_files} files back to the original Japanese code!")
        else:
            messagebox.showwarning("Notice", "No backup files (.bak) were found to restore.")
    except Exception as e:
        messagebox.showerror("Revert Error", f"An error occurred while reverting: {str(e)}")

# Setup GUI layout window
root = tk.Tk()
root.title("MochiFitter English UI Patcher")
root.geometry("540x220")
root.resizable(False, False)

instructions = tk.Label(root, text="Select the 'mochifitter' folder inside your Blender directory:", font=("Arial", 10))
instructions.pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=5, fill='x', padx=20)

path_entry = tk.Entry(frame, width=45)
path_entry.pack(side=tk.LEFT, padx=5, expand=True, fill='x')

browse_btn = tk.Button(frame, text="Browse...", command=browse_folder)
browse_btn.pack(side=tk.RIGHT, padx=5)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=20)

patch_btn = tk.Button(btn_frame, text="Translate Addon (Clean English)", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), command=run_patch, pady=8, padx=10)
patch_btn.pack(side=tk.LEFT, padx=10)

revert_btn = tk.Button(btn_frame, text="Restore Original Japanese", bg="#f44336", fg="white", font=("Arial", 10, "bold"), command=run_revert, pady=8, padx=10)
revert_btn.pack(side=tk.RIGHT, padx=10)

root.mainloop()

import PyInstaller.__main__
if __name__ == "__main__":
    PyInstaller.__main__.run(['--noconsole', '--onefile', __file__])
