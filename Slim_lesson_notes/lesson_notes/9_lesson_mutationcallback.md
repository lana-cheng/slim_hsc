mutationEffect() creates overrides default fitness calculations. 
- spatial, temporal, frequency dependent variation
- Epistatic interactions
- Occurs after late phase during fitness calculation, called for every mutation in every individual

Paramters:
- Mutation type (required)
- Optional: subpopulation
- Homozygous 

Effect:
```
mutationEffect(m2, p2) {
if (homozygous)
return 1.0 + mut.selectionCoeff;
else
return 1.0 + mut.selectionCoeff * mut.mutationType.dominanceCoeff;
}
```

Fitness: 1 is neutral.  
Selection coefficient: 0 is neutral

Spatial Variation
```
initialize() {
initializeMutationRate(1e-7);
initializeMutationType("m1", 0.5, "f", 0.0); // neutral
initializeMutationType("m2", 0.5, "f", 0.02);
initializeMutationType("m3", 0.5, "f", 0.02);
initializeGenomicElementType("g1", c(m1,m2,m3), c(1,0.01,0.01));
initializeGenomicElement(g1, 0, 99999);
initializeRecombinationRate(1e-8);
}
1 early() {
sim.addSubpop("p1", 500);
sim.addSubpop("p2", 500);
p1.setMigrationRates(p2, 0.1); // weak migration p2 -> p1
p2.setMigrationRates(p1, 0.5); // strong migration p1 -> p2
}
50000 early() {
catn("m2 fixed: " + sum(sim.substitutions.mutationType == m2));
catn("m3 fixed: " + sum(sim.substitutions.mutationType == m3));
}

mutationEffect(m2, p2) { return 0.98; }
mutationEffect(m3, p1) { return 0.98; }
```

Heterozygosity as a Parameter
- returns 0.98 if homozygous
```
mutationEffect(m2, p2) { return homozygous ? 0.98 else 0.99; }
mutationEffect(m3, p1) { return homozygous ? 0.98 else 0.99; }

```
Frequency Dependent Selection
- Beneficial at low frequencies (near 0), deleterious at high frequency (near 1)
```
initialize() {
initializeMutationRate(1e-7);
initializeMutationType("m1", 0.5, "f", 0.0); // neutral
initializeMutationType("m2", 0.5, "f", 0.1); // balanced
initializeGenomicElementType("g1", c(m1,m2), c(99999,1));
initializeGenomicElement(g1, 0, 99999);
initializeRecombinationRate(1e-8);
}
1 early() { sim.addSubpop("p1", 500); }
100000 early() { sim.simulationFinished(); }

mutationEffect(m2) {
return 1.5 - sim.mutationFrequencies(p1, mut);
}
```
Epistasis
- Genes that affect the function of one another. 
- Ex: Two loci: 1 and 2. When loc 2 is GG, AA<AC<CC in terms of expression of Gene x. When loc 2 is GT, AA, AC, CC have same level of expression of gene X. 




