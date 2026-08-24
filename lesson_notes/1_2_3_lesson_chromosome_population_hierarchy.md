Initialize
```
// set up a simple neutral simulation

initialize() {
initializeMutationRate(1e-7);
```

Mutation rate units: per base pair per gamete (New mutations arising during transmission from parent to child, not somatic). 
Pg 101

```
// m1 mutation type: neutral
initializeMutationType("m1", 0.5, "f", 0.0);
```
Paramters: (chosen name, dominance coefficient, distribution of fitness effects, selection coefficient)

Dominance coefficient: How much a mutation expresses itself in a heterozygote (one mutation copy, one wildtype copy). 
•	0: fully recessive, having one copy doesn’t affect anything
•	0.5: Codominant, being heterozygous has half the effect of being homozygous
•	1: Dominant, having one copy has full effect

DFE: Describes distribution of selection coefficient
•	“f”: fixed, every mutation has same selection coefficient
•	Exponential, normal, Gamma
•	Can use negative mean

Selection coefficient: Fitness of mutation
•	S=1: neutral
•	S=negative: deleterious
•	S=positive: beneficial
•	Fitness calculation:
o	Heterozygote: 1+h*s
o	Homozygote: 1+s

Pg 102

```
// g1 genomic element type: uses m1 for all mutations
initializeGenomicElementType("g1", m1, 1.0);
```

Defines a type of genomic region (ie. Centromeres, exons, introns) while specifying mutation types and proportions that occur in this region. 

Paramters: (chosen name, mutation types, proportions)

M1 is type of mutation identified above, 1.0 is proportion

For multiple mutations: 1:2:10 ratio of mutations m1 m2 m3. 
initializeGenomicElementType("g1", c(m1,m2,m3), c(1,2,10));

pg 103

```
// uniform chromosome of length 100 kb with uniform recombination
initializeGenomicElement(g1, 0, 99999);
```

A Genomic element is a specific region of defined by base pair indices and the type of genomic element defined above. 

Parameters: (genomic element type, starting base pair index, ending base pair index)

A genomic element doesn’t need to span a whole chromosome, it can be just a region. 

Example: Setting up chromosome with ten regions of genomic element type “g1” with spacing
```
for (index in 1:10)
initializeGenomicElement(g1, index*1000, index*1000 + 499);
initializeRecombinationRate(1e-8);}
```
pg 104

Pg 105. Can split chromosome into multiple regions each with a different recombination rate (probability of crossing over between two adjacent base pairs)

```
// create a population of 500 individuals
1 early() {
sim.addSubpop("p1", 500);
}
```
Adds a subpopulation at time tick=1. 
Early() defines part of tick cycle event occurs in. 
Parameters: (chosen name, size of added subpopulation)
Sim.addsubpop is a method defined on the object sim, which represents the species being simulated. 
```
//run to tick 10000
10000 late() {
sim.outputFixedMutations();
sim.simulationFinished();
}
```
Chromosome Hierarchy

Chromosome: sequence of genomic elements, each belonging to a genomic element type. 

Population Hierarchy

Community contains species. 

Population=species is managed by species object. Sim is default species object. Only one population per species. 

Subpopulations contain individuals. 

“Class individual” are organisms

Individuals consists of haplosomes: one homologous copy of a chromosome, one X chromosome, one Y chromosome etc. Each haplosome is associated with a chromosome. 

“Class mutation” happens in haplosomes. Haplosomes begin empty at the ancestral state and accumulate mutations (SNP). 

“Class substitution” are mutations that have reached fixation. Relative fitness effect doesn’t matter is a mutation is fixed in a population as every individual has that mutation so no fitness advantage or disadvantage exists. 

Stacking

If one mutation occurs first, and another mutation occurs at the exact same location, then both mutations are kept at that location. 

This model doesn’t make sense when modeling with single nucleotide mutations, but it approximates the behavior of two mutations occurring adjacent to each other as recombination between them is very unlikely. 

Can change setting from stacking to replacement. 
