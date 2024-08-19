---
layout: default
title:  "Discover, Measure, and Mitigate Bias in Advertising - Quick Deployment" 
parent: Applications
nav_order: 3
---

## Deploy the Tutorial bias advertising api in OpenShift
```
oc create -k applications/tutorial_bias_advertising/deployment  
```

## Delete the Tutorial bias advertising api in OpenShift
```
oc delete -k applications/tutorial_bias_advertising/deployment  
```

## This code sends a POST request to the specified URL to measure and mitigate bias in advertising predictions.
```
OPENSHIFT_URL=tutorial-bias-advertising-tutorial-bias-advertising.apps.ocp4.example.com

curl --location 'https://${OPENSHIFT_URL}/measure_mitigate_bias' \
--header 'Content-Type: application/json' \
--data '{
    "target_label_name": "predicted_conversion",
    "scores_name": "predicted_probability",
    "random_seed": 150
}'
```