==============
kaye CHANGELOG
==============

.. default-role:: smart

.. contents::













2-1
###
version message::

    2-1:split git-related prompts

- `kaye/prompt_full.md`:

    - rename role from *git commit message writer* ( <- *commit message writer*)
    - add new role *git diff summary*

- changes in others files to accomandate previous change













2-0
###
version message::

    2-0:distribute kaye as Python package

- create ``.gitignore``
- add ``requirement.txt``
- distribute ``kaye`` as a Python package

  - add sub-module ``kaye.get_prompt``
  - add sub-module ``kaye.update_vsc``

- create folder ``static_prompts`` to store predefined prompts; also new script ``generate_static_prompts.py``
- create various tests













1-4
###
version message::

    1-4:add role secretary and librarian

changes re ``./prompt/system_message.md``:

- add role *secretary*
- add role *librarian*
- use ISO 639-1 Language Code (2 letter)
- other change to the prompt















1-3
###
version message::

    1-3:add editor role

changes re ``system_message.md``:

- add a new **editor role**
- ask Kaye to provide source for in *encyclopedia role*
- add another an example of Python docstring regarding functions that return ``bool``














1-2
###
version message::

    1-2:implement roles

changes re ``system_message.md``:

- re-organize the prompt around the concept of different **roles**
- add abbreviation list, utilize it in some roles















1-1
###
version message::

    1-1:create prompt/, add commit_message.md

changes re ``system_message.md``:

- captialize *Sir* as the refer
- rename section *task* (from *mission*)

changes re ``commit_message.md``:

- new! copied from *VS code* extension ``ChatGPT - Genie AI``'s default commit prompt
















1-0
###
version message::

    1-0:create Kaye

The very first version of prompt for **Kaye**. The *mission* part is adpated from default prompt provided in *VS code* extension ``ChatGPT - Genie AI``.

