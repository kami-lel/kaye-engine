==============
kaye CHANGELOG
==============

.. default-role:: smart

.. contents::













version checklist
#################
.. rubric:: commit process

Stash aways most recent changes::

    git checkout dev
    git stash push

**Squash merge** ``main`` from ``dev``::

    git checkout main
    git merge --squash dev
    git stash pop

Inspect changes of this version::

    git status [-s]
    git diff --cached . [PATH]

Make the **version commit** with *version message* with squash commit messages::

    git commit -t .git/SQUASH_MSG

Catch up ``dev`` branch with the version::

    git checkout dev
    git merge main -X theirs --no-commit
    git restore -S -W -s main .
    git merge --continue













1-1
###
version message::

    1-0:TODO

changes re ``system_message.md``:

- captialize *Sir* as the refer















1-0
###
version message::

    1-0:create Kaye

The very first version of prompt for **Kaye**. The *mission* part is adpated from default prompt provided in *VS code* extension ``ChatGPT - Genie AI``.

