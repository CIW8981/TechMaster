# Kubernetes

Kubernetes (K8s) is an open-source container orchestration platform that automates the deployment, scaling, and management of containerized applications.

## Overview

Kubernetes provides a framework to run distributed systems resiliently. It handles scaling and failover for your applications, provides deployment patterns, and manages service discovery and load balancing.

## Core Components

### Control Plane
- **API Server**: Central management point for the cluster
- **Scheduler**: Assigns pods to nodes based on resource requirements
- **Controller Manager**: Runs controller processes
- **etcd**: Distributed key-value store for cluster data

### Node Components
- **Kubelet**: Agent that runs on each node
- **Container Runtime**: Software for running containers (Docker, containerd)
- **Kube-proxy**: Network proxy for service networking

## Key Concepts

### Pods
- Smallest deployable units in Kubernetes
- Can contain one or more containers
- Share network and storage resources

### Services
- Abstract way to expose applications running on pods
- Provide stable networking endpoints
- Support load balancing across pods

### Deployments
- Declarative updates for pods and replica sets
- Manage application rollouts and rollbacks
- Ensure desired number of replicas are running

### ConfigMaps and Secrets
- **ConfigMaps**: Store non-confidential configuration data
- **Secrets**: Store sensitive information like passwords and tokens

## Use Cases

- **Container Orchestration**: Automated deployment and scaling
- **High Availability**: Self-healing and fault tolerance
- **Multi-Cloud Deployments**: Run applications across different cloud providers
- **Microservices Management**: Coordinate complex microservices architectures

## Related Topics

- [Docker](../docker/index.md) - Container platform
- [AWS EKS](../../aws/compute/index.md) - AWS Kubernetes service
- [Terraform](../terraform/index.md) - Infrastructure as code
