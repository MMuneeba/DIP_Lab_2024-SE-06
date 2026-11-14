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

<!-- AUTO-GENERATED-README:START -->
## Lab Overview

**Topic:** Geometric Transformations with Custom Inputs

This section describes the files currently present in this lab folder.
It does not assume that every assigned exercise is completed.

## Repository Files

- [`2024-SE-06-LAB04.ipynb`](./2024-SE-06-LAB04.ipynb)
- [`generate_input_image.py`](./generate_input_image.py)
- [`input_image.png`](./input_image.png)
- [`requirements.txt`](./requirements.txt)
- [`saved_results/01_scale_enlarge_proportional_1.5x_bicubic.png`](./saved_results/01_scale_enlarge_proportional_1.5x_bicubic.png)
- [`saved_results/02_scale_reduce_proportional_0.5x_bilinear.png`](./saved_results/02_scale_reduce_proportional_0.5x_bilinear.png)
- [`saved_results/03_scale_nonproportional_fx1.8_fy0.6_lanczos.png`](./saved_results/03_scale_nonproportional_fx1.8_fy0.6_lanczos.png)
- [`saved_results/04_crop_cabin_and_lake_600_380_960_640.png`](./saved_results/04_crop_cabin_and_lake_600_380_960_640.png)
- [`saved_results/05_crop_mountain_sky_380_120_800_330.png`](./saved_results/05_crop_mountain_sky_380_120_800_330.png)
- [`saved_results/06_flip_both.png`](./saved_results/06_flip_both.png)
- [`saved_results/06_flip_horizontal.png`](./saved_results/06_flip_horizontal.png)
- [`saved_results/06_flip_vertical.png`](./saved_results/06_flip_vertical.png)
- [`saved_results/07_translate_tx+150_ty+80.png`](./saved_results/07_translate_tx+150_ty+80.png)
- [`saved_results/08_translate_tx-120_ty-60.png`](./saved_results/08_translate_tx-120_ty-60.png)
- [`saved_results/09_rotate_+30_no_expand.png`](./saved_results/09_rotate_+30_no_expand.png)
- [`saved_results/10_rotate_+30_expand.png`](./saved_results/10_rotate_+30_expand.png)
- [`saved_results/11_rotate_-45_expand.png`](./saved_results/11_rotate_-45_expand.png)
- [`saved_results/12_interpolation_bicubic_x8.png`](./saved_results/12_interpolation_bicubic_x8.png)
- [`saved_results/12_interpolation_bilinear_x8.png`](./saved_results/12_interpolation_bilinear_x8.png)
- [`saved_results/12_interpolation_lanczos_x8.png`](./saved_results/12_interpolation_lanczos_x8.png)
- [`saved_results/12_interpolation_nearest_x8.png`](./saved_results/12_interpolation_nearest_x8.png)
- [`saved_results/interactive_01_scale.png`](./saved_results/interactive_01_scale.png)
- [`saved_results/interactive_02_rotate.png`](./saved_results/interactive_02_rotate.png)
- [`saved_results/interactive_03_crop.png`](./saved_results/interactive_03_crop.png)

## File Summary

- Total files detected: 24
- Folder: `DIP_Lab_04`
- Documentation is refreshed automatically when repository changes are pushed.
<!-- AUTO-GENERATED-README:END -->
