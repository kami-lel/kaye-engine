"""
render_profile_description.py

define ``RENDER_PROFILE_DESCRIPTION`` -- the help-text epilog every
rendering command appends to its own description
"""

__all__ = ("RENDER_PROFILE_DESCRIPTION",)


RENDER_PROFILE_DESCRIPTION = """

Render Profile Options  --------------------------------------------------------

shared by every rendering command:

    --surface NAME [NAME ...], -u
        surface(s) to render for; several merge in the order given;
        names are those of `kaye-engine render-profile`
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

For how the flags resolve into one profile, see the render profile
documentation on GitHub:

    https://github.com/kami-lel/kaye-engine/blob/main/docs/render-profile-doc.md"""
