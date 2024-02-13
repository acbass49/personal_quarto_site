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
# | output: false
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import datetime

# Load my Data
prob_data = pd.read_csv('https://raw.githubusercontent.com/acbass49/Election2024/main/data/state_probabilities.csv')
tracking_data = pd.read_csv("https://raw.githubusercontent.com/acbass49/Election2024/main/data/tracking_data.csv")
simulation_data = pd.read_csv("https://raw.githubusercontent.com/acbass49/Election2024/main/data/simulation_data.csv")
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
import plotly.express as px

win_perc = simulation_data

fig = px.histogram(simulation_data, x="points", color="winner")
fig.update_layout(
    showlegend=True,
    plot_bgcolor='white',
    title_text = 'Percent of Simulations Won Over Time<br>(hover chart for more info)',
    title_x=0.5,
)

fig.show()
#
#
#
#
#
#
#
#
#

fig = go.Figure(data=go.Choropleth(
    locations=prob_data['State'], # Spatial coordinates
    z = prob_data['Trump Win Prob.'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'rdylbu_r',
    marker_line_color='white',
    hovertemplate = "State: %{location}<br>Trump Win Probability: %{z}%<extra></extra>",
    showscale=False
))

fig.update_layout(
    title_text = 'Trump Win Probability By State<br>(hover chart for more info)',
    geo_scope='usa', # limite map scope to USA
    title_x=0.5
)
config = {'displayModeBar': False, 'scrollZoom': False}
fig.show(config=config)

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
from datetime import timedelta

tracking_data = tracking_data \
    .rename(columns = {'Win Percentage':'Win_Percentage'}) \
    .assign(
        Date = lambda x:pd.to_datetime(x.Date,format='%Y-%m-%d'),
        Win_Percentage = lambda x:round(x.Win_Percentage*100,1),
        LB = lambda x:round(x.LB*100,1),
        UB = lambda x:round(x.UB*100,1),
    )

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x = tracking_data.query('Candidate == "Biden"')['Date'],
        y = tracking_data.query('Candidate == "Biden"')['Win_Percentage'],
        name = 'Biden',
        line_shape='spline'
    )
)

fig.add_trace(
    go.Scatter(
        x = tracking_data.query('Candidate == "Trump"')['Date'],
        y = tracking_data.query('Candidate == "Trump"')['Win_Percentage'],
        name = 'Trump',
        line_shape='spline'
    )
)

fig.update_layout(
    xaxis=dict(
        showline=True,
        showgrid=True,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickcolor='rgb(204, 204, 204)',
        tickformat= '%b %d',
        type='date',
        #dtick= 86400000.0,
    ),
    showlegend=True,
    plot_bgcolor='white',
    title_text = 'Percent of Simulations Won Over Time<br>(hover chart for more info)',
    title_x=0.5,
    xaxis_range=[tracking_data.Date.min()-timedelta(days=1),tracking_data.Date.max()+timedelta(days=1)],
    hovermode='x unified',
    legend_title_text = 'Candidate',
    margin={"l":100,"r":100,"t":130,"b":130},
    yaxis_range=[0,100],
    annotations = [dict(xref='paper',
        yref='paper',
        x=1, y=-0.3,
        showarrow=False,
        text ='*confidence intervals contain 95% of sample means',
        font=dict(
            size=10,
            ),)]
)

fig.update_yaxes(
    title_text = "Simulations Won(%)",
    ticksuffix="%"
)

fig.add_traces([go.Scatter(
        x = tracking_data.query('Candidate == "Trump"')['Date'], 
        y = tracking_data.query('Candidate == "Trump"')['UB'],
        name = "",
        mode = 'lines', line_color = 'rgba(0,0,0,0)',
        hoverinfo = 'skip',
        showlegend = False),
    go.Scatter(
        x = tracking_data.query('Candidate == "Trump"')['Date'], 
        y = tracking_data.query('Candidate == "Trump"')['LB'],
        name = "",
        mode = 'lines', line_color = 'rgba(0,0,0,0)',
        fill='tonexty', fillcolor = 'rgba(255, 0, 0, 0.2)',
        hoverinfo = 'skip',
        showlegend = False)])

fig.add_traces([go.Scatter(
        x = tracking_data.query('Candidate == "Biden"')['Date'], 
        y = tracking_data.query('Candidate == "Biden"')['UB'],
        name = "97.5 Win Perc",
        hovertext = None,
        showlegend = False,
        hoverinfo = 'skip',
        mode = 'lines', line_color = 'rgba(0,0,0,0)'),
    go.Scatter(
        x = tracking_data.query('Candidate == "Biden"')['Date'], 
        y = tracking_data.query('Candidate == "Biden"')['LB'],
        name = "2.5 Win Perc.",
        hovertext = None,
        mode = 'lines', line_color = 'rgba(0,0,0,0)',
        hovertemplate = '',
        showlegend = False,
        hoverinfo = 'skip',
        fill='tonexty', fillcolor = 'rgba(0, 0, 255, 0.2)')])

config = {'displayModeBar': False, 'scrollZoom': False}
fig.show(config=config)

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
