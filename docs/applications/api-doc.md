---
layout: default
title: Bias Measurement and Mitigation API
parent: Applications
nav_order: 3
---
This document provides an overview of the Bias Measurement and Mitigation API, which is designed to measure and mitigate bias in advertising datasets. The API is built using Flask and integrates with various libraries for data processing and bias analysis.

[Source](https://github.com/tosin2013/responsible-ai-ml-pipeline/blob/main/applications/tutorial_bias_advertising/app.py)

## Dependencies

The script relies on the following libraries:
- `flask`: For creating the web application and API endpoints.
- `pydantic`: For data validation and settings management using Python type annotations.
- `pandas`: For data manipulation and analysis.
- `numpy`: For numerical operations.
- `aif360`: For bias detection and mitigation algorithms.
- `logging`: For logging information and errors.
- `time`: For measuring the time taken for various operations.
- `json`: For JSON serialization and deserialization.

## API Endpoint

### `/measure_mitigate_bias`

**Method:** POST

**Description:** This endpoint accepts a JSON payload containing the target label name, scores name, and an optional random seed. It processes the data to measure and mitigate bias, returning a stream of text responses detailing the process and final results.

**Request Payload:**
```json
{
  "target_label_name": "string",
  "scores_name": "string",
  "random_seed": "integer (optional, default=1001)"
}
```

**Response:**
- **200 OK:** The request was successful, and the response will be a stream of text detailing the bias measurement and mitigation process.
- **400 Bad Request:** The request payload failed validation. The response will contain details of the validation errors.

## Data Processing

### Loading Data

The `load_data` function reads a CSV file into a pandas DataFrame. It handles various exceptions such as file not found, empty file, and other potential errors.

### Converting to Standard Dataset

The `convert_to_standard_dataset` function transforms the DataFrame into a `StandardDataset` object from the `aif360` library. This transformation includes selecting features, defining protected attributes, and setting privileged classes.

### Generating Response

The `generate_response` function is a generator that processes the data to measure and mitigate bias. It calculates bias metrics, applies post-processing techniques to mitigate bias, and yields intermediate results and final metrics.

## Running the Script

To run the script, execute the following command:
```bash
python app.py
```

The API will be available at `http://0.0.0.0:8080`.

## REST API Example
```
curl --location 'https://${FLASK_URL}/measure_mitigate_bias' \
--header 'Content-Type: application/json' \
--data '{
    "target_label_name": "predicted_conversion",
    "scores_name": "predicted_probability",
    "random_seed": 150
}'
```