## Multispecies Model

**Initializing**
```
species all initialize() {
    defineConstant("C", 100);
    initializeSliMModelType("nonWF")
}
```

species specific setup:
```
species caterpillar initialize() {
    initializeSpecies(avatar="🐛"...)
    initializeMutationType, genomic element, etc. 
}

species mosquito initialize (){
    ...
}
```

**Events**

use ticks all for all species
```
ticks all 1 early() {
    ...
}
```

**Reproduction and Callbacks**

Reproduction
```
species caterpillar reproduction() {...}

species mosquito reproduction(){...}
```

species *name* needs to be added before a callback 

**Ex: NonWF multispecies model**

NonWF model with two non-interacting species undergoing density-dependent selection. Population vs. tick graph shows mouse and fox population hovering about their carrying capacities. 
```
species all initialize() {
defineConstant("K_mouse", 5000);
defineConstant("K_fox", 500);
defineConstant("F_mouse", 10);
defineConstant("F_fox", 2);

initializeSLiMModelType("nonWF");
}

species mouse initialize() {
initializeSpecies(avatar="🐭", color="black");
}

species fox initialize() {
initializeSpecies(avatar="🦊", color="orange");
}

#Sampling excludes the focal individual aka parent 1. 

species mouse reproduction()
{
mate = subpop.sampleIndividuals(1, exclude=individual);
if (size(mate))
subpop.addCrossed(individual, mate, count=rpois(1, F_mouse));
}

species fox reproduction()
{
mate = subpop.sampleIndividuals(1, exclude=individual);
if (size(mate)) {
subpop.addCrossed(individual, mate, count=rpois(1, F_fox));
}
}

ticks all 1 early() {
mouse.addSubpop("p1", K_mouse);
fox.addSubpop("p2", K_fox);
}

#Could combine density dependent selection into ticks all event

ticks mouse early() {
p1.fitnessScaling = K_mouse / p1.individualCount;
}

ticks fox early() {
p2.fitnessScaling = K_fox / p2.individualCount;
}

ticks all 500 late() {
}
```

**Ex: Extending model above for predation**
```
#Add to initialize
defineConstant("HUNTS", 10);

ticks fox late() {
// hunting: use tag values to track what happens
// for mice: 0 means alive, 1 means killed
// for foxes: the tag value is the number of mice killed

c(p1, p2).individuals.tag = 0;

// the foxes hunt in randomized order
#Makes sure no ordering bias affects behavior of model

foxes = p2.sampleIndividuals(p2.individualCount);

#Later for hunting, the possibility of a fox making a kill is dependent on the number of mice. The more mice, the more likely a fox will kill one. 

p_kill = min(1.0, p1.individualCount / K_mouse);

for (hunter in foxes)
{
#Use a binomial distribution based on probability p_kill with HUNTS trials to draw a kill count. 

kill_count = rbinom(1, HUNTS, p_kill);

#Sample with replacement for mice to be killed for performance reasons, then use unique to remove duplicates. Although kill counts will be off in that case, it should happen rarely. Use unique(preserveOrder=F) when ordering doesn't matter to improve performance. 

killed = p1.sampleIndividuals(kill_count, replace=T);
killed = unique(killed, preserveOrder=F);

#Select mice that haven't already been killed
killed = killed[killed.tag == 0];

#Update tag values
killed.tag = 1;
hunter.tag = size(killed);
}

#Implement mortality based on tag values

#Get all mice with tag 1 and kill them

all_killed = p1.subsetIndividuals(tag=1);
mouse.killIndividuals(all_killed);

#The probability of survival for foxes is the amount of mice they hunted over their total hunts. Then, use a vectorized call with runif which is more likely to return T is p_fox_survival is low. 

p_fox_survival = foxes.tag / HUNTS;
starved = runif(foxes.size()) > p_fox_survival;
fox.killIndividuals(foxes[starved]);
}
```

Change to reproduction callback
- Scales fox's base fecundity by its fractional hunting success. 
```
species fox reproduction()
{
fecundity = F_fox * (individual.tag / HUNTS);
litterSize = rpois(1, fecundity);

if (litterSize>0) {
mate = subpop.sampleIndividuals(1, exclude=individual);
subpop.addCrossed(individual, mate, count=litterSize);
}
}
```

