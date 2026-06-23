## mateChoice() callback

- Parent 1 is chosen, then mateChoice picks parent 2
- override default mating
- can return a vector of mating weights, an individual as parent 2, float 0 (no suitable mate), NULL (use default weights)

Optimizing callback by vectorizing calculations:
- In example below, instead of calculating osize every time when mateChoice() is called, calculate osize for each individual and store it in a vector before using mateChoice(), then access the osize property within mateChoice() to avoid doing the calculations every time the function is called.  
- Also useful for mutationEffect()

Not optimized:
```
mateChoice() {
fixedMuts = sum(sim.substitutions.mutationType == m2);
for (attempt in 1:5)
{
mate = sample(p1.individuals, 1, T, weights);
osize = fixedMuts * 2 + mate.countOfMutationsOfType(m2);
if (runif(1) < log(osize + 1) * 0.1 + attempt * 0.1)
return mate;
}
return float(0);
}
```

Optimized:
- osize is a vector
- tagF: assign a float value to an individual
```
1:10001 early() {
fixedMuts = sum(sim.substitutions.mutationType == m2);
inds = p1.individuals;
osize = fixedMuts * 2 + inds.countOfMutationsOfType(m2);
inds.tagF = log(osize + 1) * 0.1;
}

mateChoice() {
for (attempt in 1:5)
{
mate = sample(p1.individuals, 1, T, weights);
if (runif(1) < mate.tagF + attempt * 0.1)
return mate;
}
return float(0);
}
```

Returning vector of mating weights:
- default: pseudo parameter "weights" is vector containing probability of each individual being chosen as a mate, which is proportional to that individual’s relative fitness.
- Overriding with mateChoice():
  - if (sum)... code in early() is for first tick where every individual's tagF value is 0. The active value of every code block is set to 1 (active) at the beginning of every tick. Setting code block s1 to 0 deactivates it, as if the code doesn't exist. 
- Returns vector of weights that slim then uses for choosing parent 2.  

```
1:10001 early() {
fixedMuts = sum(sim.substitutions.mutationType == m2);
inds = p1.individuals;

if (sum(inds.tagF) == 0.0)
s1.active = 0;

osize = fixedMuts * 2 + inds.countOfMutationsOfType(m2);
inds.tagF = log(osize + 1) * 0.1;
}

s1 mateChoice() {
return weights * p1.individuals.tagF;
}
```
