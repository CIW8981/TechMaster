# Docker

Docker is a platform for developing, shipping, and running applications in containers. Containers allow you to package an application with all its dependencies into a standardized unit for software development.

## Overview

Docker provides the ability to package and run an application in a loosely isolated environment called a container. This isolation and security allows you to run many containers simultaneously on a given host.

## Key Concepts

### Containers
- Lightweight, standalone, executable packages
- Include everything needed to run an application
- Isolated from other containers and the host system

### Images
- Read-only templates used to create containers
- Built from Dockerfiles
- Can be shared via Docker registries

### Dockerfile
- Text file containing instructions to build a Docker image
- Defines the base image, dependencies, and configuration

### Docker Compose
- Tool for defining and running multi-container applications
- Uses YAML files to configure application services

## Common Use Cases

- **Microservices Architecture**: Deploy and manage microservices independently
- **Development Environments**: Consistent development environments across teams
- **CI/CD Pipelines**: Build, test, and deploy applications automatically
- **Application Isolation**: Run multiple versions of applications on the same host

## Getting Started

Learn more about Docker fundamentals, commands, and best practices in the sections below.

## Related Topics

- [Kubernetes](../kubernetes/index.md) - Container orchestration
- [AWS ECS](../../aws/compute/index.md) - AWS container service
