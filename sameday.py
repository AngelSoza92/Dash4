from dash import Dash, dcc, html, Input, Output, dash_table, no_update,State  # Dash version >= 2.0.0
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import numpy as np
from plotly.subplots import make_subplots
import dash

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_excel('df.xlsx')
#appsd = Dash(__name__,title="SameDay", external_stylesheets=[dbc.themes.MORPH],requests_pathname_prefix='/sameday/')
appsd = dash.Dash(__name__,title="SameDay", external_stylesheets=[dbc.themes.MORPH, dbc.icons.FONT_AWESOME],requests_pathname_prefix='/sameday/')
PLOTLY_LOGO = "caja.png"

dff=df
etas = dff.ETA.unique()
depas1 = dff.DEPTO.unique()
fechas = dff.FECHA_ACT.unique()
subs=dff.SUB_ESTADO.unique()
subs1= dff[dff['CUMPLIMIENTO']=='INCUMPLIMIENTO'].SUB_ESTADO.unique()
locales=dff.LOCALDESPA.unique()
cumplimientos=dff.CUMPLIMIENTO.unique()
meses = dff.MES.unique()
años=dff.AÑO.unique()
recientes = dff.RECIENTE.unique()
flujos = dff.FLUJO.unique()
dfff = dff.pivot_table( values = "QTY",index = ["ETA", "FECHA_ACT","SUB_ESTADO"], columns = "CUMPLIMIENTO", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
long = dfff.shape[0]
columns=[{"name": c} for c in dfff.columns if c != 'id']
columnas = len(dfff.columns)-1
totalY =[]
totalX=[]

dfi = dff[dff['CUMPLIMIENTO']=='INCUMPLIMIENTO']
dfcumplimiento = dff.groupby('CUMPLIMIENTO')['QTY'].sum()
dflocaldespa = dff.groupby('LOCALDESPA')['QTY'].sum()
dfsubestado = dff.groupby('SUB_ESTADO')['QTY'].sum()
depas = dff.groupby('DEPTO')['QTY'].sum()

con=0
fig8 = make_subplots(
    rows=1, cols=3,
    specs=[
           [{"type": "domain"}, {'type':'domain'}, {'type':'domain'}]],
     subplot_titles=("Cumplimientos","CD", "Detalle Incumplimientos")
)


fig8.add_trace(go.Pie(labels=cumplimientos, values=dfcumplimiento[cumplimientos], name="Cumplimientos"), 1, 1)
fig8.add_trace(go.Pie(labels=locales, values=dflocaldespa[locales], name="Locales"), 1, 2)
fig8.add_trace(go.Pie(labels=subs1, values=dfsubestado[subs1], name="Incumplimientos"), 1, 3)
#fig8.add_trace(go.Pie(labels=depas1, values=depas[depas1], name="Dptos"), 1, 4)
fig9 = go.Figure(data=[go.Bar(x=depas1,y=depas[depas1])])

sidebar = html.Div(
    [
        html.Div(
            [
                # width: 3rem ensures the logo is the exact width of the
                # collapsed sidebar (accounting for padding)
                html.Img(src=PLOTLY_LOGO, style={"width": "4rem"}),
                html.H2("Menú"),
            ],
            className="sidebar-header",
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [html.I(className="fas fa-home me-2"), html.Span("CLU")],
                    href="/",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa fa-bar-chart"),
                        html.Span(" Despachos DD/C&C"),
                    ],
                    href="localhost:8050/clu",
                    active="partial",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa fa-hourglass-end"),
                        html.Span(" Antiguedad"),
                    ],
                    href="localhost:8050/antiguedad/",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa fa-pie-chart"),
                        html.Span(" Stock100"),
                    ],
                    href="localhost:8050/stock/",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa fa-bar-chart"),
                        html.Span(" Traspasos"),
                    ],
                    href="localhost:8050/traspasos/",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa fa-users"),
                        html.Span(" Tracking"),
                    ],
                    href="localhost:8050/app2",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa fa-tasks"),
                        html.Span(" Ordenes"),
                    ],
                    href="localhost:8050/pkt",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa fa-truck"),
                        html.Span(" Despacho SameDay"),
                    ],
                    href="localhost:8050/sameday/",
                    active="exact",
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)
content = html.Div(id="page-content", className="content")
appsd.layout = html.Div([dcc.Location(id="url"), sidebar, content])



