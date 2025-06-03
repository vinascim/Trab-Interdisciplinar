# N2 Interdisciplinar

## 🎯 Finalidade do Projeto

Criar uma aplicação em Python capaz de simular filas com múltiplos atendentes, baseando-se no modelo M/M/c. A aplicação utilizará dados reais ou simulados a partir de arquivos CSV. Além da simulação, o projeto envolve análise estatística dos dados e aplicação de práticas ágeis com o framework Scrum.

---

## 🍽️ Cenário

**Ambiente simulado:** Clínica de vacinação

---

## 📊 Pesquisa Operacional

### 💻 Desenvolvimento da Simulação

- Importação de dados (tempos entre chegadas e tempos de atendimento) via CSV  
- Execução da simulação de filas com múltiplos servidores  
- Cálculo de métricas principais do sistema de filas:
  - **P₀**: Probabilidade de sistema vazio  
  - **Pᵉ**: Probabilidade de espera  
  - **L, Lq**: Clientes médios no sistema e na fila  
  - **W, Wq**: Tempos médios no sistema e na fila  

### 📈 Geração de Gráficos

- Evolução do tempo de espera por cliente  
- Variação do tamanho da fila ao longo da simulação  
- Níveis de ocupação dos atendentes  

### 📦 Entregas

- `simulacao.py`: Código-fonte da simulação  
- `resultados.csv`: Resultados gerados  
- `relatorio_operacional.pdf`: Relatório técnico contendo:
  - Métricas calculadas  
  - Gráficos  
  - Discussões:
    - Vale a pena adicionar mais um servidor?  
    - Qual seria o impacto de um servidor mais rápido (μ maior)?

---

## 📊 Estatística

### 🔍 Análise de Dados

- Estatísticas descritivas:
  - Média, Mediana, Moda, Variância, Desvio padrão  
- Visualizações:
  - Histogramas dos tempos  
  - Boxplots comparando atendimento e espera  
- Inferência:
  - Intervalos de confiança:
    - Média do tempo de atendimento  
    - Média do tempo de espera  

### 📦 Entregas

- `analise_estatistica.py` ou `.ipynb`: Código ou notebook  
- `relatorio_estatistico.pdf`: Inclui:
  - Resultados estatísticos  
  - Análises gráficas  
  - Sugestões de melhoria

---

## 🛠️ Engenharia de Software

### 📌 Metodologia Scrum

**Papéis do Scrum:**

- **Product Owner**: Define e prioriza o backlog  
- **Scrum Master**: Facilita o processo  
- **Equipe de Desenvolvimento**: Implementa o projeto  

**Exemplo de Backlog:**

- PB1: Leitura de CSV com Pandas – Sprint 1  
- PB2: Simulação M/M/c – Sprint 1  
- PB3: Cálculo de métricas – Sprint 1  
- PB4: Gráficos da simulação – Sprint 2  

**Planejamento das Sprints:**

- **Sprint 1**: Estrutura e simulação funcional  
- **Sprint 2**: Estatística e visualizações  
- **Sprint 3**: Finalização e interface  

**Organização com Kanban:** Trello, Planner, etc.

**Cerimônias Scrum:**

- Planejamento da Sprint  
- Daily Scrum  
- Sprint Review  
- Retrospectiva  

### 📦 Entregas

- `relatorio_scrum.pdf`: Inclui:
  - Backlog  
  - Prints das cerimônias  
  - Prints do quadro Kanban  

---

## 🔧 Versionamento com Git/GitHub

### ✔️ Boas Práticas

- Histórico de commits limpo  
- Commits bem descritos e segmentados por tarefa  
- Branches separadas por área do projeto
