# Project Genesis

A survival and resource management game in development. A pilot crash-lands on an unknown planet and has to stay alive with limited resources. Long-term goal: a full game with RPG elements and moral choices.

> **Status:** Early development. The OOP rewrite can be run from the terminal with `python main.py` (agriculture and eating systems). The earlier procedural prototype is available at [v0.1.1](https://github.com/Umutk1nc/Project-Genesis/tree/v0.1.1).

## What's here
- Main menu to start the agriculture and eating systems
- Time and day periods
- Food and eating system
- Farming system (planting, watering, harvesting)
- Player condition data (health, oxygen, satiety, water, energy, morale) in the save file
- JSON-based game data and save structure

More systems will be added step by step. Planned work is tracked in Issues and the Project board.

## Setup

Requires Python 3.13 and `tabulate`:

```bash
pip install tabulate
```
Run the game:

```bash
python main.py
```