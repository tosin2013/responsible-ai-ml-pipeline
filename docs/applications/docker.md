---
layout: default
title: Dockerfile Tutorial Bias Advertising on OpenShift
parent: Applications
nav_order: 3
---

This Dockerfile is used to build a container image for the Bias in Advertising application. It is based on the Red Hat Universal Base Image (UBI) for Python 3.9 and includes steps to set up the application environment, install dependencies, and prepare the application for execution.

[Source](https://github.com/tosin2013/responsible-ai-ml-pipeline/blob/main/applications/tutorial_bias_advertising/Dockerfile)

## Dockerfile Directives

### FROM registry.access.redhat.com/ubi9/python-39
- **Description**: Specifies the base image to use for the build. In this case, it uses the Red Hat Universal Base Image (UBI) for Python 3.9.
- **Reasoning**: Using a UBI ensures compatibility with Red Hat environments and provides a secure, stable base for the application.

### WORKDIR /app
- **Description**: Sets the working directory for any subsequent `RUN`, `CMD`, `ENTRYPOINT`, `COPY`, and `ADD` instructions.
- **Reasoning**: Setting a working directory helps organize the application files within the container.

### RUN chgrp -R 0 /app && chmod -R g=u /app
- **Description**: Changes the group ownership of the `/app` directory to the root group and sets the permissions to allow the root group to read, write, and execute the files.
- **Reasoning**: This ensures that the application files are accessible and modifiable by the root group, which is a common practice for multi-user environments.

### COPY --chown=1001:0 requirements.txt requirements.txt
- **Description**: Copies the `requirements.txt` file from the host to the container and sets the ownership to user ID 1001 and group ID 0.
- **Reasoning**: This ensures that the `requirements.txt` file is owned by the appropriate user and group for the application.

### RUN pip install -r requirements.txt
- **Description**: Installs the Python dependencies listed in `requirements.txt`.
- **Reasoning**: This ensures that all required libraries are available in the container environment.

### COPY --chown=1001:0 . .
- **Description**: Copies the rest of the application files from the host to the container, setting the ownership to user ID 1001 and group ID 0.
- **Reasoning**: This ensures that all application files are available in the container and owned by the appropriate user and group.

### RUN curl -OL https://dax-cdn.cdn.appdomain.cloud/dax-bias-in-advertising/1.0.0/bias-in-advertising.tar.gz \
    && tar -zxvf bias-in-advertising.tar.gz
- **Description**: Downloads and extracts the dataset required for the application.
- **Reasoning**: This ensures that the dataset is available in the container for the application to use.

### EXPOSE 8080
- **Description**: Informs Docker that the container listens on the specified network port at runtime.
- **Reasoning**: This allows the application to be accessed on port 8080 when the container is running.

### CMD ["python", "app.py"]
- **Description**: Specifies the command to run when the container starts.
- **Reasoning**: This starts the Python application when the container is launched.

## Additional Notes
- Ensure that the `requirements.txt` file is up-to-date with all necessary dependencies.
- The dataset URL should be accessible and reliable to avoid issues during the build process.
- The Dockerfile assumes that the application code is located in the current directory on the hos