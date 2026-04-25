# ⚠️ MANDATORY FIRST ACTION — Session Start Protocol

**STOP. Before doing ANYTHING else — before reading the user's message, before answering questions, before fixing bugs — load brain context.**

Execute these reads in ONE parallel call:

1. Identity: `<BRAIN_ROOT>\identity\`
2. Project profile: `<BRAIN_ROOT>\projects\blog\profile.yaml`
3. Project rules: `<BRAIN_ROOT>\projects\blog\rules.md`
4. Memory wing: `<BRAIN_ROOT>\memory\wings\blog\`
5. Cross-cutting: `<BRAIN_ROOT>\memory\halls\`

This takes <2 seconds. Skipping it has caused real failures — see `brain\memory\halls\failures.md`. "The task is simple" is NOT a valid reason to skip.


---

name: "blog"
path: 'C:\Users\alinp\Projects\Services\blog'
description: "Markdown-based article management system for alinvoinea.eu — image optimization (sharp), Azure AI Speech TTS with SSML chunking, inventory generation, and Azure Blob Storage publishing pipeline"
tech_stack:
  languages: ["JavaScript", "PowerShell", "Python"]
  frameworks: ["Node.js"]
  package_managers: ["npm"]
  test_runners: []
  build_tools: ["make", "npm"]
  infrastructure: ["Azure Blob Storage", "Azure AI Speech"]
repo:
  type: "git"
  remote: "https://github.com/alinv0/blog.git"
  default_branch: "main"
status: "active"
tags: ["content", "blog", "azure", "tts", "markdown"]
dependencies:
  runtime: ["sharp"]
  external_services: ["Azure AI Speech (TTS)", "Azure Blob Storage"]
  sibling_projects: ["alinvoinea-eu"]
architecture:
  pattern: "CLI pipeline"
  entry_point: "manage.ps1"
  key_scripts:
    - "scripts/generate-audio.py (Azure TTS with SSML chunking)"
    - "scripts/generate-inventory.mjs (article metadata JSON)"
    - "scripts/optimize-images.mjs (sharp resize/compress)"
  two_repo_model: "Articles here, web app in alinvoinea-eu. make sync pushes to both."


---

# Project Context — blog

## Current State

Active content management system with 2 published articles. Pipeline fully functional: add → optimize → TTS → inventory → sync.

## Key Directories

- `execution-is-cheap-judgment-isnt/` — Article: AI-assisted development case study
- `the-90-percent-trap/` — Article: The 90% AI code trap
- `scripts/` — generate-audio.py, generate-inventory.mjs, optimize-images.mjs

## Active Goals

- Continue publishing engineering articles
- Audio generation pipeline stable (Azure AI Speech with SSML chunking)

## Known Issues

- Tooling files gitignored — must be set up locally after clone
- Azure TTS requires credentials (AZURE_SPEECH_KEY, AZURE_SPEECH_REGION)
- No test infrastructure

## Recent Changes

- Chunking fix for long articles (Azure TTS timeout)
- Upgraded from edge-tts to Azure AI Speech SDK with SSML + conversational style
- Offloaded article "fixing-ai-code-exposes-architecture"
- Removed tooling from git tracking (Makefile, scripts, package.json)


---

# Project Rules — blog

## Coding Rules

- Tooling files (Makefile, manage.ps1, scripts/, package.json) are **gitignored** — only articles and README tracked in git
- All automation flows through `manage.ps1` — never run scripts directly
- Azure credentials required for TTS: `AZURE_SPEECH_KEY`, `AZURE_SPEECH_REGION`
- Long articles must be chunked for TTS (max 4000 chars per chunk) to avoid Azure timeout

## File Structure Conventions

- Each article is a folder: `my-article/content.md` + `cover.png` + optional images + `audio.mp3`
- Cover image always named `cover.png`
- Frontmatter is YAML with required fields: title, slug, excerpt, category, categoryName, author, authorBio, publishedAt, coverImage, tags
- Optional frontmatter: `linkedinPost` for social media crosspost

## Naming Conventions

- Article folders: `kebab-case` matching the slug
- All images optimized to max 1200px width
- Audio files always `audio.mp3`

## Testing Requirements

- No test infrastructure (placeholder in package.json)
- Manual verification: check inventory.json after `make add`, verify blob upload after `make sync`

## Dependencies

- `sharp` (npm) for image optimization — only runtime dependency
- `azure-cognitiveservices-speech` (pip) for TTS generation
- `edge-tts` (pip) as fallback TTS (deprecated in favor of Azure AI Speech)

## Session Start Protocol (MANDATORY)

**Non-negotiable.** Before doing ANY work — even if the user reports an urgent bug — execute the brain Session Start Protocol:

1. Load identity from `brain\identity\`
2. Load this project's `profile.yaml`
3. Check memory at `brain\memory\wings\<project>\` for past session context
4. Check cross-cutting knowledge at `brain\memory\halls\`

This is one parallel read (~1s). It never delays real work. Skipping it means operating without context, which leads to worse outcomes.


---

# Guard Rails

> Hard constraints every agent must respect. Violations are blocking — stop and fix before proceeding.
> Adapted from OB1's operational guardrails for a personal multi-project environment.

## Security

1. **No secrets in code. Ever.** No API keys, tokens, passwords, connection strings, private keys, or credentials in any committed file. Use environment variables, `.env` files (gitignored), or secret managers.
2. **No secrets in comments or docs.** Don't embed real tokens in examples, TODOs, or inline comments — use `<YOUR_API_KEY>` placeholders.
3. **No base64-encoded secrets.** Encoded values that decode to credentials are still secrets.
4. **No destructive operations without confirmation.** Never run `DROP TABLE`, `DROP DATABASE`, `TRUNCATE`, `rm -rf`, or unqualified `DELETE FROM` without explicit user approval. Ask first.
5. **No dangerous system commands.** Avoid `eval()`, `exec()`, `system()`, `subprocess.call(shell=True)`, `Invoke-Expression` on untrusted input. If unavoidable, sanitize inputs and document why.
6. **No data exfiltration.** Don't send project data to external services (webhooks, ngrok, requestbin, pipedream, etc.) without explicit user approval.
7. **No prompt injection patterns.** Never write memory files, skills, or instructions containing adversarial phrases: "ignore previous instructions", "you are now", "disregard", "jailbreak", "bypass safety".
8. **Validate external input.** Data from APIs, files, user input, or environment variables must be validated before use in queries, commands, or file paths.

## Dependencies & Supply Chain

9. **Pin dependency versions.** When adding dependencies, pin to exact versions (not ranges). `package@3.2.1` not `package@^3.2.0`.
10. **Prefer established packages.** Favor well-maintained packages with large install bases. Be suspicious of packages with <100 weekly downloads, no recent commits, or single maintainers.
11. **Audit before adding.** Before adding a new dependency, check: What does it do? What permissions does it need? Does it have known vulnerabilities? Is there a simpler built-in alternative?
12. **Minimize dependencies.** Fewer dependencies = smaller attack surface. If the functionality is simple, write it inline rather than importing a package.

## Scope & Mission Fit

13. **Stay on task.** Before implementing, verify the work aligns with the project's purpose and architecture. Don't add features that belong in a different project.
14. **Respect architectural boundaries.** Don't bypass layer separations, access internal APIs from external layers, or couple modules that should be independent.
15. **Don't modify core structures without approval.** Database schemas, API contracts, configuration formats, and public interfaces are stability boundaries. Extending is fine; altering existing shape requires user approval.
16. **Check for existing solutions.** Before creating something new, check if the project already has it (different name, different location). Duplication erodes maintainability.

## File & Naming Hygiene

17. **No binary blobs in git.** Don't commit executables (`.exe`, `.dll`), archives (`.zip`, `.tar.gz`), or large binary files (>1MB). Use package managers, artifact stores, or `.gitignore`.
18. **Naming consistency.** File names, folder names, and references in documentation must match. If a README references `auth-service.ts`, the file must be named `auth-service.ts`, not `authService.ts`.
19. **Respect `.gitignore`.** Don't commit build artifacts, editor configs, temp files, or generated outputs. If you create a generated file, add it to `.gitignore`.
20. **Clean up after yourself.** Remove temporary files, debug logging, and scaffolding code before committing.

## Post-Action Follow-Up

After any significant change, verify these follow-up items:

- [ ] **Tests still pass** — Run the project's test suite
- [ ] **Documentation matches** — Update READMEs, comments, and docs that reference changed behavior
- [ ] **Related configs updated** — If you changed a schema, check migrations. If you changed an API, check clients.
- [ ] **Cross-project impact checked** — If this project is a dependency of others (check `brain/projects/`), consider downstream effects
- [ ] **Memory updated** — Persist decisions and discoveries to brain memory

## Escalation

If you encounter any of these, **stop and ask the user**:

- A security vulnerability in existing code
- A secret committed to version control (even in history)
- A dependency with a known critical CVE
- An architectural decision that's irreversible or high-impact
- Conflicting instructions between project rules and brain rules
- Anything that feels wrong but you can't articulate why
