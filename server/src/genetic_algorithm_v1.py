from dataclasses import dataclass, field
from typing import List, Callable
import random

@dataclass
class Gene:
    """Represents a single unit of data in a chromosome."""
    # value: any  # Define specific fields based on the problem domain
    pass

@dataclass
class Chromosome:
    """Represents a solution candidate."""
    genes: List[Gene] = field(default_factory=list)
    fitness: float = 0.0  # Fitness value calculated during evaluation

@dataclass
class Population:
    """Represents a group of chromosomes."""
    chromosomes: List[Chromosome] = field(default_factory=list)

@dataclass
class Constraint:
    """Represents a constraint for evaluating fitness."""
    weight: float  # Penalty for violating this constraint

    def apply(self, chromosome: Chromosome) -> float:
        """Evaluates the constraint on a chromosome and returns the penalty."""
        raise NotImplementedError

@dataclass
class FitnessEvaluator:
    """Evaluates the fitness of a chromosome based on constraints."""
    constraints: List[Constraint]

    def evaluate(self, chromosome: Chromosome) -> float:
        """Calculates the fitness by summing penalties from all constraints."""
        penalty = sum(constraint.apply(chromosome) for constraint in self.constraints)
        return max(0, 100 - penalty)  # Example: Fitness = 100 - penalty

class GeneticAlgorithm:
    """Implements the workflow of a genetic algorithm."""

    def __init__(self, population_size: int, gene_generator: Callable, fitness_evaluator: FitnessEvaluator):
        self.population = Population([self.create_chromosome(gene_generator) for _ in range(population_size)])
        self.fitness_evaluator = fitness_evaluator

    def create_chromosome(self, gene_generator: Callable) -> Chromosome:
        """Generates a chromosome with random genes."""
        genes = [gene_generator() for _ in range(random.randint(5, 10))]  # Adjust gene count as needed
        return Chromosome(genes=genes)

    def evaluate_population(self):
        """Evaluates and assigns fitness to all chromosomes in the population."""
        for chromosome in self.population.chromosomes:
            chromosome.fitness = self.fitness_evaluator.evaluate(chromosome)

    def select_parents(self) -> List[Chromosome]:
        """Selects chromosomes for reproduction using fitness-based selection."""
        self.population.chromosomes.sort(key=lambda c: c.fitness, reverse=True)
        return self.population.chromosomes[:2]  # Top two chromosomes as parents

    def crossover(self, parent1: Chromosome, parent2: Chromosome) -> Chromosome:
        """Generates a child chromosome by combining genes from parents."""
        crossover_point = random.randint(0, len(parent1.genes) - 1)
        new_genes = parent1.genes[:crossover_point] + parent2.genes[crossover_point:]
        return Chromosome(genes=new_genes)

    def mutate(self, chromosome: Chromosome, mutation_rate: float):
        """Randomly mutates genes in a chromosome based on mutation rate."""
        for gene in chromosome.genes:
            if random.random() < mutation_rate:
                # Define mutation logic here
                gene.value = random.randint(1, 100)  # Example mutation

    def run(self, generations: int, mutation_rate: float):
        """Runs the genetic algorithm for a specified number of generations."""
        for generation in range(generations):
            self.evaluate_population()
            parent1, parent2 = self.select_parents()
            child = self.crossover(parent1, parent2)
            self.mutate(child, mutation_rate)
            # Replace the weakest chromosome with the new child
            self.population.chromosomes[-1] = child

# Example Constraint
@dataclass
class SameFacultyAtDifferentLectureAtSameTime(Constraint):
    def apply(self, chromosome: Chromosome) -> float:
        # Implement constraint logic, return penalty if violated
        return random.uniform(0, 10)  # Example penalty

# Example Gene Generator
def gene_generator():
    return Gene(value=random.randint(1, 100))

# Example Usage
constraints = [SameFacultyAtDifferentLectureAtSameTime(weight=10)]
fitness_evaluator = FitnessEvaluator(constraints=constraints)
ga = GeneticAlgorithm(population_size=10, gene_generator=gene_generator, fitness_evaluator=fitness_evaluator)

ga.run(generations=50, mutation_rate=0.1)
