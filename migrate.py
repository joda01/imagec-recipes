import os
import re

def migrate_conanfile_py(file_path):
    """
    Update a `conanfile.py` to be compatible with Conan v2.
    """
    with open(file_path, "r") as file:
        content = file.read()

    # Replace `from conans` with `from conan`
    content = re.sub(r"from conans\.([a-zA-Z_]+) import", r"from conan.\1 import", content)

    # Update deprecated methods like `configure`, `source`, etc.
    replacements = {
        r"self\.default_options": "self.options",
        r"self\.source_folder": "self.source_path",
        r"self\.build_folder": "self.build_path",
        r"self\.package_folder": "self.package_path",
        r"self\.install_folder": "self.install_path",
    }

    for old, new in replacements.items():
        content = re.sub(old, new, content)

    with open(file_path, "w") as file:
        file.write(content)

    print(f"Updated {file_path} for Conan v2.")

def migrate_conanfile_txt(file_path):
    """
    Update a `conanfile.txt` to be compatible with Conan v2.
    """
    with open(file_path, "r") as file:
        lines = file.readlines()

    with open(file_path, "w") as file:
        for line in lines:
            # Replace deprecated generators with new ones
            if "generator" in line.lower():
                line = re.sub(r"cmake|cmake_multi", "CMakeDeps", line)
                line = re.sub(r"gcc", "GCCDeps", line)

            file.write(line)

    print(f"Updated {file_path} for Conan v2.")

def migrate_conan_files(base_dir):
    """
    Traverse a directory and migrate all Conan-related files.
    """
    for root, _, files in os.walk(base_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if file_name == "conanfile.py":
                migrate_conanfile_py(file_path)
            elif file_name == "conanfile.txt":
                migrate_conanfile_txt(file_path)

if __name__ == "__main__":
    # Path to the project directory
    project_dir = input("Enter the path to the project directory: ").strip()
    if os.path.isdir(project_dir):
        migrate_conan_files(project_dir)
        print("Migration completed.")
    else:
        print(f"Invalid directory: {project_dir}")
