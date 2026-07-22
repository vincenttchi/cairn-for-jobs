# Cairn for Jobs

> _A cairn is a stack of stones marking the way forward — Cairn for Jobs is a stack of AI agents marking where you are in the hunt._

> Status: early development — this is Phase 0 of the build. Not yet functional.

## The problem

Searching for a job at scale is exhausting. Customizing a resume for every
job posting, drafting authentic cover letters, preparing for interview
questions, and following up on applications can quickly become overwhelming.
As you apply to more positions, keeping track of active leads, old postings,
and tailored resumes becomes chaotic — leading to burnout and lost momentum.

## The solution

Cairn for Jobs is a self-hosted job search assistant built on top of
Obsidian. It automates the tedious parts of applying for jobs while keeping
all your files organized directly on your computer.

Instead of doing everything manually, you simply paste in a job
description, and Cairn:

1. **Evaluates job fit:** Summarizes key requirements and shows how well
   your background aligns — without deciding for you whether to apply.
2. **Keeps you in control:** Gives you a clear look at the fit assessment
   first, so you decide whether to move forward before anything else runs.
3. **Tailors your materials:** Generates a list of suggested resume edits,
   highlights interview topics to study, and asks for your real-world
   experience before drafting a cover letter.

## Design principles

- **No web scraping.** You paste in job descriptions yourself, keeping
  things reliable and private.
- **You decide, the AI advises.** Cairn highlights pros and cons, but it
  never automatically hides or discards a job posting for you.
- **No generic AI cover letters.** The system asks for your actual
  experience first. It helps you write, but it never invents stories or
  fake details.
- **Bring your own API key.** Nothing runs on a middleman server. You use
  your own AI API key, so your data stays under your control.
- **Obsidian is your database.** No separate apps or accounts needed. Your
  job applications are stored as plain text files on your device and
  organized automatically into interactive tables and visual boards.

## Pipeline overview

```mermaid
flowchart TD
    A[Master Resume] --> C[Job Matcher / Analyzer Agent]
    B[Job Description] --> C
    C --> D{YOU DECIDE}
    D -->|Skip| E[App Tracker Agent: Soft-log as 'skipped']
    D -->|Continue| F[Parallel Fan-Out]
    subgraph Parallel Generation Phase
        F --> G1[Resume Tailor Agent]
        F --> G2[Cover Letter Agent: Stage 1]
        F --> G3[Interview Prep Agent]
    end
    G1 --> H1[Resume Punch List]
    G2 --> H2[Cover Letter Talking Points]
    H2 --> I[Human Input Checkpoint: You supply real experience answers]
    I --> J[Cover Letter Agent: Stage 2]
    J --> K[Draft Cover Letter]
    H1 --> L[Reviewer Agent]
    K --> L
    L -->|Mechanical issues: Max 2 revision loops| G1
    L -->|Mechanical issues: Max 2 revision loops| J
    L -->|Needs real story / unverified claim| I
    L -->|Passed / User Satisfied| M[App Tracker Agent]
    G3 --> M
    M --> N[Obsidian Vault: New Job Entry Note]
```

## Setup

1. Clone this repo
2. Copy `.env.example` to `.env` and fill in your Anthropic and/or OpenAI key
3. Open `vault-template/` as an Obsidian vault to see the frontmatter schema
   and `.base` pipeline views
4. (Agent scripts land in later phases — this repo is currently just the
   foundation and Obsidian vault template)

## License

MIT — see [LICENSE](LICENSE).
