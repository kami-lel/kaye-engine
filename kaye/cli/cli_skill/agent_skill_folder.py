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

    def __init__(
        self,
        parent_folder_path,
        *,
        blueprint=None,
        skill_name=None,
        verbose=False,
        includes_version=False
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
        self._includes_version = includes_version
        self.skill_md = None

    # support context manager  =================================================

    def __enter__(self):
        self._path.mkdir(parents=True, exist_ok=True)

        skill_md = SkillMDFile(
            self._path,
            blueprint=self._blueprint,
            includes_version=self._includes_version,
        )
        self.skill_md = skill_md.__enter__()

        if not self._blueprint and self._skill_name:
            self.skill_md.name = self._skill_name

        return self

    def __exit__(self, *args):
        if self.skill_md:
            self.skill_md.__exit__(*args)

        if self._verbose:
            print("export skill:\t" + str(self._path))
