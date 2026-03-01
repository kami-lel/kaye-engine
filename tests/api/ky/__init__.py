def _assert_chat_blueprint_opt(opt):

    assert opt.startswith("""# Introduction
You are **Kaye**, an AI assisting *agent* to the *user*.""")

    assert opt.endswith("""# Standards
## Numerical Values with Units
- Dual Unit Systems: Present values using both the metric and US unit systems. For example:
  - Distance: `8 848m (29 029ft)`
  - Mass: `10.5kg (22 lb)`
  - Temperature: `20°C (68°F)`
- Unit Abbreviations: Always use the correct abbreviations for units to ensure clarity and precision.
- Thousands Separator: Use a space character as the thousands separator rather than a comma. For instance, express large numbers as `29 029` instead of `29,029`.

# Role""")

    # TODO more tests
