---
layout: default
title: Deployment Configuration for Tutorial Bias Advertising on OpenShift
parent: Applications
nav_order: 3
---

This document provides a detailed explanation of the Kubernetes Deployment configuration for the Tutorial Bias Advertising application, specifically tailored for deployment on OpenShift.

[Source](https://github.com/tosin2013/responsible-ai-ml-pipeline/blob/main/applications/tutorial_bias_advertising/deployment/deployment.yaml)

## Metadata

The `metadata` section contains essential information about the Deployment:

- **name**: The name of the Deployment, which is `tutorial-bias-advertising`.
- **namespace**: The namespace where the Deployment will be deployed, which is `tutorial-bias-advertising`. OpenShift uses namespaces to partition resources within a cluster.
- **labels**: Labels are used to organize and select subsets of objects. The labels for this Deployment include:
  - `app: tutorial-bias-advertising`
  - `app.kubernetes.io/component: tutorial-bias-advertising`
  - `app.kubernetes.io/instance: tutorial-bias-advertising`
  - `app.kubernetes.io/name: tutorial-bias-advertising`
  - `app.kubernetes.io/part-of: tutorial-bias-advertising`

## Spec

The `spec` section defines the desired state of the Deployment:

- **replicas**: The number of desired pods, which is set to `1`.
- **selector**: The selector defines how the Deployment finds which pods to manage. It matches pods with the label `app: tutorial-bias-advertising`.
- **template**: The pod template specification:
  - **metadata**: The metadata for the pod template, including labels like `app: tutorial-bias-advertising` and `deployment: tutorial-bias-advertising`.
  - **spec**: The specification for the pods:
    - **containers**: The list of containers to run in the pod:
      - **name**: The name of the container, which is `tutorial-bias-advertising`.
      - **image**: The Docker image to use, which is `image-registry.openshift-image-registry.svc:5000/tutorial-bias-advertising/tutorial-bias-advertising:latest`. This image is hosted in the OpenShift internal image registry.
      - **ports**: The ports to expose on the container, including `containerPort: 8080` with `protocol: TCP`.
      - **resources**: The resource requirements for the container, which are currently empty.
      - **terminationMessagePath**: The path at which the container will write termination messages, which is `/dev/termination-log`.
      - **terminationMessagePolicy**: The policy for handling termination messages, which is `File`.
      - **imagePullPolicy**: The policy for pulling the image, which is `Always`.
    - **restartPolicy**: The restart policy for all containers in the pod, which is `Always`.
    - **terminationGracePeriodSeconds**: The grace period for terminating the pod, which is `30` seconds.
    - **dnsPolicy**: The DNS policy for the pod, which is `ClusterFirst`.
    - **securityContext**: The security context for the pod, which is currently empty.
    - **schedulerName**: The name of the scheduler to use, which is `default-scheduler`.

## Deployment Strategy

The `strategy` section defines how the Deployment will be rolled out:

- **type**: The type of deployment strategy, which is `RollingUpdate`. This strategy ensures that the application is available during the update process.
- **rollingUpdate**: The configuration for the rolling update strategy:
  - **maxUnavailable**: The maximum number of pods that can be unavailable during the update, which is `25%`.
  - **maxSurge**: The maximum number of pods that can be created above the desired number of pods, which is `25%`.

## Additional Settings

- **revisionHistoryLimit**: The number of old ReplicaSets to retain to allow rollback, which is `10`. This allows for easy rollback to previous versions if needed.
- **progressDeadlineSeconds**: The maximum time in seconds for the Deployment to make progress before it is considered to be failed, which is `600` seconds. This ensures that the Deployment process does not hang indefinitely.
