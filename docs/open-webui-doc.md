# Kaye Engine: Open WebUI export

`kaye-engine upsert-open-webui-skills` (alias `o`) pushes every entry of `exportable_registry` into a running [Open WebUI](https://docs.openwebui.com) through its Skills REST API. A skill absent from the server is created, one whose fields differ is updated, and an identical one is left alone.

## Usage

```bash
OWU_API_KEY=sk-... kaye-engine upsert-open-webui-skills
kaye-engine o --dry-run                 # report only, write nothing
kaye-engine o --prune                   # also delete remote-only skills
kaye-engine o --base-url http://host:3000 --api-key sk-...
```

| Flag | Effect |
| --- | --- |
| `--base-url` | server root; default `http://localhost:8080`, no environment variable involved |
| `--api-key` | API key; overrides `OWU_API_KEY`; no default, a missing key is an error |
| `--dry-run` | plan and report, send no write request |
| `--prune` | delete remote skills whose id is not a local `canonical_name`; off by default |

The command also takes the shared verbosity flags. It exits non-zero when any request failed, or when the remote export cannot be fetched.

## Endpoints

The `/api/v1/skills` prefix is fixed. Every request carries `Authorization: Bearer <key>`.

| Call | Request |
| --- | --- |
| list | `GET /api/v1/skills/export` |
| create | `POST /api/v1/skills/create` |
| update | `POST /api/v1/skills/id/{id}/update` |
| delete | `DELETE /api/v1/skills/id/{id}/delete` |

A 400, 401, or 404 response is reported per skill and counted as a failure; one failure never aborts the rest.

## Skill Payload

| Field | Source |
| --- | --- |
| `id` | `canonical_name` |
| `name` | `display_name` |
| `description` | skill description, then `when_to_use`, joined by a blank line |
| `content` | rendered content, the same body a Claude `SKILL.md` carries |
| `meta` | `{"tags": []}` |
| `is_active` | `true` |

`access_grants` is omitted. The server overwrites every field on update, so an update always sends the full record. Only the fields above are compared to decide between update and skip; server-owned fields such as timestamps never force an update.

## Limits

- Bundled `scripts/` and `references/` are not carried over: an Open WebUI skill is a Markdown body only
- Every registry entry is pushed; there is no whitelist or blacklist yet
