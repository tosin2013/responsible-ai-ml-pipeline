---
layout: default
title: Tutorial Bias Advertising BuildConfig
parent: Applications
nav_order: 3
---

A `BuildConfig` in OpenShift is a definition of the entire build process. It specifies how to build the application from source code to an image that can be deployed. This document outlines the `BuildConfig` for the Tutorial Bias Advertising application.

[Source](https://github.com/tosin2013/responsible-ai-ml-pipeline/blob/main/applications/tutorial_bias_advertising/deployment/tutorial-bias-advertising-bc.yaml)

## Metadata

The metadata section provides essential information about the `BuildConfig`:

- **name**: `tutorial-bias-advertising`
- **namespace**: `tutorial-bias-advertising`

## Spec

The specification section defines the details of the build process:

### Source

- **type**: `Git`
- **git**:
  - **ref**: `main`
  - **uri**: `https://github.com/tosin2013/responsible-ai-ml-pipeline.git`
- **contextDir**: `applications/tutorial_bias_advertising`

### Output

- **to**:
  - **kind**: `ImageStreamTag`
  - **name**: `tutorial-bias-advertising:latest`

### Resources

No specific resource limits or requests are defined.

### Strategy

- **type**: `Docker`
- **dockerStrategy**:
  - **dockerfilePath**: `Dockerfile`

### Triggers

- **ImageChange**: Automatically triggers a new build when an image change is detected.
- **ConfigChange**: Automatically triggers a new build when the `BuildConfig` itself is changed.

## Deployment Overview

The Tutorial Bias Advertising application is deployed to OpenShift using a series of Kubernetes-like objects that work together to manage the build, deployment, and exposure of the application.

### BuildConfig

The `BuildConfig` is central to the deployment process. It defines how the application is built from source code into a deployable image. The `BuildConfig` specified here uses a Docker strategy to build the image, pulling the source code from a Git repository and using a specific Dockerfile.

### ImageStream

An `ImageStream` is used to manage the images built by the `BuildConfig`. It provides a layer of abstraction over the images, allowing for easy tagging and versioning. The `ImageStream` named `tutorial-bias-advertising:latest` is the target for the built image.

### DeploymentConfig

A `DeploymentConfig` defines how the application is deployed and scaled. It specifies the number of replicas, triggers for automatic deployment, and the strategy for deploying the application. The `DeploymentConfig` will use the image built by the `BuildConfig` and managed by the `ImageStream`.

### Service

The `Service` exposes the application within the OpenShift cluster. It provides a stable IP address and DNS name for the application, allowing other services within the cluster to communicate with it.

### Route

The `Route` exposes the application to the outside world. It provides a publicly accessible URL for the application, allowing users to access it over the internet.

## Conclusion

The `BuildConfig` for the Tutorial Bias Advertising application is a crucial part of the deployment process in OpenShift. By defining the build process and working in conjunction with `ImageStream`, `DeploymentConfig`, `Service`, and `Route`, it ensures that the application is built, deployed, and exposed consistently and efficiently.