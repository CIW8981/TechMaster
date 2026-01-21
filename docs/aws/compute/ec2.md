---
title: "Amazon EC2 (Elastic Compute Cloud)"
description: "Comprehensive guide to Amazon EC2 - virtual servers in the cloud"
tags: ["aws", "compute", "ec2", "virtual-machines"]
certification: ["cloud-practitioner", "solutions-architect", "developer", "sysops"]
difficulty: "beginner"
---

# Amazon EC2 (Elastic Compute Cloud)

Amazon Elastic Compute Cloud (EC2) provides scalable computing capacity in the AWS cloud, eliminating the need to invest in hardware upfront and allowing you to develop and deploy applications faster.

## Overview

EC2 enables you to:
- Launch virtual servers (instances) in minutes
- Scale capacity up or down based on demand
- Pay only for the capacity you use
- Choose from multiple instance types optimized for different use cases

## Key Concepts

### Instance Types

EC2 offers various instance types optimized for different use cases:

| Family | Use Case | Example Types |
|--------|----------|---------------|
| **General Purpose** | Balanced compute, memory, networking | t3, t4g, m5, m6i |
| **Compute Optimized** | High-performance processors | c5, c6i, c7g |
| **Memory Optimized** | Large datasets in memory | r5, r6i, x2idn |
| **Storage Optimized** | High sequential read/write | i3, d2, h1 |
| **Accelerated Computing** | GPU workloads | p4, g5, inf1 |

### Instance Naming Convention

Example: `m5.xlarge`
- **m** = Instance family (general purpose)
- **5** = Generation number
- **xlarge** = Size (nano, micro, small, medium, large, xlarge, 2xlarge, etc.)

## Pricing Models

### 1. On-Demand Instances
- Pay by the second (minimum 60 seconds)
- No long-term commitments
- Best for: Short-term, unpredictable workloads

**Example Pricing:**
```
t3.medium: ~$0.0416/hour
m5.large: ~$0.096/hour
```

### 2. Reserved Instances (RI)
- 1 or 3-year commitment
- Up to 75% discount compared to On-Demand
- Best for: Steady-state, predictable workloads

**Types:**
- **Standard RI**: Highest discount, less flexibility
- **Convertible RI**: Lower discount, can change instance attributes

### 3. Spot Instances
- Bid on spare EC2 capacity
- Up to 90% discount
- Can be interrupted with 2-minute warning
- Best for: Fault-tolerant, flexible workloads

### 4. Dedicated Hosts
- Physical server dedicated to your use
- Compliance and licensing requirements
- Most expensive option

## Storage Options

### Amazon EBS (Elastic Block Store)
Persistent block storage volumes for EC2 instances.

**Volume Types:**
```yaml
gp3 (General Purpose SSD):
  - IOPS: 3,000-16,000
  - Throughput: 125-1,000 MB/s
  - Use: Boot volumes, dev/test

io2 (Provisioned IOPS SSD):
  - IOPS: Up to 64,000
  - Durability: 99.999%
  - Use: Critical databases

st1 (Throughput Optimized HDD):
  - Throughput: Up to 500 MB/s
  - Use: Big data, data warehouses

sc1 (Cold HDD):
  - Lowest cost
  - Use: Infrequent access
```

### Instance Store
- Temporary block storage physically attached to host
- Data lost when instance stops/terminates
- High I/O performance
- No additional cost

## Security

### Security Groups
Virtual firewall controlling inbound and outbound traffic.

**Example Configuration:**
```
Inbound Rules:
- Type: SSH, Protocol: TCP, Port: 22, Source: 0.0.0.0/0
- Type: HTTP, Protocol: TCP, Port: 80, Source: 0.0.0.0/0
- Type: HTTPS, Protocol: TCP, Port: 443, Source: 0.0.0.0/0

Outbound Rules:
- Type: All traffic, Protocol: All, Port: All, Destination: 0.0.0.0/0
```

**Best Practices:**
- Use least privilege principle
- Restrict SSH access to specific IP ranges
- Use separate security groups for different tiers
- Regularly audit security group rules

### Key Pairs
- Public-key cryptography for secure login
- AWS stores public key, you store private key
- Required for SSH access to Linux instances
- Required for RDP password retrieval on Windows

## Networking

### Elastic IP Addresses
- Static IPv4 address for dynamic cloud computing
- Associated with your AWS account
- Can be remapped to different instances
- Charged when not associated with running instance

### Elastic Network Interfaces (ENI)
- Virtual network card
- Can attach multiple ENIs to an instance
- Useful for network and security appliances
- Attributes follow the ENI when reattached

### Placement Groups
Logical grouping of instances for specific networking needs:

**Cluster:** Low latency, high throughput (same AZ)
**Spread:** Reduced correlated failures (different hardware)
**Partition:** Large distributed workloads (Hadoop, Cassandra)

