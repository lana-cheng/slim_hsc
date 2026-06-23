## Tress

![trees](/Users/lanacheng/Documents/McCoy_Lab/Slim_notebook/Slim_lessons/images/trees.png)

**Slim**

call initializeTreeSeq() and sim.treeSeqOutput("final.trees")

set mutation rate to zero if the only mutation is neutral. 

**Tree Sequence Recording**

1. Slim simulation
2. Simplification: only keep relevant lineages
3. recapitation: simulate ancestral information backwards from slim's founding population to produce a common ancestor
4. Neutral mutation overlay: adds neutral mutations back into the tree sequence based on mutation rate

Workflow:

1. Run a simulation in slim and save a .trees file (Slim)
2. Read .trees with tskit
3. recpaitate with pyslim
4. overlay mutations with msprime
5. write out final tree sequence with .trees file

Python code for steps 2-5. Write code in textedit, then run in terminal
```
#File name: ts_overlay.py

import msprime, tskit
ts = tskit.load("overlay.trees").simplify()
mutated = msprime.sim_mutations(ts, rate=1e-7, random_seed=1, keep=True)
mutated.dump("final_overlaid.trees")
```

Terminal
```
cd ~/Desktop

python3 ts_overlay.py
```

Ex: ts_overlay.py file in desktop

**Tracking Mean Ancestry**

For a population that descended from two initial populations, we can track the mean ancestry of those individuals for locations along a chromosome. 

Ex: admix.py
- In this example, the mutation in position 0.2 came from p1 and 0.8 came from p2, which is why the percentage is at 0% and 100% for those. Other positions are a mix between the two initial populations. 

![admix](/Users/lanacheng/Desktop/admix_trees.png)

**Recapitation**

![recap](/Users/lanacheng/Desktop/recap.png)

**Examining Mutations**

Checking mean selection coefficient: selcoeff.py

