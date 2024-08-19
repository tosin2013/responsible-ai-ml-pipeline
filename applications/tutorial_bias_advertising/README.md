# Tutorial bias advertising

## Login to OpenShift
```
oc login --token=sha256~XXXXXX --server=https://api.rosa-1123.xxx.p3.example.com:443
```

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
OPENSHIFT_URL=$(oc get routes -n tutorial-bias-advertising | awk '/tutorial-bias-advertising/ {print $2}')

curl --location 'https://${OPENSHIFT_URL}/measure_mitigate_bias' \
--header 'Content-Type: application/json' \
--data '{
    "target_label_name": "predicted_conversion",
    "scores_name": "predicted_probability",
    "random_seed": 150
}'

 curl --location https://tutorial-bias-advertising-tutorial-bias-advertising.apps.rosa.rosa-vcwtg.ocyk.p3.openshiftapps.com/measure_mitigate_bias \
--header 'Content-Type: application/json' \
--data '{
    "target_label_name": "predicted_conversion",
    "scores_name": "predicted_probability",
    "random_seed": 150
}'
```