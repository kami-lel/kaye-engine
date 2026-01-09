# Kaye Flask HTTP API documentation

Port Number: `11255` (k=11, a=1, y=25, e=5)

## Endpoints

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
