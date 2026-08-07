//python3 treeseq.py

import tskit, pyslim, msprime

ts = tskit.load("hsc.trees")

# Ne is initialpop
recap = pyslim.recapitate(ts, 
    ancestral_Ne=100, 
    recombination_rate=0)

recap_simplified = recap.simplify()

tree = recap_simplified.first()
newick = tree.newick()

with open("hsc.nwk", "w") as f:
    f.write(newick)