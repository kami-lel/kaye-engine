BLUEPRINT_1_FULL = """    ○
[x] └── Project Title
[x]     ├── Description
[x]     ├── Installation
[x]     └── License"""


BLUEPRINT_1_FULL_PREVIEW = """    ○
[x] └── Project Title
[x]     ├── Description
        │   Brief overview of the project and its purpose.
[x]     ├── Installation
        │   Clone the repo and install dependencies.
[x]     └── License
            Licensed under the MIT License."""


BLUEPRINT_1_PARTIAL_1 = """    ○
[ ] └── Project Title
[x]     ├── Description
[x]     ├── Installation
[x]     └── License"""


BLUEPRINT_1_PARTIAL_1_PREVIEW = """    ○
[ ] └── Project Title
[x]     ├── Description
        │   Brief overview of the project and its purpose.
[x]     ├── Installation
        │   Clone the repo and install dependencies.
[x]     └── License
            Licensed under the MIT License."""


BLUEPRINT_1_PARTIAL_2 = """    ○
[x] └── Project Title
[ ]     ├── Description
[x]     ├── Installation
[x]     └── License"""


BLUEPRINT_1_PARTIAL_2_PREVIEW = """    ○
[x] └── Project Title
[ ]     ├── Description
        │   Brief overview of the project and its purpose.
[x]     ├── Installation
        │   Clone the repo and install dependencies.
[x]     └── License
            Licensed under the MIT License."""


BLUEPRINT_1_PARTIAL_2_PRUNED = """    ○
[x] └── Project Title
[x]     ├── Installation
[x]     └── License"""


BLUEPRINT_1_EMPTY = """    ○
[ ] └── Project Title
[ ]     ├── Description
[ ]     ├── Installation
[ ]     └── License"""


BLUEPRINT_2_FULL = """    ○
[x] └── Project Title
[x]     ├── Description
[x]     ├── Installation
[x]     ├── Usage
[x]     ├── Contributing
[x]     │   └── description
[x]     └── License"""


BLUEPRINT_2_PREVIEW = """    ○
[x] └── Project Title
[x]     ├── Description
        │   A brief overview of the project, its purpose, and go
[x]     ├── Installation
        │   1. Clone the repo
        │   2. Install dependencies
        │   3. Run the application
[x]     ├── Usage
        │   Provide instructions on how to use the application.
[x]     ├── Contributing
        │   1. Fork the repo
        │   2. Create a new branch
        │   3. Submit a pull request
[x]     │   └── description
        │       A step-by-step guide of how to contribute
[x]     └── License
            This project is licensed under the MIT License."""


BLUEPRINT_2_PARTIAL_1 = """    ○
[x] └── Project Title
[ ]     ├── Description
[x]     ├── Installation
[ ]     ├── Usage
[x]     ├── Contributing
[ ]     │   └── description
[ ]     └── License"""


BLUEPRINT_2_PARTIAL_1_PREVIEW = """    ○
[x] └── Project Title
[ ]     ├── Description
        │   A brief overview of the project, its purpose, and go
[x]     ├── Installation
        │   1. Clone the repo
        │   2. Install dependencies
        │   3. Run the application
[ ]     ├── Usage
        │   Provide instructions on how to use the application.
[x]     ├── Contributing
        │   1. Fork the repo
        │   2. Create a new branch
        │   3. Submit a pull request
[ ]     │   └── description
        │       A step-by-step guide of how to contribute
[ ]     └── License
            This project is licensed under the MIT License."""


BLUEPRINT_2_PARTIAL_1_PRUNED = """    ○
[x] └── Project Title
[x]     ├── Installation
[x]     └── Contributing"""


BLUEPRINT_2_EMPTY = """    ○
[ ] └── Project Title
[ ]     ├── Description
[ ]     ├── Installation
[ ]     ├── Usage
[ ]     ├── Contributing
[ ]     │   └── description
[ ]     └── License"""


BLUEPRINT_3_FULL = """    ○
[x] └── Main Title
[x]     ├── Introduction
[x]     │   └── Background
[x]     │       └── Importance
[x]     │           └── Objective
[x]     ├── Methods
[x]     │   └── Data Collection
[x]     │       └── Tools Used
[x]     │           └── Future Work
[x]     └── Conclusion"""


