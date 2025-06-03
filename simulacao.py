import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.special import factorial


plt.style.use('default') 
sns.set_theme() 

st.title("Simulação de Fila M/M/c - Restaurante Universitário")

uploaded_file = st.file_uploader("Faça upload do arquivo CSV com colunas 'Tempo_Espera' e 'Tempo_Atendimento'", type=["csv"])

c = st.number_input("Número de servidores (c)", min_value=1, max_value=10, value=3, step=1)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    if 'Tempo_Espera' not in df.columns or 'Tempo_Atendimento' not in df.columns:
        st.error("CSV deve conter colunas 'Tempo_Espera' e 'Tempo_Atendimento'")
    else:
        interarrival_times = df['Tempo_Espera'].values
        service_times = df['Tempo_Atendimento'].values
        
        # Simulação M/M/c
        arrival_times = np.cumsum(interarrival_times)
        n = len(arrival_times)
        start_service = np.zeros(n)
        end_service = np.zeros(n)
        servers_free_at = np.zeros(c)
        
        for i in range(n):
            arrival = arrival_times[i]
            service = service_times[i]
            server_index = np.argmin(servers_free_at)
            start = max(arrival, servers_free_at[server_index])
            servers_free_at[server_index] = start + service
            start_service[i] = start
            end_service[i] = start + service
        
        Wq = start_service - arrival_times
        W = end_service - arrival_times
        
        lam = 1 / np.mean(interarrival_times)
        mu = 1 / np.mean(service_times)
        rho = lam / (c * mu)
        
        def calc_p0(lam, mu, c, rho):
            sum_terms = sum(((lam/mu)**n) / factorial(n) for n in range(c))
            last_term = ((lam/mu)**c) / (factorial(c) * (1 - rho))
            return 1 / (sum_terms + last_term)
        
        P0 = calc_p0(lam, mu, c, rho)
        P_wait = (((lam/mu)**c) / factorial(c)) * (rho / (1 - rho)) * P0
        
        Lq = np.mean(Wq) / np.mean(service_times)
        L = np.mean(W) / np.mean(service_times)
        
        # Métricas em cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("P₀ (Sistema vazio)", f"{P0:.4f}")
            st.metric("Probabilidade de espera", f"{P_wait:.4f}")
        with col2:
            st.metric("Número médio na fila (Lq)", f"{Lq:.4f}")
            st.metric("Tempo médio de espera (Wq)", f"{np.mean(Wq):.4f}")
        with col3:
            st.metric("Tempo médio no sistema (W)", f"{np.mean(W):.4f}")
            st.metric("Número médio no sistema (L)", f"{L:.4f}")
        
        # Gráficos
        st.subheader("Visualizações")
        
        fig1, ax1 = plt.subplots(figsize=(12, 6))
        ax1.plot(range(n), Wq, marker='o', markersize=4, linestyle='-', linewidth=1, color='#2ecc71')
        ax1.set_title('Tempo de espera na fila por cliente', fontsize=14, pad=20)
        ax1.set_xlabel('Cliente', fontsize=12)
        ax1.set_ylabel('Tempo de espera (minutos)', fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.fill_between(range(n), Wq, alpha=0.2, color='#2ecc71')
        st.pyplot(fig1)
        
        time_points = np.linspace(0, max(end_service), 1000)
        queue_sizes = []
        for t in time_points:
            in_queue = np.sum((arrival_times <= t) & (start_service > t))
            queue_sizes.append(in_queue)
        
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        ax2.plot(time_points, queue_sizes, color='#e74c3c', linewidth=2)
        ax2.set_title('Tamanho da fila ao longo do tempo', fontsize=14, pad=20)
        ax2.set_xlabel('Tempo (minutos)', fontsize=12)
        ax2.set_ylabel('Número de clientes na fila', fontsize=12)
        ax2.grid(True, alpha=0.3)
        ax2.fill_between(time_points, queue_sizes, alpha=0.2, color='#e74c3c')
        st.pyplot(fig2)
        
        servers_busy = []
        for t in time_points:
            busy = np.sum((start_service <= t) & (end_service > t))
            servers_busy.append(busy)
        
        fig3, ax3 = plt.subplots(figsize=(12, 6))
        ax3.plot(time_points, servers_busy, color='#3498db', linewidth=2)
        ax3.set_title('Ocupação dos servidores ao longo do tempo', fontsize=14, pad=20)
        ax3.set_xlabel('Tempo (minutos)', fontsize=12)
        ax3.set_ylabel('Número de servidores ocupados', fontsize=12)
        ax3.grid(True, alpha=0.3)
        ax3.fill_between(time_points, servers_busy, alpha=0.2, color='#3498db')
        ax3.set_ylim(0, c) 
        st.pyplot(fig3)
        
        
        # Exportar resultados
        results = pd.DataFrame({
            'arrival_time': arrival_times,
            'start_service': start_service,
            'end_service': end_service,
            'wait_time': Wq,
            'total_time': W
        })
        csv = results.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download resultados da simulação (CSV)",
            data=csv,
            file_name='resultados_simulacao.csv',
            mime='text/csv',
        ) 