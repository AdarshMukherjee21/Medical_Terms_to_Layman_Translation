

# JEBS Synthetic Data Generation 

## Size: 1124 pairs

## Project Overview
This repository contains the workflow for the **JEBS (Jargon Explanations for Biomedical Simplification)** project. The objective is to acquire biomedical text data and generate synthetic pairs to train models in simplifying complex medical jargon.

### 1. Data AcquisitionThe foundational dataset was retrieved from the official JEBS repository.

* **Source URL:** [JEBS Data Repository](https://github.com/bill-from-ri/JEBS-data/blob/main/training.json)
* **Source File:** `training.json`

### 2. Processing PipelineThe data processing workflow is consolidated within the Jupyter Notebook: `JEBS_data_fetching_and_cleaning.ipynb`. This notebook handles two primary stages: cleaning and synthetic generation.

### Stage 1: Data Cleaning and FormattingThe raw training data was ingested, sanitized, and structured into direct pairs.

* **Process:** The notebook retrieves the raw JSON, performs necessary cleaning operations, and aligns the data into input-output pairs.
* **Intermediate Output:** `jebs_data.json`

### Stage 2: Synthetic Data GenerationUsing the structured data from Stage 1, synthetic parallel data was generated to augment the dataset.

* **Model Used:** GPT OSS 20B (Cloud Inference)
* **Process:** The cleaned pairs served as prompts or context for the model to generate additional synthetic examples.
* **Final Output Directory:** `training_data_jebs_synthetic`

## Summary of Workflow
1. **Ingestion:** Pull raw data from the JEBS GitHub source.
2. **Preprocessing:** Execute `JEBS_data_fetching_and_cleaning.ipynb` to produce the intermediate file `jebs_data.json`.
3. **Synthesis:** Continue execution within the same notebook to generate synthetic pairs using the GPT OSS 20B cloud model.
4. **Storage:** Save final synthetic datasets to `./training_data_jebs_synthetic/`.

