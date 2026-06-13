"""
agent_skill_wrapper.py

define ``AgentSkillFolder``
"""

from kaye.cli.cli_skill import convert_display_name2skill_name
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

    # constructor  =============================================================

    def __init__(self, parent_folder_path, *, blueprint=None, skill_name=None):
        if blueprint:
            self._path = parent_folder_path / convert_display_name2skill_name(
                blueprint.display_name
            )
        else:
            self._path = parent_folder_path / skill_name

        self._blueprint = blueprint
        self.skill_md = None

    # support context manager  =================================================

    def __enter__(self):
        self._path.mkdir(parents=True, exist_ok=True)

        if self._blueprint:
            skill_md = SkillMDFile(self._path, self._blueprint)
            self.skill_md = skill_md.__enter__()

        return self

    def __exit__(self, *args):
        self.skill_md.__exit__(*args)
