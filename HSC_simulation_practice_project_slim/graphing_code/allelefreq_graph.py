import matplotlib.pyplot as plt
import pandas as pd
 
f = pd.read_csv("freq2.csv")
 
lower = f["lower"]
upper = f["upper"]
count = f["number"]
 
width = upper - lower
centers = lower + width / 2
 
plt.bar(centers, count, width=width, edgecolor="black", align="center")
plt.xlabel("Allele frequency")
plt.ylabel("Number of mutations")
plt.yscale("log")
plt.grid(True)
plt.show()