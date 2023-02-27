import base64
import io

from datetime import datetime
import time

import dash
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table

import pandas as pd

from nltk.corpus import stopwords
import numpy as np
import re

stop_words = list(stopwords.words('spanish'))
app = dash.Dash(__name__, suppress_callback_exceptions=True)


#  ============================================================================
#  ======================================= layout =============================
#  ============================================================================

app.layout = html.Div([


    html.Div([

        #  ======================= Menu Desplegable =============================

        html.A([html.Img(src="./assets/simboloX.png",
                className="closebtn")], id="text", href="#"),
        html.A([html.P("Inicio")], href="#"),
        html.A([html.P("Opción 1")], href="#"),
        html.A([html.P("Opción 2")], href="#"),
        html.A([html.P("Opción 3")], href="#"),

        html.Div([
            html.H3("Cantidad de Palabras"),
            dcc.Slider(
                id='num-elementos-slider-2',
                min=10,
                max=50,
                tooltip={'always_visible': False},
                step=10,
                value=10,
            ),
        ], className="Slider"),

    ], className="sidebar", id="mySidebar"),


    #  ======================= Header =============================

    html.Div([
        html.H1(html.A("proyecto-Practica", href="http://127.0.0.1:8050")),
        html.Img(src="./assets/profile-pic (4).png")
    ], className="header", id="header"),

    #  ======================= Btn Menu =============================
    html.Div([
        html.Span([html.Img(src="./assets/menu.png", id="openNav")],
                  className="hola"),
    ], className="cont-btn-menu"),

    #  ======================= Boton bajar Archivos =============================

    html.Div([], className="alerta", id="alerta"),

    html.Div([



        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Arrastra o ',
                html.A('selecciona un archivo')
            ]),
            multiple=True
        ),
    ], className="contenedor", id="cont_id"),

    #  ======================= Todos los Graficos =============================

    html.Div([

        html.Div([

            #  ======================= Nombre del Archivo =============================

            html.H2(id="nombre_archivo"),
            html.Div([

                #  ======================= Cuarto Grafico =============================

                html.Div([
                    dcc.Graph(id='grafico-pastel')

                ], className="fig0 fig"),

                #  ======================= Primer Grafico =============================

                html.Div([
                    dcc.Graph(id='grafico-lineas')

                ], className="fig1 fig"),

                #  ======================= datos del archivo =============================

                html.Div([
                    html.Div([
                        html.Div(id="tiempo_carga"),
                        html.Div([
                            html.Img(src="./assets/bxs-time.svg")
                        ], className="img-fig2"),
                    ], className="hijo-fig2"),

                    html.Div([
                        html.Div(id="cantidad_caracteres"),
                        html.Div([
                            html.Img(src="./assets/bxs-data.svg")
                        ], className="img-fig2"),
                    ], className="hijo-fig2"),

                    html.Div([
                        html.Div(id="peso_archivo"),
                        html.Div([
                            html.Img(src="./assets/file-find-solid-24.png")
                        ], className="img-fig2"),

                    ], className="hijo-fig2")

                ], className="fig2 fig"),

                #  ======================= tercero grafico =============================

                html.Div([
                    # html.Div([
                    #     dcc.Slider(
                    #         id='num-elementos-slider',
                    #         min=1,
                    #         max=50,
                    #         step=5,
                    #         value=10,
                    #         vertical=True
                    #         # marks={i: str(i) for i in range(0, 51, 10)}
                    #     ),
                    # ]),
                    html.Div([
                        dcc.Graph(id="graficos_palabras")
                    ])

                    #  ======================= tercer grafico =============================

                ], className="fig3 fig"),

                html.Div([
                    html.Div([
                        dcc.Dropdown(['positivo', 'negativo',
                                      'neutro'], 'positivo', id="demo-dropdown"),
                    ]),

                    html.Div([
                        # html.Div([
                        #     dcc.Slider(
                        #         id='num-elementos-slider-2',
                        #         min=1,
                        #         max=40,
                        #         step=5,
                        #         value=10,
                        #         vertical=True,
                        #         className='my-slider'
                        #     ),
                        # ]),
                        html.Div([
                            dcc.Graph(id="graficos_palabras_2")
                        ])
                    ], className="contenedor_graph_palabras")


                ], className="fig4 fig"),

            ], className="cont_fig"),

        ], className="cont_secundario_fig")

    ], className="cont_principal_fig", id="alggo", style={'display': 'flex'}),


])

