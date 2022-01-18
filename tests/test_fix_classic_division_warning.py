from __future__ import generator_stop

from utils import check_on_input

CLASSIC_DIVISION = (
    """\
a /= 3
1 / 2
""",
    """\
from modernize.old_division_utils import warn_div_assign
from modernize.old_division_utils import warn_div
a /= warn_div_assign(a, 3)
warn_div(1, 2)
""",
)


CLASSIC_DIVISION_2 = (
    """\
1 / 2 * 3 / 6
4 / 7 / 8
2 * 8 / 9
""",
    """\
from modernize.old_division_utils import warn_div
warn_div(warn_div(1, 2) * 3, 6)
warn_div(warn_div(4, 7), 8)
warn_div(2 * 8, 9)
""",
)


NEW_DIVISION = (
    """\
from __future__ import division
1 / 2
a /= 3
""",
    """\
from __future__ import division
1 / 2
a /= 3
""",
)


def test_optional():
    check_on_input(CLASSIC_DIVISION[0], CLASSIC_DIVISION[0])


def test_fix_classic_division_warnings():
    check_on_input(
        *CLASSIC_DIVISION, extra_flags=["-f", "modernize.fixes.fix_classic_division_warnings"]
    )
    check_on_input(
        *CLASSIC_DIVISION_2, extra_flags=["-f", "modernize.fixes.fix_classic_division_warnings"]
    )


def test_new_division():
    check_on_input(
        *NEW_DIVISION, extra_flags=["-f", "modernize.fixes.fix_classic_division_warnings"]
    )
