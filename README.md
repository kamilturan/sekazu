# Sekazu

**Sekazu** is an integrated solution tool for **sex/gender determination from skeletal measurements** based on multiple **machine learning (ML) models** and a **graphical user interface (GUI)**.:contentReference[oaicite:0]{index=0}  

> This repository contains the source code, documentation, and example workflows for Sekazu.

---

## Table of Contents

- [Overview](#overview)  
- [Key Features](#key-features)  
- [Architecture & Workflow](#architecture--workflow)  
- [Machine Learning Models](#machine-learning-models)  
- [Tech Stack & Dependencies](#tech-stack--dependencies)  
- [Installation](#installation)  
- [Citing Sekazu](#citing-sekazu)  

---

## Overview

Gender determination is a key step in **forensic investigation, anthropology, archaeology and bioarchaeology**, especially when working with fragmented skeletal remains. Sekazu provides an end-to-end environment that:​:contentReference[oaicite:1]{index=1}  

- collects **2D landmark coordinates** on radiological or photographic bone images,  
- computes **metric features** (lengths, angles, areas, perimeters, etc.),  
- applies multiple **machine learning algorithms** for sex estimation,  
- reports performance using standard **classification metrics**.  

The system has been used on measurements from **9 different bones** (cranium, mandible, femur, patella, calcaneus, condylus occipitalis, sternum, hand bones and foot bones).:contentReference[oaicite:2]{index=2}  

---

## Key Features

- **Integrated Workflow**
  - From landmark definition → feature creation → labeling → feature computation → ML model training/testing.

- **GUI-Based Tools (PyQt5)**
  - No need to write code for routine workflows; everything is done via forms, tables and interactive views.:contentReference[oaicite:3]{index=3}  

- **Bone-Agnostic Design**
  - Any bone (or anatomical structure) can be analyzed by defining appropriate bookmarks and features.

- **Multiple ML Algorithms**
  - Decision Trees, Random Forests, Extra Trees, Gaussian Processes, Gradient Boosting, Naive Bayes, LDA, QDA, SVM and more.:contentReference[oaicite:4]{index=4}  

- **Exhaustive Feature Subset Search**
  - Tests all possible feature subsets with **k-fold cross-validation** and selects the best-performing set.

- **Rich Performance Reporting**
  - Accuracy, Sensitivity, Specificity, F1, PPV, NPV, MCC, FMI and confusion matrix are automatically computed and reported.:contentReference[oaicite:5]{index=5}  

- **Flexible Data I/O**
  - Uses common text/CSV-like formats for bookmarks, features and measurements, minimizing data transfer problems.:contentReference[oaicite:6]{index=6}  

---

## Architecture & Workflow

Sekazu is organized around **five main tools**, each accessible from the GUI:​:contentReference[oaicite:7]{index=7}  

1. **Bookmark Management Tool**
2. **Feature Management Tool**
3. **Labeling Management Tool**
4. **Calculation Tool**
5. **ML Model Tool**

A typical workflow is:

1. Define **bookmarks** (anatomical landmarks, tags, colors, planes).  
2. Build **features** from these bookmarks (length, angle, area, etc.).  
3. Label **cases** by placing bookmarks on images (collect x–y coordinates).  
4. Run **calculations** to obtain feature tables for all cases.  
5. Train and evaluate **ML models** on the calculated feature dataset.

The high-level flow chart is given in the original article (Figure 1).:contentReference[oaicite:8]{index=8}  

---

## Machine Learning Models

The ML Model Tool supports several scikit-learn–based classifiers:​:contentReference[oaicite:9]{index=9}  

- **Decision Tree Classifier (DTC)**  
- **Random Forest Classifier (RFC)**  
- **Extra Trees Classifier (ETC)**  
- **Gaussian Process Classifier (GPC)**  
- **Gradient Boosting Classifier (GBC)**  
- **Gaussian Naive Bayes (GNB)**  
- **Linear Discriminant Analysis (LDA)**  
- **Quadratic Discriminant Analysis (QDA)**  
- **Support Vector Machines (SVM)**  

Sekazu:

- Generates all **feature subsets** (from size 1 to *n*)  
- For each subset, performs **k-fold cross-validation** (k user-defined, e.g. 3, 5, 10)  
- Computes performance metrics and identifies the **best subset** for gender determination.:contentReference[oaicite:10]{index=10}  

---

## Tech Stack & Dependencies

Sekazu is implemented in **Python 3.5.8 (64-bit)** and uses the following core packages:​:contentReference[oaicite:11]{index=11}  

| Package       | Version  | Purpose                          |
|--------------|----------|----------------------------------|
| NumPy        | 1.9.3    | Numeric calculations             |
| Pandas       | 1.1.4    | Data handling & preprocessing    |
| SciPy        | 1.5.4    | Statistical analysis             |
| Matplotlib   | 3.3.2    | Plotting & visualization         |
| scikit-learn | 0.23.2   | Machine learning algorithms      |
| PyQt5        | 5.13.1   | GUI development                  |

> Newer Python and library versions may work but have not been validated against the original study.

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/sekazu.git
cd sekazu

# 2. (Optional) Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

## Citing
Turan, M. K., Sehirli, E., Oner, Z., & Oner, S. (2021). Sekazu: an integrated solution tool for gender determination based on machine learning models. Medicine, 10(2), 367-73.
