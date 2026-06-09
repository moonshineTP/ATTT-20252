---
name: cite-verify
description: >
  Use this skill whenever a response would include: a paper citation, arxiv ID,
  DOI, author name, publication venue, year of publication, a URL to a paper or
  repo, a claim about what a specific paper proves or proposes, or a statement
  like "X was introduced in [paper]" or "according to [author]". Also trigger
  when the user asks to find references for a topic, verify a citation they
  provide, or when building a related-work section. Training data citations are
  unreliable -- authors, titles, venues, and URLs are all hallucination-prone.
  Never trust memory for citation facts. Always verify before stating.
---

# Cite-Verify

**Core failure modes this skill prevents**:
- Hallucinated paper titles that sound plausible but don't exist
- Correct title, wrong author or venue
- Real paper, wrong year (common for arxiv preprints vs. published versions)
- Stale arxiv URL (paper moved, retracted, or superseded by journal version)
- Correct citation, wrong claim about what the paper actually proves
- Dead or redirected GitHub/project URLs attached to a paper

---

## Rule Zero - Never Output a Citation From Memory Alone

If the citation detail (title, author, venue, year, URL) is not confirmed by a
live fetch in this session, mark it explicitly as unverified. Do not silently
present memory-sourced citations as fact.

---

## Phase 1 - Classify What Needs Verification

Before searching, identify which citation elements are in scope:

| Element               | Staleness risk | Verification method     |
|-----------------------|----------------|-------------------------|
| Paper title           | Low            | Search + title match    |
| Author list           | Medium         | Fetch abstract page     |
| Publication year      | Medium (arxiv) | Check arxiv + DBLP      |
| Venue (conf/journal)  | Medium         | Fetch DBLP or paper page|
| arxiv ID / DOI        | High           | Direct fetch            |
| URL (project/code)    | Very high      | Direct fetch, check 200 |
| Claim about content   | Very high      | Read abstract / intro   |

---

## Phase 2 - Verification Procedures

### 2a. Verifying a paper exists and its metadata is correct

Primary: fetch the arxiv abstract page directly if an arxiv ID is known.
web_fetch: https://arxiv.org/abs/<ID>
Check: title, author list, submission date, last revised date.

If no ID is known, search:
web_search: "<title keywords> arxiv"
web_search: "<title keywords> site:semanticscholar.org"
Cross-check the result title character-by-character -- do not accept a
near-match as the same paper.

### 2b. Verifying venue and publication year

For conference papers: fetch the proceedings page or DBLP entry.
web_search: "<paper title> DBLP"
web_fetch: https://dblp.org/search?q=<title keywords>
DBLP is authoritative for CS venues. Note: arxiv submission year != publication
year. Report both if they differ.

### 2c. Verifying a URL is live

For any URL that will appear in a response, fetch it before citing it:
web_fetch: <url>
Accept only HTTP 200. If redirected, report the final URL. If 404, search for
the current canonical location (new repo, project page, or publisher page).

### 2d. Verifying what a paper claims

Do not paraphrase a paper's contribution from memory. Fetch the abstract:
web_fetch: https://arxiv.org/abs/<ID>
Read the abstract and, if needed, the introduction. Only then state what the
paper proves, proposes, or demonstrates. Attribute claims to the abstract
explicitly if the full paper was not read.

---

## Phase 3 - Output Format for Citations

Always present verified citations in a format that exposes provenance:
<Author(s)>. "<Title>". <Venue>, <Year>. <Verified URL>
[Verified: abstract fetched, URL returns 200]

If a citation is partially verified (e.g., title confirmed but URL not fetched):
[Partially verified: title confirmed via Semantic Scholar; URL not checked]

If a citation cannot be verified after search:
[Unverified: could not locate this paper in arxiv, DBLP, or Semantic Scholar.
Do not cite without independent confirmation.]

---

## Phase 4 - Related-Work Queries (finding references, not verifying known ones)

When the task is to find references on a topic rather than verify a specific
one, use:
web_search: "<topic> survey arxiv 2023 OR 2024"
web_fetch: https://paperswithcode.com/search?q=<topic>
web_search: site:semanticscholar.org "<topic>" sort:cited

Prefer: survey papers (they are pre-curated), highly cited foundational papers,
and recent papers from top venues (NeurIPS, ICML, ICLR, JMLR for ML; FOCS,
STOC, SODA for theory; etc.).

After finding candidates, apply Phase 2 verification before reporting them.

---

## Supplementary Rules

- **Retraction check**: for any paper older than 2 years that makes a strong
  empirical claim, do a quick search for "<title> retracted OR erratum".
- **Preprint vs. published**: always distinguish arxiv preprint from a
  peer-reviewed published version. They can differ substantially in claims.
- **Superseded versions**: arxiv papers are versioned (v1, v2, ...). Link to
  the latest version (`/abs/<ID>`, not `/abs/<ID>v1`) unless a specific version
  is needed.
- **Semantic Scholar as fallback**: if arxiv and DBLP fail,
  `semanticscholar.org` covers most CS/ML papers including non-arxiv ones and
  provides citation counts useful for assessing impact.