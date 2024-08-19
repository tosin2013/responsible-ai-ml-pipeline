---
layout: default
title: Kustomization Configuration
parent: Applications
nav_order: 3
---

The `Kustomization` file is a powerful tool in Kubernetes that allows for customizing raw, template-free YAML files for multiple purposes, such as multiple environments, without touching the YAML files themselves.

[Source](https://github.com/tosin2013/responsible-ai-ml-pipeline/blob/main/applications/tutorial_bias_advertising/deployment/kustomization.yaml)
[Kustomize](https://kustomize.io/)

## Resources

This Kustomization file includes the following resources:

- **namespace.yaml**: Defines the namespace for the application.
- **tutorial-bias-advertising-is.yaml**: Configures the image stream for the tutorial bias advertising application.
- **tutorial-bias-advertising-bc.yaml**: Sets up the build configuration for the application.
- **service.yaml**: Defines the service configuration to expose the application.
- **deployment.yaml**: Configures the deployment of the application.
- **route.yaml**: Sets up the route to access the application externally.

## Usage

To use this Kustomization file, follow these steps:

1. Ensure you have `kustomize` installed in your Kubernetes environment.
2. Place the `Kustomization` file and all referenced YAML files in the same directory.
3. Run the following command to apply the configuration:
   ```sh
   kustomize build . | kubectl apply -f -
   ```