appsdf = html.Div(
    [
        html.Div(
            [
                html.H3("Seguimiento Sameday", style={"textAlign":"center"}),
                html.Div([
               
                html.P('Locales, cumplimientos, flujo'), 
                dcc.Dropdown(
                locales,
                locales,multi=True,placeholder="Locales...",searchable=True,id='dLocal'
                ),
                dcc.Dropdown(
                cumplimientos,
                cumplimientos,multi=True,placeholder="Cumplimientos...",searchable=True,id='dCumplimiento'
                ) ,
                dcc.Dropdown(
                flujos,
                flujos,multi=True,placeholder="Flujos...",searchable=True,id='dFlujo'
                ) ,
                 html.P('Mes, Reciente'), 
                dcc.Dropdown(
                meses,
                meses,multi=True,placeholder="Meses...",searchable=True,id='dMeses'
                ),
                dcc.Dropdown(
                recientes,
                recientes,multi=True,placeholder="Reciente...",searchable=True,id='dReciente'
                ) ,
                ]),
                dcc.Graph(id='graph1',figure=fig8),
                dcc.Graph(id='graph2',figure=fig9),
            ],
        ),
        html.Div(id="output-graph"),
        dash_table.DataTable(
                    id="table1",
                    columns=[{"name": c, "id": c} for c in dfff.columns if c != 'id'],
                    data=dfff.to_dict("records"),
                    page_size=long,
                    sort_action="native",
                    filter_action="native",
                    sort_mode="multi",
                    column_selectable="multi",
                    row_selectable="multi",
                    style_header={
                        'backgroundColor': 'rgb(72,118,178)',
                        'color': 'white'
                    },
                    style_data={
                        'backgroundColor': 'rgb(217,227,241)',
                        'color': 'rgb(72,118,178)'
                    },
                ), 
            html.Div(id="output-table"),
    ])

