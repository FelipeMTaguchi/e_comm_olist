import streamlit as st
import sqlite3
import pandas as pd

from src.views.components import SatisfXDeliver, InventoryHeatMap, ResponseTimeBarChart
from src.models.predictive_model import DeliveryRatingPredictor



st.set_page_config(page_title="Logistics Dashboard", layout="wide")


st.markdown(
    """
    <h2 style='text-align: center; margin-top: -40px; margin-bottom: 20px;'>
        Corporate Logistics Dashboard
    </h2>
    """, 
    unsafe_allow_html=True
)

predictor = DeliveryRatingPredictor()
r2_accuracy = predictor.train()

@st.cache_data
def get_all_categories():
    
    with sqlite3.connect("database/ecommerce.db") as conn:
        df = pd.read_sql_query(
            "SELECT DISTINCT product_category_name FROM products WHERE product_category_name IS NOT NULL ORDER BY product_category_name ASC;", 
            conn
        )
    return df['product_category_name'].tolist()

try:
    categories_list = get_all_categories()
except Exception:
  
    categories_list = ["perfumaria", "esporte_lazer", "utilidades_domesticas"]


left_column, right_column = st.columns(2)


with left_column:
    reports_map = {
        "General Overview (Average Lead Time)": "rating_querie_general.sql",
        "Delayed Orders Only (Average Delay Days)": "rating_querie_delay.sql",
        "Delay Rate Share (Percentage of Delayed Orders)": "rating_querie_percentage.sql"
    }

    selected_report_label = st.selectbox(
        label="Choose temporal analysis report:",
        options=list(reports_map.keys()),
        index=0
    )

    selected_filename = reports_map[selected_report_label]

    line_component = SatisfXDeliver(
        graph_id="satisfaction_time_chart",
        title=f"Temporal Evolution: {selected_report_label}",
        query_filename=selected_filename,
        graph_s_color="turquoise",
        graph_d_color="gray"
    )
    df_line_data = line_component.run_query()
    line_fig = line_component.render_graph(df_line_data)
    
    st.plotly_chart(line_fig, use_container_width=True, key=selected_filename)

    st.markdown("---")

    bar_component = ResponseTimeBarChart(
        graph_id="response_time_chart",
        title="SLA Breaches: Avg Company Response Time for Bad Reviews (Score ≤ 2)",
        query_filename="low_rating_response_time.sql",
        bar_color="red" 
    )

    df_bar_data = bar_component.run_query()
    bar_fig = bar_component.render_graph(df_bar_data)
    st.plotly_chart(bar_fig, use_container_width=True, key="response_time_bar_chart")

with right_column:
   
    selected_category = st.selectbox(
        label="Select Product Category for Inventory Strategy Map:",
        options=categories_list,
        index=0
    )

   
    map_component = InventoryHeatMap(
        graph_id="inventory_heatmap_chart",
        title=f"Geographic Distribution for: '{selected_category}'",
        query_filename="delivery_heatmap_by_category.sql"
    )
    
    
    df_map_data = map_component.run_query(params=[selected_category])
    
    
    map_fig = map_component.render_graph(df_map_data)
    
    st.plotly_chart(map_fig, use_container_width=True, key=f"map_{selected_category}")

    st.markdown("---")
    
   
    st.subheader("Predictive Satisfaction Simulator")
    st.caption("Simulate operational delivery scenarios to estimate customer churn risk based on machine learning data.")
    
    
    simulated_days = st.slider(
        label="Simulate Delivery Lead Time (Days relative to deadline):",
        min_value=-15,
        max_value=30,
        value=0, 
        step=1,
        help="Negative numbers mean early delivery. Positive numbers mean actual delay."
    )
    
    
    predicted_score = predictor.predict_score(simulated_days)
    
    
    metric_col1, metric_col2 = st.columns(2)
    
    with metric_col1:
        
        st.metric(
            label="Predicted Review Score",
            value=f"{predicted_score:.2f} / 5.0"
        )
        
    with metric_col2:
        
        st.metric(
            label="Model Variance Coverage (R² Accuracy)",
            value=f"{r2_accuracy * 100:.1f}%"
        )