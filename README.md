# pyRTA — Response-Time Analysis in Python

The Python `response-time-analysis` package (pyRTA) implements the _response-time analyses_ (RTAs) formally verified in the [PROSA project](https://prosa.mpi-sws.org/).

It provides Python models for real-time task parameters (arrivals, execution, deadlines, priorities) and ready-to-use analyses for fixed-priority (FP), earliest-deadline-first (EDF), and FIFO schedulers, including support for non-preemptive segments and restricted-supply models.

## Features and Design
- Arrival models: periodic, periodic with jitter, sporadic, and arbitrary arrival curves, expressed either as minimum-separation vectors (i.e., "delta-min vectors") or as a list of steps and a prefix horizon.
- Preemption models: fully preemptive, fully non-preemptive, floating non-preemptive segments, and segmented limited-preemptive.
- Supply models: ideal processor and rate-delay model.
- Analyses: FP, EDF, and FIFO response-time analysis.
- Discrete time: pyRTA uses a discrete time model (`model.Duration` is an alias of `int`). Task parameters should be specified using an appropriate resolution (e.g., in nanoseconds or processor cycles).

## Installation

pyRTA is a pure Python package that can be installed from PyPI.

With the [`uv` package manager](https://docs.astral.sh/uv/) (recommended):

```bash
uv add response-time-analysis
```

With `pip`:

```bash
pip install response-time-analysis
```

## Quickstart
Compute a response-time bound for a task under fixed-priority (FP), earliest-deadline-first (EDF), and first-in-first-out (FIFO) scheduling on an ideal uniprocessor:

```python
from response_time_analysis import edf, fifo, fp
from response_time_analysis.model import (
    WCET,
    Deadline,
    FullyPreemptive,
    IdealProcessor,
    Periodic,
    Priority,
    Task,
    taskset,
)

# Two periodic tasks with implicit deadlines; higher priority has the larger numeric value as in Linux
tsk1 = Task(Periodic(period=5), FullyPreemptive(WCET(1)), Deadline(5), Priority(2))
tsk2 = Task(Periodic(period=10), FullyPreemptive(WCET(6)), Deadline(9), Priority(1))

supply = IdealProcessor()

tasks = taskset(tsk1, tsk2)

# RTA assuming uniprocessor fixed-priority scheduling.
solution = fp.rta(tasks, tsk2, supply)
assert solution.bound_found()
assert solution.response_time_bound == 8

# RTA assuming uniprocessor earliest-deadline first scheduling.
solution = edf.rta(tasks, tsk2, supply)
assert solution.bound_found()
assert solution.response_time_bound == 7

# RTA assuming uniprocessor FIFO scheduling.
solution = fifo.rta(tasks, supply)
assert solution.bound_found()
assert solution.response_time_bound == 7

# Use the horizon parameter to prevent the RTA from diverging.
tsk3 = Task(Periodic(period=9), FullyPreemptive(WCET(3)), Deadline(20), Priority(3))
overload = taskset(tsk1, tsk2, tsk3)
solution = fifo.rta(overload, supply, horizon=1000)
assert solution.bound_found() is False
assert solution.search_space is None
assert solution.response_time_bound is None
```

See the test cases in `tests/test_usage_examples.py` for further examples.

## Development
- Run tests with `uv run pytest`
- Type-check with `uvx basedpyright`
- Lint and format with `uvx ruff check --fix`

## Disclaimer

While PROSA verifies the underlying RTA theory, the implementations in pyRTA are *not* verified themselves — this is just a regular Python library.

However, pyRTA serves as the underlying RTA of the [POET](https://prosa.mpi-sws.org/poet.html) foundational response-time analysis tool, which formally _certifies_ the outputs of unverified analyses to formally prove that the particular analysis results are correct (i.e., it verifies the output of each run, rather than the full implementation). Please refer to [the POET paper](https://drops.dagstuhl.de/opus/volltexte/2022/16336/pdf/LIPIcs-ECRTS-2022-19.pdf) for a more in-depth explanation. 

## Contributions, Feedback, Questions

Please use the [project's issue tracker](https://gitlab.mpi-sws.org/RT-PROOFS/pyRTA/-/issues) or contact [Björn Brandenburg](https://people.mpi-sws.org/~bbb/).

A [Github mirror](https://github.com/PROSA-Project/pyRTA) is available and accepts [pull requests](https://github.com/PROSA-Project/pyRTA/pulls).

## Attribution

When using the pyRTA library in academic work, please cite the paper underlying the verified RTAs implemented in this library:

- Sergey Bozhko and Björn Brandenburg, “[Abstract Response-Time Analysis: A Formal Foundation for the Busy-Window Principle](https://drops.dagstuhl.de/opus/volltexte/2020/12385/pdf/LIPIcs-ECRTS-2020-22.pdf)”, *Proceedings of the 32nd Euromicro Conference on Real-Time Systems (ECRTS 2020)*, pp. 22:1–22:24, July 2020. DOI: [10.4230/LIPIcs.ECRTS.2020.22](https://doi.org/10.4230/LIPIcs.ECRTS.2020.22)

```
@inproceedings{BB:20,
  author       = {Sergey Bozhko and
                  Bj{\"{o}}rn B. Brandenburg},
  title        = {Abstract Response-Time Analysis: {A} Formal Foundation for the Busy-Window
                  Principle},
  booktitle    = {Proceedings of the 32nd Euromicro Conference on Real-Time Systems (ECRTS 2020)},
  pages        = {22:1--22:24},
  year         = {2020}
}
```
