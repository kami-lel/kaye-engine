# Guide: The sync-open-webui-skills Command

<!-- FIXME owu doc -->

This guide takes you from a fresh machine to `kaye-engine sync-open-webui-skills` (alias `o`) keeping an Open WebUI server's Agent Skills in step with your exportables. For the flags and the payload, q.v. [`open-webui-doc.md`](../open-webui-doc.md).

## Part 1: Set Up Open WebUI

### 1. Install Open WebUI Desktop

1. Download the installer for your system from the [Open WebUI Desktop releases](https://github.com/open-webui/desktop): macOS 12+ (`.dmg`), Windows 10+ (`.exe`), or Linux with glibc 2.28+ (AppImage, `.deb`, Snap, or Flatpak).
2. Launch the app. The first launch needs internet; afterwards it works offline.
3. Choose **Local** to run Open WebUI on this machine, or **Remote** to connect to an existing server by its URL.
4. Create the admin account when prompted. The first account becomes the admin.

### 2. Find the Server Address

The command needs the address the server listens on. Its default is `http://localhost:8080`.

The desktop app's documentation does not state its local port, so confirm it in the app (its connection settings, or the address of the page it opens). If it is not `8080`, pass it with `--base-url` in Part 2. For a Remote connection, use that server's URL.

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

## Part 2: Run the Command

### Give the Key

Either form works; `--api-key` wins when both are present. With neither, the command stops with an error. Exporting the key once keeps it out of your shell history.

```bash
export OWU_API_KEY=sk-...             # environment variable
kaye-engine o --api-key sk-...        # or per run
```

### Point at the Server

```bash
kaye-engine o --base-url http://host:3000
```

`--base-url` defaults to `http://localhost:8080`; no environment variable sets it.

### The Workflow

1. Preview with `-n`/`--dry-run`; it reports what would be created, updated, or skipped, and sends no write request

   ```bash
   kaye-engine o -n
   ```

2. Run for real; new skills are created, changed ones updated, identical ones left alone

   ```bash
   kaye-engine o
   ```

3. Run again; every skill now reports as skipped

4. Optionally add `--prune` to delete remote skills whose id is not a local `canonical_name`

   ```bash
   kaye-engine o -n --prune    # see what would be deleted first
   kaye-engine o --prune
   ```

> [!WARNING]
> `--prune` deletes every remote skill absent locally, including ones you made by hand in Open WebUI. Always preview it with `-n`/`--dry-run` first.

New skills are private to the key's owner. Find them under **Workspace → Skills**.

### Read the Result

The last line reports the counts: `created N, updated N, skipped N, pruned N, failed N`. The command exits non-zero when any request failed, or when the existing remote skills cannot be fetched. One failed skill never stops the others, so re-running after a fix only repeats the skills still out of date.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| `no API key` | neither `--api-key` nor `OWU_API_KEY` is set |
| HTTP 401 | key wrong, replaced by a newer one, or API keys not enabled |
| HTTP 403 or 404 on skills routes | endpoint restriction blocks `/api/v1/skills`, or this Open WebUI version has no Skills feature |
| HTTP 400 | server rejected a skill's fields; the failing skill is named in the output |
| connection refused | wrong port or the app is not running; check Part 1, step 2 |

## Good to Know

- Every registry entry is pushed; there is no whitelist or blacklist yet
- Only a Markdown body is carried over: bundled `scripts/` and `references/` of an Agent Skill are not
- Only the pushed fields decide between update and skip, so server-owned fields such as timestamps never force an update