#  ============================================================================
#  =========================== primer grafico =============================
#  ============================================================================


@app.callback(Output('grafico-lineas', 'figure'), [
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename')
])
def update_graph(contents, filename):
    x = []
    y = []
    promedio = -1

    if contents:
        if validar_nombre(filename[0]):
            contents = contents[0]
            filename = filename[0]
            df = parse_data(contents, filename)

            if validar_columna(df):
                df = df.set_index(df.columns[0])
                promedio = round(df["puntaje"].mean(), 2)

    x = [""]
    if (promedio > 0):

        fig = go.Figure(
            data=[
                go.Bar(
                    x=[promedio],
                    y=x,
                    orientation='h',
                    marker=dict(
                        color='#1f77b4', opacity=0.2, line=dict(width=0))
                )
            ]
        )
        fig.update_layout(barmode='relative',
                          title_text='Promedio de analisis')
        fig.update_xaxes(range=[-1.2, 1.2])
    else:
        fig = go.Figure(
            data=[
                go.Bar(
                    x=[promedio],
                    y=x,
                    orientation='h',
                    marker=dict(
                        color='red', opacity=0.2, line=dict(width=0))
                )
            ]
        )
        fig.update_layout(barmode='relative',
                          title_text='analisis de sentimiento')
        fig.update_xaxes(range=[-1.2, 1.2])
    return fig


#  ============================================================================
#  =========================== segundo Graficos =============================
#  ============================================================================


@app.callback(Output('graficos_palabras', 'figure'), [
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename'),
    Input('num-elementos-slider-2', 'value')
])
def update_graph(contents, filename, num_elementos):
    palabras = []
    cantidad = []

    if contents:
        if validar_nombre(filename[0]):

            contents = contents[0]
            filename = filename[0]
            df = parse_data(contents, filename)

            if validar_columna(df):

                df_tidy = contruir_df(df)

                df_tidy_2 = df_tidy["token"].value_counts().reset_index(
                    name="conteo").rename(columns={"index": "palabra"})

                top_10_palabras = df_tidy_2.nlargest(
                    num_elementos, columns="conteo")

                palabras = top_10_palabras["palabra"]
                cantidad = top_10_palabras["conteo"]

    fig = go.Figure(
        data=[
            go.Bar(
                x=cantidad,
                y=palabras,
                orientation='h',
            )
        ]
    )
    fig.update_layout(title_text="Palabras generales")
    return fig

#  ============================================================================
#  =========================== tercer Graficos =============================
#  ============================================================================


@app.callback(Output('graficos_palabras_2', 'figure'), [
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename'),
    Input('num-elementos-slider-2', 'value'),
    Input('demo-dropdown', 'value')

])
def update_graph(contents, filename, num_elementos, dropdown):
    palabras = []
    cantidad = []

    if contents:
        if validar_nombre(filename[0]):
            contents = contents[0]
            filename = filename[0]

            df = parse_data(contents, filename)

            if validar_columna(df):
                df_tidy = contruir_df(df)

                tweets = df_tidy['token'][df_tidy["sentimiento"] == dropdown].value_counts().reset_index(
                    name="conteo").rename(columns={"index": "palabra"})

                top_10_palabras = tweets.nlargest(
                    num_elementos, columns="conteo")

                palabras = top_10_palabras["palabra"]
                cantidad = top_10_palabras["conteo"]

    fig = go.Figure(
        data=[
            go.Bar(
                x=cantidad,
                y=palabras,
                orientation='h',
            )
        ]
    )

    fig.update_layout(title_text=dropdown)

    return fig


#  ============================================================================
#  =========================== curato Graficos =============================
#  ============================================================================


