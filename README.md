# EKS-Based CI/CD Pipeline Architecture

## Overview
This project demonstrates a robust CI/CD pipeline architecture deployed on AWS using Kubernetes (EKS) and Terraform. The pipeline integrates GitLab, Jenkins, SonarQube, Snyk, Docker Hub, Argo CD, and Slack to automate code management, testing, deployment, and notification processes.

## Architecture Details

### VPC and Infrastructure
- **Custom VPC**: Contains both private and public subnets spread across two Availability Zones (AZs).
  - **AZ1**:
    - **Private Subnet**: Hosts the following components running in containers:
      - GitLab (Version Control)
      - Jenkins (CI Server)
      - SonarQube (Static Code Analysis)
      - Snyk (Security Scanning)
      - Jenkins Dynamic Agent (for pipeline execution)
  - **AZ2**:
    - **Private Subnet**: Also contains EKS node groups running application pods.
  - **Both AZs**:
    - EKS Node Groups are deployed across both AZs for high availability and scalability.
  - **Public Subnet**: Contains the Application Load Balancer (ALB) for routing external traffic.

### CI/CD Pipeline
The CI/CD process is implemented in Jenkins and follows these stages:
1. **SCM**: GitLab handles source code changes, triggering the pipeline via webhooks.
2. **Static Code Analysis**: Snyk and SonarQube validate code quality and security.
3. **Unit Tests**: Automated tests ensure application functionality.
4. **Build**: Jenkins builds the Docker image for the application.
5. **Publish**: The Docker image is pushed to Docker Hub.
6. **Security Scan**: Snyk scans the Docker image for vulnerabilities.
7. **Kubernetes Manifests Update**: The Kubernetes manifests in GitLab are updated to reflect the new deployment version.
8. **Notification**: Slack notifications are sent to the team for updates.

### Continuous Deployment
- **Argo CD**: Monitors the Kubernetes manifests in the GitLab repository and applies updates to the EKS cluster.
- **Deployment Strategy**: Uses Blue-Green Deployment to ensure zero-downtime updates.

### Infrastructure Provisioning
- **Terraform**:
  - Provisions the custom VPC, subnets, and EKS cluster.
  - Creates the EKS node groups across both AZs in the private subnets.

## Key Benefits
- **Automation**: Streamlined CI/CD processes with minimal manual intervention.
- **Scalability**: EKS ensures high availability and scalability for application workloads.
- **Security**: Snyk and SonarQube provide comprehensive code quality and security checks.
- **Zero Downtime**: Blue-Green Deployment strategy minimizes risks during updates.
- **Visibility**: Slack notifications and Argo CD dashboards offer real-time visibility.

## Tools and Technologies
- **GitLab**: Source code management and version control.
- **Jenkins**: CI server for automating builds and tests.
- **SonarQube**: Static code analysis.
- **Snyk**: Security vulnerability detection.
- **Docker Hub**: Docker image registry.
- **Argo CD**: Continuous deployment to Kubernetes.
- **AWS EKS**: Managed Kubernetes service.
- **Terraform**: Infrastructure as code tool.
- **Slack**: Team collaboration and notifications.

## Setup Instructions
1. **Provision Infrastructure**:
   - Use the provided Terraform scripts to create the VPC, subnets, and EKS cluster.
2. **Set Up CI/CD Pipeline**:
   - Configure GitLab repository and Jenkins jobs.
   - Integrate SonarQube, Snyk, and Docker Hub.
3. **Deploy Application**:
   - Commit Kubernetes manifests to GitLab.
   - Ensure Argo CD is monitoring the manifests.
4. **Monitor and Notify**:
   - Validate updates on the EKS cluster.
   - Monitor notifications via Slack.

## Future Enhancements
- Implement multi-region failover for enhanced availability.
- Integrate advanced monitoring tools like Prometheus and Grafana.
- Automate disaster recovery scenarios.


```mermaid
graph TD
    subgraph VPC
        subgraph AZ1
            subgraph PrivateSubnet1
                A["GitLab Container"]
                B["Jenkins Container"]
                C["SonarQube Container"]
                D["Snyk Container"]
                E["Jenkins Dynamic Agent"]
            end
            F["EKS Node Group"]
        end

        subgraph AZ2
            subgraph PrivateSubnet2
                G["EKS Node Group"]
            end
        end

        subgraph PublicSubnet
            H["Load Balancer (ALB)"]
        end
    end

    subgraph CI/CD Pipeline
        I["SCM: Code Changes in GitLab"] --> J["Trigger CI/CD Pipeline via Webhook"]
        J --> K["Static Code Analysis: Snyk & SonarQube"]
        K --> L["Unit Tests"]
        L --> M["Build: Jenkins builds Docker Image"]
        M --> N["Publish: Push Image to Docker Hub"]
        N --> O["Snyk Scan"]
        O --> P["Update Kubernetes Manifests in GitLab"]
        P --> Q["Notify: Slack Notifications"]
    end

    subgraph Infrastructure Provisioning
        R["Provision Custom VPC with Subnets"] --> S["Deploy EKS Cluster in VPC"]
        S --> T["Node Groups Created Across AZ1 and AZ2"]
    end

    subgraph Continuous Deployment
        U["Argo CD Monitors Kubernetes Manifests"]
        U --> V["Sync Changes to EKS Cluster"]
        V --> W["Blue-Green Deployment for Zero-Downtime Updates"]
    end

    M --> U
    T --> F
    T --> G
    Q --> U




