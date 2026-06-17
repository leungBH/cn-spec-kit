# cn-spec-kit

> **Agent-Ready Product Spec Generator for Chinese ToB Software Teams**: turn a one-sentence requirement into a structured, AI-coding-agent-consumable product specification document chain.

[中文](./README.md) · [MIT License](./LICENSE)

---

## Why cn-spec-kit

Chinese ToB software teams typically face four pain points in the product spec stage:

- **Fragmented requirements**: a one-liner from a customer, interview notes, or a verbal request from a leader — quality varies wildly.
- **Incomplete deliverables**: PRD, business flows, page prototypes, permission matrices, acceptance criteria, and dev tasks are often missing pieces.
- **Hard for AI to consume**: existing documents aren't structured down to the field level, so AI coding agents don't know how to act on them.
- **Hard to control quality**: without cross-artifact consistency checks, design gaps usually surface late in development.

**cn-spec-kit** breaks this work into an 11-step standard pipeline. Each step has automated quality gates, and the **final output is an AI-friendly, structured document chain that can be fed directly into an AI coding agent**.

---

## Core Features

- **11-step standard pipeline**: input → discovery → competitive research → clarification → template selection & requirement → PRD → scope → dependency DAG → business flow → page prototype → permission matrix → acceptance criteria → dev tasks.
- **Three-layer automated quality gates**:
  1. **Step completeness gate** — checklist coverage ≥ 90% per step.
  2. **Cross-step consistency check** — roles, states, actions, and acceptance scenarios stay consistent across artifacts.
  3. **External LLM review** — a 10+ year ToB expert's perspective that actively questions design flaws.
- **Human QA confirmation gate**: Step 4.5 (requirement) and Step 8 (page prototype) require human confirmation before continuing.
- **Template override mechanism**: three-layer override (project-level `overrides/` + industry-level `presets/` + global default `templates/`).
- **Parallel agent strategy**: competitive research, HTML prototype generation, and dev task breakdown all support multi-agent parallelism.
- **Domain knowledge baked in**: 3 industry presets (manufacturing / fintech / education) with customized templates.

---

## Quick Start

> cn-spec-kit is a **skill resource pack**, not a standalone CLI tool. It is designed for use with AI Agents / AI IDEs.

### Use in skills-aware IDEs (Trae / Claude Code, etc.)

1. Clone (or copy) this repo into your IDE's skills directory:

   ```bash
   # Trae
   .trae/skills/cn-spec-kit/
   # Claude Code
   .claude/skills/cn-spec-kit/
   ```

2. Trigger it with a one-sentence requirement in the conversation, e.g.:

   ```
   Help me draft a product spec for a contract management system:
   the customer wants contract drafting, approval, archiving, ledger, and renewal reminders.
   ```

3. The AI Agent runs the 11-step pipeline automatically, producing Markdown documents at each step and running quality gates.

### Use a single step in isolation

If you already have some upstream artifacts, jump straight to the step you need:

```
I already have the discovery doc — please generate the PRD directly based on it.
```

See the "Usage Modes" section in [`SKILL.md`](./SKILL.md) for details.

---

## Output Example

After running the full pipeline, 15 structured documents are produced under `specs/<seq-feature-name>/`:

| Artifact | File | Purpose |
|----------|------|---------|
| Brief | `00-brief.md` | Original one-sentence requirement |
| Discovery | `01-discovery.md` | Customer context and business problem |
| Competitive research | `02-competitive-research.md` | Competitor feature borrowing & gap analysis |
| Requirement doc | `03-requirement.md` | Formal requirement doc by selected template |
| PRD | `04-prd.md` | Product requirements document |
| Scope selection | `05-scope-selection.md` | User-confirmed priority scope |
| Dependency DAG | `06-dependency-dag.md` | Inter-module dependency graph |
| Business flow | `07-business-flow.md` | State flow + approval flow |
| Page spec | `08-page-spec.md` | Page list + per-page detailed spec |
| HTML prototype | `09-html-prototype/` | Low-fidelity prototype (open in browser) |
| Permission matrix | `10-permission-matrix.md` | Role × feature permissions |
| Acceptance criteria | `11-acceptance.md` | Normal + abnormal + edge acceptance |
| Dev tasks | `12-dev-tasks.md` | Frontend / Backend / Test task breakdown |
| Traceability matrix | `13-traceability-matrix.md` | Requirement → artifact full-chain traceability |
| Review log | `14-review-log.md` | End-to-end review record |