## Auto Scaling

Automatically adjust capacity to maintain performance and optimize costs.

### Components

**Launch Template/Configuration:**
```yaml
AMI ID: ami-0abcdef1234567890
Instance Type: t3.medium
Key Pair: my-key-pair
Security Groups: [sg-12345678]
User Data: |
  #!/bin/bash
  yum update -y
  yum install -y httpd
  systemctl start httpd
```

**Auto Scaling Group:**
- Minimum capacity: 2
- Desired capacity: 4
- Maximum capacity: 10

**Scaling Policies:**
- Target tracking: Maintain CPU at 70%
- Step scaling: Add 2 instances when CPU > 80%
- Scheduled scaling: Scale up at 9 AM, down at 6 PM

## Monitoring and Management

### CloudWatch Metrics
**Basic Monitoring (free, 5-minute intervals):**
- CPU utilization
- Network in/out
- Disk read/write
- Status checks

**Detailed Monitoring (paid, 1-minute intervals):**
- More granular data
- Faster response to changes

### Status Checks
- **System Status Check**: AWS infrastructure issues
- **Instance Status Check**: Instance-specific issues

### EC2 Instance Metadata
Access instance information from within the instance:
```bash
# Get instance ID
curl http://169.254.169.254/latest/meta-data/instance-id

# Get instance type
curl http://169.254.169.254/latest/meta-data/instance-type

# Get public IP
curl http://169.254.169.254/latest/meta-data/public-ipv4
```

## Common Use Cases

### 1. Web Application Hosting
```
Architecture:
- Application Load Balancer
- Auto Scaling Group (t3.medium instances)
- RDS database backend
- S3 for static content
```

### 2. Batch Processing
```
Architecture:
- Spot Instances for cost savings
- S3 for input/output data
- CloudWatch Events for scheduling
- Lambda for orchestration
```

### 3. High-Performance Computing
```
Architecture:
- Compute-optimized instances (c5n.18xlarge)
- Cluster placement group
- Enhanced networking (ENA)
- EBS-optimized instances
```

## Best Practices

### Cost Optimization
- Right-size instances based on actual usage
- Use Reserved Instances for predictable workloads
- Leverage Spot Instances for fault-tolerant workloads
- Stop instances when not in use (dev/test environments)
- Use Auto Scaling to match capacity with demand

### Security
- Use IAM roles instead of access keys
- Enable encryption for EBS volumes
- Regularly patch and update instances
- Use Systems Manager for patch management
- Implement least privilege access

### Reliability
- Deploy across multiple Availability Zones
- Use Auto Scaling for fault tolerance
- Regular backups with EBS snapshots
- Implement health checks
- Use Elastic Load Balancing

### Performance
- Choose appropriate instance type for workload
- Use enhanced networking when available
- Enable EBS optimization
- Use placement groups for low latency
- Monitor and optimize based on CloudWatch metrics

## Hands-On Example

### Launching an EC2 Instance (AWS CLI)

```bash
# Create a key pair
aws ec2 create-key-pair \
  --key-name my-key-pair \
  --query 'KeyMaterial' \
  --output text > my-key-pair.pem

# Set permissions
chmod 400 my-key-pair.pem

# Launch instance
aws ec2 run-instances \
  --image-id ami-0abcdef1234567890 \
  --instance-type t3.micro \
  --key-name my-key-pair \
  --security-group-ids sg-12345678 \
  --subnet-id subnet-12345678 \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=MyWebServer}]'

# Connect to instance
ssh -i my-key-pair.pem ec2-user@<public-ip>
```

## Exam Tips

### For Cloud Practitioner
- Understand different pricing models and when to use each
- Know the difference between instance store and EBS
- Understand security groups basics
- Know what Auto Scaling does

### For Solutions Architect
- Design multi-AZ architectures for high availability
- Choose appropriate instance types for different workloads
- Understand placement groups and when to use them
- Design cost-optimized solutions with Reserved and Spot Instances

### For Developer
- Understand how to use EC2 metadata service
- Know how to configure user data for instance initialization
- Understand IAM roles for EC2
- Know how to use AWS CLI/SDKs with EC2

## Related Services

- **Amazon EBS** - Block storage for EC2
- **Elastic Load Balancing** - Distribute traffic across instances
- **Auto Scaling** - Automatic capacity management
- **AWS Lambda** - Serverless alternative to EC2
- **Amazon VPC** - Virtual network for EC2 instances

## Additional Resources

- [EC2 User Guide](https://docs.aws.amazon.com/ec2/)
- [EC2 Instance Types](https://aws.amazon.com/ec2/instance-types/)
- [EC2 Pricing](https://aws.amazon.com/ec2/pricing/)
- [EC2 Best Practices](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-best-practices.html)
