# Business knowledge base

Deep source material behind the `business-management` skill.

## What is committed and what is not

| Path | Committed? | Why |
|---|---|---|
| `README.md`, `LIBRARY.md` | Yes | Structure and catalogue — original index |
| `raw/` | **No** — git-ignored | 59 third-party commercial e-books |
| `Business_Management_Bible.md` and `Bible_Part*.md` | **No** — git-ignored | Compilations of that licensed material |

The e-books are commercially licensed third-party publications. Only the skill, its references and
this catalogue are committed. Populate `raw/` locally from your own copy.

## Expected local layout

```
knowledge/business/
├── README.md                      committed
├── LIBRARY.md                     committed
├── Business_Management_Bible.md   local only — all 59 books, ~9 MB
├── Bible_Part1_Leadership_Management.md
├── Bible_Part2_Strategy_Projects.md
├── Bible_Part3_Sales_Marketing_Customers.md
├── Bible_Part4_Finance_People_HR.md
├── Bible_Part5_Technology_Worksheets.md
└── raw/                           local only — the 59 individual e-books
```

## Reading order

1. The skill's own `references/<domain>.md` — start here, they are the distilled layer.
2. The relevant `Bible_Part*.md` — chapter-level depth for one domain group.
3. `Business_Management_Bible.md` — only when you need cross-domain search. It is ~9 MB; never load
   it whole into a model context.

## Platform note

Do not upload the full Bible to a Custom GPT or Claude Project. Upload the five `Bible_Part*` files at
most, or better, only the skill references. The distilled references are what the skill is designed
around; the Bible is the archive behind them.
