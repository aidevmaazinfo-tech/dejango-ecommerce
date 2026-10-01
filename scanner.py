import os
from pathlib import Path

def generate_tree(dir_path, output_file, exclude_dirs=None):
    if exclude_dirs is None:
        exclude_dirs = {'.git', '__pycache__', 'venv', 'env', '.idea', 'media', 'staticfiles'}
        
    root_path = Path(dir_path)
    
    if not root_path.exists():
        print(f"Error: Path {root_path} does not exist.")
        return

    lines = []
    lines.append(f"Project Structure for: {root_path.resolve()}\n")
    
    def walk_dir(current_path, prefix=""):
        try:
            items = sorted(list(current_path.iterdir()), key=lambda x: (not x.is_dir(), x.name.lower()))
        except PermissionError:
            return

        items = [item for item in items if item.name not in exclude_dirs]

        for index, item in enumerate(items):
            connector = "└── " if index == len(items) - 1 else "├── "
            lines.append(f"{prefix}{connector}{item.name}")
            
            if item.is_dir():
                extension = "    " if index == len(items) - 1 else "│   "
                walk_dir(item, prefix + extension)

    walk_dir(root_path)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
        
    print(f"Directory structure successfully saved to: {output_file}")

if __name__ == "__main__":
    target_directory = r"C:\Hassan\django_First_project--main"
    output_txt = "django_project_structure.txt"
    generate_tree(target_directory, output_txt)