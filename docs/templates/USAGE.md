# Template Usage Guide

Quick reference for using the TechMaster Learning Notes templates.

## Quick Start

1. **Choose the right template** based on your content type
2. **Copy the template** to your target location
3. **Update the metadata** in the YAML front matter
4. **Fill in the content** replacing all `[placeholders]`
5. **Add to navigation** in `mkdocs.yml`

## Template Selection

| Content Type | Template File | Use For |
|--------------|---------------|---------|
| AWS Services | `aws-service-template.md` | EC2, S3, Lambda, RDS, etc. |
| Certifications | `certification-template.md` | Exam study guides |
| Technologies | `technology-template.md` | Docker, Kubernetes, Terraform, etc. |

## Example Workflow

### Creating an AWS Service Page

```bash
# 1. Copy template
cp docs/templates/aws-service-template.md docs/aws/compute/lambda.md

# 2. Edit the file and update:
#    - YAML front matter (title, description, tags, etc.)
#    - Replace [Service Name] with "AWS Lambda"
#    - Fill in all sections with Lambda-specific content

# 3. Add to mkdocs.yml navigation:
#    - Lambda: aws/compute/lambda.md

# 4. Build and preview
mkdocs serve
```

### Creating a Certification Page

```bash
# 1. Copy template
cp docs/templates/certification-template.md docs/certifications/aws-developer/index.md

# 2. Update metadata and content
# 3. Add to navigation in mkdocs.yml
# 4. Test the build
mkdocs build --strict
```

## Metadata Quick Reference

### Minimal Required Metadata

```yaml
---
title: "Your Page Title"
description: "Brief description for SEO"
tags:
  - primary-tag
  - secondary-tag
difficulty: beginner
last_updated: "2024-01-21"
---
```

### Full Metadata (AWS Content)

```yaml
---
title: "Amazon EC2 - AWS Service Documentation"
description: "Comprehensive guide to Amazon EC2"
tags:
  - aws
  - compute
  - ec2
certification:
  - solutions-architect
  - developer
difficulty: intermediate
last_updated: "2024-01-21"
---
```

## Common Placeholders to Replace

| Placeholder | Replace With | Example |
|-------------|--------------|---------|
| `[Service Name]` | Actual service name | Amazon EC2 |
| `[Category]` | Service category | Compute |
| `[Technology Name]` | Technology name | Docker |
| `[Certification Name]` | Cert name | Solutions Architect |
| `[EXAM-CODE]` | Exam code | SAA-C03 |
| `YYYY-MM-DD` | Current date | 2024-01-21 |

## Styling Classes

### Difficulty Badges

```html
<span class="difficulty-beginner">Beginner</span>
<span class="difficulty-intermediate">Intermediate</span>
<span class="difficulty-advanced">Advanced</span>
```

### Certification Badges

```html
<span class="cert-badge">Cloud Practitioner</span>
<span class="cert-badge">Solutions Architect</span>
```

## Admonition Types

```markdown
!!! info "Title"
    Information content

!!! tip "Title"
    Tips and best practices

!!! warning "Title"
    Warnings and cautions

!!! success "Title"
    Success messages

!!! failure "Title"
    Error conditions

!!! question "Title"
    Practice questions

!!! example "Title"
    Examples and use cases
```

## Testing Your Content

```bash
# Build with strict mode (catches errors)
mkdocs build --strict

# Serve locally for preview
mkdocs serve

# Check for broken links (if you have a link checker)
# Add your link checking command here
```

## Resources

- **Full Documentation**: See `README.md` in this directory
- **Metadata Reference**: See `metadata-reference.md`
- **Example Page**: See `example-aws-service.md`
- **Custom CSS**: `docs/stylesheets/extra.css`

## Tips

- Start with the example page to see a complete implementation
- Use consistent terminology across related pages
- Include code examples that actually work
- Test all links before publishing
- Update the `last_updated` date when making changes
- Use tags consistently for better search results
