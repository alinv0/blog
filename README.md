# alinvoinea.eu — Blog

Articles and discussions for [alinvoinea.eu](https://www.alinvoinea.eu).

## Quick Start

```bash
# 1. Create a folder with your article
mkdir my-article
# Add content.md (with YAML frontmatter), cover.png, and any images

# 2. Add the article
make add FOLDER=my-article

# 3. Publish to Azure + deploy
make sync
```

## Commands

| Command | Description |
|---------|-------------|
| `make add FOLDER=name` | Optimize images, generate audio, update inventory, commit + push |
| `make delete FOLDER=name` | Remove article, update inventory, commit + push |
| `make audio FOLDER=name` | Regenerate audio for an article (deletes existing) |
| `make sync` | Upload to Azure Blob Storage + trigger CI/CD deploy |
| `make list` | List all articles |

## Article Structure

```
my-article/
  content.md      # Markdown with YAML frontmatter (required)
  cover.png       # Cover image (optional, always named cover.png)
  diagram.png     # Any referenced images (optional)
  audio.mp3       # Auto-generated TTS audio (via edge-tts)
```

## Prerequisites

- Node.js (for image optimization)
- Python 3 + `pip install edge-tts` (for audio generation)

## Frontmatter Template

```yaml
---
title: "My Article Title"
slug: my-article
excerpt: "A brief description of the article."
category: engineering
categoryName: Engineering
author: Alin Voinea
authorBio: Software Engineer
publishedAt: 2026-03-16T12:00:00Z
coverImage: cover.png
tags: tag1, tag2, tag3
---
```
