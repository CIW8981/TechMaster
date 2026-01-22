---
title: "AWS Signature Version 4 (SigV4)"
description: "Comprehensive guide to LocalStack Python library for local AWS cloud development and testing"
tags:
  - sigv4
  - aws
difficulty: intermediate
last_updated: "2026-01-22"
---

# SigV4
[x] what problem solved AWS Signature Version 4 (SigV4) in AWS?

It is the authentication protocol used to secure API requests by signing them with AWS credentials. 

- Authentication & Authorization
    - Verifies the identity of API callers to AWS services
    - Ensures only authorized users can access AWS resources
    - Requests expire after a short time window (typically 15 minutes)
    - Uses HMAC-SHA256 to create signatures without exposing secrets
    - Binds requests to specific AWS regions
    - Prevents cross-region request manipulation

[x] when I should use AWS Signature Version 4 (SigV4)

You shoudl use
    - Direct API Calls withou AWS SDKs
    - Creating webhook integrations that call AWS APIs
    - Building microservices that need direct AWS API access
    - Integrating non-AWS tools with AWS services
    - Implementing custom authentication flows

You DON'T need SigV4 when:
    - Using AWS SDKs (they handle signing automatically)
    - Using AWS CLI (signs requests internally)
    - Working with AWS services through the console
    - Using AWS-managed authentication (IAM roles, Cognito)   


[x] How to call secure Api gateway through Lambda?
```python
python
import boto3
import json

def lambda_handler(event, context):
    # Create API Gateway client
    client = boto3.client('apigateway')

    # Or use requests with IAM authentication
    import requests
    from botocore.auth import SigV4Auth
    from botocore.awsrequest import AWSRequest

    url = 'https://your-api-id.execute-api.region.amazonaws.com/stage/resource'

    # Make authenticated request
    request = AWSRequest(method='GET', url=url)
    SigV4Auth(boto3.Session().get_credentials(), 'execute-api', 'us-east-1').add_auth(request)

    response = requests.get(url, headers=dict(request.headers))
    return response.json()
```

[x] How does AWS Signature Version 4 (SigV4) works?

AWS Signature Version 4 (SigV4) works like a secure handshake in 4 simple steps:

1. Create a Fingerprint
• Take your HTTP request (method, URL, headers, body)
• Create a unique "fingerprint" using a hash function
• This ensures the request can't be changed without detection

2. Add Time and Location
• Include current timestamp and AWS region
• This prevents old requests from being reused (replay attacks)
• Requests expire after 15 minutes

3. Sign with Secret Key
• Use your AWS secret key to "sign" the fingerprint
• Like signing a document - proves it came from you
• The secret key never leaves your system

4. Send the Signature
• Attach the signature to your request headers
• AWS receives your request + signature
• AWS recreates the same signature using your stored secret key
• If signatures match = authentic request, if not = rejected

Think of it like this:
• You write a letter (HTTP request)
• You seal it with your unique wax seal (signature)
• The recipient checks if the seal matches your known seal
• If it matches, they know it's really from you and hasn't been tampered with




