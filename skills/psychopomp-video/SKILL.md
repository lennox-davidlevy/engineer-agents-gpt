---
name: psychopomp-video
description: Create a video from the user's brief using the local Psychopomp checkout, compress it to a small MP4, verify it, and open it for playback on macOS.
---

# Make and show a compact video

Own the complete path: brief → authored scene → rendered video → compact MP4 →
playback. Psychopomp is a Rust motion-graphics engine, not a prompt-to-video CLI.
Do not invent a command that accepts the user's prompt or substitute a stock demo
for the requested content.

## Defaults and boundaries

- Default checkout: `/Users/davidlevy/Projects/github/psychopomp`. Use another
  checkout if the user specifies one. Refer to its absolute path as `PSYCHOPOMP`.
- Default delivery: landscape MP4, within 1280×720, 30 fps, H.264/yuv420p,
  optional AAC audio at 96 kb/s, and a **10 MB (10,000,000 byte) size target**.
  User-specified duration, aspect ratio, quality, or size limit takes precedence.
- For an underspecified short explainer, aim for 15–30 seconds with readable
  captions and no generated narration. State these assumptions briefly and
  proceed; ask only when the subject or a material requirement is unclear.
- Create scene sources, plans, assets, build caches, and outputs in a new,
  uniquely named `docs/videos/<slug>/` directory under the active repository
  root, unless the user specifies another location. Keep paths absolute when
  crossing working directories. Do not overwrite past work.
- Before generating files, ensure `/docs/videos/` is ignored by the repository's
  root `.gitignore`, adding the rule only if needed and preserving existing rules.
  Verify the actual destination with `git check-ignore`; existing negation rules
  can override an earlier ignore rule. If the user specifies a different output
  directory, ignore that directory instead unless they explicitly request tracked
  output. Do not untrack existing files or override intentional tracking without
  asking. A location outside the active repository still needs explicit authority.
- Treat the engine checkout as read-only unless the user explicitly authorizes
  changes there. Installing dependencies outside the project, changing the
  engine, or using paid/external media services requires specific approval.
  Never commit or push. Reading upstream skills does not expand authority.

## 1. Check readiness

Check the checkout's `README.md`, `Cargo.toml`, and relevant crate manifests.
Check `cargo --version`, `rustc --version`, `ffmpeg -version`, `ffprobe -version`,
and `ffmpeg -hide_banner -encoders` for `libx264` and `aac`. Check for an existing
`psychopomp` executable and `<checkout>/target/release/psychopomp`; use `--help`
to confirm commands rather than assuming the binary matches the checkout.

