---
# Responsible AI ML Pipeline: Integrating OpenShift and IBM AI Fairness 360

layout: home
---

The [Responsible AI ML Pipeline: Integrating OpenShift and IBM AI Fairness 360](https://github.com/tosin2013/responsible-ai-ml-pipeline) repository demonstrates how to build a responsible AI pipeline by integrating Red Hat OpenShift with IBM AI Fairness 360 (AIF360) to detect and mitigate bias in machine learning models. It provides examples and tools for developing fair and ethical AI systems using containerized workflows.

## Key Features
- Detect and mitigate bias using IBM AI Fairness 360
- Deploy ML workloads on Red Hat OpenShift
- Scalable and secure AI pipelines with Kubernetes

## Getting Started

### Prerequisites
- Red Hat OpenShift cluster
- IBM AI Fairness 360 library
- Python 3.9+

### Deployment Instuctions
* [Step-by-Step Guide to Creating a Developer Sandbox on Red Hat OpenShift AI](https://tosin2013.github.io/responsible-ai-ml-pipeline/deployment/create-a-openshift-ai-sandbox.html)
* [Configure Data Science Project](https://tosin2013.github.io/responsible-ai-ml-pipeline/deployment/configure-data-science.html)
  
### Detecting Bias
[Mitigating Bias in Advertising]()
Use the [detect_and_mitigate_bias.ipynb](https://github.com/tosin2013/responsible-ai-ml-pipeline/blob/main/notebooks/ai360/detect_and_mitigate_bias.ipynb) notebook to identify bias in your datasets and models using AIF360.

### Mitigating Bias in Advertising
[Discover, Measure, and Mitigate Bias in Advertising](https://tosin2013.github.io/responsible-ai-ml-pipeline/ai360/tutorial_bias_advertising.html)
The [tutorial_bias_advertising.ipynb]([notebooks/ai360/tutorial_bias_advertising.ipynb](https://github.com/tosin2013/responsible-ai-ml-pipeline/blob/main/notebooks/ai360/tutorial_bias_advertising.ipynb)) notebook demonstrates how to mitigate bias in an advertising scenario using AIF360 and deploy the model on OpenShift.

### Deploying on OpenShift - Discover, Measure, and Mitigate Bias in Advertising
Follow the instructions in [Tutorial bias advertising Deployment on OpenShift](https://tosin2013.github.io/responsible-ai-ml-pipeline/applications/tutorial_bias_advertising.html) to deploy your bias-aware models on OpenShift.

## Integration with OpenShift

This project leverages OpenShift's API to run IBM AI Fairness 360 workloads in a containerized environment. Key benefits include:

- Scalability: Easily scale your bias detection and mitigation workflows
- Security: Utilize OpenShift's built-in security features
- Reproducibility: Containerized environments ensure consistent results
- CI/CD Integration: Automate your responsible AI pipeline

To integrate with OpenShift:

1. Build a container image with your AIF360 workload
2. Push the image to your OpenShift registry
3. Deploy the workload using OpenShift's API or web console


## Acknowledgments
- IBM for developing AI Fairness 360
- Red Hat for OpenShift platform

For more information on responsible AI practices and tools, visit [IBM Research AI](https://www.research.ibm.com/artificial-intelligence/).


Links:
- [AI Fairness 360](https://aif360.res.ibm.com/)
- [Bias-Detection-and-Mitigation-in-AI](https://github.com/BirdiD/Bias-Detection-and-Mitigation-in-AI/tree/main)
- [Discover, Measure, and Mitigate Bias in Advertising](https://github.com/Trusted-AI/AIF360/blob/main/examples/tutorial_bias_advertising.ipynb)
- [About](about.markdown)
- [AI360](ai360/index.md)
- [Deployment](deployment/index.md)
