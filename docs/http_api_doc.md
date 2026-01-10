# Kaye HTTP API documentation

## deployment as `systemd` on Ubuntu

Place the entire project folder at `/opt/kaye`.

----

Set up Python virtual environments:

```bash
cd /opt/kaye
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

----

Copy the `.service` file:

```bash
cp /opt/kaye/api/kaye_http_api.service /etc/systemd/system
```

----

Set permissions

```bash
chmod 644 /etc/systemd/system/kaye_http_api.service
```

<!-- TODO -->

































## Endpoints

Port Number: `11255` (k=11, a=1, y=25, e=5)

### Dify App Support

#### Kaye Cash Tracker

At `/kaye/dify-app/kaye-cash-tracker`

- generate prompt for: node Extract Info
- by `GET`
- response type `text/plain`





#### Kaye Commit Sense

All endpoints below `/kaye/dify-app/kaye-commit-sense`

----

`/primary-message`

- by `GET`
- response type `text/plain`

----

`/per-file-long`

- by `GET`
- response type `text/plain`

----

`/per-file-short`

- by `GET`
- response type `text/plain`





#### Kaye Event Radar

All endpoints below `/kaye/dify-app/kaye-event-radar`

----

`/filter-events`

- by `GET`
- response type `text/plain`

----

`/parse-events`

- by `GET`
- response type `text/plain`







#### Kaye Peer Coder

All endpoints below `/kaye/dify-app/kaye-peer-coder`

----

`/pre-sense`

response type: `text/plain`

- by `GET`
- response type `text/plain`

----

`/task`

- by `GET`

- support param `languages`:
  provide a `,` separated list of language abbreviations
  (specified in prompt corpus.) E.g. `?languages=cpp,py`

- support param `flags`: provide an integer flag value,
  that will be merged into when creating prompts

- response type `application/json`:

  - key `"prompt"`: concrete task prompt
  - key `"flags"`: integer value representing the prompt
