# SPDX-FileCopyrightText: 2024 Gispo Ltd. <info@gispo.fi>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import TYPE_CHECKING, NoReturn, cast

import pytest

if TYPE_CHECKING:
    from collections.abc import Callable


def fail(reason: str) -> NoReturn:
    """Wrap pytest.fail for type checking.

    With pytest 8 (resolved for Python 3.8/3.9) ty mis-binds pytest.fail's
    `reason` argument to `pytrace` at every call site; the cast gives it a
    correct signature on all resolved pytest versions.
    """
    _fail = cast("Callable[[str], NoReturn]", pytest.fail)
    _fail(reason)
