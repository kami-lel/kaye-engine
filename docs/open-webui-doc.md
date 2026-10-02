# Kaye Engine: Open WebUI export

<!-- FIXME mpv doc: owu  -->

`kaye-engine sync-open-webui-skills` (alias `o`) pushes every entry of `exportable_registry` into a running [Open WebUI](https://docs.openwebui.com) through its Skills REST API. A skill absent from the server is created, one whose fields differ is updated, and an identical one is left alone.

## Set Up Open WebUI

### 1. Install Open WebUI Desktop

1. Download the installer for your system from the [Open WebUI Desktop releases](https://github.com/open-webui/desktop): macOS 12+ (`.dmg`), Windows 10+ (`.exe`), or Linux with glibc 2.28+ (AppImage, `.deb`, Snap, or Flatpak).
2. Launch the app. The first launch needs internet; afterwards it works offline.
3. Choose **Local** to run Open WebUI on this machine, or **Remote** to connect to an existing server by its URL.
4. Create the admin account when prompted. The first account becomes the admin.

### 2. Find the Server Address

The command needs the address the server listens on. Its default is `http://localhost:8080`.

The desktop app's documentation does not state its local port, so confirm it in the app (its connection settings, or the address of the page it opens). If it is not `8080`, pass it with `--base-url` under [Usage](#usage). For a Remote connection, use that server's URL.

### 3. Enable API Keys

An admin does this once:

1. Open **Admin Panel → Settings → Authentication**.
2. Turn on **Enable API Keys** and save.

Two follow-ups matter only in some setups:

- Non-admin accounts also need the **API Keys** feature permission, under **Admin Panel → Users → Groups → Default Permissions**
- If **API Key Endpoint Restrictions** is on, add `/api/v1/skills` to its allowed paths

### 4. Create Your API Key

1. Open the profile menu, then **Settings → Account**.
2. Under **API keys**, click **Show**, then **Create new secret key**.
3. Copy the key, which looks like `sk-` followed by 32 hex characters.

Each account has one key: creating a new one invalidates the old one at once. The key acts as you, so the account needs permission to create skills (`workspace.skills` or `workspace.skills_import`); an admin account already has it.

## Usage

```bash
OWU_API_KEY=sk-... kaye-engine sync-open-webui-skills
kaye-engine o -n                        # report only, write nothing
kaye-engine o --prune                   # also delete remote-only skills
kaye-engine o --base-url http://host:3000 --api-key sk-...
```

| Flag | Effect |
| --- | --- |
| `--base-url` | server root; default `http://localhost:8080`, no environment variable involved |
| `--api-key` | API key; overrides `OWU_API_KEY`; no default, a missing key is an error |
| `-n`, `--dry-run` | plan and report, send no write request |
| `--prune` | delete remote skills whose id is not a local `canonical_name`; off by default |

The command also takes the shared verbosity flags. It exits non-zero when any request failed, or when the remote export cannot be fetched.

### Give the Key

Either form works; `--api-key` wins when both are present. With neither, the command stops with an error. Exporting the key once keeps it out of your shell history.

```bash
export OWU_API_KEY=sk-...             # environment variable
kaye-engine o --api-key sk-...        # or per run
```

### Workflow

1. Preview with `-n`/`--dry-run`; it reports what would be created, updated, or skipped, and sends no write request
2. Run for real; new skills are created, changed ones updated, identical ones left alone
3. Run again; every skill now reports as skipped
4. Optionally add `--prune`, previewing with `kaye-engine o -n --prune` first

> [!WARNING]
> `--prune` deletes every remote skill absent locally, including ones you made by hand in Open WebUI. Always preview it with `-n`/`--dry-run` first.

New skills are private to the key's owner. Find them under **Workspace → Skills**.

### Read the Result

The last line reports the counts: `created N, updated N, skipped N, pruned N, failed N`. One failed skill never stops the others, so re-running after a fix only repeats the skills still out of date.

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

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| `no API key` | neither `--api-key` nor `OWU_API_KEY` is set |
| HTTP 401 | key wrong, replaced by a newer one, or API keys not enabled |
| HTTP 403 or 404 on skills routes | endpoint restriction blocks `/api/v1/skills`, or this Open WebUI version has no Skills feature |
| HTTP 400 | server rejected a skill's fields; the failing skill is named in the output |
| connection refused | wrong port or the app is not running; check *Find the Server Address* |
