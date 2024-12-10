from dataclasses import dataclass, field
from typing import List, Callable
import random
from abc import ABC, abstractmethod
@dataclass
class Gene:
    """Represents a single unit of data in a chromosome."""
    # value: any  # Define specific fields based on the problem domain
    pass

    def to_dict(self):
        return super().to_dict()

@dataclass
class Chromosome:
    """Represents a solution candidate."""
    genes: List[Gene] = field(default_factory=list)
    fitness: float = 0.0  # Fitness value calculated during evaluation

    def to_dict(self):
        return {
            "genes":[gene.to_dict() for gene in self.genes]
        }

@dataclass
class Population:
    """Represents a group of chromosomes."""
    chromosomes: List[Chromosome] = field(default_factory=list)

@dataclass
class Constraint(ABC):
    """Represents a constraint for evaluating fitness."""
    penalty: float  # Penalty for violating this constraint

    @abstractmethod
    def apply(self, chromosome: Chromosome) -> int:
        """Evaluates the constraint on a chromosome and returns the penalty."""
        raise NotImplementedError

@dataclass
class FitnessEvaluator:
    """Evaluates the fitness of a chromosome based on constraints."""
    constraints: List[Constraint] = None

    def __post__init__(self):
        self.constraints:List[Constraint] = []

    def evaluate(self, chromosome: Chromosome) -> int:
        """Calculates the fitness by summing penalties from all constraints."""
        if len(self.constraints) > 0:

            penalty = sum(constraint.apply(chromosome) for constraint in self.constraints)
        else:
            penalty = 0
        fitness_score = max(0, 100 - penalty) 

        # Example: Fitness = 100 - penalty
        return  fitness_score


class GeneticAlgorithm:
    """Implements the workflow of a genetic algorithm."""

    def __init__(self,data_pool,gene_generator:Callable, chromosome_length:int, population_size: int,  fitness_evaluator: FitnessEvaluator):
        # print("Genetic algorithm initialized !")
        self.data_pool = data_pool
        self.chromo_number = 1
        self.gene_generator = gene_generator
        self.chromosome_length = chromosome_length
        self.population = Population([self.create_chromosome(gene_generator) for _ in range(population_size)])
        self.fitness_evaluator = fitness_evaluator


    def create_chromosome(self, gene_generator: Callable) -> Chromosome:
        """Generates a chromosome with random genes."""
        print(f"Creating chromosome + {self.chromo_number}")
        self.chromo_number+=1
        genes = [gene_generator(self.data_pool) for _ in range(0, self.chromosome_length)]  # Adjust gene count as needed
        return Chromosome(genes=genes)

    def evaluate_population(self):
        """Evaluates and assigns fitness to all chromosomes in the population."""
        # print("Evaluating population")

        for chromosome in self.population.chromosomes:

            chromosome.fitness = self.fitness_evaluator.evaluate(chromosome)
            # if chromosome.fitness != 100:
                # print(f"CHromsome fitness - {chromosome.fitness}")

    def select_parents(self) -> List[Chromosome]:
        """Selects chromosomes for reproduction using fitness-based selection."""
        # print("Selecting parents")
    
        self.population.chromosomes.sort(key=lambda c: c.fitness, reverse=True)
        return self.population.chromosomes[:2]  # Top two chromosomes as parents

    def crossover(self, parent1: Chromosome, parent2: Chromosome) -> Chromosome:
        """Generates a child chromosome by combining genes from parents."""
        # print("Performing crossover")
        crossover_point = random.randint(0, len(parent1.genes) - 1)
        new_genes = parent1.genes[:crossover_point] + parent2.genes[crossover_point:]
        return Chromosome(genes=new_genes)

    def mutate(self, chromosome: Chromosome, mutation_rate: float, mutator: Callable):
        """Randomly mutates genes in a chromosome based on mutation rate."""
        for gene in chromosome.genes:
            if random.random() < mutation_rate:
                # print(f"Mutating chromosome with mutation rate {mutation_rate}")
                # Define mutation logic here
                gene = mutator(self.data_pool)

    def run(self, generations: int, mutation_rate: float):
        """Runs the genetic algorithm for a specified number of generations."""

        for generation in range(generations):
            # print(f"Starting generation {generation}")
            self.evaluate_population()
            parent1, parent2 = self.select_parents()
            child = self.crossover(parent1, parent2)
            self.mutate(child, mutation_rate, self.gene_generator)
            self.population.chromosomes[-1] = child
            
            # Summary output every 10 generations
            if generation % 5 == 0 or generation == generations - 1:
                best_fitness = max(chromosome.fitness for chromosome in self.population.chromosomes)
                worst_fitness = min(chromosome.fitness for chromosome in self.population.chromosomes)

                print(f"Generation {generation}: Best fitness = {best_fitness}")
                print(f"Generation {generation}: Worst fitness = {worst_fitness}")
                print(f"-"*10+f" Generation - {generation}"+"-"*10)
                fitnesses = [chromosome.fitness for chromosome in self.population.chromosomes]
                print(fitnesses)
                print(f"-"*30)
            if self.population.chromosomes[0].fitness == 100:
                return self.population.chromosomes[0]
        strongest_chromosome = self.select_parents()[0]
        return strongest_chromosome

