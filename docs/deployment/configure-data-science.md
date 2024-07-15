---
layout: default
title:  "Configure Data Science Project" 
parent: Deployment Instructions
nav_order: 2
---

## TrustyAI Workloads

### Creating a Workbench
1. In the OpenShift AI workspace, click on `Create a workbench`.
   ![20240621111631](https://i.imgur.com/z5gcpKY.png)
2. Name the workbench `responsible-ai-ml-pipeline`.
3. Select the notebook image:
   - Image: `TrustyAI`
   - Version: `2024.1`
   ![20240621112811](https://i.imgur.com/JADcoD5.png)
4. Wait for the workspace to be created, then click `Open` to access it.
   ![20240603150615](https://i.imgur.com/MC7f4bK.png)
5. Authorize access to the workbench.
   ![20240603150939](https://i.imgur.com/LZApBNv.png)

### Cloning the Repository
1. Clone the repository using the following URL:
   ```
   https://github.com/tosin2013/responsible-ai-ml-pipeline.git
   ```
   ![20240625181246](https://i.imgur.com/hqqTNjq.png)
   ![20240603151456](https://i.imgur.com/AQ037lj.png)
   ![20240603151512](https://i.imgur.com/6plqczC.png)

### Running Notebooks
- **Language Metrics Notebook**:
  Navigate to `responsible-ai-ml-pipeline/notebooks/trustyai/language_metrics.ipynb`.
  ![20240715113902](https://i.imgur.com/dWNfbiV.png)

- **Group Fairness Notebook**:
  Navigate to `responsible-ai-ml-pipeline/notebooks/trustyai/group_fairness.ipynb`.
  ![20240715113833](https://i.imgur.com/GTqkqnO.png)

- **AI Fairness  Notebook**:
  Navigate to `responsible-ai-ml-pipeline/notebooks/learntools/Ai Fairness.ipynb`.
  ![20240715114135](https://i.imgur.com/TDqkIPW.png)

- **Identifying Bias in AI Notebook**:
   Navigate to `responsible-ai-ml-pipeline/notebooks/learntools/Identifying Bias in AI.ipynb`.
   ![20240715115117](https://i.imgur.com/QsVUPs2.png)

## AI 360 Workloads

### Creating a Workbench
1. In the OpenShift AI workspace, click on `Create a workbench`.
   ![20240715112403](https://i.imgur.com/bpxQI0T.png)
2. Name the workbench `ibm-ai-360`.
3. Select the notebook image:
   - Image: `Standard Data Science`
   - Version: `2024.1`
   ![20240715112114](https://i.imgur.com/E9rXMWh.png)
4. Wait for the workspace to be created, then click `Open` to access it.
   ![20240603150615](https://i.imgur.com/MC7f4bK.png)
5. Authorize access to the workbench.
   ![20240603150939](https://i.imgur.com/LZApBNv.png)

### Cloning the Repository
1. Clone the repository using the following URL:
   ```
   https://github.com/tosin2013/responsible-ai-ml-pipeline.git
   ```
   ![20240625181246](https://i.imgur.com/hqqTNjq.png)
   ![20240603151456](https://i.imgur.com/AQ037lj.png)
   ![20240603151512](https://i.imgur.com/6plqczC.png)

### Running Notebooks
- **Detect and Mitigate Bias in AI 360**:
  Navigate to `responsible-ai-ml-pipeline/notebooks/ai360/detect_and_mitigate_bias.ipynb`.
  ![20240715112655](https://i.imgur.com/Hef97JZ.png)
- **Discover, Measure, and Mitigate Bias in Advertising**:
  Navigate to `responsible-ai-ml-pipeline/notebooks/ai360/tutorial_bias_advertising.ipynb`.
  ![20240715113011](https://i.imgur.com/FYVEmyj.png)