---

## Directory Structure

```
cn-spec-kit/
├── SKILL.md                       # Skill entry doc (read by AI Agent)
├── checklists/                    # Step quality gate checklists
│   ├── acceptance-checklist.md
│   ├── permission-checklist.md
│   ├── prd-checklist.md
│   └── requirement-checklist.md
├── steps/                         # 11-step execution logic
│   ├── step1-input.md ~ step11-tasks.md
│   ├── consistency-checks.md      # Cross-step consistency rules
│   └── external-review.md         # External LLM review mechanism
├── templates/                     # Global default templates
│   ├── prd.md / business-flow.md / page-spec.md
│   ├── permission-matrix.md / acceptance-criteria.md
│   ├── dev-tasks.md / traceability-matrix.md
│   ├── requirement-presale.md     # Requirement doc template
│   ├── requirement-sdd.md         # Requirement doc template
│   ├── data-dictionary.md         # Optional: data dictionary
│   ├── non-functional.md          # Optional: non-functional spec
│   ├── review-log.md              # Review log template
│   └── index.md                   # Template catalog index
├── presets/                       # Industry presets
│   ├── manufacturing/             # Manufacturing
│   ├── fintech/                   # Financial services
│   └── education/                 # Education
├── overrides/                     # Project-level overrides (highest priority)
│   └── README.md
├── references/                    # Reference materials & tools
│   ├── external-llm-config.md     # External LLM configuration
│   ├── .cn-spec-kit-llm.example.json
│   ├── industry-templates.md
│   ├── permission-patterns.md
│   ├── tob-patterns.md
│   ├── prototype-style-reference.html
│   ├── prototype-minimal-template.html
│   └── prototype-validator.py     # HTML prototype 8 hard-constraint self-check
├── LICENSE
└── .gitignore
```

---

## Template Override Mechanism

Templates are looked up in priority order; higher priority overrides lower:

```
1. Project-level  → overrides/<template>.md
2. Industry-level → presets/<industry>/<template>.md
3. Global default → templates/<template>.md
```

**Use cases**:
- Your team has custom needs → put customized templates in `overrides/`
- You're working in a specific industry (manufacturing / fintech / education) → industry presets are loaded automatically
- Global defaults always work as a fallback — zero-config out of the box

---

## External LLM Review (Optional)

cn-spec-kit supports plugging in an external LLM as a reviewer that audits design soundness from a 10+ year ToB expert perspective.

**Configuration**: write your external LLM config to `.cn-spec-kit-llm.json` (already in `.gitignore` — **do not commit it**). See [`references/external-llm-config.md`](./references/external-llm-config.md) and [`references/.cn-spec-kit-llm.example.json`](./references/.cn-spec-kit-llm.example.json).

**Review results** are recorded in `14-review-log.md` for full traceability.

---

## Roadmap

- [x] 11-step main pipeline + three-layer quality gates
- [x] External LLM review mechanism
- [x] Template override (project / industry / global)
- [x] Industry presets (manufacturing / fintech / education)
- [x] HTML prototype 8 hard-constraints + self-check script
- [ ] More industry presets (healthcare, retail, government, …)
- [ ] Auto-generate OpenAPI / GraphQL contracts
- [ ] Deep integration with mainstream AI coding agents (Cursor / Trae / Claude Code)

---

## Contributing

Contributions via Issues or Pull Requests are welcome:

- **New industry preset**: add a directory under `presets/` with `prd.md` / `permission-matrix.md`.
- **New template**: provide a complete template under `templates/` and register it in `templates/index.md`.
- **Bug reports**: describe reproduction steps, input, expected vs. actual output.
- **Best practices**: turn your industry experience into a checklist or pattern doc.

Before submitting, please ensure: all artifact files are written in Chinese; directory and file names use English kebab-case.

---

## License

[MIT License](./LICENSE) · Copyright (c) 2026 cn-spec-kit Contributors
