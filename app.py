import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

import plotly.express as px
from dash.dependencies import Input, Output


# Get Data

url = 'https://raw.githubusercontent.com/NicJC/Datasets/main/Arrests.csv'

df = pd.read_csv(url)

df = df.loc[df.Year == 2019]

cat = df.Category.unique()

external_stylesheets = ['https://raw.githubusercontent.com/NicJC/Dash-app/main/assets/style.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    html.P("Select Arrest Category:"),

    dcc.Dropdown(
        id="dropdown",
        options=[{"label": x, "value": x} for x in cat],
        value=cat[0],
        clearable=False,
    ),

    dcc.Graph(id="bar-chart"),

])


@app.callback(
    Output("bar-chart", "figure"),
    [Input("dropdown", "value")])
def update_bar_chart(Category):
    mask = df["Category"] == Category
    fig = px.bar(df[mask], x="Date", y="Sex",
                 color="Sex", barmode="group",
                 height=530
                 )

    fig.update_layout(title_text='2019 Arrests by Category, Race and Gender')
    fig.update_layout(uniformtext_minsize=15, uniformtext_mode='hide')
    fig.update_layout(barmode='group', xaxis_tickangle=-45)
    fig.update_layout(plot_bgcolor="#fff")
    fig.update_layout(barmode="relative")
    fig.update_layout(modebar_orientation="h")
    fig.update_xaxes(title_font_family="Helvetica")
    fig.update_layout(title_font_size=30)

    return fig


app.run_server(debug=True)
