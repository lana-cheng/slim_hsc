Slimgui output outline:
tick 58000, samples from population p1 with size 216. 
3-index of mutation within output
20818-unique identifier for mutation
m1-mutation type
1862-base position where mutation is located
0-selection coeff
0.5-dominance coef
p1-which population the mutaiton originated from
56030-which generation the mutation originated
4-number of sampled haplosomes that contained the mutation
```
#OUT: 58000 58000 SS p1 216
Mutations:
3 20818 m1 1862 0 0.5 p1 56030 4
```
Haplosome output outline:
-population name, index of individual containing mutation, mutation index (referenced in mutation section above)
```
Haplosomes:
p1:i840 0
```
Gravel model of human evolution:
```
// set up a simple neutral simulation
initialize() {
initializeMutationRate(2.36e-8);
initializeMutationType("m1", 0.5, "f", 0.0);
initializeGenomicElementType("g1", m1, 1.0);
initializeGenomicElement(g1, 0, 10000);
initializeRecombinationRate(1e-8);
}

// Create the ancestral African population
1 early() { sim.addSubpop("p1", 731); }
// Expand the African population to 14474
// This occurs 148000 years (5920 generations) ago
52080 early() { p1.setSubpopulationSize(1447); }
// Split non-Africans from Africans and set up migration between them
// This occurs 51000 years (2040 generations) ago
55960 early() {
sim.addSubpopSplit("p2", 186, p1);
p1.setMigrationRates(p2, 15e-5);
p2.setMigrationRates(p1, 15e-5);
}
// Split p2 into European and East Asian subpopulations
// This occurs 23000 years (920 generations) ago
57080 early() {
sim.addSubpopSplit("p3", 55, p2);
p2.setSubpopulationSize(103); // reduce European size
// Set migration rates for the rest of the simulation
p1.setMigrationRates(c(p2, p3), c(2.5e-5, 0.78e-5));
p2.setMigrationRates(c(p1, p3), c(2.5e-5, 3.11e-5));
p3.setMigrationRates(c(p1, p2), c(0.78e-5, 3.11e-5));
}
// Set up exponential growth in Europe and East Asia
// Where N(0) is the base subpopulation size and t = gen - 57080:
// N(Europe) should be int(round(N(0) * e^(0.0038*t)))
// N(East Asia) should be int(round(N(0) * e^(0.0048*t)))
57080:58000 early() {
t = community.tick - 57080;
p2_size = round(103 * exp(0.0038 * t));
p3_size = round(55 * exp(0.0048 * t));
p2.setSubpopulationSize(asInteger(p2_size));
p3.setSubpopulationSize(asInteger(p3_size));
}

58000 late(){
p1.outputSample(216); // YRI phase 3 sample of size 108
p2.outputSample(198); // CEU phase 3 sample of size 99
p3.outputSample(206); // CHB phase 3 sample of size 103
}
```