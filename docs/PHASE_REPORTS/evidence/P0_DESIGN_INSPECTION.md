# Phase 0 inspection evidence

Date context: **2026-10-19, Pacific/Auckland**, supplied by the client. This is a retained observation record, not trial evidence. No runtime workflow, cloud inference, sandbox or deployment was run.

## Initial repository state

Commands: `git status --porcelain=v1`, `git ls-files`, `git log -1 --format='%H %s'`, `git remote -v`, file listing and full text reads of the request, root AGENTS, README and 692-line Master Design.

- Initial Git status: empty/clean.
- HEAD: `79059c132cd2242ad826f8613b284f98e2f3dbc4` — `Add Faultline Proof design and agent guidance`.
- Exactly three tracked files: `AGENTS.md`, `README.md`, `docs/MASTER_DESIGN.md`.
- Remote configured as `git@github.com:miku-wwl/faultline-proof.git`; it was not changed or pushed. Remote configuration alone does not verify public accessibility.
- No AIG decision, ADRs, phase reports, code, tests, `pyproject.toml`, `uv.lock` or local virtual environment existed.
- Ambient Python: Anaconda 3.13.9; AIG distribution absent there. `uv python list --only-installed` and executable discovery were read-only.

Protected initial SHA-256 values:

```text
AGENTS.md             15c96562f4f12cb0498ccf0da04c95b519ac9d602f08c22b2fdcd440d7e69c99
README.md             f8a46db842ceec4ff3e46d4c9e1c9f6178a13a1fa607a1128c212a31788083f6
MASTER_DESIGN.md      4b6997b7f5b42a573b5a8032a1544b77b5cfc90ff51e0f4a9e1cadf69470d10a
```

AGENTS/README must remain byte-identical. Master has only the reported design corrections; no wholesale replacement.

## Release and installed API observations

Actual command:

```powershell
git ls-remote https://github.com/miku-wwl/agentic-intent-gate.git refs/tags/v0.2.0 'refs/tags/v0.2.0^{}'
```

Returned tag object `b193d38a4804725d44ca536a3bd9778679cc7b4c`, peeled commit `7261fdd2f47d2b15fabe8faac527eeee37338eb1`. GitHub tag JSON confirms annotated commit target and unsigned status. No clone, tag modification or core edit.

An already existing Python 3.13.14 interpreter in `D:\workshop\oct\pactlens\.venv\Scripts\python.exe` was used for read-only installed-package inspection. `importlib.metadata.distribution('agentic-intent-gate')` reports 0.2.0 and direct Git metadata with the full pinned commit; module path is that environment's `Lib/site-packages/agentic_intent_gate/runtime.py`. All **57 RECORD hashes** match. Actual `uv pip check --python <interpreter>` reports 31 compatible packages. No dependency install or synchronization was performed in either consumer.

Public signatures/exports, `Runtime`, `ToolBinding`, `ToolCapability`, `ExecutionSpec`, `AttemptContext`, executor protocol and public gateway/RunService methods were inspected. `python -I` structural validation constructed only `ToolBinding`/`ToolCapability` and parsed documentation Plans: **2 accepted; 8 malformed variants rejected; unsupported enum rejected**. The schema's compact UTF-8 JSON is 788 bytes. `open_runtime` was never called, no gate/token was provisioned, and no persistent Run/Approval/Authorization/Action was created. Structural checks do not validate a consumer semantic manifest lookup or prove the enqueue implementation.

Upstream downloads were read completely and retained outside the repository. SHA-256 over actual response bytes:

