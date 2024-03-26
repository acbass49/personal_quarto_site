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
y = sequels.groupby("Year").agg('count')['Title'].to_list()
x = sequels.groupby("Year").agg('count')['Title'].index.to_list()

sns.lineplot(x=x, y=y)
plt.title("Sequels Spiked Around 2010")
plt.xlabel("Year")
plt.ylabel("Sequel Count")
plt.annotate(
    "Source: IMBD/TMBD",
    xy=(0.7, -0.17),
    xycoords="axes fraction",
)
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
