"""
agent_skill_wrapper.py

define ``AgentSkillFolder``
"""

from kaye import logger

from kaye.cli.cli_claude import convert_display_name2skill_name
from kaye.cli.cli_claude.skill_md_file import SkillMDFile


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

    def __init__(
        self,
        parent_folder_path,
        *,
        blueprint=None,
        skill_name=None,
        verbose=False,
    ):
        if blueprint:
            self._path = parent_folder_path / convert_display_name2skill_name(
                blueprint.display_name
            )
        else:
            self._path = parent_folder_path / skill_name

        self._blueprint = blueprint
        self._skill_name = skill_name
        self._verbose = verbose
        self.skill_md = None

    # support context manager  =================================================

    def __enter__(self):
        self._path.mkdir(parents=True, exist_ok=True)

        skill_md = SkillMDFile(
            self._path,
            blueprint=self._blueprint,
        )
        self.skill_md = skill_md.__enter__()

        if not self._blueprint and self._skill_name:
            self.skill_md.name = self._skill_name

        return self

    def __exit__(self, *args):
        if self.skill_md:
            self.skill_md.__exit__(*args)

        logger.succ("export skill:\t" + str(self._path))
