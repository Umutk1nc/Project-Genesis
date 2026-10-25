# Changelog

## [Unreleased]
### Changed
- `save/save_system.json` is now tracked and its current state is committed as it changes

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