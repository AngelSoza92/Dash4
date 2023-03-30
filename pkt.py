from dash import Dash, dcc, html, Input, Output, dash_table, no_update,State  # Dash version >= 2.0.0
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import numpy as np
from plotly.subplots import make_subplots
import dash


appkt = dash.Dash(__name__,title="PKT", external_stylesheets=[dbc.themes.MORPH, dbc.icons.FONT_AWESOME],requests_pathname_prefix='/pkt/')

PLOTLY_LOGO = "caja.png"
df = pd.read_excel('df5.xlsx')
dff=df
etas = dff.FECHA_SALIDA.unique()
fechas = dff.fecha_eta_cliente.unique()
estados=dff.ESTADO.unique()
regiones=dff.REGION.unique()
depas1 = dff.DPTO.unique()
ordenes=dff.TIPO_ORDEN.unique()
destinos = dff.DEST.unique()

dfff = dff.pivot_table( values = "QTY",index = ["FECHA_SALIDA"], columns = "ESTADO", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
long = dfff.shape[0]
columns=[{"name": c} for c in dfff.columns if c != 'id']
columnas = len(dfff.columns)-1
totalY =[]
totalX=[]
con=0


dfordenes = dff.groupby('TIPO_ORDEN')['QTY'].sum()
dfetas = dff.groupby('FECHA_SALIDA')['QTY'].sum()

fig8 = make_subplots(
    rows=1, cols=2,
    specs=[
           [{"type": "domain"}, {'type':'xy'}]],
     subplot_titles=("Tipos ods","FECHAS")
)


fig8.add_trace(go.Pie(labels=ordenes, values=dfordenes[ordenes], name="Ordenes"), 1, 1)

#fig8.add_trace(go.Pie(labels=etas, values=dfetas[etas], name="Locales"), 1, 2)
fig8.add_trace(go.Bar(x=etas, y=dfetas[etas], name='Fechas'),1,2)
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
appkt.layout = html.Div([dcc.Location(id="url"), sidebar, content])


appktl = html.Div(
    [
        html.Div(
            [
                html.H3("Ordenes local 100", style={"textAlign":"center"}),
                html.Div([
                
                html.P('Fechas, estados'), 
                dcc.Dropdown(
                etas,
                etas,multi=True,placeholder="Fechas...",searchable=True,id='dFecha'
                ),
                dcc.Dropdown(
                estados,
                estados,multi=True,placeholder="Estados...",searchable=True,id='dEstado'
                ) ,
                
                html.P('Ordenes, Destinos'), 
                dcc.Dropdown(
                ordenes,
                ordenes,multi=True,placeholder="Ordenes...",searchable=True,id='dOrdenes'
                ),
                dcc.Dropdown(
                destinos,
                destinos,multi=True,placeholder="Destinos...",searchable=True,id='dDestinos'
                ) ,
                ]),

                html.Div([]),
                dcc.Graph(id='graph1',figure=fig8),
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
            ],
        ),
        html.Div(id="output-graph"),
        html.Div(id="output-table"),
    ],
)

@appkt.callback([Output("table1","data"),Output("table1","columns"),Output("graph1","figure")],[Input('dFecha','value'),Input('dEstado','value'),Input('dOrdenes','value'),Input('dDestinos','value')])
def updaTable(ifechas, iestados, iordenes, idestinos):
    dfa = dff[(dff.FECHA_SALIDA.isin(ifechas)) & (dff.ESTADO.isin(iestados)) & (dff.TIPO_ORDEN.isin(iordenes)) &(dff.DEST.isin(idestinos))]
    etasii = dfa.FECHA_SALIDA.unique()
    ordenesii = dfa.TIPO_ORDEN.unique()
 

    dfetasii = dfa.groupby('FECHA_SALIDA')['QTY'].sum()
    dfordenesii = dfa.groupby('TIPO_ORDEN')['QTY'].sum()

    fig8 = make_subplots(
    rows=1, cols=2,
    specs=[
           [{"type": "domain"}, {'type':'xy'}]],
     subplot_titles=("Tipos ods","FECHAS")
    )
    fig8.add_trace(go.Pie(labels=ordenesii, values=dfordenesii[ordenesii], name="Ordenes"), 1, 1)
    fig8.add_trace(go.Bar(x=etasii, y=dfetasii[etasii], name='Fechas'),1,2)
    
    dfffq = dfa.pivot_table( values = "QTY",index = ["FECHA_SALIDA"], columns = "ESTADO", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
    
    return dfffq.to_dict("records"), [{"name": c, "id": c} for c in dfffq.columns if c != 'id'], fig8

@appkt.callback([Output("output-table","children"),Input("table1", "active_cell"), State('dFecha','value'),State('dEstado','value'),State('dOrdenes','value'),State('dDestinos','value')])
def cell_clicked(active_cell, fechaj, estadoj, ordenj, destinosj):
    if active_cell is None:
        return no_update
    dfb = dff[(dff.FECHA_SALIDA.isin(fechaj)) & (dff.ESTADO.isin(estadoj)) & (dff.TIPO_ORDEN.isin(ordenj))& (dff.DEST.isin(destinosj)) ]
    row = active_cell["row"]
    col = active_cell["column_id"]
    dfc = dfb.pivot_table( values = "QTY",index = ["FECHA_SALIDA"], columns = "ESTADO", aggfunc=np.sum,margins = True, margins_name='Total').fillna(0).reset_index()
    fechaa= dfc.at[row, dfc.columns[0]]
    print('cumpli',col)
    print(fechaa)
    
    
    if fechaa=='Total':
        fig1 = dash_table.DataTable(
            id="table2",
            columns=[{"name": c, "id": c} for c in dfb.columns],
            data= dfb[(dfb['ESTADO']== col)].to_dict("records"),
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
        data=dfb[(dfb['FECHA_SALIDA'] == fechaa)&(dfb['ESTADO']== col)].to_dict("records"),
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

@appkt.callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page_content(pathname):
    return appktl


if __name__ == "__main__":
    appkt.run_server(debug=True)