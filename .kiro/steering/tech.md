# Technology Stack

## Core Framework

- **MkDocs**: Static site generator for project documentation
- **Material for MkDocs**: Material Design theme with advanced features
- **Python 3.12**: Required runtime environment
- **pipenv**: Dependency management and virtual environment

## Key Dependencies

- `mkdocs` (>=1.5.0): Core documentation framework
- `mkdocs-material` (>=9.4.0): Material theme with navigation, search, and UI features
- `pymdown-extensions` (>=10.3.0): Markdown extensions for enhanced formatting
- `mkdocs-git-revision-date-localized-plugin` (>=1.2.0): Automatic content timestamps

## Markdown Extensions

- **Python Markdown**: abbr, admonition, attr_list, def_list, footnotes, md_in_html, toc
- **PyMdown Extensions**: arithmatex (math), betterem, caret, details, emoji, highlight, inlinehilite, keys, mark, smartsymbols, snippets, superfences (Mermaid support), tabbed, tasklist, tilde

## Plugins

- **search**: Full-text search with stemming and stop word filtering
- **tags**: Tag-based content organization
- **git-revision-date-localized**: Automatic creation/modification dates
- **mermaid2**: Diagram rendering support

## Common Commands

### Development

```bash
# Install dependencies
pipenv install

# Activate virtual environment
pipenv shell

# Start development server with live reload (http://127.0.0.1:8000)
pipenv run dev
```

### Building

```bash
# Build static site to site/ directory
pipenv run build

# Build with strict mode (catches errors)
mkdocs build --strict
```

### Validation & Testing

```bash
# Validate content (broken links, empty files, missing metadata)
pipenv run validate

# Run all validation and build checks
pipenv run test
```

### Deployment

```bash
# Deploy to GitHub Pages
pipenv run deploy
```

## File Generation

- Built site outputs to `site/` directory
- All markdown files in `docs/` are processed
- Static assets (CSS, JS, images) are copied from `docs/stylesheets/`, `docs/javascripts/`, etc.

## Configuration

- **mkdocs.yml**: Main configuration file for site structure, theme, plugins, and markdown extensions
- **Pipfile**: Python dependencies and script definitions
- **Pipfile.lock**: Locked dependency versions for reproducible builds