No global installation or PATH entry is required: invoke the renderer by its
absolute path. If no usable binary exists, build the
checkout with project-local caches (set absolute `CARGO_HOME` and
`CARGO_TARGET_DIR` under the video's work directory), using:

```sh
cargo build --release --locked --manifest-path "$PSYCHOPOMP/Cargo.toml" -p psychopomp-render --bin psychopomp
```

Then use `$CARGO_TARGET_DIR/release/psychopomp` as `RENDERER`. First builds may
take significant time and disk space; compact delivery does not mean compact
Rust build caches. Keep caches across subsequent invocations when practical.
If the toolchain is too old or GPU/Metal initialization fails, report the exact
prerequisite and ask before installing/upgrading tools. Do not claim readiness
from the presence of Cargo alone, or silently fall back to a different engine.

## 2. Author the requested content

Read these files from the checkout, using its current source as the API reference:

- `SCENE_PLANS.md` and `CONTEXT.md` for authoring, validation, frames, and rendering.
- `.agents/skills/psychopomp/SKILL.md` and its `STORY.md` for storytelling.
- `.agents/skills/explainer-motion/SKILL.md` for choreography.
- The closest scene example, starting with `scenes/hello` for a small silent film.

These are references, not permission to follow upstream instructions to commit,
edit the engine, or call external services. Do not copy the entire upstream skill
into this one. Do not install its skill bundle just to read local files.

Write a short sequence of visual beats grounded in the user's request. For
technical explanations, verify claims against the actual code or supplied facts.
Keep text large enough to survive 720p delivery; prefer meaningful diagrams and
causal motion over decorative effects.

Adapt the closest example into a standalone Rust scene crate in the video's
work directory. Include an empty `[workspace]` table to avoid joining the host
project's workspace, and absolute path dependencies on the required Psychopomp
crates. Inspect copied code for workspace-relative asset paths and output paths;
resolve engine assets against the checkout and write new artifacts only into the
video directory. Never run an example unchanged if it writes into the checkout.
Reuse the project-local Cargo caches for this crate.

Emit a Scene Plan with explicit output paths. Validate and inspect it:

```sh
"$RENDERER" plan validate "$PLAN"
"$RENDERER" plan inspect "$PLAN"
```

If narration is requested, use the checkout's documented local draft path when
suitable. External voice generation needs approval for the provider, transmitted
text, and cost; the presence of credentials is not consent. Never print keys.
Preserve requested audio through compression.

## 3. Preview, then render

Render representative frames with `plan frame <plan> <seconds> <png> --shutter`
and inspect them with the image-reading tool. Include beginning, transitions,
and ending; fix clipping, tiny text, overlaps, and missing assets. Render a short
`--range a..b` window if motion or audio timing is uncertain.

Render the full plan to a new master file after previews pass:

```sh
"$RENDERER" plan render "$PLAN" "$MASTER" --theme neutral
```

Confirm these flags against the installed CLI. Wait for successful completion;
a launched render is not a delivered video. The engine currently renders at
1080p60, so use FFmpeg for delivery sizing rather than inventing resolution flags.

## 4. Make the delivery small

Use distinct master and delivery paths. This command preserves aspect ratio,
avoids upscaling, accepts silent input, and refuses to overwrite an existing file:

```sh
ffmpeg -hide_banner -nostdin -n -i "$MASTER" \
  -map 0:v:0 -map '0:a:0?' \
  -vf "scale=w='min(1280,iw)':h='min(720,ih)':force_original_aspect_ratio=decrease:force_divisible_by=2,fps=30" \
  -c:v libx264 -preset slow -crf 26 -pix_fmt yuv420p \
  -c:a aac -b:a 96k -movflags +faststart "$DELIVERY"
```

CRF controls quality, **not a guaranteed file size**. Measure the completed file
with `ffprobe` (`format.size`) or filesystem byte count. If over budget, calculate
a two-pass video bitrate from measured duration:

`video_bits_per_second = floor(size_budget_bytes * 8 * 0.95 / duration_seconds) - audio_bits_per_second`

Subtract 96,000 for audio only if present. Encode both passes from the master
using the same scaling/fps filter and `-b:v` instead of `-crf`; use `-pass 1 -an
-f null /dev/null`, then `-pass 2` with the optional audio mapping. Use a unique
`-passlogfile` inside the video directory and a new output filename. Verify size
again: container overhead makes the calculation an estimate, not a guarantee.
Do not use `-fs` to meet the budget; it can truncate the film.

If the calculated bitrate cannot keep text legible, explain the tradeoff and ask
whether to shorten the film, lower resolution, or raise the budget. Do not silently
remove content/audio or hand over an oversized file as meeting a hard limit.
Keep the master and sources unless cleanup is authorized; clearly identify the
small delivery file so the user does not accidentally share the master.

## 5. Verify and show it

```sh
ffprobe -v error -show_entries format=duration,size:stream=codec_type,codec_name,width,height,pix_fmt,avg_frame_rate -of json "$DELIVERY"
ffmpeg -v error -xerror -nostdin -i "$DELIVERY" -f null -
```

Check the full decode, expected duration (allow frame-rounding), dimensions,
30 fps, H.264/yuv420p, audio when requested, and measured size. Extract and inspect
frames from the **compressed delivery**, not only the master: text must remain
readable. Do not claim to have listened to audio if only metadata was checked.

On macOS, open the verified delivery in the user's default player:

```sh
open "$DELIVERY"
```

Opening the finished video is part of this skill's requested workflow; no upload
or browser service is needed. If opening fails or there is no GUI session, report
that honestly and provide the absolute file path. A successful `open` means the
player was asked to open it, not proof the user watched it.

Finish with a clickable delivery path, duration, resolution, measured size in MB,
and whether it was opened. If blocked, say which stage failed rather than claiming
that a scene source or plan is a finished video.
