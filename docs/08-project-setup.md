# Three-platform project setup

Use [`11-setup-cards.md`](11-setup-cards.md) as the single canonical setup document. It provides, in
the same order for Claude, ChatGPT, and Grok:

1. Project Name
2. Objective
3. Project Instructions
4. GitHub-connected files and required uploads
5. Whole-project and skill-specific tests

The setup is deliberately below current limits: Claude uses 14 Agent Skill zips and no markdown
uploads, while ChatGPT and Grok each use five consolidated markdown uploads. Every instruction block
is below 4,000 characters.

Do not use older instructions referring to 17 ChatGPT files or 7 Grok files; those bundles were
superseded by the limit-safe five-file layout.
