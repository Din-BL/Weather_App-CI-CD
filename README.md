# **Python CI/CD Application with Terraform, EKS, and Argo CD**

---

## **Overview**

This project is a Python-based application with a CI/CD pipeline designed for seamless automation of development, testing, and deployment processes. It integrates key DevOps tools like Jenkins, Docker, Terraform, EKS (Elastic Kubernetes Service), and Argo CD to provide a scalable, automated deployment workflow.

---

## **Table of Contents**

1. [Features](#features)
2. [Workflow Overview](#workflow-overview)
3. [Project Structure](#project-structure)
4. [Requirements](#requirements)
5. [Setup and Usage](#setup-and-usage)
6. [Benefits](#benefits)

---

## **Features**

- **Python Application**: Implements core functionality using Python.
- **CI/CD Automation**: Jenkins pipeline automates testing, building, and deploying the application.
- **Containerization**: Dockerized for consistent deployment across environments.
- **Infrastructure as Code**: Terraform provisions a custom VPC, subnets, and an EKS cluster.
- **Kubernetes Management**: EKS manages scalable container orchestration.
- **Continuous Deployment**: Argo CD synchronizes Kubernetes manifests with the EKS cluster.

---

## **Workflow Overview**

1. **Code Changes**: Developers commit code to a GitLab repository, triggering the CI/CD pipeline via a webhook.
2. **CI/CD Pipeline Stages**:
   - **Build**: Jenkins builds a Docker image of the application.
   - **Test**: Automated tests validate functionality.
   - **Push**: The Docker image is pushed to a container registry (e.g., Docker Hub).
   - **Deploy**: Argo CD deploys the updated Kubernetes manifests to EKS.
3. **Infrastructure Provisioning**:
   - Terraform provisions a custom VPC with public and private subnets.
   - EKS is deployed within the VPC to manage Kubernetes workloads.
4. **Continuous Deployment**:
   - Argo CD automatically syncs changes in Kubernetes manifests to the EKS cluster.
5. **Blue-Green Deployment**: Ensures zero-downtime updates during production deployments.

---

## **Project Structure**

- **`app.py`**: Main Python application file.
- **`Dockerfile`**: Builds the application container.
- **`Jenkinsfile`**: Defines CI/CD pipeline stages.
- **`test/`**: Directory containing test files for validation.
- **`terraform/`**: Directory with Terraform files for infrastructure provisioning.
- **`k8s/`**: Kubernetes manifests for deploying the application.

---

## **Requirements**

- Python 3.8+
- Jenkins
- Docker
- Terraform
- Kubernetes CLI (`kubectl`)
- Argo CD CLI

---

## **Setup and Usage**

### **1. Clone the Repository**

```bash
git clone <repository-url>
```

### **2. Set Up Infrastructure**

Run Terraform commands to provision the required infrastructure:

```bash
cd terraform/
terraform init
terraform apply
```

### **3. Configure Jenkins Pipeline**

- Add the `Jenkinsfile` to your Jenkins server.
- Configure the pipeline with necessary credentials and environment variables.

### **4. Deploy with Argo CD**

Create and synchronize your application with Argo CD:

```bash
argocd app create <app-name> \
  --repo <repo-url> \
  --path <path-to-manifests> \
  --dest-namespace <namespace> \
  --dest-server <cluster-server>
argocd app sync <app-name>
```

---

## **Benefits**

- **Automation**: Fully automated CI/CD pipeline reduces manual effort.
- **Scalability**: EKS provides a robust and scalable infrastructure for container orchestration.
- **Reliability**: Argo CD ensures smooth and efficient deployments with automated synchronization.
- **Efficiency**: Streamlined workflows for faster development and deployment cycles.

---

This project simplifies the deployment process while ensuring scalability and reliability for Python applications. 🚀
