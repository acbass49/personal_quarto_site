# Title : sequel_analysis
# Author : Alex Bass
# Date : 30 March 2024

#loading some libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm
import scipy.stats as stats
from statsmodels.stats.outliers_influence import variance_inflation_factor

#import my data
data = pd.read_excel("./cleaned_data_w_rev.xlsx")

#create dummy variables for popular production companies
data.loc[data.production_company.isna(),"production_company"] = ""
data['warner_bros'] = data.production_company.str.contains("Warner Bros.").astype("int")
data['fox'] = data.production_company.str.contains("20th Century Fox").astype("int")
data['mgm'] = data.production_company.str.contains("Metro-Goldwyn-Mayer").astype("int")
data['universal'] = data.production_company.str.contains("Universal Pictures").astype("int")
data['disney'] = data.production_company.str.contains("Disney").astype("int")
data['paramount'] = data.production_company.str.contains("Paramount").astype("int")
data['marvel'] = data.production_company.str.contains("Marvel").astype("int")

chart_later = data[['warner_bros', 'fox', 'mgm', 'universal', 'disney', 'paramount']].sum(axis=0).sort_values(ascending=False)
data['prod_i'] = np.where(data['warner_bros'] == 1, 'Warner Bros',
  np.where(data['fox'] == 1, 'Fox',
    np.where(data['universal'] == 1,'Universal',
      np.where(data['disney'] == 1, "Disney", "Other"))))

############
# Figure 1 #
############

# I join in data; link in post
to_join = pd.read_csv("./to_join.csv")
sequels = data.query("sequel_num >= 2")

# Scatter plot X: Time, Y: Count
y = sequels.groupby("Year").agg('count')['Title'].to_list()
x = sequels.groupby("Year").agg('count')['Title'].index.to_list()

sequels = pd.DataFrame({"Num_sequels":y,"Year":x})
sequels = sequels.merge(to_join, on="Year", how="left")
y2 = sequels["Movie_num"]

fig, ax1 = plt.subplots()

