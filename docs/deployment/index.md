---
layout: default
title: Deployment Instructions
nav_order: 1
has_children: true
---

Creating Workspaces for Workbooks:

In OpenShift AI, workspaces for workbooks are created through "workbenches" within data science projects. Here's how to create a workbench:

1. Log in to the OpenShift AI dashboard.
2. Navigate to "Data Science Projects" and select or create a project.
3. In the project details page, click "Create workbench".
4. Configure the workbench:
   - Provide a name and description
   - Select a notebook image (e.g., Jupyter)
   - Choose the container size
   - Configure storage (new or existing persistent storage)
5. Click "Create Workbench"

Once created, the workbench status will change from "starting" to "running". You can then open the workbench to access Jupyter notebooks and start working on your data science projects.

These workbenches provide an isolated environment where data scientists can create, edit, and run Jupyter notebooks, access necessary resources, and collaborate on AI/ML projects within the OpenShift AI platform.