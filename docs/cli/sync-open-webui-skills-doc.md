# Guide: The sync-open-webui-skills Command

This guide shows how to keep an Open WebUI server's Agent Skills in step with your exportables using `kaye-engine sync-open-webui-skills` (alias `o`). For the flags and the payload, q.v. [`open-webui-doc.md`](../open-webui-doc.md); for a fresh machine, start with the [setup guide](open-webui-setup-doc.md).

## Before You Start

- A running Open WebUI server, with API keys enabled and one key created (both covered in the [setup guide](open-webui-setup-doc.md))
- The server address, if it is not `http://localhost:8080`

## Give the Key

Either form works; `--api-key` wins when both are present. With neither, the command stops with an error.

```bash
export OWU_API_KEY=sk-...             # environment variable
kaye-engine o --api-key sk-...        # or per run
```

## Point at the Server

```bash
kaye-engine o --base-url http://host:3000
```

`--base-url` defaults to `http://localhost:8080`; no environment variable sets it.

## The Workflow

1. Preview with `-n`/`--dry-run`; it reports what would be created, updated, or skipped, and sends no write request

   ```bash
   kaye-engine o -n
   ```

2. Run for real; new skills are created, changed ones updated, identical ones left alone

   ```bash
   kaye-engine o
   ```

3. Optionally add `--prune` to delete remote skills whose id is not a local `canonical_name`

   ```bash
   kaye-engine o -n --prune    # see what would be deleted first
   kaye-engine o --prune
   ```

> [!WARNING]
> `--prune` deletes every remote skill absent locally, including ones you made by hand in Open WebUI. Always preview it with `-n`/`--dry-run` first.

## Read the Result

The last line reports the counts: `created N, updated N, skipped N, pruned N, failed N`. The command exits non-zero when any request failed, or when the existing remote skills cannot be fetched. One failed skill never stops the others.

## Good to Know

- Every registry entry is pushed; there is no whitelist or blacklist yet
- Only a Markdown body is carried over: bundled `scripts/` and `references/` of an Agent Skill are not
- Only the pushed fields decide between update and skip, so server-owned fields such as timestamps never force an update
