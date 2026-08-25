## Non WF Models

**Setup**
- Declare model as Non Wf
```
initializeSLiMModelType("nonWF");
```
- convertToSubstitution defaults to F
- Need reproduction() callback 
  - Generates offspring for one focal individual
- No inherent population size constraint, need to impose regulation
  - Population size is regulated by mortality which depends on fitness
  - Survivial probability is capped at 100%, so additional beneficial mutations resulting in fitness of 110% won't produce a difference as all individuals survive anyways

**Example**

Initializing
- Only set mutations that are fixed and neutral to substitutions
```
initialize() {
initializeSLiMModelType("nonWF");
defineConstant("K", 500); // carrying capacity

// neutral mutations, which are allowed to fix
initializeMutationType("m1", 0.5, "f", 0.0);
m1.convertToSubstitution = T;

initializeGenomicElementType("g1", m1, 1.0);
initializeGenomicElement(g1, 0, 99999);
initializeMutationRate(1e-7);
initializeRecombinationRate(1e-8);
}

// create an initial population of 10 individuals
1 early() {
sim.addSubpop("p1", 10);
}
```

Reproduction
- reproduction() is called once for every individual. Pseudo paramters:
  - individual: focal individual
  - subpop: focal individual's subpopulation
- addCrossed(): Biparental sexual reproduction
```
// each individual reproduces itself once
reproduction() {
subpop.addCrossed(individual, subpop.sampleIndividuals(1));
}
```

**Population Regulation**
- p1.fitnessScaling: applies scaling factor to all individuals in the p1 subpopulation
- Once the population is greater than 500, fitness scaling is less than 1, and the population fluctuates around 500
```
// provide density-dependent selection
early() {
p1.fitnessScaling = K / p1.individualCount;
}
```

**Age Structure**
- Overlapping generations are allowed. 

Tracking age structure:
```
late() {
inds = p1.individuals;
cat(sim.cycle + ": " + size(inds));
catn(" (" + max(inds.age) + ", " + mean(inds.age) + ")");
}
```

Eidos console:
```
sort(p1.individuals.age)

#lists number of individuals at age 0, 1, 2, ...
tabulate(p1.individuals.age)
```

**Age Dependent Mortality**

Method 1
- Kills individuals older than 2
- use sum(inds.fitnessScaling) because it only counts individuals that survive whereas p1.individualCount counts all individuals including those marked for death
```
early() {
inds = p1.individuals;
inds.fitnessScaling = ifelse(inds.age <= 2, 1.0, 0.0);
p1.fitnessScaling = K / sum(inds.fitnessScaling);
}
```

Method 2:
- sim.killIndividuals() immediately removes those individuals from the subpopulation and overrides all other fitness effects
```
early() {
sim.killIndividuals(p1.subsetIndividuals(minAge=3));
p1.fitnessScaling = K / p1.individualCount;
}
```

**Beneficial Mutations**
- Once density dependent population regulation has an effect (fitness below 1), having a beneficial mutation in the population increases the equilibrium population size. 

**Reproduction**

Method 1:
- individual based where reproduction() is called once for each individual in a built-in for loop
```
reproduction() {
subpop.addCrossed(individual, p1.sampleIndividuals(1));
}
```

Method 2:
- reproduction() is called once and uses an eidos for loop 
- Need to deactivate the script block to prevent reproduction() from being called again within that tick by the built-in for loop
```
reproduction() {
for (ind in p1.individuals)
p1.addCrossed(ind, p1.sampleIndividuals(1));
self.active = 0;
}
```
