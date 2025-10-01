# BUG not functional


def _kaye_main(_):
    # when calling ``python -m kaye``
    kaye_psr.print_help()


kaye_psr = ArgumentParser(prog=PROGRAM_NAME, description=__doc__)
kaye_psr.set_defaults(func=_kaye_main)
kaye_subpsr = kaye_psr.add_subparsers(title="subcommands")
