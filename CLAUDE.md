# CLAUDE.md — GitHub Profile README Project

## Project Overview

This is Richard's GitHub profile repository (`oouo/oouo`). The `README.md` is rendered as the public profile page at `github.com/oouo`.

## Architecture & Design Decisions

### Design Principles (2025/2026 Best Practices)

- **Minimal and scannable** — visitors spend 3-5 seconds on a profile; every element must earn its space
- **Terminal aesthetic** — section headers use `> cat file.md` / `> ls dir/` style, reinforcing engineer identity
- **Visual-first** — icons (skillicons.dev) over text lists, animations (typing-svg, capsule-render) over static headers
- **Progressive disclosure** — `<details>` tags hide stats by default; interested visitors expand, others aren't overwhelmed
- **Dark/Light mode** — use `<picture>` + `<source media="(prefers-color-scheme: ...)">` for theme adaptation
- **Self-hosted stats** — avoid public instance rate limits
- **Responsive layout** — Streak (53%) + Stats (45%) side-by-side on desktop, stacked on mobile

### Component Stack

| Component | Service | Purpose |
|-----------|---------|---------|
| Header/Footer | `capsule-render.vercel.app` | Gradient wave animation |
| Typing Animation | `readme-typing-svg.demolab.com` | Animated name + role |
| Profile Views | `komarev.com/ghpvc` | Visitor counter badge |
| Tech Icons | `skillicons.dev` | Language & tool icons (2 rows, 6 per line) |
| Streak Stats | `streak-stats.demolab.com` | Contribution streak |
| GitHub Stats | `github-readme-stats.uuuuo.com` | Self-deployed stats card |
| GitHub Trophy | `github-profile-trophy.vercel.app` | Achievement badges (6 columns) |

### Content Structure

1. **Capsule header** — minimal wave, no text (text moved to typing SVG)
2. **Typing SVG** — rotating: "Hey, I'm Richard" / "AI / ML Engineer"
3. **Tagline** — 2-line positioning + methodology statement
4. **Social proof** — followers badge + profile views (top area)
5. **`> cat about.md`** — YAML code block with structured bio
6. **`> cat engineering_layers.md`** — numbered table (01-04) with key concepts
7. **`> ls tech/`** — skillicons.dev in 2 rows (languages+ML / infrastructure)
8. **`<details>` Stats** — collapsible: Streak + Stats side-by-side, Top Languages, Trophy wall
9. **Capsule footer** — wave closure + philosophy tagline

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
