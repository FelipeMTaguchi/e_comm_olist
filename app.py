import streamlit as st

from src.views.components import SatisfXDeliver 

# Configuração inicial da página no Streamlit
st.set_page_config(page_title="Dashboard de Logística", layout="wide")

st.title('Dashboard Corporativo de Logística')

# 1. Instanciando o componente guardado em components.py
MINHA_QUERY = "SELECT data, satisfacao, tempo_entrega FROM entregas ORDER BY data"

componente_grafico = SatisfXDeliver(
    id_graph="grafico_satisfacao_tempo",
    title="Evolução Temporal: Satisfação vs Tempo de Entrega",
    query=MINHA_QUERY,
    graph_s_color="turquoise",
    graph_d_color="gray"
)

# 2. Executa a busca no banco SQLite através da sua classe
dados_df = componente_grafico.run_query()

# 3. Gera o gráfico interativo do Plotly com o efeito "mouse on"
figura_interativa = componente_grafico.render_graph(dados_df)

# 4. Renderiza o gráfico na tela de forma nativa e responsiva
st.plotly_chart(figura_interativa, use_container_width=True)