color = '#342bbb'
ax1.set_xlabel('Year')
ax1.set_ylabel('Sequel Count', color=color)
ax1.plot(x, y, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = '#BB3E18'
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
plt.savefig("./fig1.png")

############
# Interactive Plotly Figure #
############

fig2_data = data.query("sequel_num in [1,2]") \
  .assign(log_of_revenue = lambda x:np.log(x.adjusted_rev+1))

def get_rev_1(data_part):
  tmp = data_part.sort_values("sequel_num").reset_index(drop=True)
  return tmp.loc[0,"adjusted_rev"]

def get_rev_2(data_part):
  tmp = data_part.sort_values("sequel_num").reset_index(drop=True)
  return tmp.loc[1,"adjusted_rev"]

def get_title(data_part):
  tmp = data_part.sort_values("sequel_num").reset_index(drop=True)
  return tmp.loc[0,"Title"] + " Series"

def get_prod(data_part):
  tmp = data_part.sort_values("sequel_num").reset_index(drop=True)
  return tmp.loc[0,"prod_i"]

x = data.query("sequel_num in [1,2]") \
  .groupby("sequel_group") \
  .apply(get_rev_1)

y = data.query("sequel_num in [1,2]") \
  .groupby("sequel_group") \
  .apply(get_rev_2)

title = data.query("sequel_num in [1,2]") \
  .groupby("sequel_group") \
  .apply(get_title)

prod = data.query("sequel_num in [1,2]") \
  .groupby("sequel_group") \
  .apply(get_prod)

plot_data = pd.DataFrame(
  {
    'original_revenue':x,
    'sequel_revenue':y,
    'series':title,
    'production_company':prod
  }
)

fig = px.scatter(plot_data, x="original_revenue", y="sequel_revenue", color="production_company", hover_name="series", hover_data=[ "original_revenue", 'sequel_revenue','production_company'])
fig.add_trace(go.Scatter(x=[0, 5_000_000_000], y=[0, 5_000_000_000], mode='lines', name='Profit Comparison Line'))
fig.update_traces(line_color='black')
fig.update_layout(
  title='Original Film VS. First Sequel',
  xaxis_title="First Film's Revenue (infl. adj.)",
  yaxis_title="Second Film's Revenue (infl. adj.)",
  yaxis_range=[0, 5_000_000_000],
  xaxis_range=[0, 5_000_000_000]
)
fig.add_annotation(
  text="Source: IMDB/TMDB",
  xref="paper", yref="paper",
  x=1.5, y=-0.2, showarrow=False)
fig.update_yaxes(nticks=5)
fig.show()

############
# Figure 2 #
############

def seq_diff(data_part):
  tmp = data_part.sort_values("sequel_num").reset_index(drop=True)
  val = tmp.loc[0,"adjusted_rev"] - tmp.loc[1,"adjusted_rev"]
  within_5 = np.multiply(np.divide(tmp.loc[0,"adjusted_rev"],100),5)
  if val > within_5:
    r_val = "original made more"
  elif val < -within_5:
    r_val = "sequel made more"
  else:
    r_val = "about the same"
  return r_val

fig3_data = data.query("sequel_num in [1,2]") \
  .groupby("sequel_group") \
  .apply(seq_diff)

cat_type = pd.api.types.CategoricalDtype(categories=["sequel made more", "about the same", "original made more"], ordered=True)

fig3_data = fig3_data.astype(cat_type)

p = sns.histplot(x=fig3_data, stat="proportion", shrink=.8, color='#251e83')#'#688311',
plt.title("More Than 60% of the Time, The Original Made More \$\$")
plt.ylabel("Proportion")
plt.annotate(
    "Source: IMBD/TMBD",
    xy=(0.7, -0.17),
    xycoords="axes fraction",
)
plt.savefig("./fig2.png")

############
# Figure 3 #
############

fig2_data = data.query("sequel_num in [1,2]") \
  .assign(log_of_revenue = lambda x:np.log(x.adjusted_rev+1))

p = sns.histplot(data=fig2_data, x="log_of_revenue", hue="sequel_num", element="step", palette = ['#688311', '#251e83'])
sns.move_legend(p, "upper right", title='Movies', frameon=False)
plt.title("Bimodal Distrbution at \$0 and e^19 ≈ \$180 Million")
plt.ylabel("Movie Count")
plt.xlabel("Log of Revenue")
plt.annotate(
    "Source: IMBD/TMBD",
    xy=(0.7, -0.17),
    xycoords="axes fraction",
)
plt.savefig("./fig3.png")

############
# Figure 4 #
############

fig_data = data.query("sequel_num in [1,2]") \
  .assign(log_of_revenue = lambda x:np.log(x.revenue+1))

p = sns.histplot(data=fig_data, x="IMDb Rating", hue="sequel_num", element="step", palette = ['#688311', '#251e83'])

og_med = fig_data.query("sequel_num == 1")["IMDb Rating"].median()

p.axvline(og_med, color='#688311', lw=4)

p.text(x=7.2, y=60, s=f'Original Median:\n{og_med}', color='#688311')

sql_med = fig_data.query("sequel_num == 2")["IMDb Rating"].median()

p.axvline(sql_med, color='#251e83', lw=4)

p.text(x=5.9, y=53, s=f'Sequel Median:\n{sql_med}', color='#251e83',
horizontalalignment = "right")

sns.move_legend(p, "upper left", title='Movies', frameon=False)
plt.title("On Average, Originals Have Higher Ratings")
plt.ylabel("Movie Count")
plt.xlabel("IMDB Score")
plt.annotate(
    "Source: IMBD/TMBD",
    xy=(0.7, -0.17),
    xycoords="axes fraction",
)
plt.savefig("./fig4.png")

############
# Quick Summary #
############

def imdb_diff(data_part):
  tmp = data_part.sort_values("sequel_num").reset_index(drop=True)
  return tmp.loc[0,"IMDb Rating"] - tmp.loc[1,"IMDb Rating"]

diff = data.query("sequel_num in [1,2]") \
  .groupby("sequel_group") \
  .apply(imdb_diff) \
  .mean()

diff = round(diff,2)

print(f"On average, the original is rated {diff} points higher than its sequel")

############
# Figure 5 #
############

fig2_data = data.query("sequel_num in [1,2]") \
  .assign(log_of_popularity = lambda x:np.log(x.popularity+1))

p = sns.histplot(data=fig2_data, x="log_of_popularity", hue="sequel_num", element="step", palette = ['#688311', '#251e83'])
sns.move_legend(p, "upper right", title='Movies', frameon=False)
plt.title("Similar Popularity Scores; Originals Have Slight Edge")
plt.ylabel("Movie Count")
plt.xlabel("Log of Popularity")
plt.annotate(
    "Source: IMBD/TMBD",
    xy=(0.7, -0.17),
    xycoords="axes fraction",
)
plt.savefig("./fig5.png")

############
# Figure 6 #
############

sequels12 = data.query("sequel_num in [1,2,3,4]")
x = sequels12.groupby('sequel_num')['adjusted_budget'].agg("mean").index.to_list()
y = sequels12.groupby('sequel_num')['adjusted_budget'].agg("mean").to_list()
p = sns.barplot(x=x,y=y, color="#342bbb")
plt.title("On Average, Sequels Seem to Get More Budget")
p.text(x=-0.19, y=52_000_000, s="n=410", color = "white")
p.text(x=0.8, y=57_000_000, s="n=410", color = "white")
p.text(x=1.8, y=60_000_000, s="n=189", color = "white")
p.text(x=2.85, y=68_000_000, s="n=77", color = "white")
plt.ylabel("Budget $")
plt.xlabel("Sequel Number")
plt.annotate(
    "Source: IMBD/TMBD",
    xy=(0.7, -0.17),
    xycoords="axes fraction",
)
plt.savefig("./fig6.png")

############
# Figure 7 #
############

fig, ax = plt.subplots()
y_pos = np.arange(len(chart_later.index))
ax.barh(y_pos, chart_later.values, align='center')
ax.set_yticks(y_pos, labels=chart_later.index)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Number of Sequels Made')
ax.set_title('Every Large Production Studio Makes Sequels')
plt.savefig("./fig7.png")

############
# Regression Analysis #
############

def prepare_data(data_part):
  tmp = data_part.sort_values("sequel_num").reset_index(drop=True)
  time_between = np.abs(tmp.loc[0,"Year"] - tmp.loc[1,"Year"])
  budget_diff = tmp.loc[1,"adjusted_budget"] - tmp.loc[0,"adjusted_budget"]
  same_director = int(tmp.loc[0,"Directors"] == tmp.loc[1,"Directors"])
  imdb_diff = tmp.loc[1,"IMDb Rating"] - tmp.loc[0,"IMDb Rating"]
  action = int('Action' in str(tmp.loc[1,"Genres"]))
  horror = int('Horror' in str(tmp.loc[1,"Genres"]))
  comedy = int('Comedy' in str(tmp.loc[1,"Genres"]))
  romance = int('Romance' in str(tmp.loc[1,"Genres"]))
  family = int('Family' in str(tmp.loc[1,"Genres"]))
  return_df = pd.DataFrame({
    'same_director': same_director,
    'time_between': time_between,
    'imdb_diff': imdb_diff,
    'action': action,
    'horror': horror,
    'comedy': comedy,
    'romance': romance,
    'family': family,
    'budget_diff': budget_diff,
    'warner_bros': tmp.loc[1,"warner_bros"],
    'fox': tmp.loc[1,"fox"],
    'disney': tmp.loc[1,"disney"],
    'warner_bros': tmp.loc[1,"warner_bros"],
    'universal': tmp.loc[1,"universal"],
    'marvel': tmp.loc[1,"marvel"],
    'y': tmp.loc[1,"adjusted_rev"] - tmp.loc[0,"adjusted_rev"]
  }, index = [0])
  return return_df

data_to_model = data.query("sequel_num in [1,2]") \
  .groupby("sequel_group") \
  .apply(prepare_data)

def rescale(col):
  if any(col.gt(1)) or any(col.lt(0)):
    ncol = col - col.mean()
    ncol = ncol/col.std()
  else:
    ncol = col
  return ncol

y = data_to_model.y.values
X = data_to_model.reset_index() \
  .drop(columns = ['sequel_group', 'level_1', 'y'])
X = sm.add_constant(X)

model = sm.OLS(y, X)
results = model.fit()

coef_table = results.summary2()
coef_table = coef_table.tables[1] \
  .assign(Significant = lambda x:x['P>|t|']<0.05) \
  .rename(columns = {'Coef.':'Coefficient'})

coef_table[['Coefficient', 'Significant']].to_html()


############
# Checking Regression Assumptions #
############

# 1. Plotting Residuals (Checking Linearity)
fitted_values = results.fittedvalues
residuals = results.resid
plt.scatter(fitted_values, residuals)
plt.axhline(y=0, color='r', linestyle='-')
plt.xlabel("Fitted values")
plt.ylabel("Residuals")
plt.title("Residuals vs. Fitted")
plt.show()
# Things look decent here other than a few outliers.

# 2. Checking Influential Observations
influence = results.get_influence()
cooks_distance = influence.cooks_distance
threshold = 1
g_x = [x for x in range(len(cooks_distance[0]))]
g_y = cooks_distance[0]
text = [[i,x] for i,x in enumerate(g_y) if x>threshold]
for pair in text:
  plt.text(x=pair[0]+1, y=pair[1], s=str(pair[0]))
plt.stem(g_x, g_y, markerfmt=",", use_line_collection=True)
plt.axhline(y=threshold, color='r', linestyle='-')
plt.title("Cook's Distance Plot")
plt.xlabel("Observation Number")
plt.ylabel("Cook's Distance")
plt.show()
# Bambi is a very influential observation - Maybe remove?

# 3. Residuals are Normally Distributed
stats.probplot(residuals, dist="norm", plot=plt)
plt.title("Normal Q-Q Plot")
plt.show()
#Showing an S-Shape which is indivative of Heavy Tails
#Using Robust Standard Errors

# 4. Multi-colinearity
vif = pd.DataFrame()
vif["Variable"] = X.columns
vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
#Everything looks good here.

# Given the checks, I'm going to try:
# 1. Remove the outlier - Bambi
# 2. Transform the 'Budget_diff' and 'Y' using yeojohnson transformation

# I took this function from here: \/
# https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.PowerTransformer.html
def yeojohnson_inv(X_trans, lambda_):
  if X_trans >= 0 and lambda_ == 0:
    X = np.exp(X_trans) - 1
  elif X_trans >= 0 and lambda_ != 0:
    X = (X_trans * lambda_ + 1) ** (1 / lambda_) - 1
  elif X_trans < 0 and lambda_ != 2:
    X = 1 - (-(2 - lambda_) * X_trans + 1) ** (1 / (2 - lambda_))
  elif X_trans < 0 and lambda_ == 2:
    X = 1 - np.exp(-X_trans)
  return X

data_to_model = data.query("sequel_num in [1,2]") \
  .groupby("sequel_group") \
  .apply(prepare_data)
data_to_model['budget_diff'], lambda_value_bd =  \
  stats.yeojohnson(data_to_model.budget_diff.values)
data_to_model['y'], lambda_value_y =  \
  stats.yeojohnson(data_to_model['y'])
X = data_to_model.reset_index(drop=True)
X = X.iloc[X.index.to_numpy().__ne__(94),:]
y = X.y.values
X = X.drop(columns = ['y'])
X = sm.add_constant(X)

model = sm.OLS(y, X)
results = model.fit()
robust_results = results.get_robustcov_results()

coef_table = robust_results.summary2()
coef_table = coef_table.tables[1] \
  .assign(Significant = lambda x:x['P>|t|']<0.05) \
  .rename(columns = {'Coef.':'Coefficient'})

coef_table[['Coefficient', 'Significant']].to_html()

############
# Figure 8 #
############

rnge = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])

