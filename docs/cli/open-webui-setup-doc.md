# Push Skills to Open WebUI Desktop

This guide takes you from a fresh machine to `kaye-engine sync-open-webui-skills` (alias `o`) filling your Open WebUI with skills. For the command's flags and payload, q.v. [`open-webui-doc.md`](../open-webui-doc.md).

## 1. Install Open WebUI Desktop

1. Download the installer for your system from the [Open WebUI Desktop releases](https://github.com/open-webui/desktop): macOS 12+ (`.dmg`), Windows 10+ (`.exe`), or Linux with glibc 2.28+ (AppImage, `.deb`, Snap, or Flatpak).
2. Launch the app. The first launch needs internet; afterwards it works offline.
3. Choose **Local** to run Open WebUI on this machine, or **Remote** to connect to an existing server by its URL.
4. Create the admin account when prompted. The first account becomes the admin.

## 2. Find the Server Address

The command needs the address the server listens on. Its default is `http://localhost:8080`.

The desktop app's documentation does not state its local port, so confirm it in the app (its connection settings, or the address of the page it opens). If it is not `8080`, pass it with `--base-url` in step 5. For a Remote connection, use that server's URL.

## 3. Enable API Keys

An admin does this once:

1. Open **Admin Panel → Settings → Authentication**.
2. Turn on **Enable API Keys** and save.

Two follow-ups matter only in some setups:

- Non-admin accounts also need the **API Keys** feature permission, under **Admin Panel → Users → Groups → Default Permissions**
- If **API Key Endpoint Restrictions** is on, add `/api/v1/skills` to its allowed paths

## 4. Create Your API Key

1. Open the profile menu, then **Settings → Account**.
2. Under **API keys**, click **Show**, then **Create new secret key**.
3. Copy the key, which looks like `sk-` followed by 32 hex characters.

Each account has one key: creating a new one invalidates the old one at once. The key acts as you, so the account needs permission to create skills (`workspace.skills` or `workspace.skills_import`); an admin account already has it.

## 5. Run the Command

Keep the key out of your shell history by exporting it once:

```bash
export OWU_API_KEY=sk-...
```

Preview first, then push:

```bash
kaye-engine o --dry-run     # report what would be created or updated
kaye-engine o               # push for real
kaye-engine o               # again: every skill reports as skipped
```

If the server is not on `http://localhost:8080`:

```bash
kaye-engine o --base-url http://localhost:PORT
```

New skills are private to the key's owner. Find them under **Workspace → Skills**.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| `no API key` | neither `--api-key` nor `OWU_API_KEY` is set |
| HTTP 401 | key wrong, replaced by a newer one, or API keys not enabled |
| HTTP 403 or 404 on skills routes | endpoint restriction blocks `/api/v1/skills`, or this Open WebUI version has no Skills feature |
| HTTP 400 | server rejected a skill's fields; the failing skill is named in the output |
| connection refused | wrong port or the app is not running; check step 2 |

The command exits non-zero when any skill failed. One failure never stops the others, so re-running after a fix only repeats the skills still out of date.
