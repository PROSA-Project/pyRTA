# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Changed
- When analyzing POET's extended search spaces, ensure that every solution satisfies A<=F, as the current version of POET has this requirement hard-coded on the PROSA side. This special case will be removed again once the POET certificates are modernized. 

### Added
- Added `as_arrival_curve_prefix()` to the arrival-model interface to obtain arrival-curve prefixes, plus `Task` and `TaskSet` helpers to convert arrivals to arrival-curve prefixes.

### Fixed
- Don't crash on empty `max()` in `MinimumSeparationVector::extrapolate()` when `len(dmin) == 1`.

## [0.1.0] - 2026-01-13

First public release
