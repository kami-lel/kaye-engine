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
    :example:
    >>> folder = AgentSkillFolder(path)
    >>> folder.blueprint = blueprint
    >>> with folder as agent:
    ...     pass
    """

    # support context manager  =================================================

    def __enter__(self):
        self._path.mkdir(parents=True, exist_ok=True)
        skill_md = SkillMDFile(self._path)
        skill_md.blueprint = self.blueprint
        self.skill_md = skill_md.__enter__()
        return self

    def __exit__(self, *args):
        self.skill_md.__exit__(*args)

    def __init__(self, path):
        self._path = Path(path)

        self.blueprint = None
        self.skill_md = None
