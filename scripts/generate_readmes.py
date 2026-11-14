
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LABS = {
    "DIP_Lab_01": "Python Setup, Fundamentals, and Imports",
    "DIP_Lab_02": "Digital Images, Pixels, Color, and Basic Transformations",
    "DIP_Lab_03": "Image Enhancement and Intensity Transformations",
    "DIP_Lab_04": "Geometric Transformations with Custom Inputs",
}

START = "<!-- AUTO-GENERATED-README:START -->"
END = "<!-- AUTO-GENERATED-README:END -->"

IGNORE = {
    ".git", ".venv", "venv", "__pycache__",
    ".ipynb_checkpoints", "node_modules"
}


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


def update_readme(path, title, content):
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        old = path.read_text(encoding="utf-8")
    else:
        old = f"# {title}\n\n"

    section = f"{START}\n{content.strip()}\n{END}"

    if START in old and END in old:
        before = old.split(START)[0]
        after = old.split(END, 1)[1]
        updated = before + section + after
    else:
        updated = old.rstrip() + "\n\n" + section + "\n"

    path.write_text(updated, encoding="utf-8")


def main():
    # Generate individual lab READMEs
    for folder_name, title in LABS.items():
        lab_folder = ROOT / folder_name

        if not lab_folder.is_dir():
            continue

        files = get_files(lab_folder)

        if files:
            file_list = "\n".join(
                f"- [`{name}`](./{name})" for name in files
            )
        else:
            file_list = "- No project files found yet."

        content = f"""
## Lab Overview

**Topic:** {title}

This section describes the files currently present in this lab folder.
It does not assume that every assigned exercise is completed.

## Repository Files

{file_list}

## File Summary

- Total files detected: {len(files)}
- Folder: `{folder_name}`
- Documentation is refreshed automatically when repository changes are pushed.
"""

        update_readme(
            lab_folder / "README.md",
            title,
            content
        )

    # Generate main repository README section
    lab_links = []

    for folder_name, title in LABS.items():
        if (ROOT / folder_name).is_dir():
            lab_links.append(
                f"- [{folder_name}: {title}]({folder_name}/README.md)"
            )

    main_content = f"""
## Digital Image Processing Labs

This repository contains practical work for the Digital Image Processing
course.

### Lab Documentation

{chr(10).join(lab_links)}

### Automatic Documentation

README documentation is refreshed using a Python script and GitHub Actions.
The generated file lists reflect the files detected in the repository.

### Last Repository Scan

The documentation was generated during the latest GitHub Actions run.
"""

    update_readme(
        ROOT / "README.md",
        "Digital Image Processing Lab",
        main_content
    )

    print("README files updated successfully!")


if __name__ == "__main__":
    main()
