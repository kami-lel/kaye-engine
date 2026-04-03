# Dify App Kaye Chat Documentation

## Round Flow Logic

```mermaid
flowchart TD
    start(Round Start) --> pre_start
    pre_start[post_start] --> skip
    skip{Skip Sense?} --1--> tp
    skip --0--> sense

    sense[Sense] --> tp
    tp[Get Task Prompt]-->idr

    idr{Is Direct Respond?} --1-->dr
    idr --0--> cr

    subgraph Combined Respond
    cr
    end

    subgraph Direct Respond
    dr
    end
```

#### skip sense logic

Behavior of whether **Skip Sense** and content of prompt for **Sense** are determined by:

- whether *provided* difficulty (`difficulty_override` >0) or *default* (not provided, `difficulty_override` =0.)
- **roles** provided by `role_override`

|           | provided          | default                       |
|-----------|-------------------|-------------------------------|
| static difficulty roles | skip sense | skip sense             |
| `coder`   | skip sense        | sense for coder difficulty    |
| others    | skip sense        | sense for difficulty          |
| default   | sense for role    | sense for role & difficulty   |

