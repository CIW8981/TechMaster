---
title: "Kiro CLI Commands Reference"
description: "Practical reference for Kiro CLI commands with real-world use cases and examples for AI-assisted development"
tags:
  - kiro-cli
  - commands
  - reference
  - ai-development
difficulty: beginner
last_updated: "2026-05-13"
---

# Kiro CLI Commands Reference

!!! info "Quick Reference"
    This page covers the most useful Kiro CLI commands with practical examples. Type `/help` inside any session to see all available commands.

## Starting a Session

### Basic Usage

```bash
# Start interactive chat (default agent + model)
kiro-cli chat

# Start with an initial prompt
kiro-cli chat "Explain this codebase"

# Start with a specific agent
kiro-cli chat --agent rust-expert

# Resume your last conversation
kiro-cli chat --resume

# Pick a conversation to resume
kiro-cli chat --resume-picker
```

### Headless Mode (Automation)

```bash
# Run a single task non-interactively
kiro-cli chat --no-interactive --trust-all-tools "Run tests and summarize results"

# Trust only specific tools
kiro-cli chat --trust-tools=fs_read,grep "Find all TODO comments in src/"

# Use in CI/CD or scripts
kiro-cli chat --no-interactive -a "Generate changelog from git log since last tag"
```

!!! tip "Headless Mode Tips"
    - Always use `--trust-all-tools` or `--trust-tools` to avoid hanging on approval prompts
    - Must provide the query as an argument
    - No interactive commands (`/model` picker, etc.) work in this mode

### Session Management

```bash
# List saved conversations
kiro-cli chat --list-sessions

# Delete a conversation
kiro-cli chat --delete-session <SESSION_ID>
```

## Essential Slash Commands

### `/plan` — Plan Before You Build

Switch to the planning agent for complex tasks. The planner asks clarifying questions, researches your codebase, and produces a step-by-step implementation plan before handing off to execution.

```text
# Switch to planning mode
/plan

# Start planning immediately with a prompt
/plan Build a REST API for user authentication with JWT

# Toggle back to execution mode
Shift + Tab
```

**Use cases:**

- Multi-file features where you're unsure of the approach
- Architectural decisions with tradeoffs
- Tasks you'd normally sketch on a whiteboard first

### `/context` — Manage What the Agent Sees

```text
# View context window usage (how full is it?)
/context

# Show all context files and their token costs
/context show

# Add files to context for this session
/context add README.md src/config.ts

# Add glob patterns
/context add docs/**/*.md

# Remove files from context
/context remove README.md

# Clear all session context
/context clear
```

**Use cases:**

| Command | When to Use |
|---------|-------------|
| `/context` | Check if you're running low on context space |
| `/context add` | Agent needs to see specific files you know are relevant |
| `/context show` | Debug why the agent isn't seeing certain files |
| `/context clear` | Free up space when context is bloated |

!!! warning "Session vs Permanent"
    `/context add` is temporary (session-only). For permanent context, define files in your agent configuration.

### `/compact` — Free Up Context Space

```text
/compact
```

Summarizes older conversation history to free context window space. Use when:

- `/context` shows high usage (>80%)
- Long conversation with many tool calls
- You want to keep working without starting fresh

### `/knowledge` — Persistent Memory

```text
# Show indexed knowledge bases
/knowledge show

# Index a directory for semantic search
/knowledge add -n "source code" -p ./src

# Index with filters
/knowledge add -n "rust-code" -p ./src --include "**/*.rs" --exclude "target/**"

# Update an existing knowledge base
/knowledge update -p ./src

# Search your knowledge
/knowledge search "authentication flow"

# Remove a knowledge base
/knowledge remove "old-docs"

# Cancel background indexing
/knowledge cancel

# Clear all knowledge
/knowledge clear
```

**Use cases:**

| Scenario | Command |
|----------|---------|
| Large codebase — agent can't read everything | `/knowledge add -n "src" -p ./src` |
| Documentation reference | `/knowledge add -n "docs" -p ./docs` |
| Stale index after major changes | `/knowledge update -p ./src` |
| Find code without knowing the file | Ask: "search knowledge for error handling" |

### `/agent` — Switch Agents

```text
# List available agents
/agent

# Switch to a specific agent
/agent rust-expert

# Create a new agent
/agent create my-reviewer

# Edit an agent's configuration
/agent edit my-reviewer
```

**Use cases:**

- Switch to a specialized agent for a specific task (security review, docs writing)
- Create project-specific agents with tailored context and instructions

### `/model` — Switch Models

```text
# Show available models and pick one
/model

# Switch to a specific model
/model anthropic.claude-3-5-sonnet-20241022-v2:0
```

### `/chat` — Conversation Management

```text
# Save current conversation
/chat save

# Save to a specific path
/chat save ./conversations/auth-feature.json

# Load a saved conversation
/chat load ./conversations/auth-feature.json

# Start a fresh session (keeps same agent)
/chat new

# Start fresh with an immediate prompt
/chat new "Now let's work on the frontend"
```

