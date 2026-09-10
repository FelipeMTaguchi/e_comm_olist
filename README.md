# 📊 Brazilian E-Commerce Analytics Dashboard
Este repositório contém uma aplicação web analítica e interativa desenvolvida em Python e algumas de suas bibliotecas, projetada para explorar, analisar e manipular dados do ecossistema de e-commerce brasileiro.O diferencial técnico deste projeto está na fusão da Análise de Dados com a Engenharia de Software, utilizando Programação Orientada a Objetos (POO) e padrões de arquitetura corporativa para criar um dashboard modular e extensível.🎯 Objetivo do ProjetoDemonstrar como transformar dados brutos em decisões de negócios através de uma infraestrutura limpa, eficiente e de alta performance. A aplicação simula o gerenciamento de relatórios visuais onde cada gráfico funciona como um componente independente, permitindo operações dinâmicas em tempo real.

# 🛠️ Arquitetura e Engenharia de Dados
A arquitetura do projeto foi desenhada seguindo princípios de responsabilidade única e otimização de memória, dividida em três pilares fundamentais:Ingestão e Armazenamento (SQLite3): Os dados originais em formato .csv (extraídos do Kaggle) foram modelados e indexados dentro de um banco de dados relacional local (.db).Otimização de Performance (Abordagem Híbrida): Diferente de abordagens amadoras que carregam tabelas inteiras na memória com o Pandas, este projeto utiliza queries SQL dinâmicas armazenadas em variáveis para filtrar e agregar os dados diretamente no motor do banco de dados. O Pandas é acionado exclusivamente na camada final para estruturar os dados que alimentam os gráficos.CRUD Componentizado (POO): Cada gráfico do dashboard é uma instância de uma classe herdada. Isso permite que cada componente visual gerencie seu próprio ciclo de vida através de métodos específicos:Read: Busca os dados atualizados via SQL.Update: Modifica a query dinamicamente com base nos filtros do usuário.Delete/Toggle: Manipula a visibilidade e o layout do componente na interface.

# 📂 Estrutura do Repositório
text├── database/
│   └── ecommerce.db          # Banco de Dados SQLite3 com as tabelas indexadas
├── src/
│   ├── database_connect.py   # Gerenciamento de conexões e sessões do banco
│   ├── models.py             # Definição das classes e abstração dos componentes
│   ├── controllers.py        # Lógica do CRUD e execução das queries SQL
│   └── views/
│       └── components.py     # Estilização dos gráficos (Matplotlib/Seaborn)
├── app.py                    # Arquivo principal de execução do Streamlit
├── requirements.txt          # Dependências do projeto
└── README.md                 # Documentação

# 🚀 Tecnologias Utilizadas
Python 3.x como linguagem core.Streamlit para a construção da interface web interativa.SQLite3 para o gerenciamento e persistência de dados estruturados.Pandas para manipulação fina de matrizes de dados.Matplotlib & Seaborn para a criação de data visualizations limpas e profissionais.
# 📈 Principais Insights de Negócio Disponíveis
**Análise de comportamento de compra por estado brasileiro (Geolocalização).**
**Gargalos logísticos e tempo médio de entrega por região.**
**Evolução do faturamento (GMV) e identificação de sazonalidade de vendas.**
**Segmentação de produtos e categorias mais lucrativas.**
