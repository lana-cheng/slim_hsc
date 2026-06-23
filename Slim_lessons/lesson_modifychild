## modifyChild()
- used to modify generated offspring
- returns T if offspring is added to desired subpopulation, or F if offspring is not added and new parents are drawn
- Called once for each offspring

**Epistasis:**
- creates three types of mutations with m2 and m3 being advantageous
- 20 haplosomes are drawn for each mutation, and the mutation is added at the specified location.
```
initialize() {
initializeMutationRate(1e-7);
initializeMutationType("m1", 0.5, "f", 0.0);
initializeMutationType("m2", 0.5, "f", 0.5); // mutation A
m2.convertToSubstitution = F;
m2.color = "red";
initializeMutationType("m3", 0.5, "f", 0.5); // mutation B
m3.convertToSubstitution = F;
m3.color = "#20D033";
initializeGenomicElementType("g1", m1, 1.0);
initializeGenomicElement(g1, 0, 99999);
initializeRecombinationRate(1e-8);
}

1 late() {
sim.addSubpop("p1", 500);
sample(p1.haplosomes, 20).addNewDrawnMutation(m2, 10000); // add A
sample(p1.haplosomes, 20).addNewDrawnMutation(m3, 20000); // add B
}
10000 early() { sim.simulationFinished(); }
```
- For each offspring, first check if any of the haplosomes have the mutation type. If both m2 and m3 are present, then the child is rejected. 
- If we change any() to all(), then the function checks if both haplosomes for a child has the mutation. If both haplosomes have both the mutations (homozygous for mutation A and B), then the child is rejected. 
```
modifyChild() {
hasMutA = any(child.haplosomes.countOfMutationsOfType(m2) > 0);
hasMutB = any(child.haplosomes.countOfMutationsOfType(m3) > 0);
if (hasMutA & hasMutB)
return F;
return T;
}
```

**Non-genetic inheritance**
- Can also modify child without rejecting it
- rbinom() returns vector. Parameters:
  - Number of entries in vector/number of runs (each entry is the number of successes)
  - Trials per run
  - Probability of success
```
modifyChild() {
// inherit culture from parents, with some deviation
parentCulture = mean(c(parent1, parent2).tagL0);
childCulture = rbinom(1, 1, 0.01 + 0.98 * parentCulture);
child.tagL0 = (childCulture == 1);
return T;
}
```

**Log File**
- community.createLogFile creates a file (csv here) and returns the object to "log"
  - Parameters: name of file, logInterval=1 means data is logged every tick
  - File is saved on desktop
- log.addTick() creates the first column on the spreadsheet which records the tick number
- log.addCustomColumn adds the second column with the name "fraction" and logs data using mean(p1.individuals.tagL0) every tick
- Graph can be visualized in Slim: ladybug-->file name-->right click graph title-->graph line plot 
```
1 early() {
sim.addSubpop("p1", 1000);

// make a LogFile
log = community.createLogFile("milk_drinkers.csv", logInterval=1);
log.addTick();
log.addCustomColumn("fraction", "mean(p1.individuals.tagL0);");

// start as mostly non-milk-drinkers
p1.individuals.tagL0 = asLogical(rbinom(1000, 1, 0.01));
}
```






