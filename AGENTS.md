# AGENTS.md — AI Agent Instructions for Profile README

## Context

This repository (`oouo/oouo`) serves as Richard's GitHub profile page. The `README.md` is publicly displayed at `github.com/oouo`.

## Key Constraints

- Only `README.md` is rendered on the profile; other files are repo-only
- All external services (capsule-render, typing-svg, skillicons, streak-stats) are third-party — they may deprecate; prefer self-hosted alternatives when available
- Stats card is self-deployed at `github-readme-stats.uuuuo.com` — do NOT revert to the public `github-readme-stats.vercel.app` instance

## Design Rules

1. **Terminal aesthetic** — section headers use backtick-wrapped `> command` style (e.g., `` ## `> cat about.md` ``)
2. **YAML for bio** — structured self-intro in YAML code block, not Go/Python/plain text
3. **Progressive disclosure** — stats and secondary content inside `<details>` tags; only core identity visible by default
4. **Dark/Light mode** — always use `<picture>` with `<source media="(prefers-color-scheme: ...)">` for themed images
5. **Responsive side-by-side** — Streak (53% width) + Stats (45% width) auto-stack on mobile
6. **No emoji in headings** — keep it professional; terminal style replaces emoji flair
7. **Self-hosted over public** — prefer `github-readme-stats.uuuuo.com` over any shared public instance
8. **skillicons.dev** — use `perline=6` and `theme=dark`; split into logical groups (languages vs infra)

## Content Guidelines

### Identity

- Name: Richard
- Role: AI/ML Engineer
- Core philosophy: **Prompt → Context → Harness → Loop** (four engineering layers)
- Languages: Java, Python, Go, Rust
- Focus areas: LLM Applications, Multi-Agent Systems, AI Infrastructure

### When Updating

- Preserve the four-layer engineering framework — it's the core differentiator
- Tech icons can be updated via skillicons.dev URL params (comma-separated icon names)
- Typing SVG lines are URL-encoded in the `lines=` parameter (use `+` for spaces, `%E2%86%92` for →)
- Stats themes should stay `tokyonight` (dark) and `default` (light)

### Services Reference

| Service | URL | Status Check |
|---------|-----|--------------|
| capsule-render | `capsule-render.vercel.app` | GET returns SVG |
| typing-svg | `readme-typing-svg.demolab.com` | GET returns SVG |
| skillicons | `skillicons.dev` | GET returns SVG |
| streak-stats | `streak-stats.demolab.com` | GET with `?user=oouo` returns SVG |
| github-readme-stats | `github-readme-stats.uuuuo.com` | GET `/api?username=oouo` returns SVG |
| github-profile-trophy | `github-profile-trophy.vercel.app` | GET `/?username=oouo` returns SVG |
| profile views | `komarev.com/ghpvc` | GET with `?username=oouo` returns SVG |

## Editing Workflow

1. Edit `README.md` locally
2. Preview rendered markdown (GitHub-flavored) before pushing
3. Push to `main` — profile updates immediately
4. Verify at `github.com/oouo` that all images load (especially stats card)
