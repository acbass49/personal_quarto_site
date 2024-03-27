# type: ignore
# flake8: noqa
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# | include: false
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#import my data
data = pd.read_csv("./cleaned_data.csv")
#
#
#
#
#
# | echo: false
# filter to sequels only
sequels = data.query("sequel_num >= 2")

# Scatter plot X: Time, Y: Count
# filter to sequels only
sequels = data.query("sequel_num >= 2")

# Scatter plot X: Time, Y: Count
y = sequels.groupby("Year").agg('count')['Title'].to_list()
x = sequels.groupby("Year").agg('count')['Title'].index.to_list()

sequels = pd.DataFrame({"Num_sequels":y,"Year":x})
sequels = sequels.merge(to_join, on="Year", how="left")
y2 = sequels["Movie_num"]

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Year')
ax1.set_ylabel('Sequel Count', color=color)
ax1.plot(x, y, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('Movie Count', color=color)  # we already handled the x-label with ax1
ax2.plot(x, y2, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.annotate(
    "Source: IMBD/TMBD",
    xy=(0.7, -0.17),
    xycoords="axes fraction",
)

plt.title("Sequels Spiked Around 2010")
plt.show()
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
