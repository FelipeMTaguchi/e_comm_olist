import os
import sqlite3
import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


DB_PATH = "database/ecommerce.db"
QUERIES_DIR = os.path.join("src", "queries")


class DashBComponents:
    def __init__(self, graph_id, title, query_filename):
        self.graph_id = graph_id
        self.title = title
        self.query = query_filename

    @property
    def graph_id(self):
        return self._graph_id

    @graph_id.setter
    def graph_id(self, new_id):
        if new_id:
            self._graph_id = new_id
        else:
            raise ValueError("Id field must not be empty")

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, query_filename):
        if isinstance(query_filename, str) and query_filename.strip().endswith('.sql'):
            full_path = os.path.join(QUERIES_DIR, query_filename)
            if os.path.exists(full_path):
                self._query = query_filename
            else:
                raise FileNotFoundError(f"SQL file not found at: {full_path}")
        else:
            raise TypeError("Query must be a valid '.sql' filename string")

    def run_query(self, params=None):
        full_path = os.path.join(QUERIES_DIR, self.query)
        with open(full_path, "r", encoding="utf-8") as f:
            sql_script = f.read()

        with sqlite3.connect(DB_PATH) as connection:
            df = pd.read_sql_query(sql_script, connection, params=params)
        return df


class SatisfXDeliver(DashBComponents):
    def __init__(self, graph_id, title, query_filename, graph_s_color, graph_d_color):
        super().__init__(graph_id, title, query_filename)
        self.graph_s_color = graph_s_color
        self.graph_d_color = graph_d_color

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
        """Generates interactive chart with forced high-contrast axes visibility."""
        if df.empty:
            fig = px.scatter(title="No data available for the selected period")
            return fig

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
            go.Scatter(
                x=df['date'], 
                y=df['satisfaction'], 
                name="Satisfaction",
                mode='lines+markers',
                marker=dict(size=6),
                line=dict(color=self.graph_s_color, width=2),
                hovertemplate="<b>Date:</b> %{x}<br><b>Satisfaction:</b> %{y:.2f}/5<extra></extra>"
            ),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(
                x=df['date'], 
                y=df['delivery_time'], 
                name="Delivery/Delay Metric",
                mode='lines+markers',
                marker=dict(size=6),
                line=dict(color=self.graph_d_color, width=2),
                hovertemplate="<b>Date:</b> %{x}<br><b>Value:</b> %{y}<extra></extra>"
            ),
            secondary_y=True,
        )

        fig.update_layout(
            title_text=self.title,
            title_font_size=16,
            hovermode="x unified",
            template="plotly_white",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        fig.update_yaxes(
            title_text="Rating Score (1-5)", 
            secondary_y=False,
            showgrid=True, 
            gridcolor="rgba(128, 128, 128, 0.2)",
            showline=True,
            linecolor="gray"
        )
        
        fig.update_yaxes(
            title_text="Logistics Scale Value", 
            secondary_y=True,
            showgrid=False,
            showline=True,
            linecolor="gray"
        )
        
        fig.update_xaxes(
            title_text="Timeline Period",
            showgrid=True,
            gridcolor="rgba(128, 128, 128, 0.2)",
            showline=True,
            linecolor="gray",
            type='category'
        )

        return fig


class InventoryHeatMap(DashBComponents):
    def __init__(self, graph_id, title, query_filename):
        super().__init__(graph_id, title, query_filename)
        
        
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        geojson_path = os.path.join(base_dir, "brazil_states.geojson")
        
        with open(geojson_path, "r", encoding="utf-8") as response:
            self.brazil_geojson = json.load(response)

    def render_graph(self, df):
        """Generates an interactive Choropleth Map of Brazil with a Logarithmic Color Scale."""
        if df.empty:
            fig = px.scatter(title="No data found for this category")
            return fig

        df['log_orders'] = np.log10(df['total_orders'] + 1)

        
        fig = px.choropleth(
            df,
            geojson=self.brazil_geojson,
            locations="state",       
            featureidkey="id", 
            color="log_orders",    
            color_continuous_scale="Blues", 
            title=self.title
        )

        fig.update_geos(
            fitbounds="locations", 
            visible=False
        )

        fig.update_layout(
            margin={"r":0,"t":40,"l":0,"b":0},
            title_font_size=16,
            coloraxis_colorbar=dict(
                title="Orders",
                tickvals=[np.log10(1), np.log10(10), np.log10(100), np.log10(1000), np.log10(10000)],
                ticktext=["1", "10", "100", "1K", "10K"]
            )
        )

        fig.update_traces(
            hovertemplate="<b>State:</b> %{location}<br><b>Total Orders:</b> %{customdata}<extra></extra>",
            customdata=df[['total_orders']]
        )

        return fig



class ResponseTimeBarChart(DashBComponents):
    def __init__(self, graph_id, title, query_filename, bar_color="red"):
        super().__init__(graph_id, title, query_filename)
        self.bar_color = bar_color

    def render_graph(self, df):
       
        if df.empty:
            fig = px.scatter(title="No low-rating response data available")
            return fig

        
        fig = px.bar(
            df,
            x="date",
            y="response_time_hours",
            title=self.title,
            template="plotly_white"
        )

        
        fig.update_traces(
            marker_color=self.bar_color,
            opacity=0.85,
            hovertemplate="<b>Month:</b> %{x}<br><b>Avg Response Time:</b> %{y:.1f} hours<extra></extra>"
        )

        fig.update_layout(
            hovermode="x unified",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            title_font_size=16
        )

        fig.update_yaxes(
            title_text="Avg Response (Hours)",
            showgrid=True,
            gridcolor="rgba(128, 128, 128, 0.2)",
            showline=True,
            linecolor="gray"
        )

        fig.update_xaxes(
            title_text="Timeline Period",
            showline=True,
            linecolor="gray",
            type='category'
        )

        return fig