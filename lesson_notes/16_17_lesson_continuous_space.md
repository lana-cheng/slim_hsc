## Continuous Space

Example: Setup, reprising boundary condition
- Initialize to 2D with x and y coordinates
- use runif to randomize initial positions in [0,1] grid
- modifyChild: position of child is calculated by position of parent plus some deviation drawn from rnorm. 
  - Reprising boundary condition: do {} executes as long as while{} remains true. In this case, the child's position is drawn until it is within boundaries. The function returns T to accept the child into the subpopulation. 
```
initialize() {
initializeSLiMOptions(dimensionality="xy");

initializeMutationRate(1e-7);
initializeMutationType("m1", 0.5, "f", 0.0);
initializeGenomicElementType("g1", m1, 1.0);
initializeGenomicElement(g1, 0, 99999);
initializeRecombinationRate(1e-8);
}
1 late() {
sim.addSubpop("p1", 500);

// initial positions are random in ([0,1], [0,1])
p1.individuals.x = runif(p1.individualCount);
p1.individuals.y = runif(p1.individualCount);
}

modifyChild() {
// draw a child position near the first parent, within bounds
do child.x = parent1.x + rnorm(1, 0, 0.02);
while ((child.x < 0.0) | (child.x > 1.0));

do child.y = parent1.y + rnorm(1, 0, 0.02);
while ((child.y < 0.0) | (child.y > 1.0));
return T;
}

2000 late() { sim.outputFixedMutations(); }
```

Example: Position based on parents 1 and 2
```
modifyChild() {
child.x = (parent1.x + parent2.x) / 2
}
```

**Initial Position**
Uniform
- individualCount returns 500, then pointUniform returns a vector of length 1000 with alternating x and y coordinates for each individual. setSpatialPosition assigns x and y coordinate to the corresponding individuals
- pointUniform works for any boundary to generate uniformly distributed points whereas runif only works for [0,1]. 
  - Set boundary with setSpatialBounds() method of subpopulation. 
```
p1.individuals.x = runif(p1.individualCount);
p1.individuals.y = runif(p1.individualCount);

#Better
p1.individuals.setSpatialPosition(p1.pointUniform(p1.individualCount));
```

Circle
- p is vector of length 2
```
for (ind in p1.individuals) {
do {
p = p1.pointUniform(1);
d = sqrt(sum((p - 0.5)^2));
} while (d > 0.3);
ind.setSpatialPosition(p);
}
```

Square
- d is the distance of the farthest point from the center of [0,1]. If the farthest point is greater than 0.3, meaning it is outside the boundary for initial positions, then the point will be re-generated until it meets the condition. 
```
#for initial positions [0.2, 0.8]
d = max(abs(p - 0.5));
```

**Boundary Conditions**
Reprising boundary check that works for any bounds
- modifyChild() in first example only works for [0,1]
- pointInBounds checks if the position is within bounds
- Not biased towards or away from bounds
```
modifyChild() {
// Reprising boundary conditions
do pos = parent1.spatialPosition + rnorm(2, 0, 0.02);
while (!p1.pointInBounds(pos));
child.setSpatialPosition(pos);
return T;
}
```

Stopping boundary conditions
- If a proposed coordinate is outside of bounds, it is forced within bounds and ends up on the "walls" of the graph. 
- Biased towards the edges
```
modifyChild() {
// Stopping boundary conditions
pos = parent1.spatialPosition + rnorm(2, 0, 0.1);
child.setSpatialPosition(p1.pointStopped(pos));
return T;
}
```

Absorbing boundary condition
- If a child is outside the boundary, it is rejected. Biased away from edges
```
modifyChild() {
// Absorbing boundary conditions
pos = parent1.spatialPosition + rnorm(2, 0, 0.1);
if (!p1.pointInBounds(pos))
return F;
child.setSpatialPosition(pos);
return T;
}
```

**Dispersal**
- Easier to use p1.deviatePositions() than randomizing position with rnorm
Example
- NULL: deviate all individuals in p1. Can also pass a vector of individuals
- "reprising": type of boundary condition. Choices; "none", "periodic", "reflecting", "stopping", "reprising", "absorbing"
- INF: maximum dispersal distance. INF is infinity. 
- "n", 0.1: distribution/type of dispersal kernel. We implement a normal distribution in this case with width/SD 0.1. 
```
2: late() {
p1.deviatePositions(NULL, "reprising", INF, "n", 0.1);
}
```
Process of executing deviatePositions:

(1) get the positions of all of the new juveniles (since this is a WF model, the parents are already gone),

(2) draw deviations from those initial positions (which were inherited from the first parents), from a normal dispersal kernel with the requested width, 

(3) re-draw positions as needed until they are all within bounds (reprising boundaries)

(4) set the final positions back into the individuals. (Note
that in a nonWF model with overlapping generations, you could deviate the positions of only the new offspring by starting with offspring = p1.subsetIndividuals(maxAge=0) to select the new offspring, and then calling deviatePositions() with offspring to move just those individuals.)

