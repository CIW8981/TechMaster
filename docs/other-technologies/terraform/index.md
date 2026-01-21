# Terraform

Terraform is an open-source infrastructure as code (IaC) tool that allows you to define and provision infrastructure using a declarative configuration language.

## Overview

Terraform enables you to safely and predictably create, change, and improve infrastructure. It codifies APIs into declarative configuration files that can be shared, versioned, and treated as code.

## Key Features

### Infrastructure as Code
- Define infrastructure in human-readable configuration files
- Version control your infrastructure
- Share and reuse configurations

### Execution Plans
- Preview changes before applying them
- Understand what Terraform will do before making changes
- Reduce risk of unexpected modifications

### Resource Graph
- Build a dependency graph of resources
- Parallelize creation and modification of resources
- Understand resource relationships

### State Management
- Track resource metadata and dependencies
- Enable collaboration through remote state
- Detect configuration drift

## Core Concepts

### Providers
- Plugins that interact with cloud providers and APIs
- Support for AWS, Azure, GCP, and hundreds of other services
- Define available resources and data sources

### Resources
- Infrastructure objects managed by Terraform
- Can be compute instances, networks, storage, etc.
- Defined in configuration files

### Modules
- Reusable Terraform configurations
- Encapsulate groups of resources
- Enable code organization and sharing

### State
- Mapping between configuration and real-world resources
- Stored locally or remotely
- Critical for Terraform operations

## Common Use Cases

- **Multi-Cloud Infrastructure**: Manage resources across multiple cloud providers
- **Environment Provisioning**: Create consistent dev, staging, and production environments
- **Disaster Recovery**: Quickly recreate infrastructure from code
- **Compliance and Governance**: Enforce infrastructure standards through code

## Terraform Workflow

1. **Write**: Define infrastructure in configuration files
2. **Plan**: Preview changes before applying
3. **Apply**: Provision infrastructure
4. **Destroy**: Remove infrastructure when no longer needed

## Related Topics

- [AWS Services](../../aws/index.md) - AWS infrastructure management
- [Kubernetes](../kubernetes/index.md) - Container orchestration
- [Docker](../docker/index.md) - Container platform
