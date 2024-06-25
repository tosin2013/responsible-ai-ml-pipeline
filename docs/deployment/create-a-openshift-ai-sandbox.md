---
layout: default
title:  "Step-by-Step Guide to Creating a Developer Sandbox on Red Hat OpenShift AI" 
parent: Deployment Instructions
nav_order: 1
---


## Step-by-Step Guide to Creating a Developer Sandbox on Red Hat OpenShift AI

### 1. Accessing the Red Hat Hybrid Cloud Console

1. **Sign In**:
   - Navigate to the [Red Hat Hybrid Cloud Console](https://console.redhat.com).
   - Sign in with your Red Hat account credentials. If you don't have an account, you can create one for free.

### 2. Setting Up the Developer Sandbox

1. **Obtain an OpenShift Cluster**:
   - Visit the [Developer Sandbox page](https://developers.redhat.com/developer-sandbox) to obtain an OpenShift cluster. This will enroll you in the Red Hat Developer Program if you aren't already a member.

2. **Start the Sandbox**:
   - Once logged in, you will see the option  dto start your sandbox. Click on **Develop in the sandbox with the Red Hat Developer program**.
   - Follow the prompts to set up your sandbox environment. This process may take a few minutes. 
![20240625180535](https://i.imgur.com/jFliZBM.png)

### 3. Accessing Red Hat OpenShift AI Platform

1. **Launch OpenShift AI**:
   - From the Developer Sandbox main page, click the **Launch** button for OpenShift AI.
   - You will be redirected to the OpenShift AI web interface, where you will need to log in using your Red Hat credentials.
![20240625180609](https://i.imgur.com/xaApyf9.png)
2. **Explore OpenShift AI**:
   - Once logged in, you will see a default Data Science project created for you. Click on the project name to access various features.

### 4. Creating and Configuring Resources

1. **Create Your First Workbench**:
   - Within your Data Science project, create a new Workbench. This will provide you with a Jupyter notebook environment pre-configured with popular data science tools like TensorFlow and PyTorch.

2. **Configure a Data Science Pipeline Server**:
   - Set up a Data Science Pipeline Server to manage and automate your machine learning workflows. This can be done through the OpenShift AI interface.

3. **Configure External S3 Storage Endpoints**:
   - If you need external storage, configure S3 storage endpoints to store and retrieve large datasets.

### 5. Deploying and Monitoring Data Science Models

1. **Create a Model Server**:
   - Set up a Model Server within OpenShift AI to serve your trained models. This allows you to deploy models as RESTful endpoints that can be accessed by other applications.

2. **Monitor Models**:
   - Use built-in monitoring tools to track the performance of your deployed models. OpenShift AI integrates with Prometheus for monitoring and Grafana for visualization.

### 6. Continuous Monitoring and Feedback

1. **Track Fairness Metrics**:
   - Continuously monitor fairness metrics such as statistical parity and equal opportunity. Use tools like Fiddler or IBM Fairway to detect any fairness drift over time.

2. **Implement Feedback Loop**:
   - Retrain models with updated data or adjusted algorithms if fairness metrics decline. Implement human-in-the-loop approaches for reviewing and mitigating bias in sensitive situations.

### Additional Resources

- **Documentation**:
  - Refer to the [Red Hat OpenShift AI documentation](https://access.redhat.com/documentation/en-us/red_hat_openshift_ai_self-managed/2.9/html-single/introduction_to_red_hat_openshift_ai/index) for detailed technical guides and tutorials.
  
- **Learning Paths**:
  - Explore learning paths on the [Red Hat Developer Portal](https://developers.redhat.com/products/red-hat-openshift-ai/getting-started) to build skills in training, deploying, and serving models in Red Hat OpenShift AI.

- **Support**:
  - If you need help, you can contact Red Hat support through the [Red Hat Customer Portal](https://access.redhat.com).

By following these steps, you can effectively create a developer sandbox for data science, access the Red Hat OpenShift AI platform, and deploy and monitor your data science models. This setup provides a robust environment for experimenting with AI/ML models in a secure and scalable manner.

