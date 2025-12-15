# Training Data Set Generation Pipeline
## Data Set Overview
This folder contains the complete end-to-end pipeline for creating a high-quality, domain-specific dataset for medical text simplification. The project aggregates real-world medical-to-layman pairs from open-source repositories and augments them with synthetic data generated via Large Language Models (LLMs).

## Dataset Composition
The final training dataset consists of **7,213** paired examples. The data is stratified into two primary categories: Real-world data sourced from Hugging Face and Synthetic data generated using GPT OSS 20B (Cloud).


| Data Type | Count | Percentage | Source Description |
| --- | --- | --- | --- |
| **Real Data** | **4,965** | **68.83%** | Curated pairs pulled directly from Hugging Face repositories (Med-EASi and Cochrane Simplification). |
| **Synthetic Data** | **2,248** | **31.17%** | Generated pairs derived from raw medical text (JEBS and Kaggle) using GPT OSS 20B Cloud inference for high-fidelity simplification. |
| **Total** | **7,213** | **100%** | The final aggregated corpus. |

---

## Directory Structure
The Folder is organized into modular sub-directories, each handling a specific data source or processing stage:

### 1. `\Kaggel` **Role:** Synthetic Data Source (Base).
* **Description:** Processes raw clinical notes from the 2019 Kaggle Medical Notes competition. The raw text is cleaned and used as seed data for synthetic generation.

### 2. `\JEBS` **Role:** Synthetic Data Source (Base).
* **Description:** Contains workflows for the Jargon Explanations for Biomedical Simplification (JEBS) dataset. Raw definitions are cleaned and used to prompt the generation of synthetic pairs.

### 3. `\MED_EASi` **Role:** Real Data Source.
* **Description:** Scripts to ingest the Med-EASi dataset from Hugging Face. Columns are mapped from `Expert`/`Simple` to the project standard `medical`/`layman`.

### 4. `\cochrane_simplification` **Role:** Real Data Source.
* **Description:** Scripts to ingest the Cochrane Simplification dataset from Hugging Face. Columns are mapped from `source`/`target` to the project standard `medical`/`layman`.

### 5. `\Domain_specific_Trainig_data` **Role:** Final Aggregation and Storage.
* **Description:** This directory contains the final aggregation scripts (`sythetic_json_combiner.py` and `data_aggregator_jsons.py`) and the consolidated datasets, including the final **`training_data_7213.json`**.

---

## Usage
Each subdirectory contains its own detailed `README` and specific scripts for reproducing that segment of the data pipeline. To reproduce the final dataset:

1. Run the individual pipelines in folders 1-4.
2. Execute the aggregation scripts located in `\Domain_specific_Trainig_data`.

