"""
render_profile_description.py

define ``RENDER_PROFILE_DESCRIPTION`` -- the help-text epilog every
rendering command appends to its own description
"""

__all__ = ("RENDER_PROFILE_DESCRIPTION",)


# FIXME mpv for better description

RENDER_PROFILE_DESCRIPTION = """

Render Profile Options  --------------------------------------------------------

shared by every rendering command: any subcommand that reaches
render_prompt(), directly or through Exportable.content()

    blueprint render, dynamic-node, exportable, skill, claude skills,
    claude plugin, claude marketplace, claude code,
    claude user-system-prompt, claude vs-code-extension

flags:

    --surface NAME [NAME ...], -u
        surface(s) to render for; several merge in the order given;
        absent when the consumer configured no surface profiles
    --comment, -c / --no-comment, -C
        turn the trailing generated-by comment on or off
    --conditional-sidecar NAME [NAME ...], -i
        extra sidecar names, added to the surface's
    --variant NAME [NAME ...]
        extra variant names, added to the surface's
    --sparseness N, -s
        blank-line policy: -1 one line, 0 none, 1 collapse runs to one,
        N cap runs at N, 99 no trimming
    --reverse-order
        reverse sibling order at every level of the tree walk

notes:

    claude user-system-prompt already uses -c for --coder, so its
    comment flags have no short form

    blueprint preview has the same comment flags but is not a
    rendering command

How Flags Resolve  -------------------------------------------------------------

    1. start from an empty profile, merge in each selected surface
    2. if --variant was given or any surface is selected, merge in the
       --variant names; this switches variants on, so a surface with no
       listed variants yields an empty set instead of off
    3. if --conditional-sidecar was given, merge those names in
    4. add reverse order to the mode when --reverse-order was passed
    5. merge in sparseness, comment, and mode last

--variant and --conditional-sidecar only add to what a surface provides.
sparseness and comment always come from the flag or the command's own
default, never from a surface.

Per-Command Defaults  ----------------------------------------------------------

used when a flag is omitted

    command                    comment  surface
    blueprint render           on       none
    dynamic-node               off      none
    exportable                 off      none
    skill                      off      chat
    claude skills              off      chat
    claude plugin              off      chat, cowork
    claude marketplace         off      vsc
    claude code                off      code
    claude vs-code-extension   on       vsc
    claude user-system-prompt  on       chat, cowork

a default surface only works when the consumer defines that surface name

--sparseness defaults to DEFAULT_SPARSENESS (currently 0), unless the
subcommand passes its own default

blueprint render sets the comment's blueprint name to the registered
name (<stdin> when read from stdin); a registered blueprint renders
through its registry entry's own render profile, merged under the flags,
while one read from stdin renders with the flags alone

The resolved profile travels as one render_profile= argument through
every claude export and reaches Skill.from_exportable(), where the
entry's own default is merged in, not replaced.

For the profile itself, see the render profile documentation on GitHub:

    https://github.com/kami-lel/kaye-engine/blob/main/docs/render-profile-doc.md"""
