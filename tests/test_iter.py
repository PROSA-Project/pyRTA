from response_time_analysis.iter import brute_force_steps, merge_sorted_unique


def test_merge_sorted_unique_deduplicates_sorted_iterators() -> None:
    iterators = [iter([1, 3, 5, 7]), iter([2, 3, 4, 6, 8]), iter([1, 5, 8])]

    assert list(merge_sorted_unique(iterators)) == [1, 2, 3, 4, 5, 6, 7, 8]


def test_brute_force_steps_finds_change_points() -> None:
    def step_function(delta: int) -> int:
        return delta // 3

    assert list(brute_force_steps(step_function, limit=9)) == [2, 5, 8]


def test_brute_force_steps_can_yield_successor() -> None:
    def step_function(delta: int) -> int:
        return delta // 4

    assert list(brute_force_steps(step_function, limit=10, yield_succ=True)) == [4, 8]