X_varied = {k:[v for x in range(len(rnge))] for k,v in X.mean().to_dict().items()}
X_varied = pd.DataFrame(X_varied)

X_varied['time_between'] = rnge

predictions = robust_results.get_prediction(exog=X_varied)
predictions_summary = predictions.summary_frame(alpha=0.05)

upper = [yeojohnson_inv(x,lambda_value_y) for x in predictions_summary['mean_ci_upper']]
lower = [yeojohnson_inv(x,lambda_value_y) for x in predictions_summary['mean_ci_lower']]
mns = [yeojohnson_inv(x,lambda_value_y) for x in predictions_summary['mean']]

plt.fill_between(
  x=rnge,
  y1=upper,
  y2=lower,
  alpha=0.25
)
plt.plot(rnge, mns)
plt.title("Bigger Time Gap, Bigger Revenue Loss")
plt.ylabel("Predicted Revenue of Sequel - Original ($)")
plt.xlabel("Years Between Original & Sequel")
plt.savefig("./fig8.png")

############
# Figure 9 #
############

#Need to transform range
#Invert results

rnge = stats.yeojohnson(np.array([-1_000_000,0,1_000_000]),lambda_value_bd)

X_varied = {k:[v for x in range(len(rnge))] for k,v in X.mean().to_dict().items()}
X_varied = pd.DataFrame(X_varied)

