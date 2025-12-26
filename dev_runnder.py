import bpy
import os
import sys
import traceback

TARGET_SCRIPT = "main.py"

def run_external_script():
    blend_path = bpy.data.filepath
    if not blend_path:
        print("[Error] Please save .blend file first!")
        return

    project_dir = os.path.dirname(blend_path)
    if project_dir not in sys.path:
        sys.path.append(project_dir)

    script_path = os.path.join(project_dir, TARGET_SCRIPT)
    
    print(f"\n--- Running: {TARGET_SCRIPT} ---")
    try:
        global_namespace = {"__name__": "__main__"}
        with open(script_path, 'r', encoding='utf-8') as f:
            exec(compile(f.read(), script_path, 'exec'), global_namespace)
        print("--- Done ---")
    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    run_external_script()