__all__ = [
    "assert_brace_title",
    "assert_brace1",
    "assert_brace2",
    "assert_coder_c_title",
    "assert_coder_c1",
    "assert_coder_cpp_title",
    "assert_coder_cpp1",
    "assert_js_ts00",
    "assert_js_ts01",
    "assert_js_ts11",
    "assert_js_ts12",
    "assert_js_ts21",
    "assert_js_ts22",
    "assert_js_ts23",
    "assert_js_ts24",
    "assert_cs0",
    "assert_cs1",
    "assert_py_title",
    "assert_py_intro",
    "assert_py_doc0",
    "assert_py_doc1",
    "assert_py_pytest0",
    "assert_py_pytest1",
    "assert_py_pytest2",
]




# brace  =======================================================================


def assert_brace_title(opt):
    assert "## Brace Style" in opt


def assert_brace1(opt):
    assert "- opening `{` on the **same line**" in opt


def assert_brace2(opt):
    assert "- closing `}` on its **own line**" in opt


# PLs  =========================================================================

# C  ***************************************************************************


def assert_coder_c_title(opt):
    assert "## Coder C" in opt


def assert_coder_c1(opt):
    assert "Use **C99** standard" in opt


# C++  *************************************************************************


def assert_coder_cpp_title(opt):
    assert "## Coder CPP" in opt


def assert_coder_cpp1(opt):
    assert "Use **C++17** standard" in opt


# ts & js  *********************************************************************


def assert_js_ts00(opt):
    assert "## Coder JavaScript and TypeScript" in opt


def assert_js_ts01(opt):
    assert "These standards are applicable exclusively" in opt


def assert_js_ts11(opt):
    assert "#### Naming Conventions" in opt


def assert_js_ts12(opt):
    assert "- Use **camelCase** for naming variables" in opt


def assert_js_ts21(opt):
    assert "### Documentation and Comments" in opt


def assert_js_ts22(opt):
    assert "- Ensure the code is accompanied by" in opt


def assert_js_ts23(opt):
    assert "*Example of JSDoc documentation:*" in opt


def assert_js_ts24(opt):
    assert "globalNS.method1 = function (a, b)" in opt


# c#  **************************************************************************


def assert_cs0(opt):
    assert "## Coder C Sharp" in opt


def assert_cs1(opt):
    assert "- Documentation: Use XML comments" in opt


# python  **********************************************************************


def assert_py_title(opt):
    assert "## Coder Python" in opt


def assert_py_intro(opt):
    assert "Adhere to the **PEP8** style guide," in opt


def assert_py_doc0(opt):
    assert "### Coder Python Docstring Style" in opt


def assert_py_doc1(opt):
    assert "The docstrings must be written using the" in opt


def assert_py_pytest0(opt):
    assert "### Coder Python Testing Guidelines" in opt


def assert_py_pytest1(opt):
    assert "This section pertains specifically to Python test code" in opt


def assert_py_pytest2(opt):
    assert "*Example of tests for the `add` function:*" in opt
