from flask import Flask, request, jsonify, Response
from pydantic import BaseModel, ValidationError
from typing import Optional
import pandas as pd
import numpy as np
from aif360.datasets import StandardDataset
from aif360.metrics import ClassificationMetric, BinaryLabelDatasetMetric
from aif360.algorithms.postprocessing import RejectOptionClassification
import logging
import time
import json


app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define request model
class BiasRequestModel(BaseModel):
    target_label_name: str
    scores_name: str
    random_seed: Optional[int] = 1001

# Load dataset (You may replace this with your data loading logic)
ad_conversion_dataset = pd.read_csv('bias-in-advertising/ad_campaign_data.csv')

# Define utility functions
def convert_to_standard_dataset(df, target_label_name, scores_name=""):
    protected_attributes=['homeowner']
    selected_features = ['gender', 'age', 'income', 'area', 'college_educated', 'homeowner', 'parents', 'predicted_probability']
    privileged_classes = [[0]]
    favorable_target_label = [1]
    categorical_features = ['parents','gender','college_educated','area','income', 'age']
    standard_dataset = StandardDataset(df=df, label_name=target_label_name,
                                    favorable_classes=favorable_target_label,
                                    scores_name=scores_name,
                                    protected_attribute_names=protected_attributes,
                                    privileged_classes=privileged_classes,
                                    categorical_features=categorical_features,
                                    features_to_keep=selected_features)
    if scores_name=="":
        standard_dataset.scores = standard_dataset.labels.copy()
    return standard_dataset

# Streaming generator function
def generate_response(data):
    target_label_name = data.target_label_name
    scores_name = data.scores_name
    random_seed = data.random_seed

    logger.info("Received request with target_label_name: %s, scores_name: %s, random_seed: %d", target_label_name, scores_name, random_seed)

    # Convert dataset to StandardDataset
    convert_start_time = time.time()
    ad_standard_dataset_pred = convert_to_standard_dataset(ad_conversion_dataset, target_label_name, scores_name)
    ad_standard_dataset_orig = ad_standard_dataset_pred.copy()
    ad_standard_dataset_orig.labels = ad_conversion_dataset["true_conversion"].values.reshape(-1, 1)
    ad_standard_dataset_orig.scores = ad_conversion_dataset["true_conversion"].values.reshape(-1, 1)
    convert_end_time = time.time()
    yield f"Time taken for data conversion: {convert_end_time - convert_start_time} seconds\n"
    
    # Bias metrics
    metric_start_time = time.time()
    privileged_groups= [{'homeowner': 0}]
    unprivileged_groups = [{'homeowner': 1}]
    
    metric_orig = BinaryLabelDatasetMetric(ad_standard_dataset_orig, 
                                                 unprivileged_groups=unprivileged_groups,
                                                 privileged_groups=privileged_groups)
    disparate_impact_orig = metric_orig.disparate_impact()
    yield f"Disparate impact (original): {disparate_impact_orig}\n"
    
    metric_pred = BinaryLabelDatasetMetric(ad_standard_dataset_pred, 
                                                 unprivileged_groups=unprivileged_groups,
                                                 privileged_groups=privileged_groups)
    disparate_impact_pred = metric_pred.disparate_impact()
    yield f"Disparate impact (predicted): {disparate_impact_pred}\n"
    metric_end_time = time.time()
    yield f"Time taken for bias metrics calculation: {metric_end_time - metric_start_time} seconds\n"
    
    # Post-processing to mitigate bias
    post_process_start_time = time.time()
    dataset_orig_train, dataset_orig_vt = ad_standard_dataset_orig.split([0.7], shuffle=True, seed=random_seed)
    dataset_orig_valid, dataset_orig_test = dataset_orig_vt.split([0.5], shuffle=True, seed=random_seed+1)
    
    dataset_pred_train, dataset_pred_vt = ad_standard_dataset_pred.split([0.7], shuffle=True, seed=random_seed)
    dataset_pred_valid, dataset_pred_test = dataset_pred_vt.split([0.5], shuffle=True, seed=random_seed+1)
    
    ROC = RejectOptionClassification(unprivileged_groups=unprivileged_groups,
                                     privileged_groups=privileged_groups,
                                                low_class_thresh=0.01, high_class_thresh=0.99,
                                                num_class_thresh=100, num_ROC_margin=50,
                                                metric_name="Statistical parity difference",
                                                metric_ub=0.05, metric_lb=-0.05)
    dataset_transf_pred_valid = ROC.fit_predict(dataset_orig_valid, dataset_pred_valid)
    metric_pred_valid_transf = BinaryLabelDatasetMetric(dataset_transf_pred_valid, 
                                                 unprivileged_groups=unprivileged_groups,
                                                 privileged_groups=privileged_groups)
    disparate_impact_valid_transf = metric_pred_valid_transf.disparate_impact()
    yield f"Disparate impact (transformed): {disparate_impact_valid_transf}\n"
    post_process_end_time = time.time()
    yield f"Time taken for post-processing: {post_process_end_time - post_process_start_time} seconds\n"
    
    # Return the results as JSON
    results = {
        'disparate_impact_orig': disparate_impact_orig,
        'disparate_impact_pred': disparate_impact_pred,
        'disparate_impact_valid_transf': disparate_impact_valid_transf
    }
    end_time = time.time()
    yield f"Total time taken for request: {end_time - start_time} seconds\n"
    yield json.dumps(results)

# Endpoint for bias measurement and mitigation
@app.route('/measure_mitigate_bias', methods=['POST'])
def measure_mitigate_bias():
    try:
        data = BiasRequestModel(**request.json)
    except ValidationError as e:
        return jsonify(e.errors()), 400
    
    return Response(generate_response(data), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