@appsd.callback([Output("table1","data"),Output("table1","columns"),Output("graph1","figure"),Output("graph2","figure")],[Input('dLocal','value'),Input('dCumplimiento','value'),Input('dMeses','value'),Input('dReciente','value'),Input('dFlujo','value')])
def updaTable(local, icumplimineto, imeses, ireciente,iflujo):
    dfa = dff[(dff.LOCALDESPA.isin(local)) & (dff.CUMPLIMIENTO.isin(icumplimineto)) & (dff.MES.isin(imeses)) &(dff.RECIENTE.isin(ireciente))&(dff.FLUJO.isin(iflujo))]
    print(local)
    cumplii = dfa.CUMPLIMIENTO.unique()
    localii = dfa.LOCALDESPA.unique()
    depasii = dfa.DEPTO.unique()
    subs1= dfa[dfa['CUMPLIMIENTO']=='INCUMPLIMIENTO'].SUB_ESTADO.unique()
    dfii = dfa[dfa['CUMPLIMIENTO']=='INCUMPLIMIENTO']
    dfcumplimientoi = dfa.groupby('CUMPLIMIENTO')['QTY'].sum()
    dflocaldespai = dfa.groupby('LOCALDESPA')['QTY'].sum()
    dfsubestadoi = dfii.groupby('SUB_ESTADO')['QTY'].sum()
    depas = dfa.groupby('DEPTO')['QTY'].sum()
    fig8 = make_subplots(
    rows=1, cols=3,
    specs=[
           [{"type": "domain"}, {'type':'domain'}, {'type':'domain'}, ]],
     subplot_titles=("Cumplimientos","CD", "Detalle Incumplimientos")
    )
    fig8.add_trace(go.Pie(labels=cumplii, values=dfcumplimientoi[cumplii], name="Cumplimientos"), 1, 1)
    fig8.add_trace(go.Pie(labels=localii, values=dflocaldespai[localii], name="Locales"), 1, 2)
    fig8.add_trace(go.Pie(labels=subs1, values=dfsubestadoi[subs1], name="Incumplimientos"), 1, 3)
    #fig8.add_trace(go.Pie(labels=depas1, values=depas[depas1], name="Dptos"), 1, 4)
    fig9 = go.Figure(data=[go.Bar(x=depasii,y=depas[depasii])])
    dfffq = dfa.pivot_table( values = "QTY",index = ["ETA", "FECHA_ACT","SUB_ESTADO"], columns = "CUMPLIMIENTO", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()

    return dfffq.to_dict("records"), [{"name": c, "id": c} for c in dfffq.columns if c != 'id'], fig8, fig9

@appsd.callback([Output("output-table","children"),Input("table1", "active_cell"), State('dLocal','value'),State('dCumplimiento','value'),State('dMeses','value'),State('dReciente','value'),State('dFlujo','value')])
def cell_clicked(active_cell, local, cumplimiento, mes, reciente,iflujo):
    if active_cell is None:
        return no_update
    dfb = dff[(dff.LOCALDESPA.isin(local)) & (dff.CUMPLIMIENTO.isin(cumplimiento)) & (dff.MES.isin(mes)) &(dff.RECIENTE.isin(reciente))&(dff.FLUJO.isin(iflujo))]
    row = active_cell["row"]
    col = active_cell["column_id"]
    dfc = dfb.pivot_table( values = "QTY",index = ["ETA", "FECHA_ACT","SUB_ESTADO"], columns = "CUMPLIMIENTO", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
    fechaa= dfc.at[row, dfc.columns[0]]
    fecha2= dfc.at[row, dfc.columns[1]]
    sestado= dfc.at[row, dfc.columns[2]]
    if fechaa=='Total':
        fig1 = dash_table.DataTable(
            id="table2",
            columns=[{"name": c, "id": c} for c in dfb.columns],
            data= dfb[(dfb['CUMPLIMIENTO']== col)].to_dict("records"),
            page_size=50,
            sort_action="native",
            filter_action="native",
            sort_mode="multi",
            column_selectable="multi",
            row_selectable="multi",
            style_header={
                            'backgroundColor': 'rgb(72,118,178)',
                            'color': 'white'
                        },
                        style_data={
                            'backgroundColor': 'rgb(217,227,241)',
                            'color': 'rgb(72,118,178)'
                        },
            editable=True,
            export_format='xlsx',
            export_headers='display',
            merge_duplicate_headers=True
            ),
        return fig1

    else:
        fig1=dash_table.DataTable(
        id="table2",
        columns=[{"name": c, "id": c} for c in dfb.columns],
        data=dfb[(dfb['ETA'] == fechaa)&(dfb['FECHA_ACT'] == fecha2)&(dfb['SUB_ESTADO'] == sestado)&(dfb['CUMPLIMIENTO']== col)].to_dict("records"),
        page_size=50,
        sort_action="native",
        filter_action="native",
        sort_mode="multi",
        column_selectable="multi",
        row_selectable="multi",
        style_header={
                        'backgroundColor': 'rgb(72,118,178)',
                        'color': 'white'
                    },
                    style_data={
                        'backgroundColor': 'rgb(217,227,241)',
                        'color': 'rgb(72,118,178)'
                    },
        editable=True,
        export_format='xlsx',
        export_headers='display',
        merge_duplicate_headers=True
        ),
        return fig1

@appsd.callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page_content(pathname):
    return appsdf

if __name__ == "__main__":
    appsd.run_server(debug=True)