**Interactions**
Setting up interaction
- First line: 
  - 1: integer or string id
  - "xy": dimension
  - reciprodcal: the interaction strength from individual A to individual B is the same as from B to A. 
    - A non reciprocal example: a model of trees, for example – small trees would exert very little competitive influence upon large trees, whereas large trees would exert a strong competitive
influence upon small trees.
  - maxDistance: only individuals within a distance of 0.6 will interact with the focal individual
- Second line: Interaction function with strength of interaction as a function of distance
  - "n": normal/gaussian function. Following parameters depend on the function type. 
  - 1.5: function scales to have a maximum of 1.5
  - 0.2: width/SD of normal function
  - Returns "probability" which is treated as interaction strength
```
// Set up an interaction for spatial competition
initializeInteractionType(1, "xy", reciprocal=T, maxDistance=0.6);
i1.setInteractionFunction("n", 1.5, 0.2);
```

Evaluation and queries
- evaluate() takes a snapshot of the spatial position of every individual in p1
- i1.totalOfNeighborStrengths is a query which sums all the interaction strength exerted on the focal individual by neighbors within maxDistance
- totalStrengths/inds.size() gives the mean interaction strength which is then used to calculate a fitness value used for fitness scaling
- Individuals at edges have higher fitness because neighbors are usually farther away which means a lower interaction strength. 
```
1: late() {
i1.evaluate(sim.subpopulations);

inds = p1.individuals;
totalStrengths = i1.totalOfNeighborStrengths(inds);
inds.fitnessScaling = 1.1 - totalStrengths / inds.size();
}
```

**Spatial Mate Choice**
- No interaction function needed because matechoice is only based on distance
- nearestNeighbors(individual, 3): query that finds the 3 nearest neighbor of the focal individual
- if size(neighbors) is not 0, sample 1 of the 3 neighbors and return that neighbor. Otherwise, return float(0) meaning no mate was found and a new first parent will be drawn from the population. 
```
// Set up an interaction for mate choice
initializeInteractionType(2, "xy", reciprocal=T, maxDistance=0.1);

1: mateChoice() {
neighbors = i2.nearestNeighbors(individual, 3);
return (size(neighbors) ? sample(neighbors, 1) else float(0));
}
```

**Local Density Dependence**

In WF models, after an extinction event occurs where individuals living in a region are killed, the population in the unaffected areas increase because it needs to maintain a set population size. This model isn't realistic. 

In Non WF models, local density is maintained after an extinction event because there is no set population. 

Modeling an extinction event:
```
initializeInteractionType(1, "xy", reciprocal=T, maxDistance=0.3);
i1.setInteractionFunction("n", 1.0, 0.1);

// occasional natural disasters, early()
i1.evaluate(p1);
inds = sim.subpopulations.individuals;

if (runif(1) < 0.1) {
epicenter = p1.pointUniform();
d = i1.distanceFromPoint(epicenter, inds);
affected = inds[d < 0.3];
affected.color = "cornflowerblue";

affected.fitnessScaling = 0.0;
}
```

Correcting for edge effects by calculating density based on available area:
- localPopulationDensity internally performs two functions:
  1. counts the total of neighbor strengths weighted by how close they are to the focal individual based on i1 which uses the gaussian function. 
  2. Divides by the available area. ie. use area of a semicircle instead of a full circle for individuals on the edge. 
```
#ealy()
density = i1.localPopulationDensity(inds);
inds.fitnessScaling = K / density;
```

**Periodic Boundaries**

Continuous and uniform space with no edges. 

Correcting for edge effects by removing edges:
```
initializeSLiMOptions(dimensionality="xy", periodicity="xy");

p1.deviatePositions(offspring, "periodic", INF, "n", 0.02);
```

**Spatial Maps**

Generates a spatial map based on a matrix of values. Can use interpolation (smooth value transitions with default bilinear or cubic) or no interpolation (blocks, although we can provide a larger matrix for higher resolution). 

Varying local density bassed on map values:
- mapValues starts as a 10 by 10 matrix of values generated from runif. We take the sqrt of those values to bias towards 1 (higher local density)
- To make the map periodic, we take the left edge map values with mapValues[,0] and add that column of values to the right with cbind(). We also take the map values of the first row and add it to the last. The matrix is now 11 by 11. 
- defineSpatialMap creates a spacial map with name "h"
- Finally, mapValue() retrieves the map value of an individual given their spatial position. The carrying density is scaled by that constant, and the fitnessScaling value is calculated based on the local carrying density. 
```
sim.addSubpop("p1", 500);
p1.individuals.setSpatialPosition(p1.pointUniform(500));

mapValues = matrix(sqrt(runif(100, 0, 1)), nrow=10);

mapValues = cbind(mapValues, mapValues[,0]);
mapValues = rbind(mapValues, mapValues[0,]);

map = p1.defineSpatialMap("h", "xy", mapValues, interpolate=T,
valueRange=c(0.0, 1.0), colors=c("black", "white"));
defineConstant("MAP", map);

K_local = K * MAP.mapValue(inds.spatialPosition);
inds.fitnessScaling = K_local / competition;
```

Using cubic interpolation:
- rescale() scales all the values back to the range [0,1]
```
MAP.interpolate(5, "cubic");
MAP.rescale();
```



