---
layout: default
title:  "Discover, Measure, and Mitigate Bias in Advertising" 
parent: AI Fairness 360
nav_order: 1
---

This tutorial illustrates how bias in advertising data can be discovered, measured, and mitigated using the **AI Fairness 360 (AIF360) toolkit**. We use synthetic advertising data where advertisements are targeted, and the actual and predicted conversions are collected along with additional attributes about each user. A user is considered to have converted when they click on an advertisement. This tutorial demonstrates how methods in the AIF360 toolkit can be used to discover biased subgroups, determine the amount of bias, and mitigate this bias.

Notebook for this tutorial: [Discover, Measure, and Mitigate Bias in Advertising](https://github.com/tosin2013/responsible-ai-ml-pipeline/blob/main/notebooks/ai360/tutorial_bias_advertising.ipynb)

## Use Case Description

- **Dataset**: Synthetic data of users shown advertisements with attributes such as gender, age, income, political/religious affiliation, parental status, home ownership, area (rural/urban), and education status.
- **Goal**: Discover, measure, and mitigate bias in the dataset using AIF360.
- **Steps**:
  1. Discover biased subgroups using the multidimensional subset scan (MDSS) method.
  2. Measure the bias exhibited by these subgroups using various metrics.
  3. Mitigate bias using post-processing bias mitigation approaches.

## Steps for Bias Discovery, Measurement, and Mitigation

### 1. Install Necessary Libraries

First, we need to install the necessary libraries. This includes the AIF360 toolkit and other required packages.

```python
!pip install -q git+https://github.com/Trusted-AI/AIF360
!pip install -q 'aif360[AdversarialDebiasing]'
!pip install -q 'aif360[Reductions]'
!pip install -q 'aif360[inFairness]'
!pip install -q pandas 
```

*Explanation*: These commands install the AIF360 toolkit and other necessary libraries such as pandas for data manipulation, scikit-learn for machine learning, and matplotlib and seaborn for data visualization.

### 2. Import Libraries

Next, we import the libraries we just installed.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from aif360.datasets import StandardDataset
from aif360.metrics import ClassificationMetric, BinaryLabelDatasetMetric
from aif360.algorithms.postprocessing import RejectOptionClassification
from aif360.detectors.mdss.ScoringFunctions import Bernoulli
from aif360.detectors.mdss.MDSS import MDSS
from aif360.detectors.mdss.generator import get_random_subset
from IPython.display import Markdown, display
```

*Explanation*: These imports bring in the necessary functions and classes for data manipulation, visualization, and bias detection and mitigation.

### 3. Download and Load the Dataset

We download and load the synthetic advertising dataset.

```python
import os

if not os.path.exists('bias-in-advertising/ad_campaign_data.csv'):
    !curl -OL https://dax-cdn.cdn.appdomain.cloud/dax-bias-in-advertising/1.0.0/bias-in-advertising.tar.gz
    !tar -zxvf bias-in-advertising.tar.gz

ad_conversion_dataset = pd.read_csv('bias-in-advertising/ad_campaign_data.csv')
ad_conversion_dataset.head()
```

*Explanation*: This code checks if the dataset is already present. If not, it downloads and extracts the dataset. Finally, it loads the dataset into a pandas DataFrame and displays the first few rows.

### 4. Identify Biased Subgroups Using MDSS

We use the multidimensional subset scan (MDSS) to identify biased subgroups.

```python
features_4_scanning = ['college_educated','parents','homeowner','gender','age','income','area','politics','religion']

def print_report(data, subset):
    if subset:
        to_choose = ad_conversion_dataset[subset.keys()].isin(subset).all(axis = 1)
        df = ad_conversion_dataset[['true_conversion', 'predicted_conversion']][to_choose]
    else:
        for col in features_4_scanning:
            subset[col] = list(ad_conversion_dataset[col].unique())
        df = ad_conversion_dataset[['true_conversion', 'predicted_conversion']]

    true = df['true_conversion'].sum()
    pred = df['predicted_conversion'].sum()

    print('\033[1mSubset: \033[0m')
    pprint(subset)
    print('\033[1mSubset Size: \033[0m', len(df))
    print('\033[1mTrue Clicks: \033[0m', true)
    print('\033[1mPredicted Clicks: \033[0m', pred)
    print()

np.random.seed(11)
random_subset = get_random_subset(ad_conversion_dataset[features_4_scanning], prob = 0.05, min_elements = 10000)
print_report(ad_conversion_dataset, random_subset)
```

*Explanation*: This code defines a function to print a report of the subset data. It then uses MDSS to identify a random subset of the data that might exhibit bias and prints a report for this subset.

### 5. Computation of Bias Metrics for These Subgroups

We compute bias metrics for the identified subgroups.

```python
scoring_function = Bernoulli(direction='negative')
scanner = MDSS(scoring_function)

scanned_subset, _ = scanner.scan(ad_conversion_dataset[features_4_scanning], 
                    expectations = ad_conversion_dataset['predicted_conversion'],
                    outcomes = ad_conversion_dataset['true_conversion'], 
                    penalty = 1, 
                    num_iters = 1,
                    verbose = False)

print_report(ad_conversion_dataset, scanned_subset)
```

*Explanation*: This code uses the Bernoulli scoring function to scan the dataset for biased subgroups and prints a report for the identified biased subgroup.

### 6. Bias Mitigation Using a Post-Processing Approach

We use the Reject Option Classification (ROC) post-processing approach to mitigate bias.

```python
def convert_to_standard_dataset(df, target_label_name, scores_name=""):
    protected_attributes=['homeowner']
    selected_features = ['gender', 'age', 'income', 'area', 'college_educated', 'homeowner', 'parents', 'predicted_probability']
    privileged_classes = []
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

ad_standard_dataset_pred = convert_to_standard_dataset(ad_conversion_dataset, 
                                        target_label_name = 'predicted_conversion',
                                        scores_name='predicted_probability')

ad_standard_dataset_orig = ad_standard_dataset_pred.copy()
ad_standard_dataset_orig.labels = ad_conversion_dataset["true_conversion"].values.reshape(-1, 1)
ad_standard_dataset_orig.scores = ad_conversion_dataset["true_conversion"].values.reshape(-1, 1)
```

*Explanation*: This code converts the dataset into a format compatible with AIF360 and prepares it for bias mitigation.

### 7. Compute Fairness Metrics on the Entire Dataset

We compute fairness metrics to evaluate the dataset.

```python
privileged_groups= [{'homeowner': 0}]
unprivileged_groups = [{'homeowner': 1}]

metric_orig = BinaryLabelDatasetMetric(ad_standard_dataset_orig, 
                                         unprivileged_groups=unprivileged_groups,
                                         privileged_groups=privileged_groups)
print(f"Disparate impact for the original dataset = {metric_orig.disparate_impact():.4f}")

metric_pred = BinaryLabelDatasetMetric(ad_standard_dataset_pred, 
                                         unprivileged_groups=unprivileged_groups,
                                         privileged_groups=privileged_groups)
print(f"Disparate impact for the predicted dataset = {metric_pred.disparate_impact():.4f}")
```

*Explanation*: This code calculates the disparate impact metric for both the original and predicted datasets, which helps in understanding the level of bias present.

### 8. Mitigate Bias by Transforming the Original Dataset

We transform the dataset to mitigate bias using ROC.

```python
random_seed = 1001
dataset_orig_train, dataset_orig_vt = ad_standard_dataset_orig.split([0.7], 
                                            shuffle=True, seed=random_seed)
dataset_orig_valid, dataset_orig_test = dataset_orig_vt.split([0.5], 
                                            shuffle=True, seed=random_seed+1)

dataset_pred_train, dataset_pred_vt = ad_standard_dataset_pred.split([0.7], 
                                            shuffle=True, seed=random_seed)
dataset_pred_valid, dataset_pred_test = dataset_pred_vt.split([0.5], 
                                            shuffle=True, seed=random_seed+1)

num_thresh = 300
ba_arr = np.zeros(num_thresh)
class_thresh_arr = np.linspace(0.01, 0.99, num_thresh)
for idx, class_thresh in enumerate(class_thresh_arr):
    fav_inds = dataset_pred_valid.scores > class_thresh
    dataset_pred_valid.labels[fav_inds] = dataset_pred_valid.favorable_label
    dataset_pred_valid.labels[~fav_inds] = dataset_pred_valid.unfavorable_label

    classified_metric_valid = ClassificationMetric(dataset_orig_valid,
                                         dataset_pred_valid, 
                                         unprivileged_groups=unprivileged_groups,
                                         privileged_groups=privileged_groups)

    ba_arr[idx] = 0.5*(classified_metric_valid.true_positive_rate()+
                       classified_metric_valid.true_negative_rate())

best_ind = np.where(ba_arr == np.max(ba_arr))
best_class_thresh = class_thresh_arr[best_ind]

print("Best balanced accuracy (no fairness constraints) = %.4f" % np.max(ba_arr))
print("Optimal classification threshold (no fairness constraints) = %.4f" % best_class_thresh)

metric_name = "Statistical parity difference"
metric_ub = 0.05
metric_lb = -0.05

ROC = RejectOptionClassification(unprivileged_groups=unprivileged_groups,
                                 privileged_groups=privileged_groups,
                                            low_class_thresh=0.01, high_class_thresh=0.99,
                                            num_class_thresh=100, num_ROC_margin=50,
                                            metric_name=metric_name,
                                            metric_ub=metric_ub, metric_lb=metric_lb)
dataset_transf_pred_valid = ROC.fit_predict(dataset_orig_valid, dataset_pred_valid)

print("Optimal classification threshold (with fairness constraints) = %.4f" % ROC.classification_threshold)
print("Optimal ROC margin = %.4f" % ROC.ROC_margin)

metric_pred_valid_transf = BinaryLabelDatasetMetric(dataset_transf_pred_valid, 
                                         unprivileged_groups=unprivileged_groups,
                                         privileged_groups=privileged_groups)
print(f"Disparate impact of unprivileged vs privileged groups = {metric_pred_valid_transf.disparate_impact():.4f}")
```

*Explanation*: This code splits the dataset into training, validation, and test sets. It then uses the ROC algorithm to find the optimal classification threshold and ROC margin to mitigate bias, and calculates the disparate impact metric for the transformed dataset.

### 9. Predictions from Test Set

We evaluate the model on the test set to see the impact of bias mitigation.

```python
from collections import OrderedDict

def compute_metrics(dataset_true, dataset_pred, 
                    unprivileged_groups, privileged_groups,
                    disp = True):
    classified_metric_pred = ClassificationMetric(dataset_true,
                                                 dataset_pred, 
                                                 unprivileged_groups=unprivileged_groups,
                                                 privileged_groups=privileged_groups)
    metrics = OrderedDict()
    metrics["Balanced accuracy"] = 0.5*(classified_metric_pred.true_positive_rate()+
                                         classified_metric_pred.true_negative_rate())
    metrics["Statistical parity difference"] = classified_metric_pred.statistical_parity_difference()
    metrics["Disparate impact"] = classified_metric_pred.disparate_impact()
    metrics["Average odds difference"] = classified_metric_pred.average_odds_difference()
    metrics["Equal opportunity difference"] = classified_metric_pred.equal_opportunity_difference()
    metrics["Theil index"] = classified_metric_pred.theil_index()

    if disp:
        for k in metrics:
            print("%s = %.4f" % (k, metrics[k]))

    return metrics

fav_inds = dataset_pred_test.scores > best_class_thresh
dataset_pred_test.labels[fav_inds] = dataset_pred_test.favorable_label
dataset_pred_test.labels[~fav_inds] = dataset_pred_test.unfavorable_label

metric_test_bef = compute_metrics(dataset_orig_test, dataset_pred_test, 
            unprivileged_groups, privileged_groups)

dataset_transf_pred_test = ROC.predict(dataset_pred_test)

metric_test_aft = compute_metrics(dataset_orig_test, dataset_transf_pred_test, 
            unprivileged_groups, privileged_groups)
```

*Explanation*: This code defines a function to compute various fairness metrics and then applies this function to the test set before and after bias mitigation to evaluate the effectiveness of the ROC algorithm.

### 10. Summary and Findings

- We used MDSS to identify groups with significant predictive bias.
- Non-homeowners were identified as the privileged group.
- We measured bias using the disparate impact metric.
- Bias was mitigated using the Reject Option Classification (ROC) post-processing algorithm.
- The results showed significant improvement in fairness metrics with minimal loss in balanced accuracy.

