# Med-EASi Data Processing 

## Size: 1397 pairs 
## Project Overview
This document outlines the pipeline for acquiring and standardizing the **Med-EASi** dataset. The goal is to retrieve expert-to-simple text pairs and format them into a consistent schema for downstream model training.

## 1. Data AcquisitionThe dataset was sourced from the Hugging Face Hub, specifically the repository hosted by `cbasu`.

* **Source URL:** [Hugging Face: cbasu/Med-EASi](https://huggingface.co/datasets/cbasu/Med-EASi)
* **Acquisition Tool:** `hf_med_easi_data_puller.py`

#### Ingestion ProcessThe python script `hf_med_easi_data_puller.py` was executed to pull the dataset directly from the Hugging Face API. The raw output was initially stored in CSV format to preserve the original structure.

## 2. Data Standardization and Formatting
To ensure consistency with other datasets in this project (such as the Kaggle and JEBS datasets), the raw CSV data underwent a transformation process to standardize column headers and file formats.

* **Input:** Raw CSV data generated from the acquisition step.
* **Transformation Logic:**
* The column originally labeled **"Expert"** was renamed to **"medical"**.
* The column originally labeled **"Simple"** was renamed to **"layman"**.


* **Output File:** `cbasu_Med-EASi.json`

## Summary of Workflow

1. **Extraction:** Run `hf_med_easi_data_puller.py` to download the Med-EASi dataset from Hugging Face and save it as a CSV.
2. **Normalization:** Map the source columns to the project-standard keys (`medical` and `layman`).
3. **Final Storage:** Serialize the standardized pairs into the final JSON object: `cbasu_Med-EASi.json`.

