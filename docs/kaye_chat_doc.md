# Dify App Kaye Chat Documentation


```mermaid
flowchart TD
    start(Round Start) --> pre_start
    pre_start[post_start] --> skip
    skip{Skip Sense?} --1--> ptpg
    skip --0--> sg

    subgraph Sense
    sg[Sense Prompt Getter] --> sense
    sense[Sense] --> ps
    ps[post_sense] --> psa
    end
    psa[Post Sense Assigner] --> ptpg

    subgraph Get Task Prompt
    ptpg[pre_task_prompt_getter] --> tpg
    tpg[Task Prompt Getter] --> tps
    tps[Task Prompt Setter]
    end

    tps-->idr
    idr{Is Direct Respond?} --1-->dr
    idr --0--> cr

    subgraph Combined Respond
    cr
    end

    subgraph Direct Respond
    dr
    end
```

based on provided difficulty (`difficulty_override` >0) or default/not provided difficulty (`difficulty_override` =0.)

|           | provided          | default                       |
|-----------|-------------------|-------------------------------|
| static difficulty roles | skip sense | skip sense             |
| `coder`   | skip sense        | sense difficulty for coder    |
| others    | skip sense        | sense for difficulty          |
| default   | sense for role    | sense for role & difficulty   |

