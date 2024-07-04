from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError
from typing import Optional
import pandas as pd
import numpy as np
from aif360.datasets import StandardDataset
from aif360.metrics import ClassificationMetric, BinaryLabelDatasetMetric
from aif360.algorithms.postprocessing import RejectOptionClassification
from aif360.detectors.mdss.ScoringFunctions import Bernoulli
from aif360.detectors.mdss.MDSS import MDSS
from aif360.detectors.mdss.generator import get_random_subset
import logging

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

# Endpoint for bias measurement and mitigation
@app.route('/measure_mitigate_bias', methods=['POST'])
def measure_mitigate_bias():
    try:
        data = BiasRequestModel(**request.json)
    except ValidationError as e:
        return jsonify(e.errors()), 400
    
    target_label_name = data.target_label_name
    scores_name = data.scores_name
    random_seed = data.random_seed
    
    logger.info("Received request with target_label_name: %s, scores_name: %s, random_seed: %d", target_label_name, scores_name, random_seed)
    
    # Convert dataset to StandardDataset
    ad_standard_dataset_pred = convert_to_standard_dataset(ad_conversion_dataset, target_label_name, scores_name)
    ad_standard_dataset_orig = ad_standard_dataset_pred.copy()
    ad_standard_dataset_orig.labels = ad_conversion_dataset["true_conversion"].values.reshape(-1, 1)
    ad_standard_dataset_orig.scores = ad_conversion_dataset["true_conversion"].values.reshape(-1, 1)
    
    # Bias metrics
    privileged_groups= [{'homeowner': 0}]
    unprivileged_groups = [{'homeowner': 1}]
    
    metric_orig = BinaryLabelDatasetMetric(ad_standard_dataset_orig, 
                                                 unprivileged_groups=unprivileged_groups,
                                                 privileged_groups=privileged_groups)
    disparate_impact_orig = metric_orig.disparate_impact()
    logger.info("Disparate impact (original): %f", disparate_impact_orig)
    
    metric_pred = BinaryLabelDatasetMetric(ad_standard_dataset_pred, 
                                                 unprivileged_groups=unprivileged_groups,
                                                 privileged_groups=privileged_groups)
    disparate_impact_pred = metric_pred.disparate_impact()
    logger.info("Disparate impact (predicted): %f", disparate_impact_pred)
    
    # Post-processing to mitigate bias
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
    logger.info("Disparate impact (transformed): %f", disparate_impact_valid_transf)
    
    # Return the results as JSON
    results = {
        'disparate_impact_orig': disparate_impact_orig,
        'disparate_impact_pred': disparate_impact_pred,
        'disparate_impact_valid_transf': disparate_impact_valid_transf
    }
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
