# Lab Task 04 – Geometric Transformations with Custom Inputs
Digital Image Processing Lab, Department of Software Engineering, University of Azad Jammu and Kashmir
(Semester 5, Session 2024-28)

**Student:** `<YOUR FULL NAME>`  **Roll No:** `2024-SE-<YOUR ROLL NO>`

## Contents
| File / folder | Description |
|---|---|
| `2024-SET-YOUR_ROLL_NO-LAB04.ipynb` | Completed notebook (rename `YOUR_ROLL_NO` to your roll number) |
| `input_image.png` | Input image (sunset over a mountain lake, 960×640) |
| `generate_input_image.py` | Helper script that generated the input image |
| `saved_results/` | All transformed images saved by the notebook |
| `requirements.txt` | Python packages needed |

## How to run
```
pip install -r requirements.txt
jupyter notebook
```
Open the notebook and choose **Kernel → Restart & Run All**. The cell in section 6 is interactive: type an
operation (`scale`, `crop`, `flip`, `translate`, `rotate`) and its parameters when asked (type `quit` to finish).

## What the notebook contains
* one reusable function `transform(image, operation, **params)` with full input validation
* interactive prompts that re-ask on invalid input
* demonstrations of all five operations with custom values, saved to `saved_results/`
* nearest / bilinear / bicubic / Lanczos comparison on an enlarged patch
* rejected-input examples for every operation, identity and correctness checks (Pass/Fail table)
* short explanations: coordinates vs array indexing, aspect ratio, canvas expansion, translation clipping