**Ex: Modeling Genetics**

Mice have a coat color governed by a single nucleotide locus C with incomplete dominance represented as cc=0.0, Cc=0.5, CC=1.0. 

Foxes will have a quantitative trait representing the mouse cost color that a given fox looks for when hunting. Foxes will tend to kill mice that have a coat value similar to the color they look for. 

Mouse genetic setup: Initializes a m1 mutation that represents coat color. Genomic element has only one base, representing locus C. 
```
species mouse initialize() {
initializeSpecies(avatar="🐭", color="black");
initializeMutationType("m1", 0.5, "f", 0.0); // coat-color locus
initializeGenomicElementType("g1", m1, 1.0);
initializeGenomicElement(g1, 0, 0);
initializeMutationRate(0.0);
initializeRecombinationRate(0.0);
}
```

The number of p1.haplosomes is twice K_mouse as each mouse has two haplosomes. 
```
targets = sample(p1.haplosomes, K_mouse);
targets.addNewDrawnMutation(m1, 0);
```

Fox genetic setup: 
```
species fox initialize() {
initializeSpecies(avatar="🦊", color="orange");

#m2 represents QTL loci where the effect size is drawn from a normal distribution. The selection coefficient of a single m2 mutation doesn't matter. 

initializeMutationType("m2", 0.0, "n", 0.0, 0.1); // hunting

m2.convertToSubstitution = F;
m2.mutationStackPolicy = "l";

initializeGenomicElementType("g2", m2, 1.0);
initializeGenomicElement(g2, 0, 99); // length 100

#encodes how m2 mutations arise for each generation

initializeMutationRate(1e-5); // 1e-3 per gamete
initializeRecombinationRate(0.5); // unlinked
}
```

For the initial population, we implement an m2 mutation on both haplosomes for each fox with an effect size of 0.25 (effect size totals to 0.5). Then, to add genetic diversity, we sample a random number of haplosomes and add an m2 mutation in a randomly drawn position.  
```
p2.haplosomes.addNewMutation(m2, 0.25, 0);

for (i in 1:50)
{
target = sample(p2.haplosomes, rdunif(1, 0, K_fox*2));
target.addNewDrawnMutation(m2, rdunif(1, 1, 99));
}
```

Since we are using a QTL model, the mutation effect of each m2 mutation is neutral. 
```
pecies fox mutationEffect(m2) {
return 1.0; // QTLs are neutral
}
```

Model hunting dependent on the similarity between coat value of foxes and mice. 
```
#How important the match is to mouse survival

defineConstant("MATCH_SCALE", 0.5);

// use tagF to hold individual phenotypes
mice = p1.individuals;

#Gives a coat value of 0.0, 0.5, or 1.0

pheno = mice.countOfMutationsOfType(m1) / 2;
mice.tagF = pheno;

#Sums the effect size for each m2 mutation

foxes = p2.individuals;
pheno = foxes.sumOfMutationsOfType(m2);
foxes.tagF = pheno;

for (hunter in foxes)
{
#Same code as previous model. Select mice to be 
killed that haven't already been killed. 

kill_count = rbinom(1, HUNTS, p_kill);
killed = p1.sampleIndividuals(kill_count, replace=T);
killed = unique(killed, preserveOrder=F);
killed = killed[killed.tag == 0];

#If the coat color a fox looks for (hunter.tagF) is close to the coat color of the mice (killed.tagF), the mice has a higher probability of getting killed. A perfectly mismatched mouse has a 50% chance of being killed. The probability is clamped between 0 and 1. 

match = 1.0 - abs(hunter.tagF - killed.tagF) * MATCH_SCALE;
match = pmax(pmin(match, 1.0), 0.0);

#When a match is higher, the mouse is more runif is more likely to generate number smaller than the match, resulting in the mice being killed. 

killed = killed[runif(size(killed)) < match];
killed.tag = 1;
hunter.tag = size(killed);
}
```

Evolutionary dynamics: Mouse will evolve to have rare coat colors, and foxes will evolve to have the coat value of the most common coat color. 