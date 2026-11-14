
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LABS = {
    "DIP_Lab_01": {
        "title": "Python Setup, Fundamentals, and Imports",
        "objective": (
            "Learn Python setup, basic programming concepts, "
            "functions, collections, and package imports."
        ),
        "topics": [
            "Python installation and VS Code setup",
            "Variables and data types",
            "Conditional statements",
            "For and while loops",
            "Functions and return values",
            "Lists, tuples, dictionaries, and sets",
            "Installing and importing Python libraries",
        ],
        "outcomes": [
            "Understand basic Python syntax.",
            "Write conditional statements and loops.",
            "Create reusable functions.",
            "Work with Python collections.",
            "Install and import external packages.",
        ],
        "tools": ["Python", "VS Code", "NumPy", "Pillow", "Matplotlib"],
    },

    "DIP_Lab_02": {
        "title": "Digital Images, Pixels, Color, and Basic Transformations",
        "objective": (
            "Load, inspect, display, analyze, and transform digital "
            "images using Python libraries."
        ),
        "topics": [
            "Reading and displaying digital images",
            "Image dimensions, shape, and data types",
            "Pixel coordinates and pixel values",
            "RGB and BGR color spaces",
            "Grayscale conversion and color channels",
            "Image cropping and resizing",
            "Grayscale histograms",
            "Image bit depth and intensity levels",
        ],
        "outcomes": [
            "Understand image dimensions and pixel values.",
            "Identify color channels.",
            "Convert color images to grayscale.",
            "Crop and resize images.",
            "Plot grayscale histograms.",
            "Understand resolution and bit depth.",
        ],
        "tools": ["Python", "Jupyter Notebook", "NumPy", "OpenCV", "Matplotlib"],
    },

    "DIP_Lab_03": {
        "title": "Image Enhancement and Intensity Transformations",
        "objective": (
            "Implement and compare intensity transformations and "
            "histogram-based image enhancement techniques."
        ),
        "topics": [
            "Brightness adjustment",
            "Linear contrast enhancement",
            "Contrast stretching",
            "Image negative transformation",
            "Gamma correction",
            "Grayscale histogram analysis",
            "Histogram equalization",
            "CLAHE",
            "Binary thresholding",
            "Otsu thresholding",
            "Adaptive Gaussian thresholding",
        ],
        "outcomes": [
            "Apply brightness and contrast transformations.",
            "Understand gamma correction.",
            "Analyze grayscale histograms.",
            "Perform histogram equalization.",
            "Apply global and adaptive thresholding.",
            "Compare image enhancement results.",
        ],
        "tools": ["Python", "Jupyter Notebook", "NumPy", "OpenCV", "Matplotlib"],
    },

    "DIP_Lab_04": {
        "title": "Geometric Transformations with Custom Inputs",
        "objective": (
            "Build a reusable image transformation function that "
            "accepts custom parameters and validates user inputs."
        ),
        "topics": [
            "Image scaling and resizing",
            "Image cropping",
            "Horizontal and vertical flipping",
            "Image translation",
            "Image rotation",
            "Interpolation methods",
            "Canvas expansion and clipping",
            "Input validation and error handling",
        ],
        "outcomes": [
            "Resize images using custom scale factors.",
            "Crop images using coordinate boundaries.",
            "Flip images in different directions.",
            "Translate images using custom offsets.",
            "Rotate images with optional canvas expansion.",
            "Validate transformation parameters.",
            "Compare interpolation methods.",
        ],
        "tools": ["Python", "Jupyter Notebook", "NumPy", "OpenCV", "Matplotlib"],
    },
}

START = "<!-- AUTO-GENERATED-README:START -->"
END = "<!-- AUTO-GENERATED-README:END -->"

IGNORE = {
    ".git", ".venv", "venv", "__pycache__",
    ".ipynb_checkpoints", "node_modules"
}

CATEGORIES = {
    "Python files": {".py"},
    "Jupyter notebooks": {".ipynb"},
    "Images and outputs": {".png", ".jpg", ".jpeg", ".bmp", ".gif"},
    "Reports and documents": {".pdf", ".docx", ".doc"},
    "Other files": set(),
}


def get_files(folder):
    result = []

    for path in sorted(folder.rglob("*")):
        if not path.is_file():
            continue

        relative = path.relative_to(folder)

        if any(part in IGNORE for part in relative.parts):
            continue

        if path.name.lower() == "readme.md":
            continue

        result.append(relative.as_posix())

    return result


def categorize_files(files):
    groups = {name: [] for name in CATEGORIES}

    for filename in files:
        extension = Path(filename).suffix.lower()
        matched = False

        for category, extensions in CATEGORIES.items():
            if extension in extensions:
                groups[category].append(filename)
                matched = True
                break

        if not matched:
            groups["Other files"].append(filename)

    return groups


def make_file_list(files):
    if not files:
        return "- No files detected yet."

    return "\n".join(
        f"- [`{name}`](./{name})" for name in files
    )


def make_documentation(folder_name, info, files):
    groups = categorize_files(files)

    sections = []

    for category, category_files in groups.items():
        if category_files:
            sections.append(
                f"### {category}\n\n{make_file_list(category_files)}"
            )

    file_sections = "\n\n".join(sections)

    topics = "\n".join(f"- {item}" for item in info["topics"])
    outcomes = "\n".join(f"- {item}" for item in info["outcomes"])
    tools = ", ".join(info["tools"])

    return f"""
## Lab Overview

{info["objective"]}

## Topics Covered

{topics}

## Learning Outcomes

{outcomes}

## Tools and Technologies

{tools}

## Repository Files

The following files were detected automatically in this lab folder.

{file_sections}

## Lab Statistics

- Lab folder: `{folder_name}`
- Total detected files: **{len(files)}**

## Documentation Note

This README is automatically refreshed when repository changes are pushed.
The file list reflects the current repository contents. It does not
automatically verify that every assignment exercise is complete.
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
    lab_links = []

    for folder_name, info in LABS.items():
        folder = ROOT / folder_name

        if not folder.is_dir():
            print(f"Skipping missing folder: {folder_name}")
            continue

        files = get_files(folder)
        content = make_documentation(folder_name, info, files)

        update_readme(
            folder / "README.md",
            info["title"],
            content
        )

        lab_links.append(
            f"- [{folder_name} — {info['title']}]"
            f"({folder_name}/README.md) — {len(files)} files"
        )

        print(f"Updated: {folder_name}/README.md")

    main_content = f"""
## About This Repository

This repository contains practical work for the
**Digital Image Processing** course.

## Lab Documentation

{chr(10).join(lab_links)}

## Technologies Used

- Python
- Jupyter Notebook
- NumPy
- OpenCV
- Matplotlib

## Automatic Documentation System

Individual lab README files and this main README are refreshed
automatically using Python and GitHub Actions.

## Documentation Accuracy

Lab descriptions are based on the assignment topics.
Repository file lists are detected automatically.
File presence alone does not confirm assignment completion.
"""

    update_readme(
        ROOT / "README.md",
        "Digital Image Processing Lab",
        main_content
    )

    print("All available README files updated successfully!")


if __name__ == "__main__":
    main()
