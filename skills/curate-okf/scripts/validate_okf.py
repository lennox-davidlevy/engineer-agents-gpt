#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6,<7"]
# ///

"""Validate an Open Knowledge Format v0.2 bundle.

Errors are file-level conformance failures. Warnings are producer-quality
findings that a permissive OKF consumer must tolerate.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from urllib.parse import unquote

import yaml

RESERVED = {"index.md", "log.md"}
STATUSES = {"draft", "stable", "deprecated"}
TRUST_ACTOR = re.compile(r"^(?:human:\S+|process:\S+|[^\s/]+/[^\s/]+)$")
SOURCE_ACTOR = re.compile(r"^(?:[^\s:/]+:\S+|[^\s/]+/[^\s/]+)$")
HEADING = re.compile(r"^#{1,6}\s+\S", re.MULTILINE)
LOG_HEADING = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+[\"'][^\"']*[\"'])?\)")
FOOTNOTE = re.compile(r"\[\^([^\]\s]+)\]")
CITATIONS = re.compile(r"^#{1,6}\s+Citations\s*$", re.MULTILINE)
FENCE = re.compile(r"```[\s\S]*?```|~~~[\s\S]*?~~~")
INLINE_CODE = re.compile(r"(`+)(.*?)\1", re.DOTALL)
HTML_COMMENT = re.compile(r"<!--[\s\S]*?-->")
LIST_ITEM = re.compile(r"^( *)(?:[-+*]|\d+[.)])[ \t]+")
REFERENCE_DEFINITION = re.compile(
    r"^ {0,3}\[([^\]\n]+)\]:[ \t]*(?:<([^>\n]+)>|(\S+))(?:[ \t]+.*)?$",
    re.MULTILINE,
)
REFERENCE_USE = re.compile(r"(?<!!)\[([^\]\n]+)\]\[([^\]\n]*)\]")
SHORTCUT_REFERENCE = re.compile(r"(?<!!)(?<!\])\[([^\]\n]+)\](?![\[(])")
SCHEME = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    concepts: int = 0

    def error(self, path: str, message: str) -> None:
        self.errors.append(f"{path}: {message}")

    def warn(self, path: str, message: str) -> None:
        self.warnings.append(f"{path}: {message}")


@dataclass(frozen=True)
class Document:
    path: Path
    relative: str
    body: str
    metadata: dict | None


def split_frontmatter(text: str) -> tuple[str | None, str]:
    text = text.removeprefix("\ufeff")
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return None, text
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "".join(lines[1:index]), "".join(lines[index + 1 :])
    return None, text


def starts_frontmatter(text: str) -> bool:
    lines = text.removeprefix("\ufeff").splitlines()
    return bool(lines and lines[0].strip() == "---")


def parse_yaml(raw: str, relative: str, report: Report) -> dict | None:
    try:
        metadata = yaml.safe_load(raw)
    except yaml.YAMLError as error:
        detail = str(error).splitlines()[0]
        report.error(relative, f"frontmatter is not valid YAML: {detail}")
        return None
    if not isinstance(metadata, dict):
        report.error(relative, "frontmatter must be a YAML mapping")
        return None
    return metadata


def read_utf8(path: Path, relative: str, report: Report) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        report.error(relative, f"cannot read as UTF-8: {error}")
        return None


def valid_date(value: object) -> bool:
    try:
        date.fromisoformat(str(value))
    except ValueError:
        return False
    return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(value)))


def valid_instant(value: object) -> bool:
    if isinstance(value, datetime):
        return True
    text = str(value)
    try:
        datetime.fromisoformat(text.replace("Z", "+00:00").replace("z", "+00:00"))
    except ValueError:
        return False
    return "T" in text or " " in text


def mask_non_link_contexts(markdown: str) -> str:
    without_fences = FENCE.sub("", markdown)
    without_comments = HTML_COMMENT.sub("", without_fences)
    without_indented_code = mask_indented_code(without_comments)
    return INLINE_CODE.sub("", without_indented_code)


def mask_indented_code(markdown: str) -> str:
    output: list[str] = []
    list_containers: list[tuple[int, int]] = []
    for raw_line in markdown.splitlines(keepends=True):
        expanded = raw_line.expandtabs(4)
        if not expanded.strip():
            output.append(raw_line)
            continue
        list_item = LIST_ITEM.match(expanded)
        if list_item:
            indent = len(list_item.group(1))
            inside_parent_list = any(
                marker_indent < indent for marker_indent, _ in list_containers
            )
            if indent >= 4 and not inside_parent_list:
                output.append("\n" if raw_line.endswith("\n") else "")
                continue
            list_containers = [
                container for container in list_containers if container[0] < indent
            ]
            list_containers.append((indent, list_item.end()))
            output.append(raw_line)
            continue
        indent = len(expanded) - len(expanded.lstrip(" "))
        active_containers = [
            container for container in list_containers if container[0] < indent
        ]
        code_indent = active_containers[-1][1] + 4 if active_containers else 4
        if indent >= code_indent:
            output.append("\n" if raw_line.endswith("\n") else "")
            continue
        list_containers = active_containers
        output.append(raw_line)
    return "".join(output)


def normalize_reference_label(label: str) -> str:
    return " ".join(label.split()).casefold()


def markdown_link_targets(markdown: str) -> tuple[list[str], list[str]]:
    searchable = mask_non_link_contexts(markdown)
    definitions: dict[str, str] = {}
    for match in REFERENCE_DEFINITION.finditer(searchable):
        target = match.group(2) or match.group(3)
        definitions[normalize_reference_label(match.group(1))] = target
    without_definitions = REFERENCE_DEFINITION.sub("", searchable)

    targets = list(LINK.findall(without_definitions))
    undefined: list[str] = []
    for text, explicit_label in REFERENCE_USE.findall(without_definitions):
        label = explicit_label or text
        target = definitions.get(normalize_reference_label(label))
        if target is None:
            undefined.append(label)
        else:
            targets.append(target)
    for label in SHORTCUT_REFERENCE.findall(without_definitions):
        if label.startswith("^"):
            continue
        target = definitions.get(normalize_reference_label(label))
        if target is not None:
            targets.append(target)
    return targets, undefined


def validate_actor(
    value: object,
    field_name: str,
    relative: str,
    report: Report,
    *,
    source_author: bool = False,
) -> None:
    if not isinstance(value, str) or not value.strip():
        report.warn(relative, f"`{field_name}` must identify an actor")
        return
    actor = value.strip()
    lower = actor.lower()
    if lower.startswith(("human:", "process:")) and not actor.startswith(("human:", "process:")):
        report.warn(relative, f"`{field_name}` must use the exact lowercase actor prefix")
    elif source_author and not SOURCE_ACTOR.fullmatch(actor):
        report.warn(
            relative,
            f"`{field_name}` should use <prefix>:<id> or <producer>/<version>",
        )
    elif not source_author and not TRUST_ACTOR.fullmatch(actor):
        report.warn(
            relative,
            f"`{field_name}` should use human:<id>, process:<id>, or <producer>/<version>",
        )


def validate_window(value: object, field_name: str, relative: str, report: Report) -> None:
    if not isinstance(value, dict):
        report.warn(relative, f"`{field_name}` must be a mapping with `from` and `to`")
        return
    for edge in ("from", "to"):
        if edge not in value or not valid_date(value[edge]):
            report.warn(relative, f"`{field_name}.{edge}` must use YYYY-MM-DD")


def validate_sources(metadata: dict, body: str, relative: str, report: Report) -> None:
    if "sources" not in metadata:
        return
    sources = metadata["sources"]
    if not isinstance(sources, list):
        report.warn(relative, "`sources` must be a list")
        return
    seen_ids: set[str] = set()
    for index, source in enumerate(sources):
        label = f"sources[{index}]"
        if not isinstance(source, dict):
            report.warn(relative, f"`{label}` must be a mapping")
            continue
        resource = source.get("resource")
        if not isinstance(resource, str) or not resource.strip():
            report.warn(relative, f"`{label}.resource` is required")
        source_id = source.get("id")
        if source_id is not None:
            if not isinstance(source_id, str) or not source_id.strip():
                report.warn(relative, f"`{label}.id` must be a non-empty string")
            elif source_id in seen_ids:
                report.warn(relative, f"duplicate source id `{source_id}`")
            else:
                seen_ids.add(source_id)
        if "author" in source:
            validate_actor(
                source["author"],
                f"{label}.author",
                relative,
                report,
                source_author=True,
            )
        if "usage_count" in source and (
            not isinstance(source["usage_count"], int) or isinstance(source["usage_count"], bool)
        ):
            report.warn(relative, f"`{label}.usage_count` must be an integer")
        elif (
            "usage_count" in source
            and "usage_window" not in source
            and "usage_window" not in metadata
        ):
            report.warn(
                relative,
                f"`{label}.usage_count` requires a source or shared `usage_window`",
            )
        if "last_modified" in source and not valid_date(source["last_modified"]):
            report.warn(relative, f"`{label}.last_modified` must use YYYY-MM-DD")
        if "usage_window" in source:
            validate_window(source["usage_window"], f"{label}.usage_window", relative, report)
    if "usage_window" in metadata:
        validate_window(metadata["usage_window"], "usage_window", relative, report)
    for footnote in sorted(set(FOOTNOTE.findall(mask_non_link_contexts(body)))):
        if footnote not in seen_ids:
            report.warn(relative, f"footnote `[^{footnote}]` matches no `sources[].id`")


def validate_trust(metadata: dict, relative: str, report: Report) -> None:
    if "generated" in metadata:
        generated = metadata["generated"]
        if not isinstance(generated, dict):
            report.warn(relative, "`generated` must be a mapping")
        else:
            validate_actor(generated.get("by"), "generated.by", relative, report)
            if "at" in generated and not valid_instant(generated["at"]):
                report.warn(relative, "`generated.at` must be an ISO 8601 datetime")

    if "verified" not in metadata:
        return
    verified = metadata["verified"]
    if isinstance(verified, dict):
        events = [verified]
    elif isinstance(verified, list):
        events = verified
    else:
        report.warn(relative, "`verified` must be a mapping or list")
        return
    for index, event in enumerate(events):
        label = f"verified[{index}]"
        if not isinstance(event, dict):
            report.warn(relative, f"`{label}` must be a mapping")
            continue
        validate_actor(event.get("by"), f"{label}.by", relative, report)
        if "at" not in event or not valid_instant(event["at"]):
            report.warn(relative, f"`{label}.at` must be an ISO 8601 datetime")


def inline_computation_count(body: str) -> int:
    match = re.search(
        r"^#\s+Computation\s*$([\s\S]*?)(?=^#\s+|\Z)",
        body,
        flags=re.MULTILINE | re.IGNORECASE,
    )
    if not match:
        return 0
    return len(re.findall(r"```[\s\S]*?```|~~~[\s\S]*?~~~", match.group(1)))


def validate_bundle_path(
    value: str,
    field_name: str,
    concept_path: Path,
    root: Path,
    relative: str,
    report: Report,
) -> None:
    if SCHEME.match(value):
        return
    candidates = (
        [root / value.lstrip("/")]
        if value.startswith("/")
        else [concept_path.parent / value, root / value]
    )
    inside: list[Path] = []
    for candidate in candidates:
        resolved = candidate.resolve()
        try:
            resolved.relative_to(root.resolve())
        except ValueError:
            continue
        inside.append(resolved)
        if resolved.exists():
            return
    if not inside:
        report.warn(relative, f"`{field_name}` path escapes the bundle")
    else:
        report.warn(relative, f"`{field_name}` points to missing bundle path `{value}`")


def validate_attested_computation(
    metadata: dict,
    body: str,
    concept_path: Path,
    root: Path,
    relative: str,
    report: Report,
) -> None:
    runtime = metadata.get("runtime")
    if not isinstance(runtime, str) or not runtime.strip():
        report.warn(relative, "an Attested Computation requires `runtime`")

    parameters = metadata.get("parameters")
    if parameters is not None:
        if not isinstance(parameters, list):
            report.warn(relative, "`parameters` must be a list")
        else:
            for index, parameter in enumerate(parameters):
                label = f"parameters[{index}]"
                if not isinstance(parameter, dict):
                    report.warn(relative, f"`{label}` must be a mapping")
                    continue
                for field_name in ("name", "type"):
                    value = parameter.get(field_name)
                    if not isinstance(value, str) or not value.strip():
                        report.warn(relative, f"`{label}.{field_name}` must be a non-empty string")
                if not isinstance(parameter.get("required"), bool):
                    report.warn(relative, f"`{label}.required` must be a boolean")

    inline_count = inline_computation_count(body)
    computation = metadata.get("computation")
    if computation is not None:
        if not isinstance(computation, str) or not computation.strip():
            report.warn(relative, "`computation` must be a non-empty path")
        else:
            validate_bundle_path(
                computation, "computation", concept_path, root, relative, report
            )
        if inline_count:
            report.warn(relative, "provide an inline computation or `computation` path, not both")
    elif inline_count != 1:
        report.warn(
            relative,
            "an inline Attested Computation requires exactly one fenced block under `# Computation`",
        )

    for field_name in ("executor", "attester"):
        contract = metadata.get(field_name)
        if contract is None:
            report.warn(relative, f"an Attested Computation requires `{field_name}`")
            continue
        if not isinstance(contract, dict):
            report.warn(relative, f"`{field_name}` must be a mapping")
            continue
        resource = contract.get("resource")
        if not isinstance(resource, str) or not resource.strip():
            report.warn(relative, f"`{field_name}.resource` must be a non-empty string")
        else:
            validate_bundle_path(
                resource,
                f"{field_name}.resource",
                concept_path,
                root,
                relative,
                report,
            )
        if field_name == "executor":
            receipt = contract.get("receipt")
            if not isinstance(receipt, list) or not receipt or not all(
                isinstance(item, str) and item.strip() for item in receipt
            ):
                report.warn(relative, "`executor.receipt` must be a list of non-empty strings")


def validate_optional_fields(
    metadata: dict,
    body: str,
    concept_path: Path,
    root: Path,
    relative: str,
    report: Report,
) -> None:
    if "timestamp" in metadata:
        report.warn(relative, "legacy `timestamp` should migrate to `generated.at`")
    if CITATIONS.search(mask_non_link_contexts(body)):
        report.warn(relative, "legacy `# Citations` should migrate to `sources`")
    for field_name in ("title", "description"):
        value = metadata.get(field_name)
        if not isinstance(value, str) or not value.strip():
            report.warn(relative, f"recommended field `{field_name}` is absent or empty")
    if "resource" in metadata and (
        not isinstance(metadata["resource"], str) or not metadata["resource"].strip()
    ):
        report.warn(relative, "`resource` must be a non-empty string")
    if "tags" in metadata and (
        not isinstance(metadata["tags"], list)
        or not all(isinstance(tag, str) and tag.strip() for tag in metadata["tags"])
    ):
        report.warn(relative, "`tags` must be a list of non-empty strings")
    if "status" in metadata:
        status = metadata["status"]
        if not isinstance(status, str) or status not in STATUSES:
            report.warn(relative, "`status` must be draft, stable, or deprecated")
    if "stale_after" in metadata and not valid_date(metadata["stale_after"]):
        report.warn(relative, "`stale_after` must use YYYY-MM-DD")

    validate_trust(metadata, relative, report)
    validate_sources(metadata, body, relative, report)

    if metadata.get("type") == "Attested Computation":
        validate_attested_computation(
            metadata, body, concept_path, root, relative, report
        )


def validate_index(
    path: Path,
    relative: str,
    root: Path,
    text: str,
    report: Report,
) -> Document:
    raw, body = split_frontmatter(text)
    metadata = None
    if raw is None and starts_frontmatter(text):
        report.error(relative, "unterminated frontmatter block")
    if raw is not None:
        if path != root / "index.md":
            report.error(relative, "only the bundle-root index may have frontmatter")
        else:
            metadata = parse_yaml(raw, relative, report)
            if metadata is not None and set(metadata) != {"okf_version"}:
                report.error(relative, "root index frontmatter may contain only `okf_version`")
            elif metadata is not None and not isinstance(metadata.get("okf_version"), str):
                report.error(relative, "`okf_version` must be a string")
            elif metadata is not None and metadata["okf_version"] != "0.2":
                report.warn(
                    relative,
                    f"bundle targets OKF {metadata['okf_version']}; this validator checks v0.2",
                )
    if not HEADING.search(body):
        report.error(relative, "index must contain at least one Markdown heading")
    return Document(path, relative, body, metadata)


def validate_log(path: Path, relative: str, text: str, report: Report) -> Document:
    _, body = split_frontmatter(text)
    if not HEADING.search(body):
        report.error(relative, "log must contain at least one Markdown heading")
    dates: list[date] = []
    for heading in LOG_HEADING.findall(body):
        if not valid_date(heading):
            report.error(relative, f"log date heading `{heading}` must use YYYY-MM-DD")
            continue
        dates.append(date.fromisoformat(heading))
    if dates != sorted(dates, reverse=True):
        report.error(relative, "log date headings must be newest first")
    return Document(path, relative, body, None)


def validate_concept(
    path: Path, relative: str, root: Path, text: str, report: Report
) -> Document:
    report.concepts += 1
    raw, body = split_frontmatter(text)
    if raw is None:
        report.error(relative, "missing YAML frontmatter")
        return Document(path, relative, body, None)
    metadata = parse_yaml(raw, relative, report)
    if metadata is None:
        return Document(path, relative, body, None)
    type_value = metadata.get("type")
    if not isinstance(type_value, str) or not type_value.strip():
        report.error(relative, "missing or empty required `type`")
    validate_optional_fields(metadata, body, path, root, relative, report)
    return Document(path, relative, body, metadata)


def internal_target(target: str, document: Document, root: Path) -> Path | None:
    target = unquote(target).strip("<>")
    if not target or target.startswith("#") or SCHEME.match(target):
        return None
    target = target.split("#", 1)[0].split("?", 1)[0]
    if not target:
        return None
    candidate = root / target.lstrip("/") if target.startswith("/") else document.path.parent / target
    return candidate.resolve()


def validate_links_and_navigation(
    documents: list[Document], root: Path, report: Report
) -> None:
    concepts = {
        document.path.resolve(): document.relative
        for document in documents
        if document.path.name not in RESERVED
    }
    indexed: set[Path] = set()
    root_resolved = root.resolve()
    for document in documents:
        link_targets, undefined_references = markdown_link_targets(document.body)
        for label in sorted(set(undefined_references)):
            report.warn(document.relative, f"undefined reference link `[{label}]`")
        for raw_target in link_targets:
            target = internal_target(raw_target, document, root)
            if target is None:
                continue
            try:
                target.relative_to(root_resolved)
            except ValueError:
                report.warn(document.relative, f"internal link `{raw_target}` escapes the bundle")
                continue
            if not target.exists():
                report.warn(document.relative, f"broken internal link `{raw_target}`")
                continue
            if document.path.name == "index.md" and target in concepts:
                indexed.add(target)
    for path, relative in sorted(concepts.items(), key=lambda item: item[1]):
        if path not in indexed:
            report.warn(relative, "concept is not listed by any index")


def validate_bundle(root: Path) -> Report:
    report = Report()
    documents: list[Document] = []
    markdown_files = sorted(
        path for path in root.rglob("*.md") if ".git" not in path.relative_to(root).parts
    )
    for path in markdown_files:
        relative = path.relative_to(root).as_posix()
        text = read_utf8(path, relative, report)
        if text is None:
            continue
        if path.name == "index.md":
            documents.append(validate_index(path, relative, root, text, report))
        elif path.name == "log.md":
            documents.append(validate_log(path, relative, text, report))
        else:
            documents.append(validate_concept(path, relative, root, text, report))

    if not (root / "index.md").is_file():
        report.warn(".", "root index.md is absent; consumers must synthesize navigation")
    validate_links_and_navigation(documents, root, report)
    return report


def print_report(report: Report) -> None:
    for error in report.errors:
        print(f"ERROR {error}")
    for warning in report.warnings:
        print(f"WARN {warning}")
    concept_word = "concept" if report.concepts == 1 else "concepts"
    if report.errors:
        error_word = "error" if len(report.errors) == 1 else "errors"
        print(
            f"OKF validation failed: {report.concepts} {concept_word}, "
            f"{len(report.errors)} {error_word}, {len(report.warnings)} warnings"
        )
    else:
        print(
            f"OKF validation passed: {report.concepts} {concept_word}, "
            f"{len(report.warnings)} warnings"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path, help="OKF bundle directory")
    arguments = parser.parse_args()
    if not arguments.bundle.is_dir():
        print(f"not a directory: {arguments.bundle}", file=sys.stderr)
        return 2
    report = validate_bundle(arguments.bundle.resolve())
    print_report(report)
    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
