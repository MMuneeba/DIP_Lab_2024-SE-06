
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

START = "<!-- AUTO-GENERATED-README:START -->"
END = "<!-- AUTO-GENERATED-README:END -->"

IGNORE = {
    ".git", ".venv", "venv", "__pycache__",
    ".ipynb_checkpoints", "node_modules"
}

# Detailed information for existing labs
LAB_INFO = {
    "DIP_Lab_01": {
        "title": "Python Setup, Fundamentals, and Imports",
        "objective": "Learn Python setup, programming fundamentals, functions, collections, and package imports.",
        "topics": [
            "Python installation and VS Code",
            "Variables and data types",
            "Conditional statements and loops",
            "Functions and collections",
            "Installing and importing libraries"
        ]
    },
    "DIP_Lab_02": {
        "title": "Digital Images, Pixels, Color, and Basic Transformations",
        "objective": "Load, inspect, display, analyze, and transform digital images.",
        "topics": [
            "Image dimensions and pixel values",
            "RGB, BGR, and grayscale",
            "Color channels",
            "Cropping and resizing",
            "Histograms and bit depth"
        ]
    },
    "DIP_Lab_03": {
        "title": "Image Enhancement and Intensity Transformations",
        "objective": "Implement and compare image enhancement and intensity transformations.",
        "topics": [
            "Brightness and contrast",
            "Image negative",
            "Gamma correction",
            "Histogram equalization",
            "CLAHE and thresholding"
        ]
    },
    "DIP_Lab_04": {
        "title": "Geometric Transformations with Custom Inputs",
        "objective": "Apply geometric transformations using custom parameters and input validation.",
        "topics": [
            "Scaling and resizing",
            "Cropping and flipping",
            "Image translation and rotation",
            "Interpolation methods",
            "Canvas expansion and validation"
        ]
    }
}


def get_title(folder_name):
    if folder_name in LAB_INFO:
        return LAB_INFO[folder_name]["title"]

    number = folder_name.replace("DIP_Lab_", "")
    return f"Digital Image Processing - Lab {number}"


def get_files(folder):
    files = []

    for path in sorted(folder.rglob("*")):
        if not path.is_file():
            continue

        relative = path.relative_to(folder)

        if any(part in IGNORE for part in relative.parts):
            continue

        if path.name.lower() == "readme.md":
            continue

        files.append(relative.as_posix())

    return files


def categorize_files(files):
    categories = {
        "Python Files": [],
        "Jupyter Notebooks": [],
        "Images and Outputs": [],
        "Reports and Documents": [],
        "Other Files": []
    }

    for filename in files:
        ext = Path(filename).suffix.lower()

        if ext == ".py":
            categories["Python Files"].append(filename)
        elif ext == ".ipynb":
            categories["Jupyter Notebooks"].append(filename)
        elif ext in [".png", ".jpg", ".jpeg", ".bmp", ".gif"]:
            categories["Images and Outputs"].append(filename)
        elif ext in [".pdf", ".docx", ".doc"]:
            categories["Reports and Documents"].append(filename)
        else:
            categories["Other Files"].append(filename)

    return categories


def file_links(files):
    if not files:
        return "- No files detected yet."

    return "\n".join(
        f"- [`{name}`](./{name})" for name in files
    )


def make_lab_content(folder_name, title, files):
    info = LAB_INFO.get(folder_name)

    if info:
        objective = info["objective"]
        topics = "\n".join(
            f"- {topic}" for topic in info["topics"]
        )
    else:
        objective = (
            "This lab folder was detected automatically. "
            "Add its assignment objectives and topics to the "
            "project documentation when available."
        )
        topics = (
            "- Topics will be documented when assignment details "
            "are available."
        )

    categories = categorize_files(files)

    file_sections = []

    for category, category_files in categories.items():
        if category_files:
            file_sections.append(
                f"### {category}\n\n{file_links(category_files)}"
            )

    grouped_files = "\n\n".join(file_sections)

    return f"""
## Lab Overview

{objective}

## Topics Covered

{topics}

## Repository Files

{grouped_files if grouped_files else "No files detected yet."}

## Lab Statistics

- Lab folder: `{folder_name}`
- Total detected files: **{len(files)}**

## Documentation Note

This README is automatically updated using the files detected
inside this folder. File presence does not confirm that every
assignment requirement has been completed.
"""


def update_readme(path, title, content):
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        old = path.read_text(encoding="utf-8")
    else:
        old = f"# {title}\n\n"

    section = f"{START}\n{content.strip()}\n{END}"

    if START in old and END in old:
        before = old.split(START, 1)[0]
        after = old.split(END, 1)[1]
        updated = before + section + after
    else:
        updated = old.rstrip() + "\n\n" + section + "\n"

    path.write_text(updated, encoding="utf-8")


def main():
    lab_folders = sorted(
        folder for folder in ROOT.glob("DIP_Lab_*")
        if folder.is_dir()
    )

    lab_links = []

    for folder in lab_folders:
        folder_name = folder.name
        title = get_title(folder_name)
        files = get_files(folder)

        content = make_lab_content(
            folder_name, title, files
        )

        update_readme(
            folder / "README.md",
            title,
            content
        )

        lab_links.append(
            f"- [{folder_name}: {title}]"
            f"({folder_name}/README.md) — {len(files)} files"
        )

        print(f"Updated: {folder_name}/README.md")

    main_content = f"""
## About This Repository

Digital Image Processing practical work and lab documentation.

## Lab Documentation

{chr(10).join(lab_links) if lab_links else "No lab folders detected."}

## Technologies

- Python
- Jupyter Notebook
- NumPy
- OpenCV
- Matplotlib

## Automatic Documentation

This README and individual lab README files are updated
automatically using Python and GitHub Actions.

New folders matching `DIP_Lab_*` are detected automatically.

## Documentation Accuracy

File lists are generated from repository contents.
Assignment completion is not automatically verified.
"""

    update_readme(
        ROOT / "README.md",
        "Digital Image Processing Lab",
        main_content
    )

    print("All README files generated successfully!")


if __name__ == "__main__":
    main()
