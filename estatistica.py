import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from fpdf import FPDF
from datetime import datetime

# Carregar os dados
df = pd.read_csv('estatistica/estatistica.csv')

# Configuração do estilo dos gráficos
plt.style.use('default')  # Usando estilo padrão do matplotlib
sns.set_theme()  # Usando tema padrão do seaborn

# 1. Análise Estatística Descritiva
print("=== Estatísticas do Tempo de Atendimento ===")
estatisticas_atendimento = {
    'Média': df['service_time'].mean(),
    'Mediana': df['service_time'].median(),
    'Moda': df['service_time'].mode().values[0],
    'Variância': df['service_time'].var(),
    'Desvio Padrão': df['service_time'].std()
}

for stat, value in estatisticas_atendimento.items():
    print(f'{stat}: {value:.2f}')

print("\n=== Estatísticas do Tempo entre Chegadas ===")
estatisticas_chegadas = {
    'Média': df['interarrival_time'].mean(),
    'Mediana': df['interarrival_time'].median(),
    'Moda': df['interarrival_time'].mode().values[0],
    'Variância': df['interarrival_time'].var(),
    'Desvio Padrão': df['interarrival_time'].std()
}

for stat, value in estatisticas_chegadas.items():
    print(f'{stat}: {value:.2f}')

# 2. Geração de Gráficos
plt.figure(figsize=(15, 10))

# Histogramas
plt.subplot(2, 2, 1)
sns.histplot(data=df, x='interarrival_time', bins=30, color='#2ecc71')
plt.title('Histograma - Tempo entre Chegadas', fontsize=12)
plt.xlabel('Tempo (minutos)')
plt.ylabel('Frequência')

plt.subplot(2, 2, 2)
sns.histplot(data=df, x='service_time', bins=30, color='#3498db')
plt.title('Histograma - Tempo de Atendimento', fontsize=12)
plt.xlabel('Tempo (minutos)')
plt.ylabel('Frequência')

# Boxplots
plt.subplot(2, 2, 3)
sns.boxplot(data=df, y='interarrival_time', color='#2ecc71')
plt.title('Boxplot - Tempo entre Chegadas', fontsize=12)
plt.ylabel('Tempo (minutos)')

plt.subplot(2, 2, 4)
sns.boxplot(data=df, y='service_time', color='#3498db')
plt.title('Boxplot - Tempo de Atendimento', fontsize=12)
plt.ylabel('Tempo (minutos)')

plt.tight_layout()
plt.savefig('graficos_analise.png')
plt.close()

# 3. Intervalos de Confiança
def calcular_ic(dados, confianca):
    media = np.mean(dados)
    n = len(dados)
    std_erro = stats.sem(dados)
    ic = stats.t.interval(confianca, n-1, media, std_erro)
    return ic

niveis_confianca = [0.90, 0.95, 0.99]

print("\n=== Intervalos de Confiança para Tempo de Atendimento ===")
ic_atendimento = {}
for nivel in niveis_confianca:
    ic = calcular_ic(df['service_time'], nivel)
    ic_atendimento[nivel] = ic
    print(f'IC {nivel*100}%: [{ic[0]:.2f}, {ic[1]:.2f}]')

print("\n=== Intervalos de Confiança para Tempo entre Chegadas ===")
ic_chegadas = {}
for nivel in niveis_confianca:
    ic = calcular_ic(df['interarrival_time'], nivel)
    ic_chegadas[nivel] = ic
    print(f'IC {nivel*100}%: [{ic[0]:.2f}, {ic[1]:.2f}]')

# 4. Geração do Relatório PDF
def gerar_relatorio_pdf():
    pdf = FPDF()
    pdf.add_page()
    
    # Configuração de fonte
    pdf.set_font('Arial', 'B', 16)
    
    # Título
    pdf.cell(0, 10, 'Relatório de Análise Estatística', 0, 1, 'C')
    pdf.ln(10)
    
    # Data
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Data: {datetime.now().strftime("%d/%m/%Y")}', 0, 1)
    pdf.ln(10)
    
    # Estatísticas Descritivas
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Estatísticas Descritivas', 0, 1)
    pdf.ln(5)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Tempo entre Chegadas:', 0, 1)
    pdf.set_font('Arial', '', 12)
    for stat, value in estatisticas_chegadas.items():
        pdf.cell(0, 10, f'{stat}: {value:.2f}', 0, 1)
    pdf.ln(5)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Tempo de Atendimento:', 0, 1)
    pdf.set_font('Arial', '', 12)
    for stat, value in estatisticas_atendimento.items():
        pdf.cell(0, 10, f'{stat}: {value:.2f}', 0, 1)
    pdf.ln(10)
    
    # Intervalos de Confiança
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Intervalos de Confiança', 0, 1)
    pdf.ln(5)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Tempo entre Chegadas:', 0, 1)
    pdf.set_font('Arial', '', 12)
    for nivel, ic in ic_chegadas.items():
        pdf.cell(0, 10, f'IC {nivel*100}%: [{ic[0]:.2f}, {ic[1]:.2f}]', 0, 1)
    pdf.ln(5)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Tempo de Atendimento:', 0, 1)
    pdf.set_font('Arial', '', 12)
    for nivel, ic in ic_atendimento.items():
        pdf.cell(0, 10, f'IC {nivel*100}%: [{ic[0]:.2f}, {ic[1]:.2f}]', 0, 1)
    pdf.ln(10)
    
    # Interpretações e Sugestões
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Interpretações e Sugestões', 0, 1)
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, 'Interpretações:')
    pdf.multi_cell(0, 10, f'- O tempo médio entre chegadas é de {estatisticas_chegadas["Média"]:.2f} minutos')
    pdf.multi_cell(0, 10, f'- O tempo médio de atendimento é de {estatisticas_atendimento["Média"]:.2f} minutos')
    pdf.multi_cell(0, 10, f'- A variabilidade do tempo de atendimento (DP: {estatisticas_atendimento["Desvio Padrão"]:.2f}) indica a necessidade de padronização do processo')
    pdf.ln(5)
    
    pdf.multi_cell(0, 10, 'Sugestões de Melhoria:')
    pdf.multi_cell(0, 10, '1. Implementar sistema de agendamento para melhor distribuição das chegadas')
    pdf.multi_cell(0, 10, '2. Padronizar o processo de atendimento para reduzir a variabilidade')
    pdf.multi_cell(0, 10, '3. Considerar aumento do número de servidores em horários de pico')
    
    # Adicionar gráficos
    pdf.add_page()
    pdf.image('graficos_analise.png', x=10, y=10, w=190)
    
    pdf.output('relatorio_analise.pdf')

# Gerar o relatório PDF
gerar_relatorio_pdf()
print("\nRelatório gerado com sucesso em 'relatorio_analise.pdf'")