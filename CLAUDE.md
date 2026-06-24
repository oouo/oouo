# CLAUDE.md — GitHub Profile README Project

## Project Overview

This is Richard's GitHub profile repository (`oouo/oouo`). The `README.md` is rendered as the public profile page at `github.com/oouo`.

## Architecture & Design Decisions

### Design Principles (2025/2026 Best Practices)

- **Minimal and scannable** — visitors spend 3-5 seconds on a profile; every element must earn its space
- **Visual-first** — icons (skillicons.dev) over text lists, animations (typing-svg, capsule-render) over static headers
- **Single-column flow** — no side-by-side layouts that break on mobile
- **Dark/Light mode** — use `<picture>` + `<source media="(prefers-color-scheme: ...)">` for theme adaptation
- **Self-hosted stats** — avoid public instance rate limits

### Component Stack

| Component | Service | Purpose |
|-----------|---------|---------|
| Header/Footer | `capsule-render.vercel.app` | Gradient wave animation |
| Typing Animation | `readme-typing-svg.demolab.com` | Animated tagline loop |
| Profile Views | `komarev.com/ghpvc` | Visitor counter badge |
| Tech Icons | `skillicons.dev` | Language & tool icons |
| Streak Stats | `streak-stats.demolab.com` | Contribution streak |
| GitHub Stats | `github-readme-stats.uuuuo.com` | Self-deployed stats card |

### Content Structure

1. **Capsule header** — name + role with wave animation
2. **Typing SVG** — rotating tagline: "Prompt → Context → Harness → Loop" / "Building Intelligent Systems with Code"
3. **About** — 2-line positioning statement
4. **Engineering Layers** — Prompt → Context → Harness → Loop in vertical flow
5. **Tech icons** — Two rows via skillicons.dev (languages / tools)
6. **Stats** — Streak + GitHub Stats with dark/light mode support
7. **Capsule footer** — wave closure

### The Engineering Philosophy

Richard's AI engineering methodology expressed as four layers:

```
Prompt Engineering      → Instruction design, few-shot, CoT, structured output
Context Engineering     → RAG, vector search, memory, knowledge management
Harness Engineering     → Agents, tool use, MCP, multi-agent orchestration
Loop Engineering        → Autonomous pipelines, feedback loops, self-healing
```

### Tech Stack (Richard's)

- **Languages**: Java, Python, Go, Rust
- **AI/ML**: LLM, RAG, Agents, MCP, Multi-Modal
- **Infrastructure**: Kubernetes, Docker, Cloud Native
- **Data**: PostgreSQL, Redis, Vector DB

## Configuration

### Self-deployed github-readme-stats

- Domain: `github-readme-stats.uuuuo.com`
- Platform: Vercel (forked from anuraghazra/github-readme-stats)
- Requires: GitHub PAT configured in Vercel environment variables

### Color Scheme

- Primary blue: `58a6ff` (GitHub dark mode link color)
- Background gradient: `0d1117 → 161b22 → 0d1117` (GitHub dark theme)
- Stats theme: `tokyonight` (dark) / `default` (light)

## Maintenance Notes

- Only `README.md` is rendered on the profile page; other files don't affect display
- If stats card fails, check PAT expiry in Vercel dashboard
- `skillicons.dev` icons update automatically when new tools are added upstream
- `capsule-render` and `streak-stats` are community-maintained; monitor for deprecation
