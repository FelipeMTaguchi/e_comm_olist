import sqlite3
import pandas as pd
import matplotlib as plt
import plotly.graph_objects as go

from plotly.subplots import make_subplots

DB_PATH = "database/ecommerce.db"

class DashBComponents:
    def __init__(self, id_graph, title, query):
        self.id_graph = id_graph
        self.title = title
        self.query = query

    @property
    def id_graph(self):
        return self._id_graph

    @id_graph.setter
    def id_graph(self, new_id):
        if new_id:
            self._id_graph = new_id
        else:
            raise ValueError ("Id field must not be empty")

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, querie_str):
        if isinstance(querie_str, str) and querie_str.strip():
            self._query = querie_str
        else:
            raise TypeError("Querie invalid")

    def run_query(self):
        with sqlite3.connect(DB_PATH) as connection:
            df = pd.read_sql_query(self.query, connection)
        return df

class SatisfXDeliver(DashBComponents):
    def __init__(self, id_graph, title, query, graph_s_color, graph_d_color):

        super().__init__(id_graph, title, query)
        self.graph_s_color = graph_s_color

    @property
    def graph_s_color(self):
        return self._graph_s_color

    @graph_s_color.setter
    def graph_s_color(self, color):
        if isinstance(color, str) and color.lower() in ('turquoise', 'red'):
            self._graph_s_color = color
        else:
            raise TypeError('Color field must be a text')
        
    @property
    def graph_d_color(self):
        return self._graph_d_color

    @graph_d_color.setter
    def graph_d_color(self, color):
    
        if isinstance(color, str) and color.lower() in ('gray', 'black'):
            self._graph_d_color = color
        else:
            raise TypeError('Color field must be a text')
        
    def render_graph(self, df):
        """
        Gera o gráfico interativo. 
        df deve conter as colunas: 'data', 'satisfacao' e 'tempo_entrega'
        """
        # Criando um gráfico com dois eixos Y (já que tempo e satisfação têm escalas diferentes)
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # 1. Linha de Satisfação
        fig.add_trace(
            go.Scatter(
                x=df['data'], 
                y=df['satisfacao'], 
                name="Satisfação",
                mode='lines+markers',
                line=dict(color=self.graph_s_color),
                # Customização do 'Mouse On' (Hover)
                hovertemplate="<b>Data:</b> %{x}<br><b>Satisfação:</b> %{y:.1f}/5<extra></extra>"
            ),
            secondary_y=False,
        )

        # 2. Linha de Tempo de Entrega
        fig.add_trace(
            go.Scatter(
                x=df['data'], 
                y=df['tempo_entrega'], 
                name="Tempo de Entrega (dias)",
                mode='lines+markers',
                line=dict(color=self.graph_d_color),
                # Customização do 'Mouse On' (Hover)
                hovertemplate="<b>Data:</b> %{x}<br><b>Tempo:</b> %{y} dias<extra></extra>"
            ),
            secondary_y=True,
        )

        # Configurações de layout e comportamento do mouse
        fig.update_layout(
            title_text=self.title,
            hovermode="x unified", # Faz o display mostrar os dois valores juntos ao passar o mouse na data
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        # Atualizando títulos dos eixos
        fig.update_xaxes(title_text="Period")
        fig.update_yaxes(title_text="Rating", secondary_y=False)
        fig.update_yaxes(title_text="Deliver time (days)", secondary_y=True)

        return fig