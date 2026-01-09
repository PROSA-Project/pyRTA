import heapq
from collections.abc import Callable, Iterable, Iterator


def merge_sorted_unique(iters: Iterable[Iterator[int]]) -> Iterator[int]:
    """
    Merge multiple increasing iterators of unique ints into a single
    increasing iterator without repetition.
    """
    heap: list[tuple[int, int, Iterator[int]]] = []
    for idx, it in enumerate(iters):
        try:
            first = next(it)
            heap.append((first, idx, it))
        except StopIteration:
            pass

    heapq.heapify(heap)
    last_yielded = None

    while heap:
        value, idx, it = heapq.heappop(heap)

        if last_yielded != value:
            yield value

        last_yielded = value

        try:
            nxt = next(it)
            heapq.heappush(heap, (nxt, idx, it))
        except StopIteration:
            pass


def brute_force_steps(
    sb: Callable[[int], int], limit: int | None = None, yield_succ: bool = False
) -> Iterator[int]:
    delta = 0
    njobs = sb(delta)
    while limit is None or delta <= limit:
        njobs_plus_1 = sb(delta + 1)
        if njobs != njobs_plus_1:
            yield delta + 1 if yield_succ else delta
        delta, njobs = delta + 1, njobs_plus_1
