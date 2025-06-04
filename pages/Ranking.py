import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image

# Configuração da página com layout mais amplo
st.set_page_config(
    page_title="📈 Ranking de Projetos", 
    page_icon="📈",
    layout="wide"
)

# ESTILOS E CSS CUSTOMIZADO
st.markdown("""
    <style>
        /* Estilos gerais */
        .stApp {
            background-color: #f8f9fa;
        }
        
        /* Cabeçalhos */
        .main-header {
            color: #4B0082;
            text-align: center;
            padding: 1rem;
            border-bottom: 2px solid #4B0082;
            margin-bottom: 2rem;
        }
        
        /* Cards */
        .custom-card {
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            background: white;
            border-left: 4px solid #4B0082;
        }
        
        /* Dataframes */
        .stDataFrame {
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        /* Títulos */
        .section-title {
            color: #4B0082;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }
        
        /* Rodapé */
        .footer {
            text-align: center;
            color: #6c757d;
            font-size: 0.9rem;
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid #dee2e6;
        }
    </style>
""", unsafe_allow_html=True)

# CABEÇALHO
image = Image.open('headerRank.png')
st.image(image, use_container_width=True)

# TÍTULO PRINCIPAL
st.markdown("""
    <div class="main-header">
        <h1 style='margin:0;'>📈 Ranking de Projetos</h1>
        <p style='margin:0; font-size:1.1rem;'>Comparativo de Avaliações</p>
    </div>
""", unsafe_allow_html=True)

# Importando Arquivos DF
arquivo1 = "avaliacoes01.xlsx"
arquivo2 = "avaliacoes02.xlsx"

# Colunas Desejadas
colunas_desejadas = [
    "Média Problema",
    "Média Solução",
    "Média Formulário",
    "Média Final",
    "Avaliador"
]

# Verificação dos arquivos
if not os.path.exists(arquivo1) or not os.path.exists(arquivo2):
    st.error("Arquivos não encontrados")
else:
    df1 = pd.read_excel(arquivo1)
    df2 = pd.read_excel(arquivo2)
    
    # Container para o ranking geral
    with st.container():
        st.markdown("""
            <div class="custom-card">
                <h2 style='color: #4B0082; text-align: center;'>🏆 Ranking Geral</h2>
            </div>
        """, unsafe_allow_html=True)
        
        if "Média Final" in df1.columns and "Média Final" in df2.columns:
            media_geral_1 = df1["Média Final"].mean()
            media_geral_2 = df2["Média Final"].mean()

            ranking_df = pd.DataFrame({
                "Projeto": ["Projeto 1", "Projeto 2"],  # Substituir pelos nomes reais
                "Média Final": [media_geral_1, media_geral_2]
            }).sort_values(by="Média Final", ascending=False).reset_index(drop=True)
            
            ranking_df.index = ranking_df.index + 1
            ranking_df.index.name = "Posição"

            # Exibição do ranking com estilo
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("**Ranking Comparativo**")
                st.dataframe(
                    ranking_df.style.format({"Média Final": "{:.2f}"}),
                    height=150,
                    use_container_width=True
                )
            
            with col2:
                st.markdown("**Visualização Gráfica**")
                fig_rank = px.bar(
                    ranking_df,
                    x="Projeto",
                    y="Média Final",
                    color="Projeto",
                    text="Média Final",
                    labels={"Média Final": "Média"},
                    color_discrete_sequence=["#4B0082", "#011B70"]
                )
                fig_rank.update_traces(
                    texttemplate='%{text:.2f}',
                    textposition='outside',
                    marker_line_color='rgb(8,48,107)',
                    marker_line_width=1.5
                )
                fig_rank.update_layout(
                    yaxis_range=[0, max(ranking_df["Média Final"] * 1.2)],
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_rank, use_container_width=True)

    # Comparação por critérios
    st.markdown("""
        <div class="custom-card">
            <h2 style='color: #4B0082; text-align: center;'>📊 Análise por Critérios</h2>
        </div>
    """, unsafe_allow_html=True)
    
    colunas_comuns = df1.columns.intersection(df2.columns)
    colunas_validas = [col for col in colunas_desejadas if col in colunas_comuns]

    if not colunas_validas:
        st.warning("Nenhuma das colunas desejadas está presente em ambos os arquivos.")
    else:
        for coluna in colunas_validas:
            if pd.api.types.is_numeric_dtype(df1[coluna]) and pd.api.types.is_numeric_dtype(df2[coluna]):
                if "Avaliador" in df1.columns and "Avaliador" in df2.columns:
                    with st.expander(f"🔍 {coluna}", expanded=False):
                        st.markdown(f"<h3 style='color: #011B70;'>{coluna}</h3>", unsafe_allow_html=True)
                        
                        media1 = df1.groupby("Avaliador")[coluna].mean()
                        media2 = df2.groupby("Avaliador")[coluna].mean()

                        comparacao = pd.concat([media1, media2], axis=1, 
                                              keys=["Projeto 1", "Projeto 2"]).dropna()

                        if not comparacao.empty:
                            comparacao_reset = comparacao.reset_index().melt(
                                id_vars="Avaliador",
                                var_name="Projeto",
                                value_name="Média"
                            )
                            
                            fig = px.bar(
                                comparacao_reset,
                                x="Projeto",
                                y="Média",
                                color="Avaliador",
                                barmode="group",
                                title=f"Comparativo de {coluna} por Avaliador",
                                text_auto=".2f",
                                color_discrete_sequence=px.colors.qualitative.Pastel
                            )
                            fig.update_layout(
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)'
                            )
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Mostrar tabela com dados
                            st.dataframe(
                                comparacao.style.format("{:.2f}"),
                                use_container_width=True
                            )
                        else:
                            st.info(f"Nenhum avaliador comum entre os dois projetos para {coluna}.")
            elif coluna == "Avaliador":
                with st.expander("👥 Lista de Avaliadores", expanded=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Projeto 1**")
                        st.dataframe(
                            df1[["Avaliador"]].drop_duplicates().reset_index(drop=True),
                            height=300,
                            use_container_width=True
                        )
                    with col2:
                        st.markdown("**Projeto 2**")
                        st.dataframe(
                            df2[["Avaliador"]].drop_duplicates().reset_index(drop=True),
                            height=300,
                            use_container_width=True
                        )

# RODAPÉ
st.markdown("""
    <div class="footer">
        CIP - Central de Inovações e Projetos | Versão 2.0
    </div>
""", unsafe_allow_html=True)