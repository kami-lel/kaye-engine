"""
render_parser.py

define ``register_render_parser``
"""

import dataclasses
from argparse import RawDescriptionHelpFormatter

import kamilog
from kaye_engine import LOGGER_NAME
from kaye_engine.cli import DEFAULT_SPARSENESS
from kaye_engine.cli.blueprint.aux_input import get_cmd_blueprint
from kaye_engine.cli.blueprint.aux_output import (
    emit_str,
    pick_render_fx,
    run_cmd_and_exit,
)
from kaye_engine.cli.blueprint.blueprint_arg_parser import (
    build_blueprint_arg_parser,
    build_no_dependencies_arg_parser,
)
from kaye_engine.cli.cli_setup_guard import check_corpus_setup_for_cli
from kaye_engine.cli.claude.setup import get_surface_profiles
from kaye_engine.cli.render_profile_parser import (
    RENDER_PROFILE_DESCRIPTION,
    build_render_profile_parent_parser,
    resolve_render_profile,
)
from kamilog import (
    add_verbose_arguments,
    set_logging_level_by_namespace,
)

# logger  ######################################################################
logger = kamilog.getLogger(LOGGER_NAME)

# todo cli prompt generate: allow sidecars be arg

# constants  ###################################################################
_HELP = "render a blueprint into a concrete prompt"

_DESCRIPTION = _HELP + """

renders blueprint into a final system prompt; the result is printed to stdout

select BLUEPRINT by canonical name in blueprint registry:

    kaye-engine blueprint render my-blueprint

reading blueprint from stdin, a preview tree or JSON:

    kaye-engine blueprint render < my-blueprint.json
    cat my-tree.txt | kaye-engine blueprint render
"""


# auxiliaries  #################################################################
def _render_main(args):
    set_logging_level_by_namespace(args, logger=logger)
    check_corpus_setup_for_cli()

    loaded = get_cmd_blueprint(args.BLUEPRINT)
    render_profile = resolve_render_profile(
        args,
        surface_profiles=get_surface_profiles(),
        default_show_comment=True,
    )
    render_profile = dataclasses.replace(
        render_profile, display_name=loaded.display_name
    )

    # a registered blueprint keeps its entry's own render defaults
    if loaded.registry is not None:
        render_profile = loaded.registry.resolve_profile(render_profile)

    render_fx = pick_render_fx(args.is_no_dependencies)

    emit_str(render_fx(loaded.blueprint, profile=render_profile))


# Public API  ##################################################################
def register_render_parser(cli_subparser):
    """
    register the ``kaye blueprint render`` subcommand parser
    """
    render_parser = cli_subparser.add_parser(
        "render",
        help=_HELP,
        description=_DESCRIPTION + RENDER_PROFILE_DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
        aliases=["r"],
        parents=[
            build_blueprint_arg_parser(is_render_profile=True),
            build_no_dependencies_arg_parser(),
            build_render_profile_parent_parser(
                default_sparseness=DEFAULT_SPARSENESS,
                surface_profiles=get_surface_profiles(),
            ),
        ],
    )

    add_verbose_arguments(render_parser)

    render_parser.set_defaults(
        func=lambda args: run_cmd_and_exit(_render_main, args)
    )
