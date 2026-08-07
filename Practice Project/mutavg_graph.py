//python3 mutavg_graph.py

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

f = pd.read_csv("mut_avg_file.csv")
x_data = f.iloc[:, 0]
y_data = f.iloc[:, 2]

end = int(x_data.max())
step = 30

plt.plot(x_data, y_data)
plt.xlabel(f.columns[0])
plt.ylabel(f.columns[2])

plt.xticks(np.arange(0, end + 1, step))

plt.grid(True)
plt.show()