@app.callback(Output('grafico-pastel', 'figure'), [
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename'),

])
def update_graph(contents, filename):

    night_colors = ['rgb(56, 75, 126)', 'rgb(18, 36, 37)', 'rgb(34, 53, 101)',
                    'rgb(36, 55, 57)', 'rgb(6, 4, 4)']
    list_senti = []
    list_conteo = []

    if contents:
        print(filename[0])
        if validar_nombre(filename[0]):
            contents = contents[0]
            filename = filename[0]
            df = parse_data(contents, filename)

            if validar_columna(df):

                valores = df["sentimiento"].value_counts().reset_index(
                    name="conteo").rename(columns={"index": "sentimiento"})

                list_senti = valores["sentimiento"]
                list_conteo = valores["conteo"]

    fig = go.Figure(
        data=[
            go.Pie(
                values=list_conteo,
                labels=list_senti,
                textinfo='label+percent',
                hole=.3,
                pull=[0, 0, 0.2, 0],
                marker_colors=night_colors
            )
        ]
    )

    fig.update_layout(title_text="Grafico Sentimientos")

    return fig


#  ============================================================================
#  =========================== titulo del archivo =============================
#  ============================================================================


@app.callback(Output('nombre_archivo', 'children'), [
    Input('upload-data', 'filename'),

])
def update_output(filename):
    nombre_archivo = []

    if filename:
        if validar_nombre(filename[0]):
            nombre_archivo = filename[0]
    return f'nombre del archivo: {nombre_archivo}'

#  ============================================================================
#  ============================= tiempo de carga =============================
#  ============================================================================


@app.callback(Output('tiempo_carga', 'children'), [
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename')
])
def update_output(contents, filename):
    tiempo_carga_rd = 0

    start_time = datetime.now()
    inicio_segundos = start_time.strftime("%S.%f")
    if contents:
        if validar_nombre(filename[0]):
            contents = contents[0]
            filename = filename[0]
            df = parse_data(contents, filename)
            df = df.set_index(df.columns[0])

    end_time = datetime.now()
    final_segundos = end_time.strftime("%S.%f")

    loading_time = float(final_segundos) - float(inicio_segundos)
    tiempo_carga_rd = round(loading_time, 2)
    return f'Tiempo de carga: {tiempo_carga_rd} sg'


#  ============================================================================
#  ============================= cantidad de datos =============================
#  ============================================================================

@app.callback(Output('cantidad_caracteres', 'children'), [
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename')
])
def update_output(contents, filename):

    cantidad = []

    if contents:
        if validar_nombre(filename[0]):
            contents = contents[0]
            filename = filename[0]
            df = parse_data(contents, filename)
            df = df.set_index(df.columns[0])
            cantidad = df.shape[0]

    return f'Elementos cargados: {cantidad}'


#  ============================================================================
#  ============================= tamaño de archivo =============================
#  ============================================================================

@app.callback(Output('peso_archivo', 'children'), [
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename')
])
def update_output(contents, filename):

    mb_size = 0
    kb_size = 0

    if contents:
        if validar_nombre(filename[0]):
            contents = contents[0]
            filename = filename[0]
            df = parse_data(contents, filename)
            df = df.set_index(df.columns[0])

            bytes_size = df.memory_usage().sum()

            if bytes_size >= 1024:

                kb_size = bytes_size / 1024
                return f'peso del archivo: {round(kb_size)} KB'

            elif kb_size >= 1024:
                mb_size = round(kb_size / 1024, 2)
                return f"peso del archivo: {mb_size} MB"


def parse_data(contents, filename):
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    try:
        if "csv" in filename:
            # Assume that the user uploaded a CSV or TXT file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif "xls" in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif "txt" or "tsv" in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            df = pd.read_csv(io.StringIO(
                decoded.decode("utf-8")), delimiter=r"\s+")
    except Exception as e:
        # print(e)
        return html.Div(["There was an error processing this file."])
    return df


