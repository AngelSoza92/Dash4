import dash
import dash_core_components as dcc
import dash_html_components as html
from matplotlib.axis import XTick
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import requests
from traitlets import TraitType
from dash import Dash, dcc, html, Input, Output

app1 = dash.Dash(__name__)

data1 = requests.get('http://10.107.226.241/tracking_labor2.php')
jsondata1 = data1.json()
#crear tabla
columns=['QUANTITY','F_MOD','DIA','HASTA','USUARIO','DESDE', 'FLUJO','HORA_','MINUTO','MIN_HORA','HORA','TRANSACTION_ID','TIPO','LOC','CD','OPERACION']

dataTr=[]

for col in jsondata1:
    for x in jsondata1[col]:
        dataTr.append([col,x['F_MOD'],x['DIA'],x['HASTA'],x['USUARIO'],x['DESDE'], x['FLUJO'],x['HORA_']*1,x['MINUTO'],x['MIN_HORA'],x['HORA']*1,x['TRANSACTION_ID'],x['TIPO'],x['LOC'],x['CD'],x['OPERACION']])
dfTr = pd.DataFrame(dataTr, columns=columns)




fiPi = px.scatter(dfTr, x="HORA", y="USUARIO", color="TIPO",title="TR por tipo",height=1900,width=2400 )
#fiPi = fiPi.update_xaxes(showgrid=True, gridcolor='black')
#fiPi = fiPi.update_xaxes(minor=dict(ticklen=24, tickcolor="black"))
fiPi = fiPi.update_xaxes(scaleratio=1)
fiAlm = px.scatter(dfTr, x="HORA", y="USUARIO", color="LOC",title="TR por zona")
fiAlm = fiAlm.update_yaxes(autorange="reversed")
SIDEBAR_STYLE={
    "position":"fixed",
    "top":0,
    "left":0,
    "bottom":0,
    "width":"86rem",
    "padding":"2rem 1rem",
    "background-color":"#f8f9fa",
    "overflow":"scroll"
}
CONTENT_STYLE={
    "margin-left":"4rem",
    "margin-right":"2rem",
    "padding":"2rem 1 rem",
    "display":"inline-block"
    
}

dd=html.Div([
    html.H1("Dashboards web", style={'text-aling':'center'}),
    dcc.Dropdown(id="CDslctd",
    options=[
        {"label":"sólo CD2", "value":"CD2"},
        {"label":"sólo CD1", "value":"CD1"},
        {"label":"sólo DD", "value":"C&C"},
        {"label":"todos los CD", "value":"ALL"}],
    multi=False,
    value="ALL",
    style={"width":"40%"}
    ),
    html.Div(id='output_container', children=[]),
    html.Br(),
    dcc.Graph(id='trGraph_',figure={}),
    dcc.Graph(id='znGraph_',figure={})
])

@app.callback([Output(component_id='output_container', component_property='children'),
Output(component_id='trGraph_',component_property='figure'),
Output(component_id='znGraph_',component_property='figure')],[Input(component_id='CDslctd', component_property='value')])
def upgrade_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))
    container = "El CD elegido por el usuario fue: {}".format(option_slctd)
    df2 = dfTr.copy()
    if option_slctd=="ALL":
        df2 = dfTr.copy()
    else:
        df2 = dfTr[dfTr["CD"]==option_slctd]
    
    #plotly express
    figO = px.scatter(df2, x="HORA", y="USUARIO", color="TIPO",title="TR por tipo", height=1200,width=2000 )
    
    figA = px.scatter(df2, x="HORA", y="USUARIO", color="LOC",title="TR por zona", height=1200,width=2000 )
    figA = figA.update_yaxes(autorange="reversed")
    return container, figO, figA

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display.4"),
        html.Hr(),
        html.P("Deslizar", className="lead"),
    ],
    style=SIDEBAR_STYLE
)

maindiv = html.Div(
    id="trGraph",
    children=[
        html.Div([
        html.H1(children="Análisis TR",),
        html.P(
            children="Analiza las transacciones realizadas"
            " por el personal que marcó ingreso en huellero"
            " en un lapso determinado", className="lead"
        ),
        dcc.Graph(
            figure=fiPi
        )]),
       
    ]
)

divarea = html.Div(
    id="znGraph",
    children=[
        html.Div([
        html.H1(children="Análisis TR",),
        html.P(
            children="Analiza las transacciones realizadas"
            " por el personal que marcó ingreso en huellero"
            " en un lapso determinado", className="lead"
        ),
        dcc.Graph(
            figure=fiAlm
        )]),
       
    ]
)
#app.css.append_css({"https://codepen.io/chriddyp/pen/bWLwgP.css"})
app1.layout = html.Div([dd])

if __name__ == "__main__":
    app1.run_server()
