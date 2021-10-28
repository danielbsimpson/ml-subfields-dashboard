from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

# read the data
df = pd.read_csv('data.csv')

# generate the sunburst
fig=px.sunburst(df, 
                 path=['main', 'lvl1', 'lvl2', 'lvl3'], # column names, order matters
                 color = 'lvl1'
)

fig.update_layout(
    autosize=False,
    width=600,
    height=750,
    )

fig.update_traces(textfont=dict(size=10))


external_stylesheets = [dbc.themes.LUX]

app = dash.Dash(
    __name__, external_stylesheets=external_stylesheets, title='ML subfields')

server = app.server

df = df.replace('<br>',' ', regex=True)

app.layout = html.Div(
    children=[
    html.H1(
        children='Machine Learning',
        style={
                    "font-weight":"bold",
                    "font-size":"30px",
                    "width":"100%",
                    "height":"100%",
                    "text-align":"center",
            }
            ),

    html.Div(
        children='''
        An interactive visual describing the many fields of machine learning.
    ''',
        style={
                    "font-weight":"bold",
                    "font-size":"20px",
                    "width":"100%",
                    "height":"100%",
                    "text-align":"center",
            }
    ),
    html.Div([
        html.Div([
            dcc.Graph(
                id='ml_sunburst',
                figure=fig,
            )
        ], style={
                'width':'50%',
            }
        ),
        html.Div([
            html.Br(),
            html.P('Please select a subfield of machine learning that you would like to learn about:'),
            html.Br(),
            dcc.Dropdown(
                id='first_dropdown',
                options=[{'label': x, 'value': x} for x in df.lvl1.unique()], # select only lvl2 options for display, remove <br>
                value='Supervised', # default value
                multi=False,
            ),
            html.Br(),
            html.P('Now select the topic you are interested in learning about:'),
            html.Br(),
            dcc.Dropdown(
                id='second_dropdown',
                options=[], # select only lvl3 options and remove all NaN values
                value=[],
                multi=False,
            ),
            html.Br(),
            html.Div(
                id="text-description",
                children="You have not selected a topic yet."
            ),


        ],
            style={
                'width':'40%',
            },
        ),
    ], className='row',
    )
],
)

# link the first two dropdowns with a callback
@app.callback(
    [Output(component_id='second_dropdown', component_property='options'),
     Output(component_id='second_dropdown', component_property='value')],
    [Input(component_id='first_dropdown', component_property='value')]
)
def update_subfield(subfield_option):
    df2 = df[df['lvl1'] == subfield_option]
    subfields_selected = [{'label': c, 'value': c} for c in sorted(df2.lvl2.unique())] # generate the list of value and label pairs from the filtered df
    values_selected = [x['value'] for x in subfields_selected]
    return subfields_selected, values_selected

@app.callback(
    Output(component_id='text-description', component_property="children"),
    [Input(component_id='second_dropdown', component_property='value')]
)
def print_text(subject):
    if type(subject) is list:
        raise dash.exceptions.PreventUpdate
    else:
        desc = 'You would like to learn about ' + str(subject)
        return desc

if __name__ == '__main__':
    app.run_server(host = '0.0.0.0', port=8080, debug=True)