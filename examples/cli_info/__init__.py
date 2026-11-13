"""
examples/cli_info/__init__.py

shared helpers of the ``*_demo.py`` scripts: populate kaye-engine
with a demo consumer, run a ``kaye-engine`` command through the real CLI
parser, and print banners around each run
"""

import json
import tempfile
from pathlib import Path

from kaye_engine import (
    StringDynamicSubstitution,
    load_corpus_tree,
    populate_abbr_data_with_json_file,
    register_abbr_glossary,
    register_blueprint,
    register_consumer,
    register_corpus_under_node,
    register_dynamic_substitution,
    register_render_profile,
    set_entry_consumer,
)
from kaye_engine.cli.cli_main import register_cli_main_parser
from kaye_engine.prompt import register_affordance, register_variant
from kaye_engine.prompt.blueprint import (
    create_blueprint_from_node,
    get_corpus_node,
)
from kaye_engine.prompt.blueprint.render_profile import RenderProfile

__all__ = (
    "DEMO_BLUEPRINT",
    "DEMO_GLOSSARY",
    "DEMO_SUBSTITUTION",
    "populate_demo_consumer",
    "run_demo",
)

# constants  ###################################################################
DEMO_CONSUMER = "demo-consumer"
DEMO_GLOSSARY = "demo-terms"
DEMO_BLUEPRINT = "demo-rules"
DEMO_SUBSTITUTION = "demo-greeting"
DEMO_SURFACE = "demo-surface"
BANNER_WIDTH = 80

DEMO_CORPUS = """\
# Demo Rules

Greet the user with (((demo-greeting))).

## {description}

demo rules for the print-out demo

## {when_to_use}

whenever the demo needs a skill

## Tone

stay brief and polite

## Format

answer in short bullet lists
"""

# abbr json: meaning -> its abbrs, per the abbrs.json schema
DEMO_ABBRS = {
    "demonstration": {
        "remark": "short for a sample",
        "abbrs": {
            "demo": {
                "priority": 1,
                "tags": ["common", "ascii_only", DEMO_GLOSSARY],
                "wrap": "word",
            },
        },
    },
    "configuration": {
        "abbrs": {
            "cfg": {
                "priority": 2,
                "tags": ["always_understand", "ascii_only", DEMO_GLOSSARY],
                "wrap": "word",
            },
        },
    },
}


# auxiliaries  #################################################################
def print_banner(heading, ruler="#"):
    """
    print a centered banner: heading flanked by two spaces, ruler-filled
    to ``BANNER_WIDTH``

    :param heading: banner text
    :type heading: str
    :param ruler: single char filling the line
    :type ruler: str
    """
    print("  {}  ".format(heading).center(BANNER_WIDTH, ruler))


def print_title_box(title, subtitle):
    """
    print the boxed run title

    :param title: first line of the box
    :type title: str
    :param subtitle: second line of the box
    :type subtitle: str
    """
    print("#" * BANNER_WIDTH)
    print("# {}".format(title))
    print("# {}".format(subtitle))
    print("#" * BANNER_WIDTH)


def run_cmd(argv):
    """
    parse ``argv`` with the real CLI parser and run its function, so the
    command prints exactly what a shell call would

    :param argv: arguments after ``kaye-engine``
    :type argv: list[str]
    :return: exit status the command ended with, 0 when it returned
    :rtype: int
    """
    cli_parser, _ = register_cli_main_parser()
    try:
        args = cli_parser.parse_args(argv)
        args.func(args)
    except SystemExit as e:
        return e.code if isinstance(e.code, int) else 1
    return 0


def run_cmd_rows(rows):
    """
    run every row under a banner naming the exact command; a ``-l`` row
    runs plain, then with ``-l``

    :param rows: (argv, whether the command carries -l) per row
    :type rows: tuple[tuple[list[str], bool]]
    """
    for argv, has_long in rows:
        variants = [argv, argv + ["-l"]] if has_long else [argv]
        for variant_argv in variants:
            print_banner("$ kaye-engine {}".format(" ".join(variant_argv)))
            status = run_cmd(variant_argv)
            if status != 0:
                print("(exit status {})".format(status))
            print()


# Public API  ##################################################################
def populate_demo_consumer(abbr_dir):
    """
    register one demo consumer with a glossary, abbreviations, a
    substitution, an affordance family, a render profile, a corpus and
    one blueprint, in the order the consumer doc requires

    :param abbr_dir: existing folder to hold the generated abbrs.json
    :type abbr_dir: Path
    """
    register_consumer("Demo Consumer", DEMO_CONSUMER, "0.1.0")

    register_abbr_glossary(
        DEMO_GLOSSARY,
        True,
        is_sorted=True,
        consumer=DEMO_CONSUMER,
        description="demo abbreviations",
        when_to_use="whenever the demo reads shorthand",
    )
    abbr_path = abbr_dir / "abbrs.json"
    abbr_path.write_text(json.dumps(DEMO_ABBRS), encoding="utf-8")
    populate_abbr_data_with_json_file(abbr_path)

    register_dynamic_substitution(
        DEMO_SUBSTITUTION, StringDynamicSubstitution("a warm hello")
    )

    register_affordance("demo-echo", "print text back")
    register_variant("Demo:echo", "demo-echo", "echo text to stdout")
    register_variant("Demo:say", "demo-echo", "say text aloud")
    register_render_profile(
        DEMO_SURFACE,
        RenderProfile(variants=("Demo:echo",), sparseness=0),
        "demo target",
    )

    register_corpus_under_node((), DEMO_CORPUS)
    load_corpus_tree()
    register_blueprint(
        DEMO_BLUEPRINT,
        create_blueprint_from_node(
            get_corpus_node("Demo Rules"), is_recursive=True
        ),
        consumer=DEMO_CONSUMER,
    )
    set_entry_consumer(DEMO_CONSUMER)


def run_demo(title, subtitle, rows):
    """
    populate the demo consumer, then run ``rows``: the whole body of a
    ``*_demo.py`` script

    :param title: script name for the title box
    :type title: str
    :param subtitle: what the script prints
    :type subtitle: str
    :param rows: (argv, whether the command carries -l) per row
    :type rows: tuple[tuple[list[str], bool]]
    """
    print_title_box(title, subtitle)
    with tempfile.TemporaryDirectory() as tmp_dir:
        populate_demo_consumer(Path(tmp_dir))
        run_cmd_rows(rows)
