

# Medical-to-Layman Text Simplification: A Multi-Stage Fine-Tuning Approach
## Project Overview **Course:** Natural Language Processing (NLP)

**Objective:** To develop a model capable of translating complex medical jargon into accessible layman terminology.

### Problem Statement
Medical documentation and clinical notes often contain highly specialized terminology that acts as a barrier to patient understanding. Standard language models may struggle to simplify this content effectively without losing clinical precision. Our goal is to bridge this communication gap by training a model specifically optimized for **Medical-to-Layman** translation.

---

## Methodology
To achieve high-quality simplification, we implemented a **Two-Stage Transfer Learning** strategy using the `flan-t5-base` model. This approach relies on first teaching the model the *task* of simplification, and then adapting it to the *domain* of medicine.

### The Two-Stage Process
1. **Stage 1: Task Adaptation (General Simplification)**
* **Goal:** Teach the model the mechanics of text simplification (syntax reduction, vocabulary substitution) without restricting it to a specific domain.
* **Data:** Wikipedia Simplification Dataset.
* **Outcome:** A model proficient in general language simplification.


2. **Stage 2: Domain Adaptation (Medical Specific)**
* **Goal:** Fine-tune the Stage 1 model on our curated medical dataset.
* **Data:** The aggregated 7,213 pairs (Real + Synthetic) documented in the `Training Data Set Generation` folder.
* **Outcome:** A final model that applies simplification logic specifically to medical contexts.

![Two-Stage Training Pipeline Diagram](./Diagram.png)

---

## Repository Structure
This repository is organized to reflect the chronological stages of our training pipeline and experiments.

### Core Pipeline* **`Training Data Set Generation/`**
* Contains all scripts for scrapping, cleaning, and synthesizing the medical dataset (Kaggle, JEBS, Med-EASi, Cochrane).


* **`Stage 1 Code/`**
* Scripts used to fine-tune the base `flan-t5` model on Wikipedia data.


* **`Stage 1 results/`** 
* Checkpoints and evaluation metrics from the general simplification training.


* **`Stage 2 Code/`**
* Scripts for the second training phase, taking the Stage 1 model and fine-tuning it on the medical corpus.


* **`Stage 2 results/`**
* **Final Model Outputs.** Contains the performance metrics and generated examples from our best-performing model.



### Experimental testing **`Experiment-only domain specific training/`**
* **Purpose:** To validate the necessity of the two-stage approach.
* **Process:** In this experiment, we fine-tuned the base `flan-t5` model *directly* on the medical data, skipping Stage 1.
* **Comparison:** Comparing results from this folder against `Stage 2 results` demonstrates the performance gain achieved by pre-training on general simplification tasks first.



---

# Contributors
1. Krish Bhatia
2. Sailendra Kolluru 
3. Aryan Rao
4. Adarsh Mukherjee 