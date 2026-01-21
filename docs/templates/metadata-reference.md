# Page Metadata Reference

This document provides a comprehensive reference for the metadata structure used across all TechMaster Learning Notes pages.

## Metadata Structure

All pages should include YAML front matter at the top of the file with the following structure:

```yaml
---
title: "Page Title"
description: "Brief description for SEO and previews"
tags:
  - tag1
  - tag2
  - tag3
certification:  # Optional
  - cert1
  - cert2
difficulty: level
last_updated: "YYYY-MM-DD"
---
```

## Field Definitions

### Required Fields

#### title
- **Type**: String
- **Required**: Yes
- **Description**: The page title displayed in navigation and browser tabs
- **Format**: Use title case, be descriptive but concise
- **Examples**:
  - `"Amazon EC2 - AWS Service Documentation"`
  - `"AWS Solutions Architect - Study Guide"`
  - `"Docker - Learning Guide"`

#### description
- **Type**: String
- **Required**: Yes
- **Description**: Brief description for search engines and page previews
- **Format**: 1-2 sentences, 120-160 characters recommended
- **Examples**:
  - `"Comprehensive guide to Amazon EC2 including features, use cases, and best practices"`
  - `"Complete study guide for AWS Solutions Architect certification exam"`

#### tags
- **Type**: Array of strings
- **Required**: Yes
- **Description**: Tags for categorization and search
- **Format**: Lowercase, hyphenated for multi-word tags
- **Minimum**: 2 tags
- **Maximum**: 10 tags recommended
- **Examples**:
  ```yaml
  tags:
    - aws
    - compute
    - ec2
    - virtual-machines
  ```

#### difficulty
- **Type**: String (enum)
- **Required**: Yes
- **Description**: Content difficulty level
- **Valid Values**:
  - `beginner`: Introductory content, no prerequisites
  - `intermediate`: Requires basic understanding
  - `advanced`: Deep technical content, significant experience required
- **Example**: `difficulty: intermediate`

#### last_updated
- **Type**: String (date)
- **Required**: Yes
- **Description**: Date of last content update
- **Format**: `YYYY-MM-DD` (ISO 8601)
- **Example**: `last_updated: "2024-01-21"`

### Optional Fields

#### certification
- **Type**: Array of strings
- **Required**: No (but recommended for AWS content)
- **Description**: Relevant AWS certifications
- **Valid Values**:
  - `cloud-practitioner`
  - `solutions-architect`
  - `developer`
  - `sysops`
  - `devops-engineer`
  - `advanced-networking`
  - `security-specialty`
  - `machine-learning-specialty`
  - `database-specialty`
  - `data-analytics-specialty`
  - `sap-on-aws-specialty`
- **Example**:
  ```yaml
  certification:
    - solutions-architect
    - developer
  ```

#### exam_code
- **Type**: String
- **Required**: No (only for certification pages)
- **Description**: Official AWS exam code
- **Format**: Uppercase with hyphen
- **Examples**:
  - `exam_code: "CLF-C02"`
  - `exam_code: "SAA-C03"`
  - `exam_code: "DVA-C02"`

## Tag Categories

### AWS Service Tags

**Primary Tag**: Always include `aws` as the first tag

**Category Tags** (choose one):
- `compute`
- `storage`
- `networking`
- `databases`
- `security`
- `management`
- `analytics`
- `machine-learning`
- `developer-tools`
- `migration`
- `containers`
- `serverless`

**Service Tags** (specific service):
- `ec2`
- `s3`
- `lambda`
- `rds`
- `dynamodb`
- `vpc`
- `cloudfront`
- `iam`
- `cloudwatch`
- etc.

**Example**:
```yaml
tags:
  - aws
  - compute
  - ec2
  - virtual-machines
  - auto-scaling
```

### Certification Tags

**Primary Tags**: Always include both `aws` and `certification`

**Level Tags** (choose one):
- `foundational`
- `associate`
- `professional`
- `specialty`

**Certification Name Tags**:
- `cloud-practitioner`
- `solutions-architect`
- `developer`
- `sysops`
- `devops-engineer`
- `advanced-networking`
- `security-specialty`
- `machine-learning-specialty`
- `database-specialty`
- `data-analytics-specialty`

**Example**:
```yaml
tags:
  - aws
  - certification
  - associate
  - solutions-architect
  - exam-prep
```

### Technology Tags

**Primary Tag**: Technology name

**Category Tags**:
- `containers`
- `orchestration`
- `iac` (Infrastructure as Code)
- `cicd`
- `monitoring`
- `programming`
- `databases`
- `web-development`

**Specific Tags**: Related concepts or tools