X_varied['budget_diff'] = rnge

predictions = robust_results.get_prediction(exog=X_varied)
predictions_summary = predictions.summary_frame(alpha=0.05)

upper = [yeojohnson_inv(x,lambda_value_y) for x in predictions_summary['mean_ci_upper']]
lower = [yeojohnson_inv(x,lambda_value_y) for x in predictions_summary['mean_ci_lower']]
mns = [yeojohnson_inv(x,lambda_value_y) for x in predictions_summary['mean']]

plt.fill_between(
  x=rnge,
  y1=upper,
  y2=lower,
  alpha=0.25
)
plt.plot(rnge, mns)
plt.title("Budget Difference? - No Impact")
plt.ylabel("Predicted Revenue of Sequel - Original ($)")
plt.xlabel("Budget Sequel - Original ($)")
plt.savefig("./fig9.png")

############
# Figure 10 #
############

rnge = np.array([0,1])

X_varied = {k:[v for x in range(len(rnge))] for k,v in X.mean().to_dict().items()}
X_varied = pd.DataFrame(X_varied)

X_varied['same_director'] = rnge

predictions = robust_results.get_prediction(exog=X_varied)
predictions_summary = predictions.summary_frame(alpha=0.05)

upper = [yeojohnson_inv(x,lambda_value_y) for x in predictions_summary['mean_ci_upper']]
lower = [yeojohnson_inv(x,lambda_value_y) for x in predictions_summary['mean_ci_lower']]
mns = [yeojohnson_inv(x,lambda_value_y) for x in predictions_summary['mean']]

plt.fill_between(
  x=rnge,
  y1=upper,
  y2=lower,
  alpha=0.25
)
plt.plot(rnge, mns)
plt.title("Same Director? - No Impact")
plt.ylabel("Predicted Revenue of Sequel - Original ($)")
plt.xlabel("0=Diff Director;1=Same Director")
plt.savefig("./fig10.png")
