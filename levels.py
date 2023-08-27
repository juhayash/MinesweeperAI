# levels.py
import copy
# import heapq
# import multiprocessing.pool as mpool
import os
import random
# import shutil
import time
# import math

# have to make a class Individual or replace it or something 
# also replace the placeholder

# Define Minesweeper-specific tiles
options = [
    "E",  # Empty cell
    "B",  # Bomb cell
    "1", "2", "3", "4", "5", "6", "7", "8"  # Numbered cells
    # Add flagged cells and other types as needed
]

# Define Minesweeper-specific parameters
width = 10  # Width of the Minesweeper grid
height = 10  # Height of the Minesweeper grid
bomb_density = 0.2  # Proportion of cells that are bombs
mutation_rate = 0.01 # added mutation rate

# Update Individual_Grid class for Minesweeper
class Individual_Grid(object):
    __slots__ = ["genome", "_fitness"]

    def __init__(self, genome):
        self.genome = copy.deepcopy(genome)
        self._fitness = None

    # Update fitness calculation for Minesweeper
    def calculate_fitness(self):
        bomb_positions = []
        number_positions = []
        
        # Find positions of bombs and numbered cells
        for y in range(height):
            for x in range(width):
                if self.genome[y][x] == "B":
                    bomb_positions.append((x, y))
                elif self.genome[y][x] in ("1", "2", "3", "4", "5", "6", "7", "8"):
                    number_positions.append((x, y))
        
        # Calculate fitness based on distance between bombs and numbers
        fitness = 0
        for bomb_x, bomb_y in bomb_positions:
            min_distance = float("inf")
            for number_x, number_y in number_positions:
                distance = abs(bomb_x - number_x) + abs(bomb_y - number_y)
                min_distance = min(min_distance, distance)
            # Subtract distance to encourage placing bombs near numbered cells
            fitness -= min_distance
        
        self._fitness = fitness
        return self

    # Update mutation for Minesweeper
    def mutate(self, genome):
            new_genome = copy.deepcopy(self.genome)

            for y in range(height):
                for x in range(width):
                    if random.random() < mutation_rate:
                        if new_genome[y][x] == "E":
                            new_genome[y][x] = "B" if random.random() < bomb_density else "E"
                        elif new_genome[y][x] == "B":
                            new_genome[y][x] = "E" if random.random() < bomb_density else "B"
            
            return new_genome

    # Update empty_individual and random_individual for Minesweeper
    @classmethod
    def empty_individual(cls):
        # Generate an empty Minesweeper grid
        g = [["E" for _ in range(width)] for _ in range(height)]
        return cls(g)

    @classmethod
    def random_individual(cls):
        # Generate a random Minesweeper grid with bombs and numbers
        g = [random.choices(options, weights=[1 - bomb_density, bomb_density] + [1] * 8, k=width)
             for _ in range(height)]
        return cls(g)
    
    def to_level(self): # New method to output the genome
        return self.genome

# Update generate_successors for Minesweeper
def generate_successors(population):
    results = []

    for _ in range(len(population)):
        parent = random.choice(population)
        child = copy.deepcopy(parent)
        child.genome = parent.mutate(child.genome)
        results.append(child)

    return results


# Update the ga function for Minesweeper
def ga():
    pop_limit = 100
    generations = 50
    population = [Individual_Grid.random_individual() for _ in range(pop_limit)]

    for generation in range(generations):
        print("Generation:", generation + 1)
        
        # Calculate fitness for the entire population
        for individual in population:
            individual.calculate_fitness()
        
        # Sort population by fitness in descending order
        population.sort(key=lambda ind: ind._fitness, reverse=True)
        
        # Print information about the best individual in this generation
        best_individual = population[0]
        print("Best fitness:", best_individual._fitness)
        
        # Generate successors for the next generation
        population = generate_successors(population)
    
    return population

def generate_best_level():
    final_gen = sorted(ga(), key=lambda x: x._fitness, reverse=True)
    best = final_gen[0]
    return best.to_level()

if __name__ == "__main__":
    if not os.path.exists('levels'):  # Ensure levels directory exists
        os.makedirs('levels')
    final_gen = sorted(ga(), key=lambda x: x._fitness, reverse=True)
    best = final_gen[0]
    print("Best fitness:", best.fitness())
    now = time.strftime("%m_%d_%H_%M_%S")
    for k in range(0, 10):
        with open("levels/" + now + "_" + str(k) + ".txt", 'w') as f:
            for row in best.to_level():
                f.write("".join(row) + "\n")