**Example**:
```yaml
tags:
  - docker
  - containers
  - containerization
  - devops
```

### Resource Tags

**Primary Tag**: Resource type

**Resource Type Tags**:
- `glossary`
- `cheat-sheet`
- `practice-lab`
- `reference`
- `tutorial`
- `guide`

**Example**:
```yaml
tags:
  - aws
  - reference
  - cheat-sheet
  - quick-reference
```

## Complete Examples

### AWS Service Page

```yaml
---
title: "Amazon EC2 - AWS Service Documentation"
description: "Comprehensive guide to Amazon EC2 including features, use cases, and best practices for virtual machines in the cloud"
tags:
  - aws
  - compute
  - ec2
  - virtual-machines
  - auto-scaling
  - elastic-compute
certification:
  - solutions-architect
  - developer
  - sysops
difficulty: intermediate
last_updated: "2024-01-21"
---
```

### Certification Page

```yaml
---
title: "AWS Solutions Architect Associate - Study Guide"
description: "Complete study guide for AWS Solutions Architect Associate certification exam with practice questions and exam tips"
tags:
  - aws
  - certification
  - associate
  - solutions-architect
  - exam-prep
  - study-guide
exam_code: "SAA-C03"
difficulty: intermediate
last_updated: "2024-01-21"
---
```

### Technology Page

```yaml
---
title: "Docker - Learning Guide"
description: "Comprehensive guide to Docker including concepts, best practices, and practical examples for containerization"
tags:
  - docker
  - containers
  - containerization
  - devops
  - deployment
difficulty: beginner
last_updated: "2024-01-21"
---
```

### Resource Page

```yaml
---
title: "AWS Services Glossary"
description: "Comprehensive glossary of AWS services, terms, and concepts for quick reference"
tags:
  - aws
  - reference
  - glossary
  - terminology
  - quick-reference
difficulty: beginner
last_updated: "2024-01-21"
---
```

## Validation Checklist

Before publishing a page, verify:

- [ ] All required fields are present
- [ ] Title is descriptive and follows naming conventions
- [ ] Description is 120-160 characters
- [ ] At least 2 tags are included
- [ ] Tags follow the category structure
- [ ] Difficulty level is appropriate
- [ ] Date format is correct (YYYY-MM-DD)
- [ ] Certification tags match valid values (if applicable)
- [ ] Exam code is correct (if applicable)

## Best Practices

### Title Guidelines
- Use clear, descriptive titles
- Include the service/technology name
- Add context (e.g., "Study Guide", "Learning Guide", "Documentation")
- Keep under 60 characters for SEO

### Description Guidelines
- Write compelling, informative descriptions
- Include key topics covered
- Use action words (learn, master, understand)
- Optimize for search engines

### Tag Guidelines
- Start with broad tags, then get specific
- Use consistent tag names across pages
- Avoid redundant tags
- Include both category and specific tags
- Use lowercase and hyphens

### Difficulty Guidelines
- **Beginner**: No prerequisites, introductory content
- **Intermediate**: Assumes basic knowledge, practical examples
- **Advanced**: Deep technical content, complex scenarios

### Update Frequency
- Update `last_updated` when making significant content changes
- Minor typo fixes don't require date updates
- Review and update content quarterly

## Metadata in MkDocs

The metadata is used by MkDocs and plugins for:

- **Search**: Tags improve search relevance
- **Navigation**: Title appears in menus
- **SEO**: Description used in meta tags
- **Tags Plugin**: Creates tag pages and indexes
- **Git Plugin**: Shows last modified dates
- **Social Cards**: Generates preview images

## Tools and Validation

### Metadata Validation Script

```python
# validate_metadata.py
import yaml
import sys
from pathlib import Path

def validate_metadata(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract front matter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            metadata = yaml.safe_load(parts[1])
            
            # Validate required fields
            required = ['title', 'description', 'tags', 'difficulty', 'last_updated']
            for field in required:
                if field not in metadata:
                    print(f"Missing required field: {field}")
                    return False
            
            # Validate difficulty
            if metadata['difficulty'] not in ['beginner', 'intermediate', 'advanced']:
                print(f"Invalid difficulty: {metadata['difficulty']}")
                return False
            
            # Validate tags
            if not isinstance(metadata['tags'], list) or len(metadata['tags']) < 2:
                print("Tags must be a list with at least 2 items")
                return False
            
            print("Metadata validation passed!")
            return True
    
    print("No front matter found")
    return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        validate_metadata(sys.argv[1])
```

## Additional Resources

- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [YAML Specification](https://yaml.org/spec/)
- [SEO Best Practices](https://developers.google.com/search/docs)
