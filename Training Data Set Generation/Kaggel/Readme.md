# Synthetic Medical-to-Layman Data Generation Pipeline 

## Size: 1239 pairs

# Project Overview

preprocessing raw text, and generating synthetic parallel data (Medical vs. Layman terminology). The pipeline utilizes data sourced from the **2019 Kaggle Medical Notes Competition** to create a clean training dataset.

## 1. Data AcquisitionThe primary dataset was obtained from the Kaggle Medical Notes 2019 competition.

* **Source URL:** [Kaggle Medical Notes 2019](https://www.kaggle.com/competitions/medicalnotes-2019/data?select=data.zip)
* **File:** `data.zip`

#### Data SpecificationsThe archive contains clinical note text files. The filenames are strictly numerical, ranging from `1001.txt` to `2239.txt`.

* **Training Set:** Files `1001.txt` through `1826.txt`.
* **Testing Set:** Files `1827.txt` through `2239.txt`.

#### Raw Data StorageUpon extraction, all raw text files were stored in the following directory:
`./data_raw`

## 2. Preprocessing Pipeline
### Step 1: HTML CleaningThe raw clinical notes contained HTML tags and formatting artifacts. These were removed to ensure textual purity.

* **Script Used:** `html_data_cleaner_kaggel.py`
* **Process:** The script iterates through the raw data directory, stripping HTML tags and normalizing the text.
* **Output:** `cleaned_medical_texts.json`
* *Format:* A JSON object containing multiple keys, where each value represents a specific segment of cleaned medical text.



### Step 2: Synthetic Data GenerationUsing the cleaned JSON data, a synthetic data generation process was executed to create parallel text pairs.

* **Objective:** To map complex medical terminology to accessible layman descriptions.
* **Input:** `cleaned_medical_texts.json`
* **Process:** The synthetic data maker parsed the cleaned text to generate corresponding medical and layman pairs using ***gpt oss 20b cloud***.
* **Final Output Location:** `training_data_kaggel`

## Summary of Workflow
1. **Ingestion:** Download `data.zip` and extract to `./data_raw`.
2. **Cleaning:** Execute `html_data_cleaner_kaggel.py` to produce `cleaned_medical_texts.json`.
3. **Synthesis:** Run the synthetic generation tool to populate `training_data_kaggel` with the final paired datasets.

