# Development Scripts

This directory contains automation scripts for developing and maintaining the MkDocs site.

## Available Scripts

All scripts should be run using `pipenv run <script>` for proper environment management.

### dev.py
**Purpose:** Start local development server with live reload

**Usage:**
```bash
pipenv run dev
```

**Features:**
- Starts MkDocs development server on http://127.0.0.1:8000
- Enables live reload for instant preview of changes
- Automatically watches for file changes

---

### build.py
**Purpose:** Build the static site for production

**Usage:**
```bash
pipenv run build
```

**Features:**
- Cleans previous build directory
- Builds site with strict mode enabled
- Validates configuration and content
- Outputs to `site/` directory

---

### validate.py
**Purpose:** Validate content for common issues

**Usage:**
```bash
pipenv run validate
```

**Checks:**
- ✅ Broken internal links
- ✅ Empty markdown files
- ✅ Missing title headings
- ✅ Unclosed code blocks
- ✅ Missing metadata frontmatter

---

### test.py
**Purpose:** Run all validation and build checks

**Usage:**
```bash
pipenv run test
```

**Runs:**
1. Content validation
2. Build test

---

## Quick Reference

| Task | Command |
|------|---------|
| Start dev server | `pipenv run dev` |
| Build site | `pipenv run build` |
| Validate content | `pipenv run validate` |
| Run all tests | `pipenv run test` |
| Deploy to GitHub Pages | `pipenv run deploy` |

## Exit Codes

All scripts follow standard exit code conventions:
- `0` - Success
- `1` - Failure

This allows integration with CI/CD pipelines and automated workflows.

## Requirements

- Python 3.12+
- MkDocs and dependencies (installed via pipenv)

## Integration with CI/CD

These scripts can be integrated into CI/CD pipelines using pipenv:

```yaml
# Example GitHub Actions workflow
- name: Install dependencies
  run: |
    pip install pipenv
    pipenv install

- name: Validate Content
  run: pipenv run validate

- name: Build Site
  run: pipenv run build

- name: Deploy to GitHub Pages
  run: pipenv run deploy
```

## Direct Script Execution

If needed, scripts can also be run directly:

```bash
python scripts/dev.py
python scripts/build.py
python scripts/validate.py
python scripts/test.py
```

However, using `pipenv run` is recommended to ensure the correct environment.
