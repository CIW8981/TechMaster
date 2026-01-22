# Project Structure

## Directory Organization

```
.
├── docs/                      # All content source files
│   ├── aws/                   # AWS service documentation
│   │   ├── compute/           # EC2, Lambda, etc.
│   │   ├── storage/           # S3, EBS, EFS, etc.
│   │   ├── networking/        # VPC, Route 53, CloudFront, etc.
│   │   ├── databases/         # RDS, DynamoDB, etc.
│   │   ├── security/          # IAM, KMS, etc.
│   │   └── management/        # CloudWatch, CloudFormation, etc.
│   ├── certifications/        # Certification study materials
│   │   ├── aws-cloud-practitioner/
│   │   ├── aws-solutions-architect/
│   │   ├── aws-developer/
│   │   └── aws-sysops/
│   ├── other-technologies/    # Non-AWS technologies
│   │   ├── docker/
│   │   ├── kubernetes/
│   │   ├── terraform/
│   │   └── programming/
│   ├── resources/             # Shared resources
│   │   ├── glossary.md
│   │   ├── cheat-sheets/
│   │   └── practice-labs/
│   ├── templates/             # Content templates
│   │   ├── aws-service-template.md
│   │   ├── certification-template.md
│   │   ├── technology-template.md
│   │   ├── README.md
│   │   └── USAGE.md
│   ├── includes/              # Reusable content snippets
│   ├── javascripts/           # Custom JavaScript
│   ├── stylesheets/           # Custom CSS
│   └── index.md               # Homepage
├── scripts/                   # Development automation
│   ├── dev.py                 # Start dev server
│   ├── build.py               # Build static site
│   ├── validate.py            # Content validation
│   ├── test.py                # Run all tests
│   └── README.md
├── site/                      # Generated static site (gitignored)
├── .kiro/                     # Kiro configuration
│   └── steering/              # AI assistant guidance
├── mkdocs.yml                 # MkDocs configuration
├── Pipfile                    # Python dependencies
├── Pipfile.lock               # Locked dependencies
├── DEVELOPMENT.md             # Development guide
└── .gitignore
```

## Content Organization Patterns

### AWS Services
- Each service category has its own subdirectory under `docs/aws/`
- Each service gets an `index.md` or dedicated file (e.g., `ec2.md`)
- Use `aws-service-template.md` for consistency

### Certifications
- Each certification has its own directory under `docs/certifications/`
- Main content in `index.md` within each certification folder
- Organized by exam domains and objectives
- Use `certification-template.md` for structure

### Other Technologies
- Each technology has its own directory under `docs/other-technologies/`
- Main content in `index.md` within each technology folder
- Use `technology-template.md` for consistency

## File Naming Conventions

- Use lowercase with hyphens for directories: `aws-cloud-practitioner/`
- Use lowercase with hyphens for files: `aws-service-template.md`
- Index files: Always `index.md` for directory landing pages
- Specific pages: Descriptive names like `ec2.md`, `glossary.md`

## Navigation Structure

Navigation is defined in `mkdocs.yml` under the `nav:` section. Structure follows:

```yaml
nav:
  - Home: index.md
  - AWS Technologies:
    - Overview: aws/index.md
    - Compute: aws/compute/index.md
  - Certifications:
    - Overview: certifications/index.md
  - Other Technologies:
    - Overview: other-technologies/index.md
  - Resources:
    - Overview: resources/index.md
```

## Content Templates

Templates in `docs/templates/` provide standardized structure:

- **aws-service-template.md**: For AWS service documentation
- **certification-template.md**: For certification study guides
- **technology-template.md**: For non-AWS technologies

All templates include YAML frontmatter with metadata (title, description, tags, difficulty, last_updated).

## Metadata Structure

Every content page should include YAML frontmatter:

```yaml
---
title: "Page Title"
description: "SEO-friendly description"
tags:
  - primary-tag
  - category-tag
  - specific-tag
certification:           # Optional, for AWS content
  - solutions-architect
  - developer
difficulty: beginner|intermediate|advanced
last_updated: "YYYY-MM-DD"
---
```

## Asset Organization

- **Custom CSS**: `docs/stylesheets/extra.css`
- **Custom JavaScript**: `docs/javascripts/` (e.g., `mathjax.js`)
- **Reusable snippets**: `docs/includes/` (auto-appended via pymdownx.snippets)
- **Images**: Store near related content or in dedicated assets folder

## Build Output

- Static site generated in `site/` directory
- Includes all processed markdown, assets, search index, and theme files
- Should be gitignored (regenerated on each build)
