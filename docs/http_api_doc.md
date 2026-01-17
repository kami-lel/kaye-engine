# Kaye HTTP API documentation

## deployment as `systemd` on Ubuntu

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
cp /opt/kaye/api/kaye_http_api.service /etc/systemd/system
```

----

Set permissions, enable boot-start service, & check status

```bash
chmod 644 /etc/systemd/system/kaye_http_api.service
systemctl daemon-reload
systemctl enable kaye_http_api.service
systemctl status kaye_http_api.service
```

































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





#### Kaye Chat

All endpoints below `/kaye/dify-app/ky`

----

`/pre-sense`

response type: `text/plain`

- by `GET`
- response type `text/plain`

----

`/chat`

response type: `text/plain`

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

All endpoints below `/kaye/dify-app/kyc`

----

`/pre-sense`

response type: `text/plain`

- by `GET`
- response type `text/plain`

----

`/chat`

- by `GET`

- support param `languages`:
  provide a `,` separated list of language abbreviations
  (specified in prompt corpus.) E.g. `?languages=cpp,py`

- support param `flags`: provide an integer flag value,
  that will be merged into when creating prompts

- response type `application/json`:

  - key `"prompt"`: concrete task prompt
  - key `"flags"`: integer value representing the prompt
