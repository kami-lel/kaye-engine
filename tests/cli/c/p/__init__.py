def assert_edit_changelog0(testee_content):

    return "#### edit CHANGELOG" in testee_content


def assert_edit_changelog1(testee_content):
    return (
        "- edit `CHANGELOG.md` or CHANGELOG-Style File "
        "to reflect the current project state"
        in testee_content
    )


def assert_edit_changelog2(testee_content):
    return (
        "- Follow the **CHANGELOG Writer** rule for format, versioning, "
        "and entry style"
        in testee_content
    )


def assert_edit_readme0(testee_content):
    return "#### edit README" in testee_content


def assert_edit_readme1(testee_content):
    return "follow `Coder README Writer`" in testee_content


def assert_edit_readme2(testee_content):
    return (
        "update applicable overview, features, setup, usage, "
        "configuration, commands, contribution notes, security notes, and "
        "license details"
        in testee_content
    )


def assert_edit_readme3(testee_content):
    return (
        "prioritize the root README when multiple README-style files exist"
        in testee_content
    )


def assert_edit_agents0(testee_content):
    return "#### edit AGENTS" in testee_content


def assert_edit_agents1(testee_content):
    return "follow `Coder AGENTS Writer`" in testee_content


def assert_edit_agents2(testee_content):
    return (
        "preserve or add required frontmatter when applicable" in testee_content
    )


def assert_edit_agents3(testee_content):
    return (
        "avoid moving human-facing content from README files into AGENTS "
        "files unless it is useful for coding agents"
        in testee_content
    )
