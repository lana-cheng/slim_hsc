All values are vectors. Operations are vectorized

Methods beginning with "-" are called for each entry in the vector.  

Methods beginning with "+" are called once and uses all the entries as inputs. 

c() creates a vector by concatenation

```
c(2:5, 7)=2 3 4 5 7
```

defineConstant("name", value/vector) defines a constant globally. 

Function signatures:
- (return type)functionName(paramters)
- $ indicates required value
- [] are optional parameters
- numeric means integer or float
- void means not return value
- "*" means any type 
- "+" means non-object type
- lif means logic, integer float

Create vector of all mutations
```
muts=sim.mutations
size(muts)
873
```
Prints information for mutation in first index
```
muts[0].str()
```
Creates vector of mutation positions(property of mutation). 
```
positions=muts.position
size(positions)
```
Prints all positions
```
positions
```
all() is T if all entries return T, any() is T if any entry returns T
```
small=positions<10000
> all(small)
F
> any(small)
T
```
sum() returns number of T. T=1, F=0. 
```
> sum(small)
81
> mean(small)
0.0927835
>mean(sim.mutations.position<10000)
0.0927835
```
x[] vector of T/F as input returns a vector with only entries that are T
```
x = 1:10
> x[c(T, F, T, T, F, F, F, T, F, T)]
1 3 4 8 10
```
Logical operators: & is and, | is or
```
x=1:10
x[c(T, F, T, T, F, F, F, T, F, T) & (x % 2 == 0)]
4 8 10
```
Draws random sample, sets beneficial selection coefficient for all individuals in the sample
```
s=sample(sim.mutations,20)
> s.setSelectionCoeff(0.05)
```
Performs functions above at tick 5000
```
5000 late() {
s = sample(sim.mutations, 20);
s.setSelectionCoeff(0.05);
}
```