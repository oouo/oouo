# AGENTS.md — AI Agent Instructions for Profile README

## Source of Truth

- `AGENTS.md` is the canonical, cross-agent project instruction file.
- `CLAUDE.md` is a regular compatibility entry point that imports this file with `@AGENTS.md`.
- Keep shared rules here. Add content to `CLAUDE.md` only when it is genuinely Claude-specific.
- Keep this file limited to current constraints and durable decisions. History belongs in Git.

## Project Scope

This repository (`oouo/oouo`) is Richard's GitHub profile. `README.md` is the public entry point at `github.com/oouo`; the local SVG files it references are also part of the rendered page.

| Path | Responsibility |
|------|----------------|
| `README.md` | Public profile content and layout |
| `assets/github-stats-dark.svg` | Repository-hosted dark statistics card |
| `assets/github-stats-light.svg` | Repository-hosted light statistics card |
| `.github/workflows/update-stats.yml` | Scheduled and manual card refresh |
| `docs/stats-maintenance.md` | Statistics architecture, validation and operations |

## Identity Contract

- Name: Richard
- Role: AI/ML Engineer
- Core philosophy: **Prompt → Context → Harness → Loop**
- Languages: Java, Python, Go, Rust
- Focus: LLM Applications, Multi-Agent Systems, AI Infrastructure

The four-layer engineering framework is the profile's core differentiator and must be preserved.

## README Design Rules

1. **Minimal and scannable** — keep the core identity visible and secondary content collapsed.
2. **Terminal aesthetic** — section headings use backtick-wrapped `> command` text, such as ``## `> cat about.md```.
3. **YAML biography** — keep the structured self-introduction in a YAML code block.
4. **Progressive disclosure** — statistics stay inside a `<details>` block.
5. **Dark and light modes** — themed images use `<picture>` with matching `<source media="(prefers-color-scheme: ...)">` elements.
6. **Professional headings** — do not use emoji in headings.
7. **Technology icons** — keep logical language/ML and infrastructure groups; use `theme=dark` and `perline=6`.
8. **Responsive markup** — avoid fixed multi-column assumptions that break when GitHub stacks content on mobile.

Keep the current content order:

1. Capsule header
2. Typing SVG with name, role and four-layer methodology
3. One-line positioning statement
4. Followers and profile views
5. YAML biography
6. Four engineering layers
7. Two technology icon groups
8. Collapsible local statistics card
9. Philosophy line and capsule footer

Do not reintroduce Streak, Top Languages or Trophy sections unless the user explicitly asks for them.

## Statistics Card Contract

- README must load the two local files in `assets/`; it must not request a live statistics card during page rendering.
- The only statistics source is the self-hosted `https://github-readme-stats.uuuuo.com/api`. Never switch to the public `github-readme-stats.vercel.app` instance.
- Themes remain `tokyonight` for dark mode and `default` for light mode, with animations disabled.
- The workflow runs daily at 08:08 Asia/Shanghai (00:08 UTC) and also supports manual dispatch.
- Download both cards to a temporary directory, validate both, then install them together. A failed refresh must leave the committed cards untouched.
- Preserve the response type, minimum size, XML root, expected fields, error-card and unsafe-content checks.
- Pin third-party GitHub Actions to a full commit SHA.

The detailed runbook lives only in `docs/stats-maintenance.md`; do not duplicate it here.

## External Services

The current README uses `capsule-render.vercel.app`, `readme-typing-svg.demolab.com`, `skillicons.dev` and `komarev.com/ghpvc`. They are third-party services and may deprecate; prefer a self-hosted or repository-hosted replacement when practical.

Typing SVG lines are URL-encoded: use `+` for spaces and `%E2%86%92` for `→`.

## Editing and Verification

1. Preserve unrelated user changes in the working tree.
2. Preview `README.md` as GitHub-flavored Markdown after layout changes.
3. When statistics behavior changes, keep README, workflow, assets and `docs/stats-maintenance.md` consistent.
4. Validate workflow YAML, both SVG files and whitespace before handoff:

   ```bash
   ruby -ryaml -e 'YAML.load_file(".github/workflows/update-stats.yml")'
   xmllint --noout assets/github-stats-dark.svg assets/github-stats-light.svg
   git diff --check
   ```

5. Do not commit or push unless the user explicitly requests it.
