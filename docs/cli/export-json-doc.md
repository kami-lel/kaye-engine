# Guide: The export-json Command

This guide shows how to dump every exportable into one JSON file with `kaye-engine export-json` (alias `json`). The registry side is in [`exportable-registry-doc.md`](../exportable-registry-doc.md).

## Run It

```bash
kaye-engine export-json                 # write ./exportable-as-json.json
kaye-engine json -f FILE                # write to FILE instead
```

- `-f`, `--output-file`: path to write to; default `exportable-as-json.json` in the current directory
- `--dry-run`: render every entry and report the file with the `dry` badge, write nothing
- `-v`, `-q`, `-V`, `-Q`: verbosity

The command overwrites an existing output file.

## Output Shape

A flat object, keyed by canonical name and sorted by key, indented by 2 spaces:

```json
{
  "coder-python": "…rendered content…",
  "style-markdown": "…rendered content…"
}
```

Every entry of `exportable_registry` is included, each value being that entry's `content()`. There is no whitelist or blacklist yet.

## How Content Is Rendered

Content is rendered with sparseness `0`, which collapses every blank-line run to nothing, while each entry's own profile still governs everything else.

`{avoid}` content is folded inline into each value rather than split into a sibling entry. This differs from `export-image-prompt`, which writes `{avoid}` content to separate `-AVOID` files.
