#!/usr/bin/env python3
"""
Deps - Smart Dependency Assistant with personality
Usage:
    deps.py --dev /path/to/project
    deps.py --packageit /path/to/project
"""

import sys
import os
import subprocess
import ast
import venv
import shutil
import time

PIP_MAP = {
    "PIL": "Pillow",
    "cv2": "opencv-python",
    "pytube": "pytube",
}

def print_thinking(msg):
    print(f"🤔 {msg}")
    time.sleep(0.6)  

def print_action(msg):
    print(f" {msg}")

def scan_imports(file_path):
    imports = set()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=file_path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split(".")[0])
    except Exception as e:
        print(f"Could not scan {file_path}: {e}")
    return imports

def find_python_files(root_path):
    py_files = []
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files

def map_to_pip(imports):
    pip_packages = set()
    for imp in imports:
        if imp in PIP_MAP:
            pip_packages.add(PIP_MAP[imp])
    return pip_packages

def create_venv(path):
    venv_path = os.path.join(path, ".venv")
    if not os.path.exists(venv_path):
        print_action(f"Creating a virtual environment at {venv_path}...")
        venv.create(venv_path, with_pip=True)
    else:
        print_thinking("Found an existing virtual environment. I'll use it.")
    pip_path = os.path.join(venv_path, "bin", "pip")
    return pip_path

def install_package(pip_path, package):
    print_thinking(f"I will try to install '{package}'...")
    try:
        subprocess.run([pip_path, "install", package], check=True)
        print_action(f"Installed {package} successfully!")
    except subprocess.CalledProcessError:
        print(f"I found no installation candidate for '{package}'. I'll exit now.")
        sys.exit(1)

def dev_mode(path):
    py_files = find_python_files(path)
    all_imports = set()
    for f in py_files:
        all_imports.update(scan_imports(f))

    pip_packages = map_to_pip(all_imports)
    if not pip_packages:
        print_action("Looks like you don't need me! All dependencies are satisfied.")
        return

    pip_path = create_venv(path)
    for pkg in pip_packages:
        install_package(pip_path, pkg)
    print_action("Dev environment is ready. Go make something awesome!")

def packageit_mode(path):
    print_action("Packaging your project with embedded Deps assistant...")
    assistant_code = f"""#!/usr/bin/env python3
# Auto-generated deps assistant
import subprocess, os, ast, venv, sys, time
PIP_MAP = {PIP_MAP}

def scan_imports(file_path):
    imports = set()
    with open(file_path, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read())
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split('.')[0])
    return imports

def main():
    files = [os.path.join(dp,f) for dp,dn,fn in os.walk('.') for f in fn if f.endswith('.py')]
    imports = set()
    for f in files:
        imports.update(scan_imports(f))
    missing = [PIP_MAP[i] for i in imports if i in PIP_MAP]
    if missing:
        print('Missing packages:', missing)
        venv_path = './.venv'
        if not os.path.exists(venv_path):
            venv.create(venv_path, with_pip=True)
        pip_path = os.path.join(venv_path, 'bin', 'pip')
        for pkg in missing:
            try:
                subprocess.run([pip_path, 'install', pkg], check=True)
                print(f'Installed {{pkg}} successfully!')
            except:
                print(f'Could not find installation candidate for {{pkg}}. Exiting.')
                sys.exit(1)
    else:
        print('All dependencies satisfied!')

if __name__ == '__main__':
    main()
"""
    out_path = os.path.join(path, "deps_assistant.py")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(assistant_code)
    os.chmod(out_path, 0o755)
    print_action(f"✅ Embedded deps_assistant created at {out_path}")

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    mode, path = sys.argv[1], sys.argv[2]
    if not os.path.exists(path):
        print(f"Path {path} does not exist")
        sys.exit(1)
    if mode == "--dev":
        dev_mode(path)
    elif mode == "--packageit":
        packageit_mode(path)
    else:
        print(f"Unknown mode {mode}. Use --dev or --packageit")
        sys.exit(1)

if __name__ == "__main__":
    main()
