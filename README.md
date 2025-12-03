# Code and data for: Fine-Tuning Bulk-oriented Universal Interatomic Potentials for Surfaces: Accuracy, Efficiency, and Forgetting Control

This repository contains the training commands, post-processing scripts, and figure source data used in the manuscript:

> **Fine-Tuning Bulk-oriented Universal Interatomic Potentials for Surfaces: Accuracy, Efficiency, and Forgetting Control**
> Jaekyun Hwang¹, Taehun Lee², Yonghyuk Lee³,* , Su-Hyun Yoo¹,*

¹ Digital Chemical Research Center, Korea Research Institute of Chemical Technology, Daejeon 34114, Republic of Korea
² Division of Advanced Materials Engineering, Jeonbuk National University, Jeonju 54896, Republic of Korea
³ Department of Chemical and Biochemical Engineering, Dongguk University, Seoul 04620, Republic of Korea

Preprint: https://arxiv.org/abs/2509.25807

The main purpose of this repository is to make it possible to **reproduce the trained models and the key figures** (especially the force comparison and kernel density estimation shown in Figure 3), using the same settings as in the paper.

---

## Repository structure

```text
project/
├─ train/
│   ├─ train_mace.sh
├─ postprocessing/
│   ├─ force_compare.py
├─ kernel_density_estimation/
│   ├─ Fig_3.py
│   ├─ Fig_3.csv
│   ├─ Fig_3.png
├─ data/
│   ├─ Fig_2a.csv
│   ├─ Fig_2b.csv
│   ├─ ...
└─ environment.yml
```

---

## How to use this repository

### 1. Set up the environment

`environment.yml` is a conda environment specification exported from the environment used to run the experiments.

You can recreate the environment with:

```bash
conda env create -n <ENV_NAME> -f environment.yml
conda activate <ENV_NAME>
```

---

### 2. Train the models (`train/`)

- **`train/train_mace.sh`**
  Shell script that collects representative command-line calls used to train the MACE models in the paper.

  - The script is written based on the Au system and shows the exact options for three training strategies (training from scratch, fine-tuning, multi-head fine-tuning).
  - For other systems, the same commands can be reused by changing only the training epoch parameter (`max_num_epochs`), keeping all other options identical.

  This script serves as a **template for all training runs**: to reproduce another system, start from the Au command and modify only the number of epochs as needed.

From the project root:

```bash
cd train
bash train_mace.sh
```

This will train the Au models as configured in `train_mace.sh`.
To train other systems, reuse the same commands and adjust only `max_num_epochs` as described above, while keeping all other options the same.

> **Note:** The raw DFT datasets are **not** redistributed in this repository.
> Please follow the instructions in the manuscript to obtain the original data and adapt the data paths in `train_mace.sh` accordingly.

---

### 3. Generate force comparison data (`postprocessing/`)

- **`postprocessing/force_compare.py`**
  Python script used to compute the absolute values of the reference forces (`forces`) and the MACE-predicted forces (`MACE_forces`), and to analyze the resulting force errors.
  The output is used as the input data for the kernel density estimation in Figure 3.

Example usage:

```bash
cd postprocessing
python force_compare.py ../train/test_MACE_predicted.extxyz
```

The script reads in the forces used in the study (reference forces and corresponding MACE_forces from the same file), computes `|F_DFT|`, `|F_MACE|`, and writes them into `Fig_3.csv` in a tabular format suitable for further analysis and plotting.

---

### 4. Plot Figure 3 (`kernel_density_estimation/`)

- **`kernel_density_estimation/Fig_3.csv`**
  CSV file containing the processed data used to produce Figure 3.
  (Created by `postprocessing/force_compare.py`.)

- **`kernel_density_estimation/Fig_3.py`**
  Python script that reads `Fig_3.csv` and generates the kernel density estimation (KDE) plot corresponding to Figure 3 in the manuscript.

  Example usage:

  ```bash
  cd ../kernel_density_estimation
  python Fig_3.py
  ```

  This script performs the KDE and produces a figure file (`Fig_3.png`).

- **`kernel_density_estimation/Fig_3.png`**
  An output plot of Figure 3.
  The figure can always be regenerated from `Fig_3.csv` and `Fig_3.py`.

---

### 5. Figure source data (`data/`)

- **`data/Fig_2a.csv`, `data/Fig_2b.csv`, ...**
  Source data for all figures.
  Each CSV corresponds to one panel or subfigure.

  Please adapt the following description to match your actual columns:

  - `Fig_2a.csv`: training set size vs. energy/force RMSE for a given system.
  - `Fig_2b.csv`: diatomic potential energy curve data (e.g., distance, DFT energy, predicted energy).
  - Additional files follow the same idea for other figures.

These files are provided to make it straightforward to reproduce the plots in the paper or to perform additional analysis.

---

## Citation

If you use this code or data in your own work, please cite:

> Jaekyun Hwang, Taehun Lee, Yonghyuk Lee, and Su-Hyun Yoo,
> *Fine-Tuning Bulk-oriented Universal Interatomic Potentials for Surfaces: Accuracy, Efficiency, and Forgetting Control*,
> arXiv:2509.25807 (2025).

A journal citation can be added here once the paper is accepted.

---

## License

MIT License

Copyright (c) 2025 Jaekyun Hwang
