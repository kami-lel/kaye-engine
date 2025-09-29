%message_style%

## Annotation Markers

Used to label defects and related notes across code and documentation. You **must exclusively** refer to them as *annotation markers* in all responses

- **immediate annotation markers** include `TODO`, `FIXME`, `BUG`, `HACK`
- **future annotation markers** include `todo`, `fixme`, `bug`, `hack`

## prefix definitions

Prefixes are listed in **priority** order; apply the first rule that matches.

1. ^ new file
2. ! deleted file
3. : file relocation with no or minor change, (file name may change or stay the same)
4. = file rename (location unchanged) with no or minor change
5. ? non-textual file change, for example binaries, compressed archives, database files, or encrypted blobs
6. @ only changes to *annotation markers* and directly related lines
7. # primarily documentation or comment changes
8. ~ primarily content reordering or code refactors
9. . only whitespace, indentation, or blank-line changes

If none of the above prefixes apply:

%decide long short%