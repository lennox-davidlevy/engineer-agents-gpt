# Local verification and skill authoring

Replace Cursor `control-ui`, `control-cli`, `deslop`, and `create-skill` steps
with the procedures below. Preserve the upstream behavior/evidence standards.

## Browser and command-line checks

- For web UI work, discover the available Playwright tools through Code Mode.
  Navigate to a local app instance, inspect the page, perform the user action,
  and capture the observable result. Use existing project browser tests when
  they cover the same path. Never use Desktop browser automation or disable
  sandboxing to make a launch succeed.
- For a CLI, use `shell` with the repository's documented command, controlled
  input, and isolated output directory. Assert the exit code and the output or
  file change the user observes. Use an explicit timeout. Do not mistake a
  help-page check for proof of interactive terminal behavior.
- For HTTP services or libraries, use the existing public-interface tests or
  documented local client. Do not invent test-only production endpoints.
- For interactive TUIs, Electron, mobile, or native desktop apps, first locate
  an existing compatible harness. If absent, state the exact missing driver.
  Do not claim Playwright covers a native app merely because it launches.

Use processes, ports, data directories, and browser contexts owned by this run.
Retain evidence after teardown. Do not kill unrelated processes or perform
destructive cleanup without authorization. Run `test-audit` for test changes.

## Generated skills

Use the available `skill-creator` workflow instead of Cursor's built-in
`create-skill`, and disclose that substitution. Write authorized project-local
skills under `.opencode/skills/<id>/SKILL.md`, including a descriptive `name`
and `description`. Keep feature maps, scripts, and references beside the skill.
Do not add `disable-model-invocation: true` when discovery is intended.

For create-verification-skill, retain the upstream launch, doctor, drive,
evidence, cleanup, and feature-map contract. Replace every output path beginning
`.cursor/skills/` with `.opencode/skills/`. Execute one actual mapped feature
before calling the generated skill verified. For maintain-verification-skill,
inspect and exercise the existing OpenCode skill in the same location.

For automate-me, produce a project-local skill only after the user approves its
scope. Do not create another primary agent, a global rule, or an always-on
Cursor mode as an incidental consequence. Generated verification skills are
shared project skills unless the user separately requests agent restrictions.

## Cleanup and review

For `deslop`, inspect the diff directly, apply the relevant bundled principles,
remove unsupported complexity, and run the focused checks. Do not pretend the
Cursor plugin ran. Ask the existing reviewer for an independent review when
appropriate. Upstream commit/PR steps do not authorize commits, pushes, or
external writes.
