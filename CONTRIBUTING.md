# Contributing to the Project

Thank you for your interest in contributing to our project! This document will guide you through the process of setting up your development environment, creating new notebooks, and adding new applications to the project.

## Setting Up Your Development Environment

### 1. Creating a Developer Sandbox on Red Hat OpenShift AI

Follow the detailed guide in [docs/deployment/create-a-openshift-ai-sandbox.md](docs/deployment/create-a-openshift-ai-sandbox.md) to set up your developer sandbox on Red Hat OpenShift AI. This will provide you with the necessary environment to develop and test your contributions.

### 2. Configuring Data Science Workloads

Refer to [docs/deployment/configure-data-science.md](docs/deployment/configure-data-science.md) for instructions on how to configure data science workloads in your sandbox. This includes setting up workbenches, cloning repositories, and running notebooks.

## Creating New Notebooks

### 1. Using the Tutorial Bias Advertising Notebook as a Template

You can use the [notebooks/ai360/tutorial_bias_advertising.ipynb](notebooks/ai360/tutorial_bias_advertising.ipynb) as a template for creating new notebooks. This notebook demonstrates how to discover, measure, and mitigate bias in advertising data using the AI Fairness 360 (AIF360) toolkit.

### 2. Guidelines for New Notebooks

- Ensure that your notebook follows the structure and style of the existing notebooks.
- Include detailed markdown cells explaining each step of the process.
- Use clear and descriptive variable names.
- Add comments in your code to explain complex sections.

## Adding New Applications

### 1. Using the Tutorial Bias Advertising Application as a Template

Refer to [applications/tutorial_bias_advertising/README.md](applications/tutorial_bias_advertising/README.md) for instructions on how to deploy and test the tutorial bias advertising application. You can use this as a template for creating new applications.

### 2. Guidelines for New Applications

- Create a new directory for your application under the `applications` directory.
- Include a `README.md` file with instructions on how to deploy and test your application.
- Use Kubernetes YAML files for defining deployment configurations.
- Ensure that your application is well-documented and includes clear instructions for setup and usage.

## Submitting Your Contributions

1. Fork the repository and create your branch from `main`.
2. Make your changes and ensure that your code is well-documented.
3. Test your changes thoroughly in your development environment.
4. Submit a pull request to the main repository.
5. Ensure that your pull request includes a detailed description of the changes you made.

Thank you for contributing to our project!
