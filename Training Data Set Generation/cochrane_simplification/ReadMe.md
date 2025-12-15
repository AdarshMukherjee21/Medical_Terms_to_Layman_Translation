# Cochrane Simplification Data Processing

## Size: 3568 pairs 

## Project Overview
This document details the workflow for acquiring and standardizing the **GEM/Cochrane Simplification** dataset. The objective is to extract source text and simplified summaries to create a standardized "medical-to-layman" parallel corpus.

## 1. Data AcquisitionThe dataset was retrieved from the Hugging Face Hub, specifically the repository hosted by the **GEM Benchmark**.

* **Source URL:** [Hugging Face: GEM/cochrane-simplification](https://huggingface.co/datasets/GEM/cochrane-simplification)
* **Acquisition Tool:** `hf_cochrance_data_puller.py`

### Ingestion Process
The script `hf_cochrance_data_puller.py` was executed to interface with the Hugging Face API. The raw dataset was downloaded and saved locally in CSV format to ensure data integrity before transformation.

* **Intermediate Output:** `cochrane_simplification_full.csv`

## 2. Data Standardization and FormattingFollowing acquisition, the CSV data was processed to align with the project's consistent schema using a dedicated conversion script.

* **Transformation Tool:** `csv_to_json.py`
* **Input:** `cochrane_simplification_full.csv`
* **Transformation Logic:**
* The column originally labeled **"source"** was renamed to **"medical"**.
* The column originally labeled **"target"** was renamed to **"layman"**.


* **Final Output File:** `cochrane_simplification_full.json`

## Summary of Workflow
1. **Extraction:** Execute `hf_cochrance_data_puller.py` to pull the dataset from Hugging Face and store it as `cochrane_simplification_full.csv`.
2. **Normalization:** Run `csv_to_json.py` to process the CSV, mapping the `source` and `target` columns to the standardized keys.
3. **Final Storage:** Serialize the final cleaned pairs into `cochrane_simplification_full.json`.

