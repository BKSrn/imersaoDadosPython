import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Dashboard do projeto",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Carrega os dados da web
df = pd.read_csv("https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv")

# Título principal
st.title("📊 Dashboard do projeto")
st.markdown("Este é um dashboard interativo para análise de dados.")
st.markdown("---")

# Cria sidebar para filtros
st.sidebar.header("Filtros")

# Filtros de ano
anosDisponiveis = sorted(df['ano'].unique())
anosSelecionados = st.sidebar.multiselect("Selecione os anos:", anosDisponiveis, default=anosDisponiveis)
# Filtro de senioridade
senioridadesDisponiveis = sorted(df['senioridade'].unique())
senioridadesSelecionadas = st.sidebar.multiselect("Selecione as senioridades:", senioridadesDisponiveis, default=senioridadesDisponiveis)
# Filtro de contratos
contratosDisponiveis = sorted(df['contrato'].unique())
contratosSelecionados = st.sidebar.multiselect("Selecione os contratos:", contratosDisponiveis, default=contratosDisponiveis)

# Filtragem do DataFrame 
# O dataframe principal é filtrado com base nas seleções feitas na sidebar
dfFiltrado = df[
    (df['ano'].isin(anosSelecionados)) &
    (df['senioridade'].isin(senioridadesSelecionadas)) &
    (df['contrato'].isin(contratosSelecionados))
]

# Metricas Principais (KPIs) 
st.subheader("Métricas de Salário anual em USD")

if not dfFiltrado.empty:
    salario_medio = dfFiltrado['usd'].mean()
    salario_maximo = dfFiltrado['usd'].max()
    total_registros = dfFiltrado.shape[0]
    cargo_mais_frequente = dfFiltrado['cargo'].mode()[0]
else:
    salario_medio, salario_mediano, salario_maximo, total_registros, cargo_mais_comum = 0, 0, 0, ""

col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário médio", f"${salario_medio:,.0f}")
col2.metric("Salário máximo", f"${salario_maximo:,.0f}")
col3.metric("Total de registros", f"{total_registros:,}")
col4.metric("Cargo mais frequente", cargo_mais_frequente)
st.markdown("---")

# --- Análises Visuais com Plotly ---
st.subheader("Gráficos")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not dfFiltrado.empty:
        topCargos = dfFiltrado.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        graficoCargos = px.bar(
            topCargos,
            x='usd',
            y='cargo',
            orientation='h',
            title="Top 10 cargos por salário médio",
            labels={'usd': 'Média salarial anual (USD)', 'cargo': ''}
        )
        graficoCargos.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(graficoCargos, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de cargos.")


with col_graf2:
    if not dfFiltrado.empty:
        graficoHist = px.histogram(
            dfFiltrado,
            x='usd',
            nbins=30,
            title="Distribuição de salários anuais",
            labels={'usd': 'Faixa salarial (USD)', 'count': ''}  
        )
        graficoHist.update_layout(title_x=0.1)
        st.plotly_chart(graficoHist, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de distribuição.")

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not dfFiltrado.empty:
        remotoContagem = dfFiltrado['remoto'].value_counts().reset_index()
        remotoContagem.columns = ['tipo_trabalho', 'quantidade']
        graficoRemoto = px.pie(
            remotoContagem,
            names='tipo_trabalho',
            values='quantidade',
            title='Proporção dos tipos de trabalho',
            hole=0.5  
        )
        graficoRemoto.update_traces(textinfo='percent+label')
        graficoRemoto.update_layout(title_x=0.1)
        st.plotly_chart(graficoRemoto, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")

with col_graf4:
    if not dfFiltrado.empty:
        df_de = dfFiltrado[dfFiltrado['cargo'] == 'Data Engineer']
        media_de_pais = df_de.groupby('residencia_iso3')['usd'].mean().reset_index()
        graficoPaises = px.choropleth(
            media_de_pais,
            locations='residencia_iso3',
            color='usd',
            color_continuous_scale='rdylgn',
            title='Salário médio de Data Engineers por país',
            labels={'usd': 'Salário médio (USD)=', 'residencia_iso3': 'País='})
        graficoPaises.update_layout(title_x=0.1)
        st.plotly_chart(graficoPaises, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de países.") 


st.markdown("---")
st.subheader("Tabela de Dados Filtrados")
st.dataframe(dfFiltrado.drop(columns=['residencia_iso3']))
st.markdown("---")

# Footer
st.markdown(
    """
    <div style='text-align: center; margin-top: 50px; padding: 20px; background-color: #f0f2f6; border-radius: 10px;'>
        <h4 style='color: #262730; margin-bottom: 15px;'>📊 Dashboard de Análise de Dados</h4>
        <p style='color: #262730; margin-bottom: 10px; font-size: 14px;'>
            <strong>Desenvolvido com:</strong> 
            <span style='color: #ff4b4b;'> Streamlit</span> • 
            <span style='color: #636ef8;'> Plotly</span> • 
            <span style='color: #ff6b6b;'> Pandas</span>
        </p>
        <p style='color: #666; font-size: 12px; margin-bottom: 15px;'>
            Dashboard interativo para análise de salários e dados profissionais
        </p>
        <div style='margin-top: 15px; padding-top: 15px; border-top: 1px solid #ddd;'>
            <p style='color: #666; font-size: 11px; margin: 0;'>
                © 2025 • Projeto Alura • Dados atualizados dinamicamente
            </p>
            <p style='color: #888; font-size: 10px; margin: 5px 0 0 0;'>
                Última atualização: 08/2025
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Informações adicionais na sidebar
st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    ### ℹ️ Sobre este Dashboard
    
    **Funcionalidades:**
    - 📊 Análise de salários anual
    - 🏢 Filtros por senioridade
    - 📝 Tipos de contrato
    - 📈 Métricas em tempo real
    
    **Dados:**
    - Fonte: Dataset de salários
    - Atualizações: Dinâmicas
    
    **Tecnologias:**
    - Python 
    - Streamlit 
    - Plotly & Pandas
    """
)