@app.callback(
    Output('cont_id', 'style'),
    Output('alggo', 'style'),
    Output("alerta", 'children'),
    # Output('mensajeError', 'children'),
    Input('upload-data', 'filename'),
    Input('upload-data', 'contents')
)
def ocultar_upload(filename, contents):

    if filename:
        df = parse_data(contents[0], filename[0])

        if validar_nombre(filename[0]):

            if validar_columna(df):

                return {'display': 'none'}, {'display': 'flex'}, crearElementodiv("el archivo cargo correctamente", "-50%", "#090")

            else:

                return {'display': 'flex'}, {'display': 'none'}, crearElementodiv("verifique que el archivo tenga la columna Texto", "0", "#ED0007")

        else:
            return {'display': 'flex'}, {'display': 'none'}, crearElementodiv("Verifique que el archivo tenga la extencion .txt, .csv, .xls", "0", "#ED0007")

    else:
        return {'display': 'flex'}, {'display': 'none'}, crearElementodiv("esto es una prueba", "-50%", "#ED0007")


@app.callback(
    Output("alerta-mos", 'style'),
    Input('upload-data', 'filename'),
    Input('upload-data', 'contents')
)
def algo(contents, filename):
    if filename:

        if not validar_nombre(filename[0]):
            time.sleep(3.5)
            return {'left': '-50%'}

        df = parse_data(contents[0], filename[0])
        if not validar_columna(df):
            time.sleep(3.5)
            return {'left': '-50%'}
    else:
        return {'left': '-50%'}


def crearElementodiv(texto, porcentaje, bg):

    print(texto, porcentaje)

    return html.Div([
        html.P([texto], id="mensajeError", className="texto-alerta"),
        html.Div([
            html.Img(src="./assets/profile-pic (4).png",
                         className="img-alerta")
        ], className="cont-img-alerta", style={"background": bg}),
    ], id="alerta-mos", style={"position": "absolute", "left": porcentaje, "width": "400px", "background": bg}),


def limpiar_tokenizar(texto):
    '''
    Esta función limpia y tokeniza el texto en palabras individuales.
    El orden en el que se va limpiando el texto no es arbitrario.
    El listado de signos de puntuación se ha obtenido de: print(string.punctuation)
    y re.escape(string.punctuation)
    '''

    # Se convierte todo el texto a minúsculas
    nuevo_texto = texto.lower()
    # Eliminación de páginas web (palabras que empiezan por "http")
    nuevo_texto = re.sub('http\S+', ' ', nuevo_texto)
    # Eliminación de signos de puntuación
    regex = '[\\!\\"\\#\\$\\%\\&\\\'\\(\\)\\*\\+\\,\\-\\.\\/\\:\\;\\<\\=\\>\\?\\@\\[\\\\\\]\\^_\\`\\{\\|\\}\\~]'
    nuevo_texto = re.sub(regex, ' ', nuevo_texto)
    # Eliminación de números
    nuevo_texto = re.sub("\d+", ' ', nuevo_texto)
    # Eliminación de espacios en blanco múltiples
    nuevo_texto = re.sub("\\s+", ' ', nuevo_texto)
    # Tokenización por palabras individuales
    nuevo_texto = nuevo_texto.split(sep=' ')
    # Eliminación de tokens con una longitud < 2
    nuevo_texto = [token for token in nuevo_texto if len(token) > 1]

    return (nuevo_texto)


def contruir_df(data_frame):

    if "Texto" in data_frame:
        data_frame = data_frame.rename(columns={'Texto': 'texto'})

    data_frame['texto_tokenizado'] = data_frame['texto'].apply(
        lambda x: limpiar_tokenizar(x))
    df_tidy = data_frame.explode(column='texto_tokenizado')
    df_tidy = df_tidy.drop(columns='texto')
    df_tidy = df_tidy.rename(columns={'texto_tokenizado': 'token'})
    df_tidy = df_tidy[~(df_tidy["token"].isin(stop_words))]
    return df_tidy


def validar_nombre(filename):
    if ".xls" in filename or ".csv" in filename or ".xlsx" in filename:
        return True
    else:
        return False


def validar_columna(data_frame):

    if "texto" in data_frame.columns:
        return True

    elif "Texto" in data_frame.columns:
        return True

    else:
        return False


if __name__ == '__main__':
    app.run_server(debug=True)
