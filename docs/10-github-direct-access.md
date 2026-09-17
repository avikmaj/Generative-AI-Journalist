# Reading from GitHub instead of uploading

Short answer: **partly, and one fact governs everything** — this repository is **private**. Confirmed
against the GitHub API, not assumed: `visibility: PRIVATE`. Unauthenticated raw URLs return 404.

So "just point the model at the raw URL" only works for a platform that authenticates as you. Claude
does. ChatGPT needs an Action carrying a token. Grok's URL attachment needs a public URL and therefore
does not work at all while the repo is private.

But one thing must stay uploaded everywhere, and it is worth being precise about why.

## The rule that decides what can be fetched

| Content | Must be present every turn? | Where it lives |
|---|---|---|
| Project instructions | Yes | Pasted. Always. |
| Skill bodies | Yes | Uploaded — zips on Claude, knowledge files on ChatGPT and Grok |
| Reference corpora (DV Bible, Film Bible, curriculum, library) | No | Fetchable from GitHub on demand |

A failed fetch of a corpus is graceful: the model says it could not read the file, and you know to
retry. A failed fetch of a **skill** is silent — an empty procedure and a confident answer look
identical from the outside. That is the failure mode this whole library is built to prevent, so skills
stay uploaded even where fetching is technically possible.

Upload [`platforms/SOURCE_MAP.md`](../platforms/SOURCE_MAP.md) — about 7 KB — and every corpus becomes
addressable without holding a copy.

## Claude — yes, use the GitHub integration

Claude has a native GitHub integration that adds files and folders straight into **project knowledge**,
not just a chat ([Claude Help Center](https://support.claude.com/en/articles/10167454-use-the-github-integration)).

1. In the project knowledge section, click **+**
2. Choose **GitHub**
3. Paste `https://github.com/avikmaj/Generative-AI-Journalist`
4. In the file browser, select **only** the files you want — see the recommended set below
5. Add them

Two things to know before relying on it:

- **Sync is manual.** Use the Sync icon and **Sync now** to pick up repository changes. Claude does not
  poll. After you change a skill or corpus, sync deliberately, or the project is silently stale.
- **Selection matters.** The docs state the selected content must fit Claude's context window and
  recommend avoiding unnecessary files. Do not select the whole repo — `knowledge/` alone is over 1 MB
  of markdown. Paid plans get RAG for Projects, which raises the ceiling roughly tenfold and activates
  automatically as knowledge approaches the limit
  ([Claude Support](https://support.claude.com/en/articles/11473015-retrieval-augmented-generation-rag-for-projects)).

Recommended selection — 5 files, replacing all 11 markdown uploads:

```text
model/MODEL_CARD.md
knowledge/dv/DV_Engineering_Bible_Vol1.md
knowledge/dv/AI_DV_Master_Engineer_v3_1.md
knowledge/dv/agentic_ai_dv_architecture.md
knowledge/outskill/CURRICULUM.md
```

Add `knowledge/film/AI_Film_Production_Bible_v2_Vol1.md` if you do film work. Skip the rest until you
need them.

**The 14 skill zips are still required.** Agent Skills are a separate mechanism from project knowledge;
selecting `skills/` through the GitHub browser puts the text in knowledge, where it is passive
reference material rather than an installed skill with a trigger. The two are not interchangeable.

Net effect on Claude: **11 markdown uploads become 0.** Skills unchanged.

## ChatGPT — no, not without an Action

A Custom GPT cannot fetch a URL you name. Its only web mechanism is a search tool that takes a short
model-written query and returns top-ranked results; it cannot be pointed at a specific address
([OpenAI community](https://community.openai.com/t/can-we-use-url-as-a-knowledge-for-answer/1266778)).
This is the source of the familiar "I'm unable to directly access external links" reply even with
browsing enabled.

Two honest options:

**Option A — keep uploading, but trim to 17.** Drop the two corpus indexes and keep everything that
must load deterministically:

| Keep | Count |
|---|---|
| `SKILL_*.md` | 15 |
| `MODEL_CARD.md` | 1 |
| `PROMPTS.md` | 1 |

Drop `KNOWLEDGE_DV.md`, `KNOWLEDGE_BUSINESS.md`, `KNOWLEDGE_FILM.md` and `EVALS.md`. That is 19 → 17,
and it frees the most space for the least loss, since `KNOWLEDGE_FILM.md` largely duplicates content
already inside the film skill files.

**Option B — add an authenticated fetch Action.** Because the repo is private, the Action must call the
contents API with a token, not a bare raw URL:

```text
GET https://api.github.com/repos/avikmaj/Generative-AI-Journalist/contents/{path}?ref=main
Authorization: Bearer <fine-grained PAT, Contents: read, this repo only>
Accept: application/vnd.github.raw
```

Use a fine-grained token scoped to this one repository with read-only Contents permission. Do not use
the `?token=` form that appears in API responses — those are short-lived and expire, so a doc or Action
built on them breaks silently within the hour.

Then upload `SOURCE_MAP.md` so the GPT knows the valid paths. This does not reduce the 15 skill files,
because a skill that arrives by Action can fail to arrive.

Start with Option A. Add the Action only if you find yourself wanting corpus detail the skills do not
carry.

## Grok — API yes, app unverified

xAI documents attaching a file by **publicly accessible** URL rather than uploading it, using
`{"type": "input_file", "file_url": "..."}`
([xAI docs](https://docs.x.ai/developers/model-capabilities/files/chat-with-files)). Two limitations
stack here:

- It requires a *public* URL, so it cannot reach this repository while it is private.
- It is documented for the API. Whether the Grok **app** exposes it in project files is **UNVERIFIED**;
  the documentation does not say and I have not confirmed it in the UI.

So for Grok today: upload the 7 files as the checklist says. This is no real loss — the Grok bundle is
already the leanest of the three, its 4 family files carry the skills, and no Bible corpus is included,
so there was little to save.

The Grok bundle is already the leanest of the three — its 4 family files contain the skills, and no
Bible corpus is included — so there is little to save here anyway.

## Summary

| Platform | Direct reads while repo is private | Markdown uploads before | After |
|---|---|---|---|
| Claude | Yes — integration reads as your GitHub account | 11 | 0 (+14 skill zips, unchanged) |
| ChatGPT | Only via an Action with a scoped PAT | 19 | 17, or 17 + an Action for corpora |
| Grok | No — its URL attachment needs a public URL | 7 | 7 |

## If you make the repository public

Nothing licensed is tracked — the OUTSKILL PDFs, the purchased business e-books and the Bible
compilations are all git-ignored, and CI fails if any of them reach `dist/`. So publishing is safe from
a licensing standpoint, and it would unlock:

- Grok URL attachment, on the API and in the app if the app supports it
- A ChatGPT Action with no token to manage
- Plain `raw.githubusercontent.com` fetches from anything, including scripts

What you would be publishing: your DV methodology, the traceability spine, the VIP sign-off policy and
your synthesised notes from paid courses. The notes are yours, but they are derived from material you
paid for, and the DV content reflects professional practice. That is a judgement call about your own
work, not a licensing question — which is why the repo stays private until you say otherwise.

## The trade-off worth naming

Fetching keeps every project current with one `git push` and removes the stale-copy problem entirely.
It also makes every answer depend on a network call that can fail mid-task, and on Claude the sync is
manual anyway — so "always current" is not free there either. While the repo is private, it also means
managing a token on any platform that is not Claude.

The split above is the compromise: deterministic things are local, bulky things are remote. Do not move
skills to the remote side to save upload effort. The upload is a one-time cost; a skill that silently
fails to load is a permanent, invisible one.
