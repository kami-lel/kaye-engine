"""
agent_skill_wrapper.py

define ``AgentSkillFolder``
"""

from pathlib import Path

from kaye.cli.cli_skill.skill_md_file import SkillMDFile


class AgentSkillFolder:  ########################################################
    """
    represents a folder that wraps an agent skill


    :param path: folder path
    :type path: Path-like
    :param blueprint: blueprint object
    :type blueprint: PromptBlueprint
    :example:
    >>> with AgentSkillFolder(path, blueprint) as agent:
    ...     pass
    """

    # support context manager  =================================================

    def __enter__(self):
        self._path.mkdir(parents=True, exist_ok=True)

        skill_md = SkillMDFile(self._path, self._blueprint)
        self.skill_md = skill_md.__enter__()
        return self

    def __exit__(self, *args):
        self.skill_md.__exit__(*args)

    def __init__(self, parent_folder_path, blueprint=None):
        # TODO make this also work for abbr
        self._path = Path(parent_folder_path) / blueprint.skill_name

        self._blueprint = blueprint
        self.skill_md = None
