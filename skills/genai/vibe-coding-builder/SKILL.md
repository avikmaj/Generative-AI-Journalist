---
name: vibe-coding-builder
description: "Plan and drive no-code and AI-assisted app builds in Lovable, Bolt, v0, Replit or Cursor: PRD-first scoping, one-feature-at-a-time loops, prompting the invisible architecture and UX layers, recovery when the build breaks, and shipping with auth, payments and deploy. Load when the user wants to build or debug an app by describing it to an AI. Not for hand-written production codebases or agent harness design."
---

# Vibe coding builder

Grounded in OUTSKILL Book Two. The clearer the description, the closer the build.

## Know the three layers before prompting

**Frontend** (what the user sees and clicks) · **Backend** (logic and rules on the server) ·
**Database** (where data is stored and read). An API is the waiter carrying requests between them.
Name which layer a request touches before you write the prompt — a request that silently spans all
three is why builds come back wrong.

## Procedure

1. **Write a short PRD first**: what it does, for whom, the three core screens, the data it stores,
   and what is explicitly out of scope for v1. Two hundred words is enough. Skipping the PRD is the
   single largest cause of a build that drifts.
2. **Prompt the invisible parts too.** The AI will not add these unasked:
   - Architecture — "store users in a `users` table", "add Google auth", "row-level security so a
     user reads only their own rows"
   - UX — empty states, loading states, error states, mobile-first layout, form validation
   - Operational — environment variables, seed data, a health check
3. **Run the loop, one feature at a time.**

   | # | Step | Discipline |
   |---|---|---|
   | 1 | Describe the feature in one clear sentence | One feature. Never a giant ask. |
   | 2 | Generate | Let the AI build it |
   | 3 | Preview | Look at the running result, not the code |
   | 4 | Refine | Change one thing, regenerate |
   | 5 | Deploy | Push it live once the feature works |

4. **Give context when it breaks.** Paste the literal error text and a screenshot. Describing an error
   in your own words loses the information that would have fixed it.
5. **Revert rather than pile on.** When two consecutive fix attempts fail, return to the last working
   version and re-approach with a smaller ask. Stacked fix attempts corrupt working code.
6. **Ship the business layer** once the core works: payments (Stripe, Razorpay), login (Google auth),
   deploy on Vercel, attach a domain.

## Choosing the tool

| Tool | Best at |
|---|---|
| Lovable | Full-stack apps with a database and auth from a prompt |
| Bolt | Fast in-browser full-stack prototypes |
| v0 | UI and component generation, design-forward frontends |
| Replit | Prompt-to-app with a hosted runtime and deploy |
| Cursor | Editing an existing codebase with the model in the IDE |

Verify current capabilities and pricing before recommending one; mark version-specific claims
`UNVERIFIED` if unsourced.

## Recovery ladder

| Symptom | First move |
|---|---|
| Build fails to compile | Paste the full error verbatim; ask for the minimal fix only |
| Feature works, looks wrong | Screenshot + "change only the spacing/colour of X" |
| Regression after a new feature | Revert; re-add the feature as a separate, smaller ask |
| Data not persisting | Ask it to show the schema and the write path |
| Auth loops or 403s | Ask for the auth flow and the row-level-security policy explicitly |
| Model rewrites unrelated files | State "do not modify any file other than X" |

## Output format

PRD → data model → feature queue in build order → the exact prompt for feature 1 → deploy checklist →
`Open questions`.
