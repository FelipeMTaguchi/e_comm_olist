# Dashboard Corporativo de Logística & Fidelização - E-commerce Olist

Este projeto é um sistema analítico interativo voltado para a otimização logística e retenção de clientes em e-commerce, desenvolvido com foco em tomadas de decisão estratégicas. O dashboard conecta a performance de entrega das transportadoras com a satisfação final do consumidor, permitindo planejar estoques regionais e prever riscos operacionais.

---

## 🚀 Funcionalidades Principais

*   **Análise Temporal Dinâmica:** Gráfico de duas linhas comparando a evolução mensal da satisfação dos clientes (1 a 5 estrelas) com métricas de tempo de entrega e taxas de atraso.
*   **Inteligência Geográfica (Mapa de Calor):** Visualização coroplética do Brasil mapeando a densidade de pedidos por estado e categoria de produto. Utiliza normalização logarítmica para atenuar o viés de alta concentração no estado de São Paulo.
*   **Monitoramento de SLA de Suporte:** Gráfico de barras que acompanha o tempo médio (em horas) que a empresa leva para responder a avaliações críticas (Notas ≤ 2), isolando gargalos no atendimento.
*   **Simulador Preditivo (Machine Learning):** Simulador interativo que utiliza um modelo estatístico para prever o impacto de cenários operacionais (atrasos ou adiantamentos) na nota final do cliente.

---

## 🛠️ Arquitetura de Software e Organização do Código

O projeto foi construído seguindo rigorosos padrões de engenharia de software, garantindo manutenibilidade e escalabilidade do código:

*   **Programação Orientada a Objetos (POO):** Utilização de herança e polimorfismo através de uma classe base estrutural (`DashBComponents`), especializada em componentes visuais distintos (`SatisfXDeliver`, `InventoryHeatMap`, `ResponseTimeBarChart`).
*   **Separação de Responsabilidades (SoC):** As regras de negócio e consultas ao banco de dados estão 100% isoladas em arquivos físicos `.sql` na pasta `src/queries/`, permitindo alterações analíticas sem a necessidade de modificar o backend em Python.
*   **Encapsulamento de IA:** O ciclo de vida do modelo preditivo está isolado na classe `DeliveryRatingPredictor`, gerenciando autonomamente o carregamento de dados históricos, treinamento e inferência.
*   **Robustez de Caminhos:** Manipulação de caminhos absolutos de forma dinâmica com o módulo `os.path`, garantindo execução estável do sistema de forma offline e independente do diretório de chamada no terminal.

---

## 🧠 Lógica e Inteligência Preditiva

Para o simulador de satisfação, foi implementado um modelo de **Regressão Linear Simples** através da biblioteca `Scikit-Learn`. 
*   **Variável Independente (X):** Dias de atraso (valores positivos) ou dias de antecedência (valores negativos).
*   **Variável Dependente (Y):** Nota da avaliação (*Review Score* de 1.0 a 5.0).
*   **Poder Explicativo ($R^2$):** O modelo aponta uma variância de **7.1%**. Estatisticamente, isso comprova que, em cenários reais de comportamento humano no varejo digital, a eficiência logística isolada dita quase um décimo de toda a oscilação de humor e fidelidade do consumidor, validando investimentos em centros de distribuição descentralizados.

---

## 📦 Tecnologias Utilizadas

*   **Linguagem:** Python 3.12
*   **Interface Web:** Streamlit
*   **Banco de Dados:** SQLite
*   **Visualização de Dados:** Plotly (Express & Graph Objects) e Pandas
*   **Machine Learning:** Scikit-Learn e NumPy

---

## 🛠️ Como Executar o Projeto Localmente

1. Certifique-se de ter o banco de dados público da Olist convertido para SQLite na pasta `database/ecommerce.db`.
2. Certifique-se de possuir o arquivo de coordenadas geográficas `brazil-states.geojson` na raiz do projeto.
3. Instale as dependências necessárias no seu ambiente virtual:
   ```bash
   pip install streamlit pandas numpy plotly scikit-learn
   ```
4. Execute o dashboard através do terminal:
   ```bash
   streamlit run app.py
   ```
