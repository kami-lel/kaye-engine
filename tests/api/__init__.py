def assert_briefness_style(opt):
    assert """### Commentary Case
- begin 1st sentence with a lowercase letter; use standard sentence capitalization for the 2nd and subsequent sentences
- use *Title Case* for **a few important words** within a sentence
- the last sentence should not end with punctuation""" in opt

    assert """## Briefness Style
- write in **newspaper headlinese**, prioritize brevity over grammar
- use present for current, infinitive for planned
- omit articles (a, an, the) and helper verbs, use strong nouns, verbs""" in opt


def assert_annotation_markers(opt):
    assert (
        """## Annotation Markers

Used to label defects and related notes across code and documentation. You must refer them as *annotation markers* or *AM*:"""
        in opt
    )

    assert """### Meaning""" in opt
