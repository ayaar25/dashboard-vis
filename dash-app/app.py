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

# np.random.seed(999)
# dataset = pd.DataFrame({
#   "Sex": np.random.randint(0, 2, 1000),
#   "Years": np.random.randint(1970, 1980, 1000),
#   "Age": np.random.randint(18, 65, 1000),
#   "v1": np.random.randint(0, 2, 1000),
#   "v2": np.random.randint(0, 2, 1000),
#   "v3": np.random.randint(0, 2, 1000),
#   "Category": np.random.randint(0, 8, 1000),
#   "Percentage": np.random.randint(1, 10, 1000)
# })

# group_scatter = pd.DataFrame({'count':dataset.groupby(['Age', 'Percentage', 'Category']).size()}).reset_index()
# group_scatter['count'] = group_scatter['count'].apply(lambda x: x*10)

# df = px.data.gapminder()

external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    className="container-fluid",
    children=[
        html.H1(children='Visualisasi Data Kementrian Kesehatan'),

        html.Div(
            className="row",
            children=[
                html.Div(
                    className="col-sm-10",
                    children=[
                        dcc.Graph(id='bar-graph1'),
                        html.Div(
                            className="btn-group d-flex",
                            children=[
                                html.Button('Jenis Kelamin', className="btn btn-light", id='sex-button'),
                                html.Button('Faktor Resiko', className="btn btn-light", id='risk-factor-button'),
                                html.Button('Umur', className="btn btn-light", id='age-button'),
                                html.Button('Suku Ayah', className="btn btn-light", id='father-tribe-button'),
                                html.Button('Suku Ibu', className="btn btn-light", id='mother-tribe-button')
                            ]
                        ),
                    ]
                ),
                html.Div(
                    className="col-sm-2",
                    children=[
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
        ),

        # html.Div(
        #     className="row",
        #     children=[
        #         html.Div(
        #             className="col-sm-8",
        #             children=[
        #                 dcc.Graph(id='dummy-graph2')
        #             ]
        #         ),
        #         html.Div(
        #             className="col-sm-2",
        #             children=[
        #                 dcc.Dropdown(
        #                     id = 'multi-options',
        #                     options = [
        #                         {'label': 'HIV', 'value': 0},
        #                         {'label': 'Smoking', 'value': 1},
        #                         {'label': 'Fart', 'value': 2},
        #                         {'label': 'Stress', 'value': 3},
        #                         {'label': 'Diet', 'value': 4},
        #                         {'label': 'Cancer', 'value': 5},
        #                         {'label': 'Tea', 'value': 6},
        #                         {'label': 'Coffee', 'value': 7}
        #                     ],
        #                     value = [0, 1],
        #                     multi = True
        #                 )
        #             ]
        #         )
        #     ]
        # ),

    
    

    dcc.Graph(
        id='dummy-graph3',
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

def update_figure1(selected_var, sex_clicked, risk_clicked, age_clicked, father_tribe_clicked, mother_tribe_clicked):
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
        'layout' : {
            'title': 'Frekuensi Tahap Survey vs ' + title_feature,
            'barmode': 'stack'
        }
    }

# @app.callback(
#     Output(component_id='dummy-graph2', component_property='figure'),
#     [Input(component_id='multi-options', component_property='value')]
# )
# def update_figure2(selected_opt):
#     traces = []

#     grouped_sum_1 = dataset.groupby(['Category']).sum()['v1']
#     list_sum_1 = grouped_sum_1.values.tolist()
#     grouped_sum_2 = dataset.groupby(['Category']).sum()['v2']
#     list_sum_2 = grouped_sum_2.values.tolist()
#     grouped_sum_3 = dataset.groupby(['Category']).sum()['v3']
#     list_sum_3 = grouped_sum_3.values.tolist()

#     y_opt = []
#     for opt in selected_opt:
#         y = []
#         y.append(list_sum_1[opt])
#         y.append(list_sum_2[opt])
#         y.append(list_sum_3[opt])
#         y_opt.append(y)

#     for i in range(len(selected_opt)):
#         traces.append(go.Bar(name=str(selected_opt[i]), x=y_opt[i], y=['v1', 'v2', 'v3'], orientation='h'))
    
#     return {
#         'data' : traces,
#         'layout' : {
#             'title': 'Dummy Data Visualization',
#             'barmode': 'stack'
#         }
#     }

if __name__ == '__main__':
    app.run_server(debug=True)