# Example Constraint
@dataclass
class SameFacultyAtDifferentLectureAtSameTime(Constraint):
    penalty: float   # Penalty weight for constraint violation

    def apply(self, chromosome: Chromosome) -> float:
        total_penalty = 0
        genes = chromosome.genes
        for slot_len in range(len(genes) - 1):
            for next_slot_len in range(slot_len + 1, len(genes)):
                slot = genes[slot_len]
                next_slot = genes[next_slot_len]
                
                # Ensure slots have valid assignments
                if slot.slot_alloted_to is not None and next_slot.slot_alloted_to is not None:
                    if not slot.slot_alloted_to.fixed_slot and not next_slot.slot_alloted_to.fixed_slot:
                        if (slot.slot_alloted_to.faculty_id == next_slot.slot_alloted_to.faculty_id 
                                and slot.working_day_id == next_slot.working_day_id
                                and self.is_overlap(slot, next_slot)):
                            total_penalty+= self.penalty
        return total_penalty

    @staticmethod
    def is_overlap(slot1, slot2) -> bool:
        """Checks if two slots overlap based on start and end times."""
        return not (slot1.end_time <= slot2.start_time or slot1.start_time >= slot2.end_time)

    # def to_dict(self):
    #     """Returns a dictionary representation of the constraint."""
    #     base_dict = super().to_dict() if hasattr(super(), "to_dict") else {}
    #     base_dict.update({
    #         "failed_weightage": self.penalty,
    #     })
    #     return base_dict
    


@dataclass
class NoLectureAtBreak(Constraint):
    penalty :float


    
    def apply(self,chromosome:Chromosome):
        total_penalty = 0
        slots = chromosome.genes
        for i in range(len(slots)):
            slot = slots[i]
            if slot.slot_alloted_to is not None:
                if slot.slot_alloted_to.fixed_slot == True and (slot.start_time != slot.slot_alloted_to.start_time or slot.end_time != slot.slot_alloted_to.end_time):
                    # print(f"SLot start time - {slot.start_time} SLot end time - {slot.end_time} SLote alloted start time - {slot.slot_alloted_to.start_time} SLot alloted to endtime - {slot.slot_alloted_to.end_time}")
                    total_penalty+= self.penalty

        return total_penalty

# Example Gene Generator
# def gene_generator():
#     return Gene(value=random.randint(1, 100))

# Example Usage
# constraints = [SameFacultyAtDifferentLectureAtSameTime(weight=10)]
# fitness_evaluator = FitnessEvaluator(constraints=constraints)
# ga = GeneticAlgorithm(population_size=10, gene_generator=gene_generator, fitness_evaluator=fitness_evaluator)

# ga.run(generations=50, mutation_rate=0.1)
