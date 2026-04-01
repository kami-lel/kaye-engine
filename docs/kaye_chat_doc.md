# Dify App Kaye Chat Documentation


```mermaid
flowchart TD
    start(Round Start) --> pre_start
    pre_start[Post Start] --> skip
    skip{Skip Sense?} --1--> a
    skip --0--> sg

    subgraph Sense
    sg[Sense Prompt Getter] --> sense
    sense["`**Sense**`"] --> post_sense
    end

    post_sense[Post Sense] --> a
```