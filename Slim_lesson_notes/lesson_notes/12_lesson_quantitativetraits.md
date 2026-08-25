## Quantitative Trait

Quantitative Traits
- governed by multiple QTLs instead of a single locus
- Produces continuous variation (ie height)
- Selection coefficient is re-purposed to represent the value of effect size
- Since no selection coefficient is needed, DFE is re-purposed as the distribution of effect sizes
- Selection coefficients are set to 1 (neutral) for each mutation with mutationEffect() {return 1.0;} as mutations only have an effect when considered with other mutations and not by themselves
- Use convertToSubstitution=F

Phenotype
- Calculated from effect size of QTL mutations
- Simple model: additive effects which is the sum of all the effects. 
  - use sumOfMutationsOfType() which normally adds the selection coefficient of each mutation but is re-purposed as the sum of QTL effects
  - Can also model non additive effects, environmental noise etc. 
- Produces a phenotypic trait value, can be stored with tagF

Fitness
- Fitness as a function of the phenotypic trait value
- Apply fitnessScaling

![selection_types](/Users/lanacheng/Documents/McCoy_Lab/Slim_notebook/Slim_lessons/images/selection_types.png) 

Stabilizing Selection
- Good to use dnorm() for gaussian fitness function

**QTL-based model**

Initializing
- the effect size/selection coefficient of m2 is drawn from a normal distribution with substitutions=F
- genomic element g2, which is in the middle section, contains m1 neutral mutations with fitness=0 and m2 mutations
- mutationEffect() is used to return a selection coefficient value of 1 for each m2 mutation as they have no intrinsic fitness effect
- dumpFrequencies is a user defined function
```
initialize() {
initializeMutationRate(1e-7);
initializeMutationType("m1", 0.5, "f", 0.0); // neutral
initializeMutationType("m2", 0.5, "n", 0.0, 0.5); // QTLs
m2.convertToSubstitution = F;

initializeGenomicElementType("g1", m1, 1);
initializeGenomicElementType("g2", c(m1,m2), c(0.9,0.1));
initializeGenomicElement(g1, 0, 20000);
initializeGenomicElement(g2, 20001, 30000);
initializeGenomicElement(g1, 30001, 99999);

initializeRecombinationRate(1e-8);
}

mutationEffect(m2) { return 1.0; }

1 early() { sim.addSubpop("p1", 500); }

20000 late() {
catn("\nDID NOT REACH OPTIMUM");
dumpFrequencies(sim.mutationsOfType(m2));
}
```

dumpFrequencies
- Function returns no value (void), intakes vector where each entry is class Mutation
- For each mutation, we store the frequency and effect size/selection coefficient
- Here, we only need frequencies and effect sizes for m2 mutations
- Returns matrix using cbind()
```
function (void)dumpFrequencies(object<Mutation> muts) {
if (muts.size())
{
#NULL means calculate frequency from entire population
freqs = sim.mutationFrequencies(NULL, muts);
coeffs = muts.selectionCoeff;
catn();
print(cbind(freqs, coeffs));
}
}
```
- Output:
```
        [,0]    [,1]
[0,] 0.003      0.877338
[1,] 1          -0.541942
[2,] 1          0.270283
[3,] 0.047      0.38477
[4,] 0.151      -0.234286
```

Phenotypic Trait Values and fitness effect
- Mapping of phenotype to fitness
- 1: means run from tick 1 to end
- phenotypes is vector where each entry is the phenotypic trait value for an individual
  - sumOfMutationsOfType(m2) searches the individual's haplosomes, finds m2 mutations, and adds the effect size/selection coefficient of those mutations
- fitness effect can be calculated based on four parameters:
  - dnorm() returns a value based on a normal distribution with mean 10 and SD 5 for each phenotypic trait value as input
  - Scaled by 10 for selection strength
  - Baseline of 1 
- The fitness effect is stored in the fitnessScaling property of individuals. The fitness value computed for the individual will be multiplied by this value
```
1: late() {
inds = sim.subpopulations.individuals;
phenotypes = inds.sumOfMutationsOfType(m2);
inds.fitnessScaling = 1.0 + dnorm(phenotypes, 10.0, 5.0) * 10.0;
}
```

Tracking Mean Phenotype
- First calculates the mean phenotypic value of all individuals
- If mean phenotype is close to the optimum within a given tolerance, the simulation finishes and prints a summary of the QTLs. 
```
// Output and check for termination
mean_phenotype = mean(phenotypes);
if (abs(mean_phenotype - 10.0) < 0.1)
{
catn("\n" + sim.cycle + ": REACHED OPTIMUM");
catn("Final phenotype == " + mean_phenotype);
dumpFrequencies(sim.mutationsOfType(m2));
sim.simulationFinished();
}
else if (sim.cycle % 100 == 0)
{
catn(sim.cycle + ": Mean phenotype == " + mean_phenotype);
}
```

**Modifications**
- Can have different optimum values based on tick number
- Can add environmental variance by creating a variable (ie "noise"). For each individual, a noise value is assigned from a distribution. Phenotypes is then the sum of noise and QTL effect sizes
```
#population of size 500
inds = sim.subpopulations.individuals;
additive = inds.sumOfMutationsOfType(m2);
noise=rnorm(500, 0.0, 1.0);
phenotypes = additive+noise;
```
- Heritability: measure of the degree to which the phenotypes of offspring are predictable from the phenotypes of their parents
```
1: late() {
inds = sim.subpopulations.individuals;
additive = inds.sumOfMutationsOfType(m2);
noise=rnorm(500, 0.0, 0.1);
phenotypes = additive+noise;
heritability = var(additive)/var(phenotypes);}
```
- Phenotypic plasticity: An organism that exhibits phenotypic plasticity is able to adapt, to a limited extent, to the environment in which it finds itself
- Can use modifyChild() to 1. calculate phenotypic trait value of child 2. compare it to the environment 3. assign a plastic effect value based on the environment 4. store value with tagF