# Devlog

## Phase 0 — Foundation & Design Decisions

- Figured out the core idea: you paste in a job posting yourself (no
  scraping), a matcher agent tells you how well you fit without deciding
  for you whether to apply, and the cover letter agent asks for your
  real experience before writing anything, so it never makes stuff up.
- Decided the reviewer agent would be one piece of code reused twice,
  once checking the resume and once checking the cover letter, instead
  of writing two separate agents. The checklist is different for each,
  but the job is basically the same: read a document, check it against
  some rules, hand back a list of issues.
- Decided the matcher should never auto-skip a posting based on its own
  score. You always make the final call on whether to apply, no matter
  what the AI thinks of your odds.
- Designed how job entries actually show up in Obsidian: a plain table
  view of everything, a kanban-style board grouped by status so it
  feels like the board you started with but does not get overwhelming,
  and a separate follow-up view so applications you have already sent
  do not get lost.

## Phase 1 — Job Matcher Agent

- Getting text out of a resume was not quite as simple for both file
  types. PDFs worked cleanly right away. Word documents needed extra
  work, since Word does not always mark a bullet point as a bullet
  point in a way that is easy to detect. A couple of resumes had
  bullets that looked totally normal on screen but were not flagged as
  list items underneath, so the first, simpler check missed them.
- Tried the matcher's prompt against two different OpenAI models. Both
  occasionally called something a "clear match" when it was really
  just a guess or a stretch, and one run mixed up two different
  certifications on the resume, saying one was still in progress when
  it was actually the other one. Rewriting the prompt to be stricter
  helped some, but did not fully stop it from happening.
- Decided not to keep chasing a perfect prompt; this kind of mistake is
  exactly what the reviewer agent (coming in a later phase) is meant to
  catch, so it made more sense to let that step do its job instead of
  trying to prevent every possible error this early.

## Phase 2 — Refining the Full Pipeline Diagram

- Reviewed the diagram from Phase 0 against what Phase 1 actually
  taught us, now that a real agent had been built and tested against it.
- Fixed a real gap in the diagram: the resume and job posting were not
  shown reaching all three agents that actually need them (resume
  tailor, cover letter, interview prep); only the matcher had access to
  both. Added a single node that combines the resume and posting, then
  branches out to all three agents from there, so the diagram now
  accurately reflects what each agent needs as input.
- Created a second, simplified diagram showing only the agents and how
  they hand off work to each other, with the decision points and file
  details removed. This one is meant to be read in a few seconds and
  sits near the top of the README, while the detailed diagram stays
  further down for anyone who wants the complete picture, including
  where the user is expected to act.
- Color-coded both diagrams by category: one color for raw inputs
  (resume, job posting), one for AI agents doing work, one for points
  where the user is the one making a decision, and one for outputs an
  agent hands back. Added a legend to the detailed diagram so the
  colors do not need to be memorized to be understood.
- Discussed adding an optional input for information the user finds on
  their own, such as something a recruiter mentioned, a company's
  engineering blog, or culture notes, that the cover letter and
  interview prep agents could reference. Decided to hold off until
  Phase 3's core agents are built and tested, so a new input does not
  get layered onto agents that have not been validated yet.
- One open question carried into Phase 3: the interview prep agent
  still skips the reviewer entirely and goes straight to being saved.
  Left as-is for now, but worth revisiting once there is real interview
  prep output to actually evaluate against.
- Added a progress checklist to the README, placed just before the
  Setup section, so anyone reading the repo can see which phases are
  done at a glance instead of relying on a single status line.
