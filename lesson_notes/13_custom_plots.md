## Custom Plots
```
10000 early()
{
#plotting is a slimgui function
if (exists("slimgui"))
{
#collect data
subs = sim.substitutions;
subs = subs[subs.mutationType == m4];
timesToFix = subs.fixationTick - subs.originTick;
coeffs = subs.selectionCoeff;

#if we want to include 0 in the axes, we need to add it to the collected data with c()
plot = slimgui.createPlot("Fixation analysis",
xrange=range(c(0, coeffs)), yrange=range(c(0, timesToFix)),
xlab="Selection coefficient", ylab="Fixation time");

#x axis, y axis, symbol=16 is filled circle
plot.points(coeffs, timesToFix, symbol=16, size=0.6);
}
sim.simulationFinished();
}
```
