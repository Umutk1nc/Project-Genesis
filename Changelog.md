# Changelog

## [Unreleased]

## [0.2.0-alpha.2] - 2026-10-28
### Changed
- Code, data files, JSON keys, schemas and in-game texts translated to English (PEP 8 naming)
- Save files have a `save_version` (2). Old Turkish-key saves are no longer compatible
- `save/save_system.json` is now tracked and its current state is committed as it changes

### Fixed
- Planting with an empty food stock no longer traps the player in a prompt
- Harvest crash caused by a missing food field
- Irrigation menu navigation (Select Another Field, Main Menu) and the crash on full fields

## [0.2.0-alpha.1] - 2026-10-24
### Changed
- Rewrote the prototype with an OOP architecture (farming, eating, time)
- Data files and folder names translated to English
- Save data split into a tracked template (`save_example.json`) and a local, untracked `save_system.json`
- Systems no longer start the game when imported

### Notes
- No entry point yet, so this version cannot be run as a game

## [0.1.1] - 2026-10-23
### Added
- Farming system: field view, planting, watering table, harvest flow (work in progress)

## [0.1.0] - 2026-10-22
### Added
- Pre-OOP prototype: time system, survival meters, eating system
- JSON-based game data and save structure