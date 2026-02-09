from math import floor, ceil


def _print_heading(content):
    filler_length = (76 - len(content)) / 2
    FILLER = "#"
    print(
        "\n"
        + FILLER * ceil(filler_length)
        + "  "
        + content
        + "  "
        + FILLER * floor(filler_length)
        + "\n"
    )


# Fixme rename all tests using -
