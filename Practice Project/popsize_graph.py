//python3 popsize_graph.py

//normal axis
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

f=pd.read_csv("pop_size_file.csv")
x_data = f.iloc[:, 0]
y_data = f.iloc[:, 1]

plt.plot(x_data, y_data)
plt.xlabel(f.columns[0])
plt.ylabel(f.columns[1])

end = int(x_data.max())
step = 50
plt.xticks(np.arange(0, end + 1, step))

plt.grid(True)
plt.show()

//two graphs, one normal, one semi log on y

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
 
f = pd.read_csv("pop_size_file.csv")
x_data = f.iloc[:, 0]
y_data = f.iloc[:, 1]
 
end = int(x_data.max())
step = 30
 
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
 
# Left: normal linear axes
ax1.plot(x_data, y_data)
ax1.set_xlabel(f.columns[0])
ax1.set_ylabel(f.columns[1])
ax1.set_xticks(np.arange(0, end + 1, step))
ax1.set_title("Linear scale")
ax1.grid(True)
 
# Right: semi-log (y-axis log scale)
ax2.semilogy(x_data, y_data)
ax2.set_xlabel(f.columns[0])
ax2.set_ylabel(f.columns[1])
ax2.set_xticks(np.arange(0, end + 1, step))
ax2.set_title("Semi-log (log y-axis)")
ax2.grid(True)
 
plt.tight_layout()
plt.show()
