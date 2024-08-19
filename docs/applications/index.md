---
layout: default
title: Applications
nav_order: 3
has_children: true
---


Examples of using OpenShift's orchestration capabilities to ensure high availability, scalability, and resource efficiency. In these examples IBM AI Fairness 360 will use OpenShift's built-in security features for authentication and authorization. The workload might also integrate with other AI/ML tools in the OpenShift ecosystem, such as Jupyter notebooks for interactive analysis or MLflow for model tracking. Overall, this setup would enable data scientists and developers to easily incorporate fairness considerations into their ML workflows within a robust, cloud-native environment.

# Deployment to OpenShift

This section provides detailed instructions on how to deploy the Tutorial Bias Advertising application to OpenShift using the provided configuration files.

## Deployment Files

- **deployment/deployment.yaml**: This file defines the deployment configuration, including the number of replicas, the container image to use, and resource limits.
- **deployment/service.yaml**: This file defines the service configuration, which exposes the deployment to the network.
- **deployment/route.yaml**: This file defines the route configuration, which exposes the service to the outside world.
- **deployment/namespace.yaml**: This file defines the namespace where the application will be deployed.
- **deployment/tutorial-bias-advertising-bc.yaml**: This file defines the build configuration for the application.
- **deployment/tutorial-bias-advertising-is.yaml**: This file defines the ImageStream configuration, which is already documented in this document.

## Step-by-Step Deployment Instructions

1. **Create the Namespace**:
   ```sh
   oc apply -f deployment/namespace.yaml
   ```

2. **Create the Build Configuration**:
   ```sh
   oc apply -f deployment/tutorial-bias-advertising-bc.yaml
   ```

3. **Create the ImageStream**:
   ```sh
   oc apply -f deployment/tutorial-bias-advertising-is.yaml
   ```

4. **Create the Deployment**:
   ```sh
   oc apply -f deployment/deployment.yaml
   ```

5. **Create the Service**:
   ```sh
   oc apply -f deployment/service.yaml
   ```

6. **Create the Route**:
   ```sh
   oc apply -f deployment/route.yaml
   ```

By following these steps, you will successfully deploy the Tutorial Bias Advertising application to OpenShift.
