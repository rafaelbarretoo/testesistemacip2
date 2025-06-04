import streamlit as st
import pandas as pd
import os
import io
import plotly.express as px
from PIL import Image

# Configuração da página
st.set_page_config(
    page_title="📊 Projeto", 
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
        .abstencao-row {
            background-color: #fff3cd !important;
        }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho
image = Image.open('headerresul.png')
st.image(image, use_container_width=True)

st.markdown("""
    <div class="main-header">
        <h1 style='margin:0;'>Projeto CIP 2025</h1>
        <p style='margin:0; font-size:1.1rem;'>SUP - Ger - Proponente</p>
    </div>
""", unsafe_allow_html=True)

# Processamento dos dados
arquivo = "avaliacoes01.xlsx"

if os.path.exists(arquivo):
    df = pd.read_excel(arquivo)
    
    # Criar cópia para exibição
    df_display = df.copy()
    
    # Filtrar apenas avaliações válidas (não abstenções)
    df_calculos = df[df['Abstenção'] != 'Sim'].copy()
    
    # Verificar se há avaliações válidas
    tem_avaliacoes_validas = not df_calculos.empty
    
    # Cálculos das médias (apenas se houver avaliações válidas)
    if tem_avaliacoes_validas:
        media_geral_final = df_calculos["Média Final"].mean()
        media_problema = df_calculos["Média Problema"].mean()
        media_solucao = df_calculos["Média Solução"].mean()
        
        # Status do projeto
        if media_geral_final > 3.9:
            status = "APROVADA"
            cor_status = "#28a745"
            emoji_status = "🟢"
        elif media_geral_final > 2:
            status = "REVISÃO"
            cor_status = "#ffc107"
            emoji_status = "🟡"
        else:
            status = "REPROVADA"
            cor_status = "#dc3545"
            emoji_status = "🔴"
    else:
        media_geral_final = media_problema = media_solucao = 0
        status = "SEM AVALIAÇÕES VÁLIDAS"
        cor_status = "#6c757d"
        emoji_status = "❓"

    # MÉTRICAS PRINCIPAIS
    st.markdown("### 📊 Resumo das Avaliações")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        valor = f"{media_problema:.2f}" if tem_avaliacoes_validas else 'N/A'
        progresso = media_problema if tem_avaliacoes_validas else 0
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem; color: #6c757d;">Média Problema</div>
                <div style="font-size: 1.8rem; font-weight: bold; color: #4B0082;">{valor}</div>
                <progress value="{progresso}" max="5" style="width:100%; height:6px; border-radius:3px;"></progress>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        valor = f"{media_solucao:.2f}" if tem_avaliacoes_validas else 'N/A'
        progresso = media_solucao if tem_avaliacoes_validas else 0
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem; color: #6c757d;">Média Solução</div>
                <div style="font-size: 1.8rem; font-weight: bold; color: #4B0082;">{valor}</div>
                <progress value="{progresso}" max="5" style="width:100%; height:6px; border-radius:3px;"></progress>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        valor = f"{media_geral_final:.2f}" if tem_avaliacoes_validas else 'N/A'
        progresso = media_geral_final if tem_avaliacoes_validas else 0
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem; color: #6c757d;">Média Geral</div>
                <div style="font-size: 1.8rem; font-weight: bold; color: #4B0082;">{valor}</div>
                <progress value="{progresso}" max="5" style="width:100%; height:6px; border-radius:3px;"></progress>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem; color: #6c757d;">Status do Projeto</div>
                <div style="font-size: 1.8rem; font-weight: bold; color: {cor_status};">{emoji_status} {status}</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Gráfico de médias por avaliador (apenas avaliações válidas)
    with st.expander("📈 Médias por Avaliador", expanded=True):
        if tem_avaliacoes_validas:
            colunas_medias = ["Avaliador", "Média Problema", "Média Solução", "Média Final"]
            df_medias = df_calculos[colunas_medias]
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
        else:
            st.warning("Não há avaliações válidas para exibir o gráfico.")

    # Tabela de médias (mostrando todos, mas destacando abstenções)
    with st.expander("📋 Tabela de Médias Por Avaliador", expanded=True):
        colunas_medias = ["Avaliador", "Abstenção", "Média Problema", "Média Solução", "Média Final"]
        if not df.empty:
            df_medias = df_display[colunas_medias].copy()
            df_medias.index = df_medias.index + 1
            
            # Aplicar estilo
            def highlight_abstencao(row):
                if row['Abstenção'] == 'Sim':
                    return ['background-color: #fff3cd'] * len(row)
                return [''] * len(row)
            
            st.dataframe(
                df_medias.style.apply(highlight_abstencao, axis=1).format(
                    na_rep="Abstenção", 
                    subset=["Média Problema", "Média Solução", "Média Final"]
                ),
                use_container_width=True
            )
        else:
            st.warning("Nenhum dado disponível.")

    # Tabela completa
    with st.expander("📋 Tabela Completa", expanded=False):
        if not df.empty:
            df_display.index = df_display.index + 1
            st.dataframe(
                df_display.style.format(na_rep="Abstenção"),
                use_container_width=True
            )
        else:
            st.warning("Nenhum dado disponível.")

    # Matriz de análise (apenas avaliações válidas)
    with st.expander("📊 Matriz de Análise: Problema vs Solução", expanded=False):
        if tem_avaliacoes_validas:
            fig_matrix = px.scatter(
                df_calculos,
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
        else:
            st.warning("Não há avaliações válidas suficientes para exibir a matriz.")

    # Estatísticas por critério (apenas avaliações válidas)
    with st.expander("📊 Estatísticas por Critério", expanded=False):
        if tem_avaliacoes_validas:
            numeric_cols = df_calculos.select_dtypes(include=['float64', 'int64']).columns
            estatisticas = df_calculos[numeric_cols].describe().T[["mean", "std"]]
            estatisticas = estatisticas.rename(columns={"mean": "Média", "std": "Desvio Padrão"})
            st.dataframe(
                estatisticas.style.format("{:.2f}"),
                use_container_width=True
            )
        else:
            st.warning("Não há avaliações válidas para calcular estatísticas.")
   
    # COMENTÁRIOS DOS AVALIADORES (mostra todos, incluindo abstenções)
    st.markdown("### 💬 Comentários dos Avaliadores")
    
    if not df.empty and "Avaliador" in df.columns and "Observação" in df.columns:
        for index, row in df.iterrows():
            comentario = row['Observação'] if pd.notna(row['Observação']) else "Sem comentários registrados"
            if row['Abstenção'] == 'Sim':
                comentario = "Avaliador optou por abster-se"
            
            st.markdown(f"""
                <div class="comment-box">
                    <div style="font-weight: bold; color: #4B0082;">{row['Avaliador']} 
                        <span style="font-size: 0.8rem; color: #6c757d;">
                            {'🔘 Abstenção' if row['Abstenção'] == 'Sim' else '✅ Avaliado'}
                        </span>
                    </div>
                    <div style="margin-top: 0.5rem;">{comentario}</div>
                </div>
            """, unsafe_allow_html=True)

    # STATUS DAS AVALIAÇÕES (conta todos os registros)
    st.markdown("### 📌 Status das Avaliações")
    
    avaliadores_esperados = 8
    total_avaliadores = df["Avaliador"].nunique()
    avaliadores_validos = len(df_calculos)
    avaliadores_pendentes = max(0, avaliadores_esperados - total_avaliadores)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem; color: #6c757d;">Registros Totais</div>
                <div style="font-size: 1.8rem; font-weight: bold; color: #4B0082;">{total_avaliadores}</div>
                <progress value="{total_avaliadores}" max="{avaliadores_esperados}" style="width:100%; height:6px; border-radius:3px;"></progress>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem; color: #6c757d;">Avaliações Válidas</div>
                <div style="font-size: 1.8rem; font-weight: bold; color: #28a745;">{avaliadores_validos}</div>
                <progress value="{avaliadores_validos}" max="{avaliadores_esperados}" style="width:100%; height:6px; border-radius:3px;"></progress>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem; color: #6c757d;">Avaliações Pendentes</div>
                <div style="font-size: 1.8rem; font-weight: bold; color: #4B0082;">{avaliadores_pendentes}</div>
                <progress value="{avaliadores_pendentes}" max="{avaliadores_esperados}" style="width:100%; height:6px; border-radius:3px;"></progress>
            </div>
        """, unsafe_allow_html=True)

    # EXPORTAÇÃO DE DADOS (exporta tudo, incluindo abstenções)
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
