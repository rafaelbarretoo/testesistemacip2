
import streamlit as st
import pandas as pd
import os
import io
import plotly.express as px
from PIL import Image

# Configuração da página
st.set_page_config(
    page_title="📊 Projeto ", 
    page_icon="📊",
    layout="wide"
)

# Estilos CSS consistentes
st.markdown("""
    <style>
        .stApp {
            background-color: #f8f9fa;
        }
        .main-header {
            color: #4B0082;
            text-align: center;
            padding: 1rem;
            border-bottom: 2px solid #4B0082;
            margin-bottom: 2rem;
        }
        .metric-card {
            border-radius: 10px;
            padding: 1.5rem;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
            border-left: 4px solid #4B0082;
        }
        .comment-box {
            background-color: #f8f9fa;
            border-radius: 5px;
            padding: 1rem;
            margin-bottom: 1rem;
            border-left: 4px solid #4B0082;
        }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho
image = Image.open('headerresul.png')
st.image(image, use_container_width=True)

st.markdown("""
    <div class="main-header">
        <h1 style='margin:0;'> Projeto </h1>
        <p style='margin:0; font-size:1.1rem;'>SUP - Ger - Proponente</p>
    </div>
""", unsafe_allow_html=True)

# Processamento dos dados
arquivo = "avaliacoes02.xlsx"

if os.path.exists(arquivo):
    df = pd.read_excel(arquivo)
    
    # Cálculos das médias
    media_geral_final = df["Média Final"].mean()
    media_problema = df["Média Problema"].mean()
    media_solucao = df["Média Solução"].mean()
    
    # Status do projeto
    status = "APROVADA" if media_geral_final > 3.9 else "REVISÃO" if media_geral_final > 2 else "REPROVADA"
    cor_status = "#28a745" if media_geral_final > 3.9 else "#ffc107" if media_geral_final > 2 else "#dc3545"
    emoji_status = "🟢" if media_geral_final > 3.9 else "🟡" if media_geral_final > 2 else "🔴"

    # MÉTRICAS PRINCIPAIS
    
    st.markdown("### 📊 Resumo das Avaliações")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem; color: #6c757d;">Média Problema</div>
                <div style="font-size: 1.8rem; font-weight: bold; color: #4B0082;">{media_problema:.2f}</div>
                <progress value="{media_problema}" max="5" style="width:100%; height:6px; border-radius:3px;"></progress>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem; color: #6c757d;">Média Solução</div>
                <div style="font-size: 1.8rem; font-weight: bold; color: #4B0082;">{media_solucao:.2f}</div>
                <progress value="{media_solucao}" max="5" style="width:100%; height:6px; border-radius:3px;"></progress>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem; color: #6c757d;">Média Geral</div>
                <div style="font-size: 1.8rem; font-weight: bold; color: #4B0082;">{media_geral_final:.2f}</div>
                <progress value="{media_geral_final}" max="5" style="width:100%; height:6px; border-radius:3px;"></progress>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem; color: #6c757d;">Status do Projeto</div>
                <div style="font-size: 1.8rem; font-weight: bold; color: {cor_status};">{emoji_status} {status}</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Gráfico de médias por avaliador
    with st.expander("Médias por Avaliador"):
        st.markdown("#### 📈Médias por Avaliador")
        colunas_medias = ["Avaliador", "Média Problema", "Média Solução", "Média Final"]
        df_medias = df[colunas_medias]
        df_plot = df_medias.melt(id_vars=["Avaliador"], var_name="Critério", value_name="Nota")
    
        fig = px.bar(df_plot, x="Avaliador", y="Nota", color="Critério", barmode="group",
                color_discrete_map={
                    "Média Problema": "#6f42c1",
                    "Média Solução": "#007bff",
                    "Média Final": "#4B0082"
                },
                height=400)
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

if os.path.exists(arquivo):
    df = pd.read_excel(arquivo)
   

    # Tabela de médias
    colunas_medias = [
        "Avaliador",
        "Média Problema",
        "Média Solução",
        "Média Final"
    ]
    with st.expander("**Tabela de Médias Por Avaliador**"):
        df_medias = df[colunas_medias]    
        st.subheader("📋 Tabela de Médias por Avaliador")
        df_medias.index = df_medias.index +1
        st.dataframe(df_medias)
    
    # Tabela completa
    with st.expander("**Tabela Completa**"):
        st.subheader("📋 Tabela Completa")
        df.index = df.index +1
        df.name= "Posição"
        st.dataframe(df)
        media_colunas = df.mean(numeric_only= True)
    #st.write("Média de cada critério")
    #st.dataframe(media_colunas.to_frame(name="Média").T)

    # Matriz de análise
    st.markdown("#### Matriz de Análise: Problema vs Solução")
    if "Média Problema" in df.columns and "Impacto da Solução" in df.columns:
        fig_matrix = px.scatter(
            df,
            x="Média Problema",
            y="Média Solução",
            color="Avaliador",
            size="Média Final",
            hover_data=["Média Solução"],
            color_discrete_sequence=px.colors.qualitative.Dark24,
            height=500
        )
        fig_matrix.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_matrix, use_container_width=True)

    with st.expander("**Estatísticas por Critério**"):
        st.markdown("Estatísticas por Critério")
        estatisticas = df.describe().T[["mean", "std"]].rename(columns={"mean":"Média","std":"Desvio Padrão"})
        st.dataframe(estatisticas.style.format("{:.2f}"), use_container_width= True)
  
   
    # COMENTÁRIOS DOS AVALIADORES
   
    
    st.markdown("### 💬 Comentários dos Avaliadores")
    
    if "Avaliador" in df.columns and "Observação" in df.columns:
        for index, row in df.iterrows():
            if pd.notna(row["Observação"]):
                st.markdown(f"""
                    <div class="comment-box">
                        <div style="font-weight: bold; color: #4B0082;">{row['Avaliador']}</div>
                        <div style="margin-top: 0.5rem;">{row['Observação']}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="padding: 1rem; background-color: #f8f9fa; border-radius: 5px; margin-bottom: 1rem;">
                        <div style="font-weight: bold; color: #4B0082;">{row['Avaliador']}</div>
                        <div style="margin-top: 0.5rem; color: #6c757d;">Sem comentários registrados</div>
                    </div>
                """, unsafe_allow_html=True)

    # ==============================================
    # STATUS DAS AVALIAÇÕES
    # ==============================================
    
    st.markdown("### 📌 Status das Avaliações")
    
    avaliadores_esperados = 8
    total_avaliadores = df["Avaliador"].nunique()
    avaliadores_pendentes = max(0, avaliadores_esperados - total_avaliadores)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem; color: #6c757d;">Avaliações Realizadas</div>
                <div style="font-size: 1.8rem; font-weight: bold; color: #4B0082;">{total_avaliadores}</div>
                <progress value="{total_avaliadores}" max="{avaliadores_esperados}" style="width:100%; height:6px; border-radius:3px;"></progress>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem; color: #6c757d;">Avaliações Pendentes</div>
                <div style="font-size: 1.8rem; font-weight: bold; color: #4B0082;">{avaliadores_pendentes}</div>
                <progress value="{avaliadores_pendentes}" max="{avaliadores_esperados}" style="width:100%; height:6px; border-radius:3px;"></progress>
            </div>
        """, unsafe_allow_html=True)

    # ==============================================
    # EXPORTAÇÃO DE DADOS
    # ==============================================
    
    st.markdown("### 📤 Exportar Dados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # CSV
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        st.download_button(
            "📥 Download como CSV",
            csv_buffer.getvalue(),
            file_name="avaliacoes.csv",
            mime="text/csv"
        )
    
    with col2:
        # Excel
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        st.download_button(
            "📊 Download como Excel",
            excel_buffer.getvalue(),
            file_name="avaliacoes.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

else:
    st.markdown("""
        <div style="text-align: center; padding: 2rem; background-color: #f8f9fa; border-radius: 10px;">
            <h3 style='color: #6c757d;'>📭 Nenhum dado disponível</h3>
            <p>Ainda não há avaliações registradas.</p>
        </div>
    """, unsafe_allow_html=True)

# Rodapé
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #6c757d; font-size: 0.9rem;">
        CIP - Central de Inovações e Projetos | Versão 2.0
    </div>
""", unsafe_allow_html=True)

st.page_link("🏠_Home.py", label="Home", icon="🏠")