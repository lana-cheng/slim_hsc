## Recombination  

![recombination](/Users/lanacheng/Documents/McCoy_Lab/Slim_notebook/recombination.png)

Creating random recombination map.  
* rate picks 1000 uniform random samples within range
* sample() picks 999 random end points, sorts them in ascending order, appends position 99999 (last base pair) as endpoints for each recombination rate.   
>rates = runif(1000, 1e-9, 1e-7);  
ends = c(sort(sample(0:99998, 999)), 99999);   
initializeRecombinationRate(rates, ends);