BLUEPRINT_3_FULL_PREVIEW = """    ○
[x] └── Main Title
[x]     ├── Introduction
        │   Brief introduction to the topic.
[x]     │   └── Background
        │       Context or history relevant to the topic.
[x]     │       └── Importance
        │           Why this topic matters in the current scenar
[x]     │           └── Objective
        │               The primary goal of this document.
[x]     ├── Methods
        │   Overview of the methodologies used.
[x]     │   └── Data Collection
        │       How data was gathered for analysis.
[x]     │       └── Tools Used
        │           List of tools utilized during the project.
[x]     │           └── Future Work
        │               Suggestions for future research or tasks
[x]     └── Conclusion
            Summarizing the findings and implications."""


BLUEPRINT_3_PARTIAL_1 = """    ○
[x] └── Main Title
[x]     ├── Introduction
[x]     │   └── Background
[x]     │       └── Importance
[x]     │           └── Objective
[ ]     ├── Methods
[ ]     │   └── Data Collection
[ ]     │       └── Tools Used
[ ]     │           └── Future Work
[x]     └── Conclusion"""

BLUEPRINT_3_PARTIAL_1_PREVIEW = """    ○
[x] └── Main Title
[x]     ├── Introduction
        │   Brief introduction to the topic.
[x]     │   └── Background
        │       Context or history relevant to the topic.
[x]     │       └── Importance
        │           Why this topic matters in the current scenar
[x]     │           └── Objective
        │               The primary goal of this document.
[ ]     ├── Methods
        │   Overview of the methodologies used.
[ ]     │   └── Data Collection
        │       How data was gathered for analysis.
[ ]     │       └── Tools Used
        │           List of tools utilized during the project.
[ ]     │           └── Future Work
        │               Suggestions for future research or tasks
[x]     └── Conclusion
            Summarizing the findings and implications."""


BLUEPRINT_3_PARTIAL_1_PRUNED = """    ○
[x] └── Main Title
[x]     ├── Introduction
[x]     │   └── Background
[x]     │       └── Importance
[x]     │           └── Objective
[x]     └── Conclusion"""


BLUEPRINT_3_PARTIAL_2 = """    ○
[x] └── Main Title
[ ]     ├── Introduction
[x]     │   └── Background
[ ]     │       └── Importance
[x]     │           └── Objective
[ ]     ├── Methods
[x]     │   └── Data Collection
[ ]     │       └── Tools Used
[x]     │           └── Future Work
[ ]     └── Conclusion"""


BLUEPRINT_3_PARTIAL_2_PREVIEW = """    ○
[x] └── Main Title
[ ]     ├── Introduction
        │   Brief introduction to the topic.
[x]     │   └── Background
        │       Context or history relevant to the topic.
[ ]     │       └── Importance
        │           Why this topic matters in the current scenar
[x]     │           └── Objective
        │               The primary goal of this document.
[ ]     ├── Methods
        │   Overview of the methodologies used.
[x]     │   └── Data Collection
        │       How data was gathered for analysis.
[ ]     │       └── Tools Used
        │           List of tools utilized during the project.
[x]     │           └── Future Work
        │               Suggestions for future research or tasks
[ ]     └── Conclusion
            Summarizing the findings and implications."""


BLUEPRINT_3_PARTIAL_2_PRUNED = """    ○
[x] └── Main Title
[ ]     ├── Introduction
[x]     │   └── Background
[ ]     │       └── Importance
[x]     │           └── Objective
[ ]     └── Methods
[x]         └── Data Collection
[ ]             └── Tools Used
[x]                 └── Future Work"""


BLUEPRINT_3_EMPTY = """    ○
[ ] └── Main Title
[ ]     ├── Introduction
[ ]     │   └── Background
[ ]     │       └── Importance
[ ]     │           └── Objective
[ ]     ├── Methods
[ ]     │   └── Data Collection
[ ]     │       └── Tools Used
[ ]     │           └── Future Work
[ ]     └── Conclusion
"""


BLUEPRINT_EMPTY_PRUNED = """    ○"""


def _split_content_and_comment(preview_tree):
    lines = preview_tree.splitlines()
    tree = "\n".join(lines[:-1])
    comment = lines[-1]
    return tree, comment
