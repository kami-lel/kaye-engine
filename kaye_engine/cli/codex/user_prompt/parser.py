"""render the Chat Blueprint as the Codex global AGENTS.md"""

from argparse import RawDescriptionHelpFormatter

import kamilog
from kaye_engine.cli import DEFAULT_SPARSENESS
from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli
from kaye_engine.cli.codex import CODEX_DOC_DESCRIPTION
from kaye_engine.cli.codex.exportable_name import (
    get_codex_chat_exportable,
    get_codex_merged_coder_exportable,
)
from kaye_engine.cli.render_profile_description import (
    RENDER_PROFILE_DESCRIPTION,
)
from kaye_engine.cli.render_profile_parser import (
    build_render_profile_parent_parser,
    resolve_render_profile,
)
from kaye_engine.cli.verbosity import apply_verbosity_arg

# constants  ===================================================================

_DESCRIPTION = (
    __doc__
    + """

result is printed to stdout

    kaye-engine codex usp > ~/.codex/AGENTS.md
"""
    + CODEX_DOC_DESCRIPTION
    + RENDER_PROFILE_DESCRIPTION
    + """

render defaults: surface=codex, comment=True, sparseness=0

-c is taken by --coder, so the comment flags have no short form
"""
)


def generate_codex_user_system_prompt(*, use_coder=False, render_profile=None):
    """
    :param use_coder: whether to render the merged Coder exportable
            instead of the plain Chat exportable
    :type use_coder: bool
    :param render_profile: forwarded to ``exportable.content(...)``
    :type render_profile: RenderProfile, optional
    :return: the rendered Codex global prompt
    :rtype: str
    """
    exportable = (
        get_codex_merged_coder_exportable()
        if use_coder
        else get_codex_chat_exportable()
    )
    return exportable.content(profile=render_profile)


def _user_prompt_main(args):
    apply_verbosity_arg(args)
    check_corpus_setup_for_cli()

    render_profile = resolve_render_profile(
        args,
        default_show_comment=True,
    )
    print(
        generate_codex_user_system_prompt(
            use_coder=args.coder, render_profile=render_profile
        )
    )


# pylint: disable=missing-function-docstring
def register_codex_user_prompt_parser(cli_subparser):  #########################
    user_prompt_parser = cli_subparser.add_parser(
        "user-system-prompt",
        help=__doc__,
        description=_DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["usp"],
        parents=[
            build_render_profile_parent_parser(
                default_surface=("codex",),
                default_sparseness=DEFAULT_SPARSENESS,
            )
        ],
    )

    user_prompt_parser.add_argument(
        "-c",
        "--coder",
        action="store_true",
        default=False,
        help="append Coder Blueprint content after the Chat Blueprint",
    )

    kamilog.add_verbose_arguments(user_prompt_parser)

    user_prompt_parser.set_defaults(func=_user_prompt_main)
