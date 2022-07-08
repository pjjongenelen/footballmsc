import eredivisie_nlp as enlp
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd

df_total = pd.read_pickle(enlp.determine_root() + "/data/grades+twitter.pkl")
# normalize the fotmob scores, to have the same average as AD and VI
df_total.FM = df_total.FM - 1
df_total.reset_index(inplace=True, drop=True)

app = dash.Dash()

fig = px.scatter(
    df_total,
    x='AD',
    y='score_robbert',
    hover_name='player_id',
    size_max=60
)

app.layout = html.Div(
    [
        html.Div([dcc.Dropdown(id='squad_dropdown', options=sorted(set(df_total.home)))]),
        html.Div([dcc.Graph(id='ad_rob', figure=fig)])
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)