### `/tools` — Manage Tool Permissions

```text
# Show all available tools
/tools

# Trust all tools (no more approval prompts)
/tools trust-all

# Trust a specific tool
/tools trust shell

# Revoke trust
/tools untrust shell

# Reset all trust settings
/tools reset
```

### `/code` — Code Intelligence

```text
# Check code intelligence status
/code status

# Initialize code intelligence for your workspace
/code init

# Get a codebase overview
/code overview

# Get a summary of the codebase
/code summary

# View code intelligence logs
/code logs
```

## TUI Commands & Shortcuts

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Shift + Tab` | Toggle between planning and execution mode |
| `Ctrl + R` | Search command history |
| `Ctrl + C` | Cancel current operation or exit |
| `Ctrl + G` | Monitor subagent sessions |
| `Up/Down` | Navigate command history |

### TUI-Only Commands

```text
/copy          # Copy last response to clipboard
/editor        # Open $EDITOR to compose a multi-line prompt
/transcript    # Open full conversation in $PAGER
/spawn         # Spawn a new agent session with a task
/theme         # Select a terminal theme
/reply         # Open editor pre-filled with last response to compose a reply
```

## Utility Commands

```text
/help          # Show all available commands
/guide         # Switch to guide agent for Kiro CLI help
/guide How do I configure agents?   # Ask guide a question directly
/feedback      # Submit feedback or report issues
/hooks         # View configured hooks
/mcp           # Show configured MCP servers
/prompts       # List available prompt templates
/usage         # Show billing and usage information
/clear         # Clear conversation history (no summary, just wipe)
/quit          # Exit the session
```

## Settings (CLI)

```bash
# List all configured settings
kiro-cli settings list

# List ALL available settings (including unset)
kiro-cli settings list --all

# Get a setting value
kiro-cli settings chat.defaultModel

# Set a value
kiro-cli settings chat.defaultModel "anthropic.claude-3-5-sonnet-20241022-v2:0"
kiro-cli settings chat.defaultAgent my-agent

# Toggle features
kiro-cli settings chat.enableKnowledge true
kiro-cli settings chat.enableSubagent true
kiro-cli settings chat.enableThinking true

# Delete a setting
kiro-cli settings --delete chat.defaultModel

# Delete multiple with glob
kiro-cli settings --delete "knowledge.*"

# Open settings file in editor
kiro-cli settings open
```

### Key Settings Reference

| Setting | Purpose | Example |
|---------|---------|---------|
| `chat.defaultAgent` | Agent for new sessions | `my-project-agent` |
| `chat.defaultModel` | Default AI model | `anthropic.claude-3-5-sonnet-20241022-v2:0` |
| `chat.enableKnowledge` | Enable knowledge bases | `true` |
| `chat.enableSubagent` | Enable subagent spawning | `true` |
| `chat.enableThinking` | Enable thinking/reasoning | `true` |
| `chat.enableCodeIntelligence` | Enable LSP-based code intelligence | `true` |
| `knowledge.indexType` | Search type: `Fast` (BM25) or `best` (semantic) | `Fast` |
| `knowledge.maxFiles` | Max files to index | `10000` |

## Real-World Workflow Examples

### Example 1: Starting a New Feature

```text
# 1. Plan the feature
/plan Add WebSocket support for real-time notifications

# 2. (Answer planner's questions, approve plan)

# 3. Switch to execution (Shift+Tab) and implement

# 4. Save progress
/chat save
```

### Example 2: Debugging a Production Issue

```text
# 1. Add relevant logs/code to context
/context add src/api/orders.ts src/services/payment.ts

# 2. Describe the problem with evidence
"Users get 500 errors on POST /orders when cart has 50+ items.
Error from logs: PayloadTooLargeError: request entity too large"

# 3. Let the agent investigate and fix
```

### Example 3: Large Codebase Exploration

```text
# 1. Index the codebase
/knowledge add -n "project" -p ./src --exclude "node_modules/**,dist/**"

# 2. Ask questions using knowledge
"How does the authentication middleware work?"
"Find where we handle rate limiting"
"What services depend on the user module?"
```

### Example 4: Automated Code Quality Check

```bash
# Run from CI or a script
kiro-cli chat --no-interactive --trust-all-tools \
  "Review src/api/ for security issues. Report findings as a markdown table with severity, file, line, and description."
```

## Related Topics

- [Vibe Coding Best Practices](vibe-coding.md) — How to communicate effectively with the agent
- [Prompt Engineering Fundamentals](index.md) — Core prompting techniques

---

**Tags**: #kiro-cli #commands #reference #ai-development

**Difficulty**: <span class="difficulty-beginner">Beginner</span> | <span class="difficulty-intermediate">Intermediate</span>
