import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly import express as px

import numpy as np
import pandas as pd
import plotly.express as px


np.random.seed(999)
dataset = pd.DataFrame({
  "Sex": np.random.randint(0, 2, 1000),
  "Years": np.random.randint(1970, 1980, 1000),
  "Age": np.random.randint(18, 65, 1000),
  "v1": np.random.randint(0, 2, 1000),
  "v2": np.random.randint(0, 2, 1000),
  "v3": np.random.randint(0, 2, 1000),
  "Category": np.random.randint(0, 8, 1000),
  "Percentage": np.random.randint(1, 10, 1000)
})

group_scatter = pd.DataFrame({'count':dataset.groupby(['Age', 'Percentage', 'Category']).size()}).reset_index()
group_scatter['count'] = group_scatter['count'].apply(lambda x: x*10)

df = px.data.gapminder()

external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    html.Label('Checkboxes'),
        dcc.Checklist(
            id='var-checkboxes',
            options=[
                {'label': 'V1', 'value': 'v1'},
                {'label': 'V2', 'value': 'v2'},
                {'label': 'V3', 'value': 'v3'}
            ],
            value=['v1', 'v2', 'v3']
        ),
    
    dcc.Graph(id='dummy-graph1'),

    html.Button('Year', id='year-button'),
    html.Button('Sex', id='sex-button'),
    html.Button('Age', id='age-button'),

    dcc.Dropdown(
        id = 'multi-options',
        options = [
            {'label': 'HIV', 'value': 0},
            {'label': 'Smoking', 'value': 1},
            {'label': 'Fart', 'value': 2},
            {'label': 'Stress', 'value': 3},
            {'label': 'Diet', 'value': 4},
            {'label': 'Cancer', 'value': 5},
            {'label': 'Tea', 'value': 6},
            {'label': 'Coffee', 'value': 7}
        ],
        value = [0, 1],
        multi = True
    ),
    dcc.Graph(id='dummy-graph2'),

    dcc.Graph(
        id='dummy-graph3',
        figure={
            'data' : [
                go.Scatter(
                    x = group_scatter['Age'],
                    y = group_scatter['Percentage'],
                    mode = 'markers',
                    marker = {
                        'color' : group_scatter['Category'],
                        'size'  : group_scatter['count']
                    }
                )
            ],
            'layout' : {
                'title' : 'Dummy Data Visualization'
            }
        }
    
    )

])

@app.callback(
    Output(component_id='dummy-graph1', component_property='figure'),
    [Input(component_id='var-checkboxes', component_property='value'),
    Input(component_id='year-button', component_property='n_clicks_timestamp'),
    Input(component_id='sex-button', component_property='n_clicks_timestamp'),
    Input(component_id='age-button', component_property='n_clicks_timestamp')],
)

def update_figure1(selected_var, year_clicked, sex_clicked, age_clicked):
    buttons = [0, 0, 0]
    traces = []
    col = "Years"
    
    if year_clicked == None:
        buttons[0] = 0
    else:
        buttons[0] = year_clicked
    
    if sex_clicked == None:
        buttons[1] = 0
    else:
        buttons[1] = sex_clicked

    if age_clicked == None:
        buttons[2] = 0
    else :
        buttons[2] = age_clicked
    
    if buttons.index(max(buttons)) == 0:
        col = 'Years'
    elif buttons.index(max(buttons)) == 1:
        col = 'Sex'
    else:
        col = 'Age'

    for var in selected_var:
        traces.append(go.Bar(name=var, x=dataset.groupby([col]).sum()[var].index.tolist(), y=dataset.groupby([col]).sum()[var].values.tolist()))
    
    return {
        'data' : traces,
        'layout' : {
            'title': 'Dummy Data Visualization',
            'barmode': 'stack'
        }
    }

@app.callback(
    Output(component_id='dummy-graph2', component_property='figure'),
    [Input(component_id='multi-options', component_property='value')]
)
def update_figure2(selected_opt):
    traces = []

    grouped_sum_1 = dataset.groupby(['Category']).sum()['v1']
    list_sum_1 = grouped_sum_1.values.tolist()
    grouped_sum_2 = dataset.groupby(['Category']).sum()['v2']
    list_sum_2 = grouped_sum_2.values.tolist()
    grouped_sum_3 = dataset.groupby(['Category']).sum()['v3']
    list_sum_3 = grouped_sum_3.values.tolist()

    y_opt = []
    for opt in selected_opt:
        y = []
        y.append(list_sum_1[opt])
        y.append(list_sum_2[opt])
        y.append(list_sum_3[opt])
        y_opt.append(y)

    for i in range(len(selected_opt)):
        traces.append(go.Bar(name=str(selected_opt[i]), x=y_opt[i], y=['v1', 'v2', 'v3'], orientation='h'))
    
    return {
        'data' : traces,
        'layout' : {
            'title': 'Dummy Data Visualization',
            'barmode': 'stack'
        }
    }

if __name__ == '__main__':
    app.run_server(debug=True)