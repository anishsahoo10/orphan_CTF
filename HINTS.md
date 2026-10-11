# PROJECT APEX HORIZON // DEFENSE AUDIT FIELD HINTS
## Clandestine Telemetry Node Investigation Guide

> Document Classification: RESTRICTED // AUDITOR EYES ONLY  
> Target System: Apex Aeronautics Staging Relay (`APX-NODE-01`)  
> Environment: Internal Range (`192.168.0.0/24`)

---

### Notice to Investigators
This field guide provides structured, tiered intelligence clues. It intentionally does not contain direct answers, exploit payloads, or flag strings. 

If you are stuck at any phase, you may review the corresponding tier or provide the **Inquiry Prompt** to an AI reasoning assistant to understand the underlying networking, database, or operating system concepts.

---

### Phase 1: Signal Interception (Milestone 1)

#### Threat Briefing
Apex flight operations maintain an unacknowledged staging gateway. Standard web browsers automatically parse HTML and render the visual interface, but low-level telemetry nodes broadcast machine-readable diagnostics during the initial network handshake.

#### Tier 1: Surface Clue
Do not rely solely on a graphical web browser. A web browser requests a page and renders only the response body. Look at what the web server transmits *before* the HTML body begins.

#### Tier 2: Technical Vector
HTTP transactions consist of two distinct sections: Headers (metadata, server version, custom tracking tags) and Body (rendered HTML). Misconfigured development servers often leak internal node identifiers in custom header attributes.

#### Tier 3: Inquiry Prompt (For AI or Self-Study)
> *"In Linux command-line utilities such as `curl`, what command flag requests only the HTTP response headers from a remote server without downloading the HTML body, and why do developers leave custom headers like `x-*` in staging environments?"*

---

### Phase 2: Operational Waypoints (Milestone 4)

#### Threat Briefing
Maritime radar sweeps have detected intermittent radar blips in the Mediterranean basin. To locate the physical test facility, you need exact geographic coordinates and relay frequencies.

#### Tier 1: Surface Clue
Not all critical intelligence requires complex exploitation. Human error and rushed deployment schedules frequently result in sensitive internal memoranda being left in public view.

#### Tier 2: Technical Vector
Review every exposed record on the unauthenticated telemetry board. Technical contractors frequently mix mundane status announcements with operational deployment memos.

#### Tier 3: Inquiry Prompt (For AI or Self-Study)
> *"In cybersecurity audits, what is Sensitive Information Disclosure (CWE-200), and what methodologies do auditors use to extract intelligence from publicly accessible technical memos and configuration notes?"*

---

### Phase 3: Archive Query Manipulation (Milestone 2)

#### Threat Briefing
Lead Avionics Engineer Daniel Mercer (`d.mercer`) was issued temporary terminal access keys by Apex systems administration. His personal dispatch is stored inside the local telemetry archive but is hidden from unauthenticated board views.

#### Tier 1: Surface Clue
The search pill on the telemetry dashboard queries an internal relational database. How does a database decide whether to include or exclude a record from the search results?

#### Tier 2: Technical Vector
The search mechanism builds a query dynamically. In SQL, search parameters are enclosed within delimiter characters. If an input can break out of those delimiters and introduce a condition that the database engine evaluates as unconditionally TRUE, the filter no longer restricts any rows.

#### Tier 3: Inquiry Prompt (For AI or Self-Study)
> *"Explain the fundamental mechanics of a Boolean-based SQL Injection vulnerability in a search form. Specifically, how do string delimiters (quotes), boolean operators (`OR`), tautologies (`1=1`), and database comment syntax (`--`) interact to force a database into returning all records?"*

---

### Phase 4: Visual Surveillance Vault (Milestone 5)

#### Threat Briefing
The Ministry of Defense requires photographic evidence of the uncatalogued prototype aircraft and subterranean hangar. The photo repository is secured behind an access clearance gate.

#### Tier 1: Surface Clue
Do not attempt password dictionary attacks or brute-force tools against the login portal. The defense contractor does not use default credentials.

#### Tier 2: Technical Vector
Security assessments rely on credential chaining. An exploit executed against one layer (such as the database in Phase 3) frequently produces credentials belonging to an authorized operator.

#### Tier 3: Inquiry Prompt (For AI or Self-Study)
> *"In penetration testing, what is Credential Chaining? Once valid credentials for an internal user are recovered from a previous vulnerability, how should an auditor use them to elevate their situational awareness and access restricted administrative resources?"*

---

### Phase 5: Mainframe Authority Override (Milestone 3)

#### Threat Briefing
With evidence in hand, the final objective is full administrative dominion over the telemetry mainframe to shut down rogue autonomous flight testing.

#### Tier 1: Surface Clue
Establishing an SSH session with an engineer's account gives you standard user privileges. Standard users cannot read protected files in `/root/`. You must identify a path to elevate your authority to the root user.

#### Tier 2: Technical Vector
Inspect the administrative delegations assigned to your account using the system's delegation query command. If a user is permitted to execute a specific maintenance or diagnostic script with superuser privileges without entering a password, inspect the write permissions of that script file.

#### Tier 3: Inquiry Prompt (For AI or Self-Study)
> *"In Linux privilege escalation, what is a Sudo Misconfiguration involving NOPASSWD? If `sudo -l` reveals that a low-privilege user can run a specific shell script as root, and the permissions on that script allow write access by the user, how can this trust relationship be leveraged to obtain an interactive root shell?"*

---

### Auditor Diagnostic Checklist
Before concluding that an exploit has failed, verify the following environmental conditions:
1. Is your attacking machine on the same subnet as the target node (`192.168.0.0/24`)?
2. Are you testing HTTP communications on port `8000` rather than the standard port `80`?
3. In SQL injection strings, did you include comment characters to neutralize trailing query syntax?
4. In Linux script manipulation, did you append your payload without destroying existing required interpreter directives (`#!/bin/bash`)?
