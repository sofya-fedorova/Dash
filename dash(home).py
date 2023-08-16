# Import packages
import datetime

from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.express as px
#########################################################
def get_year(s):
    return s[-4:]
########################################################
# Incorporate data
##############################################
data = pd.read_excel('1.xlsx')

y = sorted(data.Date.unique())
n_y = []
for i in y:
    n_y.append(i[-4:])

#############################################
# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = ['style.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

# App layout
app.layout = dbc.Container([
    html.Header('Дашборд1', className='header'),
    # html.H3('Дашборд1'),
    dbc.Row([
           dbc.Col([
                html.Div([
                    html.P("Среднее значение ", className='text_in_card', style={'margin-top':'10px'}),
                    html.P({}, className='num', id="avg")
                ],
                     className="text-primary text-center fs-3")
           ], width=6, className='card'),dbc.Col([
                html.Div([
                    html.P("Максимальное значение", className='text_in_card'),
                    html.P({}, className='num', id="max")
                ],
                     className="text-primary text-center fs-3")
           ], width=6, className='card'),dbc.Col([
                html.Div([
                    html.P("Минимальное значение", className='text_in_card'),
                    html.P({}, className='num', id="min")
                ],
                     className="text-primary text-center fs-3")
           ], width=6, className='card')
    ],className='row_s'),
    dbc.Row([
        html.Div([
            dcc.RangeSlider( int(min(n_y)) , int(max(n_y)), id = 'slider',
                             marks={i: '{}'.format(i) for i in range(int(min(n_y)), int(max(n_y)), 1)},
                             value=[int(datetime.datetime.now().year)-1,int(datetime.datetime.now().year)],
                             dots=False,
                             step=1,
                             updatemode='drag'
                             )
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure={}, id='SD', className='SD')
        ], width=3),
        dbc.Col([
                    dcc.Graph(figure={}, id='HI')
                ], width=9, className='HI'),
    ], className='row_s'),
################Гистограма с накоплением по годам#############################
    html.Div([
        html.H3('Динамика по годам'),
        dcc.RadioItems(options=['Size', 'Type'],
                    value='Size',
                    inline=True,
                    id='radio-items', className='radio_button'),
        dcc.Graph(figure={}, id='HIyear')
    ], className='HIyear')

], fluid=True, className='container')
def get_date(slider):
    df = data.copy()
    df['Date'] = df['Date'].apply(get_year)
    df['Date'] = df['Date'].astype(int)
    df = df[(df['Date'] >= slider[0]) & (df['Date'] <= slider[1])]
    return df
# Add controls to build the interaction
@callback(
    Output(component_id='HIyear', component_property='figure'),
    Input(component_id='radio-items', component_property='value'),
    # Input(component_id='slider', component_property='value')
)
def HIyearGraf(item):
    # df1 = get_date(slider) можно сделать тоже по периоду
    df1 = data.copy()
    df1['Date'] = df1['Date'].apply(get_year)
    df1['Date'] = df1['Date'].astype(int)
    fig = px.histogram(df1, x="Date", y='Value', color=item, histfunc='sum', range_x=[min(df1['Date']), max(df1['Date'])]
                       ).update_xaxes(categoryorder='total descending')
    fig.update_xaxes(title_text='Дата')
    fig.update_yaxes(title_text='Значение')
    return fig


@callback(
    Output(component_id='SD', component_property='figure'),
    Input(component_id='slider', component_property='value')
)

def update_SDgraph(slider):
    # df = get_date(slider, data)
    df = data.copy()
    df['Date'] = df['Date'].apply(get_year)
    df['Date'] = df['Date'].astype(int)
    df = df[(df['Date'] >= slider[0]) & (df['Date'] <= slider[1])]
    print(slider)
    fig = px.sunburst(df, path=['Type', 'Size'], values='Value')
    return fig
@callback(
    Output(component_id='HI', component_property='figure'),
    Input(component_id='slider', component_property='value'))
def update_HIgraph(slider):
    df = data.copy()
    df['Date'] = df['Date'].apply(get_year)
    df['Date'] = df['Date'].astype(int)
    df = df[(df['Date'] >= slider[0]) & (df['Date'] <= slider[1])]
    fig = px.histogram(df, x="Size",
                             y = 'Value',
                             color="Type",
                       title = 'Гистограмма',
                       histfunc  = 'sum').update_xaxes(categoryorder='total descending')
    fig.update_xaxes(title_text='Количество')
    fig.update_yaxes(title_text='Размер')
    return fig

@callback(
    Output(component_id='avg', component_property='children'),
    Input(component_id='slider', component_property='value'))

def updateAvg(slider):
    df = get_date(slider)
    return round(df.Value.mean(),2)

@callback(
    Output(component_id='max', component_property='children'),
    Input(component_id='slider', component_property='value'))

def updateMax(slider):
    df = get_date(slider)
    return df.Value.max()

@callback(
    Output(component_id='min', component_property='children'),
    Input(component_id='slider', component_property='value'))

def updateMax(slider):
    df = get_date(slider)
    return df.Value.min()
# Run the app
if __name__ == '__main__':
    app.run(debug=True)