# Kaye Flask HTTP API documentation

### deployment as `systemd` on Ubuntu

Place the entire project folder at `/opt/kaye`.

----

Set up Python virtual environments:

```bash
cd /opt/kaye
python -m venv venv
source venv/bin/activate
pip install .
```

----

Copy the `.service` file:

```bash
cp /opt/kaye/scripts/kaye_http_api.service /etc/systemd/system
```

----

Set permissions, enable boot-start service, & check status

```bash
chmod 644 /etc/systemd/system/kaye_http_api.service
systemctl daemon-reload
systemctl enable kaye_http_api.service
systemctl status kaye_http_api.service
```

----

If resource under `/opt/kaye` is updated, restart service:

```bash
systemctl daemon-reload
systemctl restart kaye_http_api.service
```

































## Endpoints

Port Number: `11255` (k=11, a=1, y=25, e=5) or `11256` for debugging.


































## Dify App Support

### Kaye Cash Tracker

At `/kaye/dify-app/kaye-cash-tracker/extract`

- generate prompt for: node Extract Info
- by `GET`
- response type `text/plain`













### Kaye Commit Sense

All endpoints below `/kaye/dify-app/kaye-commit-sense`

----

`/primary-message`

- by `GET`
- response type `text/plain`
- param `allows_md`:

  - `?allows_md=1`: the prompt will instruct to utilize markdown syntax
  - `?allows_md=0`: forbid usage of markdown syntax

----

`/per-file-long`

- by `GET`
- response type `text/plain`
- param `allows_md`, v.s.

----

`/per-file-short`

- by `GET`
- response type `text/plain`
- param `allows_md`, v.s.













### Kaye Chat

All endpoints below `/kaye/dify-app/ky`





#### sense

`/sense`

- by `POST`
- request body type: `application/json`
- request body entries:

  - `"pre_sense_role"`
  - `"difficulty_override"`

- response type `text/plain`





#### task

`/task`

- by `POST`
- request body type: `application/json`
- request body entries:

  - `"role"`
  - `"programming_languages"`:
    provide a `,`-separated list of language abbreviations
    (specified in prompt corpus.) E.g. `?languages=cpp,py`
  - `"query"`: content of user query

- response type `text/plain`












### Kaye Event Radar

All endpoints below `/kaye/dify-app/kaye-event-radar`

----

`/filter-events`

- by `GET`
- response type `text/plain`

----

`/parse-events`

- by `GET`
- response type `text/plain`
