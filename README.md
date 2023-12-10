# Minesweeper AI with Genetic Algorithms

## Overview
This project reimagines the creation and experience of Minesweeper levels by utilizing genetic algorithms. The aim of this project is to offer players a unique gameplay experience with levels tailored to different difficulty settings. This approach allows for the introduction of new features and challenges, enhancing the classic Minesweeper game with AI-driven complexity.

## Problem Addressed
Traditional Minesweeper games increase difficulty by altering the board size and mine count. Our project maintains a constant board size, varying the number and configuration of mines based on the chosen difficulty level. This approach creates more diverse game boards and offers a progressive difficulty curve.

## Technical Solution
Our Minesweeper AI uses a Genetic Algorithm to generate game grids:
- **Representation**: Game grids are 2D arrays with diverse tile types (empty cells, bombs, numbered cells).
- **Fitness Calculation**: Fitness is based on the arrangement of bombs and numbered cells, with higher scores indicating better configurations.
- **Mutation and Selection**: Mutations introduce changes to individuals, creating new game grids. Selection favors individuals with higher fitness.
- **Generation Evolution**: The AI evolves the population through selection, mutation, and fitness evaluation.

## Novelty
The project's uniqueness lies in using genetic algorithms for Minesweeper level creation, introducing randomness and adaptability. Each level is distinct, offering novel challenges to the players.

## Fun Bits
- **Pre-defined Mine Shapes**: Introducing mine clusters and zigzags for unexpected configurations.
- **Tile Variations**: Mystery Tiles (unknown mine count) and Trigger Tiles (reveal another tile's value temporarily).

## Benefits
This project benefits both players and game designers:
- **Players**: Offers varied challenges for all skill levels.
- **Designers**: Inspires the use of genetic algorithms in game design for enhanced and expanded gameplay experiences.

## Mementos

### Interface Screenshots
<div style="position: relative;">
  <span style="position: absolute; top: 0; left: 0; background-color: rgba(255, 255, 255, 0.7); padding: 5px;"></span>
  <img src="https://github.com/juhayash/MinesweeperAI/assets/140232266/159c6d4d-2c93-4a0b-b060-24d618ee86c2" alt="Game View Screenshot 1" width="400"/>
  <img src="https://github.com/juhayash/MinesweeperAI/assets/140232266/c73b86ad-ab40-4d4f-bcb8-f0fabe41ade3" alt="Game View Screenshot 2" width="400"/>
</div>

### Generated Level Examples
<div style="position: relative;">
  <span style="position: absolute; top: 0; left: 0; background-color: rgba(255, 255, 255, 0.7); padding: 5px;"></span>
  <img src="https://github.com/juhayash/MinesweeperAI/assets/140232266/c8f5135c-3a16-49ae-b083-62dc18ef5e61" alt="Generated Levels" width="400"/>
</div>



