import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly import express as px

import numpy as np
import pandas as pd
import plotly.express as px

dataset_bar = pd.read_csv('../data/risk_factor.tsv', sep='\t')
dataset_bubble = pd.read_csv('../data/bubble.tsv', sep='\t')

total_respondents = []
for i in range(len(dataset_bubble)):
    total_respondents.append(dataset_bubble['non_stroke'][i]+dataset_bubble['stroke'][i])

colors = []
for i in range(len(dataset_bubble)):
    colors.append('rgb'+ str((np.random.randint(0,256), np.random.randint(0,256), np.random.randint(0,256))))

dataset_bubble['total_respondents'] = total_respondents
dataset_bubble['color'] = colors
dataset_bubble['importance'] = dataset_bubble['importance'].apply(lambda x: x*10)

external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    className="container-fluid",
    children=[
        html.Div(
            className="container-fluid",
            children=[
                html.H1(
                    children='Visualisasi Data Kementrian Kesehatan'
                )
            ]
        ),

        html.Div(
            className="container-fluid",
            children=[
                html.Div(
                    className="card",
                    children=[
                        html.Div(
                            className="card-header",
                        ),
                        html.Div(   
                            className="card-body row",
                            children=[
                                html.Div(
                                    className="col-sm-10",
                                    children=[
                                        dcc.Graph(id='bar-graph1'),
                                        html.Div(
                                            className="btn-group d-flex",
                                            children=[
                                                html.Button('Jenis Kelamin', className="border border-secondary btn btn-light", id='sex-button'),
                                                html.Button('Faktor Resiko', className="border border-secondary btn btn-light", id='risk-factor-button'),
                                                html.Button('Umur', className="border border-secondary btn btn-light", id='age-button'),
                                                html.Button('Suku Ayah', className="border border-secondary btn btn-light", id='father-tribe-button'),
                                                html.Button('Suku Ibu', className="border border-secondary btn btn-light", id='mother-tribe-button')
                                            ]
                                        ),
                                    ]
                                ),
                                html.Div(
                                    className="col-sm-2",
                                    children=[
                                        html.Br(),
                                        html.Div(
                                            className="form-check",
                                            children=[
                                                html.H5(
                                                    children="Tahapan Survey"
                                                ),
                                                dcc.Checklist(
                                                    className="form-check-label",
                                                    id='var-checkboxes',
                                                    options=[
                                                        {'label': ' 2011', 'value': '2011'},
                                                        {'label': ' 2012', 'value': '2012'},
                                                        {'label': ' 2015', 'value': '2015'}
                                                    ],
                                                    value=['2011', '2012', '2015'],
                                                    labelStyle={'display': 'block'}
                                                )
                                            ]
                                        )
                                     ]
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
        html.Br(),
        html.Div(
            className="container-fluid",
            children=[
                html.Div(
                className="card",
                children=[
                    html.Div(
                        className="card-header"
                    ),
                    html.Div(
                        className="card-body",
                        children=[
                            dcc.Graph(
                                id='scatter-graph3',
                                figure={
                                    'data' : [
                                        go.Scatter(
                                            x = dataset_bubble['total_respondents'],
                                            y = dataset_bubble['stroke'],
                                            text = dataset_bubble['jenis'],
                                            mode = 'markers',
                                            marker = {
                                                'color' : dataset_bubble['color'],
                                                'size'  : dataset_bubble['importance']
                                            }
                                        )
                                    ],
                                    'layout' : dict(
                                        title = "Jenis Faktor Resiko vs Jumlah Penderita Stroke vs Besar Resiko",
                                        xaxis = {'title' : 'Jumlah Responden'},
                                        yaxis = {'title' : 'Jumlah Responden dengan Stroke'}
                                    )
                                }
                            )
                        ]
                    )
                ]
            ),
        html.Br()
        ]
    )
])

@app.callback(
    Output(component_id='bar-graph1', component_property='figure'),
    [Input(component_id='var-checkboxes', component_property='value'),
    Input(component_id='sex-button', component_property='n_clicks_timestamp'),
    Input(component_id='risk-factor-button', component_property='n_clicks_timestamp'),
    Input(component_id='age-button', component_property='n_clicks_timestamp'),
    Input(component_id='father-tribe-button', component_property='n_clicks_timestamp'),
    Input(component_id='mother-tribe-button', component_property='n_clicks_timestamp')],
)

def update_figure(selected_var, sex_clicked, risk_clicked, age_clicked, father_tribe_clicked, mother_tribe_clicked):
    buttons = [0, 0, 0, 0, 0]
    traces = []
    col = "umur"
    title_feature = "Umur"
    
    if sex_clicked == None:
        buttons[0] = 0
    else:
        buttons[0] = sex_clicked
    
    if risk_clicked == None:
        buttons[1] = 0
    else:
        buttons[1] = risk_clicked

    if age_clicked == None:
        buttons[2] = 0
    else :
        buttons[2] = age_clicked
    
    if father_tribe_clicked == None:
        buttons[3] = 0
    else :
        buttons[3] = father_tribe_clicked
    
    if mother_tribe_clicked == None:
        buttons[4] = 0
    else :
        buttons[4] = mother_tribe_clicked
    
    if buttons.index(max(buttons)) == 0:
        col = 'jenis_kelamin'
        title_feature = "Jenis Kelamin"
    elif buttons.index(max(buttons)) == 1:
        col = 'insiden_stroke'
        title_feature = "Faktor Resiko"
    elif buttons.index(max(buttons)) == 2:
        col = 'umur'
        title_feature = "Umur"
    elif buttons.index(max(buttons)) == 3:
        col = 'suku_ayah'
        title_feature = "Suku Ayah"
    else:
        col = 'suku_ibu'
        title_feature = "Suku Ibu"

    df_fitur = pd.DataFrame({'count': dataset_bar.groupby([col, "tahap"]).size()}).reset_index()

    for var in selected_var:
        traces.append(go.Bar(name=var, x=df_fitur.loc[df_fitur['tahap']==int(var)][col].tolist(), y=df_fitur.loc[df_fitur['tahap']==int(var)]['count'].tolist()))
    
    return {
        'data' : traces,
        'layout' : dict(
            title= 'Jumlah Responden vs ' + title_feature,
            barmode= 'stack',
            yaxis={'title':'Jumlah Responden'}
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)