from collections.abc import Callable


def inequality(
    lhs: Callable[[int], int] = lambda x: x,
    rhs: Callable[[int], int] = lambda x: x,
    horizon: int | None = None,
    start: int = 1,
    step: Callable[[int, int, int], int] = lambda x, lh, rh: max(lh, x + (lh - rh)),
) -> int | None:
    "Iteratively try to find a solution solving lhs(x) <= rhs(x)."

    x = start
    lh, rh = 0, 0
    while True:
        last_lh, last_rh = lh, rh
        try:
            lh = lhs(x)
            rh = rhs(x)
        except OverflowError:
            # If we manage to overflow, then we certainly didn't converge.
            return None
        assert lh >= last_lh  # lhs must be monotonically increasing
        assert rh >= last_rh  # rhs must be monotonically increasing
        if lh <= rh:
            return x
        elif horizon is not None and x > horizon:
            # We didn't converge before the horizon, so we give up.
            return None
        else:
            x = step(x, lh, rh)
