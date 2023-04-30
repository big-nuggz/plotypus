# plotypus
![sample chart](https://github.com/big-nuggz/plotypus/blob/main/plot.png)

simple charting module that utilized numpy and opencv woop woop

# installation
navigate to your project directory and do
```
git clone https://github.com/big-nuggz/plotypus.git
```
you need numpy and opencv so if you don't have them do
```
pip install numpy opencv-python
```

# usage
```python
# import it
from plotypus import Fig

# create plot area
plt = Fig()

# generate some kind of data
import numpy as np

increment = 0.001
x = np.arange(-np.pi, np.pi + increment, increment)
y = np.sin(x)

# plot
plt.plot(x, y)

# show and save
plt.show()
plt.save('./fig.png')
```
for more stuff look inside the plotypus.py, it has more in-depth sample program in there

# other nfo
butts