| Resource at pinned release unless stated | SHA-256 |
|---|---|
| `docs/ADAPTER_GUIDE.md` | `d94b7871990cd73f7086732d3bbe2aa70d064839533ba93f3121ed4324348f4d` |
| `docs/V0.2.0-CONSUMER-HANDOFF.md` | `770bcb3cbec87c9d78a501b08855e078dbebc0b97bb1413396c31642fab0bbf3` |
| `examples/consumer/app.py` | `621b13a61d83b3c0d974c7384440011a6441250e3e038d9887378bf767fa736c` |
| Post-release handoff from `main`, last-changing commit `3305eb179914c27d89628bc4a4e7e18e1893b5f9` | `311302a2eaee38af1ac092b3db161bfdbc901331a04917b5ab686b9b6468c4f0` |
| `LICENSE` | `0c0161ec165055e89796da5596bb946b247c7339cca9581e3180d7333edfd56d` |
| `pyproject.toml` | `83a338feb59ec9f4d66f11f1514237b925f047fabccee8ac37d51f5256015ba9` |

An initial guessed `runtime/__init__.py` URL returned 404. Inspection corrected the path to the installed **`runtime.py` module**; no package/API conclusion relies on the failed URL. `git diff --check` initially caught newly introduced trailing whitespace; it was corrected before final validation.

## External research

Official event/live/guidelines, Vultr docs, Docker docs, SQLite docs and public PatchProof/Airlock team ideas were retrieved read-only. The rule book's text browser yielded an empty shell; raw HTTP HTML and its `__NEXT_DATA__` embedded `source.compiledSource` supplied the actual 20,514-character MDX content. This was text extraction, not execution of website code. No explicit event-specific AIG reuse/pre-kickoff permission was located. No organizer communication or form submission occurred.

Raw source snapshots are local research scratch, **not tracked source and not executed trial artifacts**. Current scratch path:

```text
D:\Ollama\Temp\faultline-phase0-65656e4fe9c5439e9be035d97910a2fa
```

HTTP 200 response snapshots (dynamic pages may differ on later retrieval):

| Source | Bytes | SHA-256 |
|---|---:|---|
| [Event](https://lablab.ai/ai-hackathons/vultr-hackathon) | 1493306 | `a64440e10d256bbd0fc03f07f9f520475172f297d735839fe8cda149c45112f0` |
| [Live](https://lablab.ai/ai-hackathons/vultr-hackathon/live) | 187724 | `55b5bc1554d127663b0f0c31119054f38bb85629d337fe9d410ab1efc7b31917` |
| [General guidelines](https://lablab.ai/ai-articles/hackathon-guidelines) | 148717 | `573732b647b55f47ace35cdbb4564b5f3cd59270101383efa5fce465d4e9598f` |
| [General reuse guide](https://lablab.ai/guide/ai-hackathons) | 157342 | `81caf5cceb690c3b4c0d7f9254d584e960f97c8304cc015a74f71abfde1fa8ba` |
| [Rule book](https://lablab.ai/hackathon-rules) | 26829 | `a42b00caa1b3add7dda72049bd5074fd6523182f008165d39200d9d0b2626b4b` |
| [Vultr Python guide](https://docs.vultr.com/how-to-use-vultr-serverless-inference-in-python) | 261277 | `32661389ce29d22c7d695ef741ef415bfb97193b4bedf0625327b8e4d9785182` |

Actual UTC milestone conversions were checked with Windows `.NET TimeZoneInfo` (`New Zealand Standard Time`, DST applied). An initial Python `zoneinfo` check could not run because that existing environment lacks `tzdata`; no package was installed, and the final check uses OS rules. The live countdown's zeros were not treated as an event start signal. No exact wall-clock retrieval time is claimed beyond the supplied client date.

## Final local validation

Machine results are retained in [P0_DOCUMENT_VALIDATION.json](P0_DOCUMENT_VALIDATION.json): installed source metadata, structural schema cases, JSON/code-fence/local-link checks, phase time-budget arithmetic, schedule conversion, protected-file hashes, documentation hashes and changed-path scope. File hash inventory excludes the machine record itself to avoid self-reference. `git diff --check` covers tracked changes; added Markdown is separately checked for trailing whitespace and valid JSON fences/links.

All product functional, integration, security, race/recovery, browser, inference and cloud tests remain **NOT RUN**. No code/containers/cloud resources, commit, push, tag, publication or final submission was produced. No secrets or private DBs are included in this documentation evidence.
