import streamlit as st
from PIL import Image

# Configuração da página com layout mais amplo
st.set_page_config(
    page_title="🏠 Home - Avaliação de Projetos", 
    page_icon="🏠",
    layout="wide"
)

# ESTILOS E CSS CUSTOMIZADO (mesmo do primeiro código)
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
        
        /* Botões */
        .stButton>button {
            background-color: #4B0082;
            color: white;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            margin-top: 1rem;
        }
        
        /* Projetos */
        .project-card {
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1rem 0;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            border-left: 3px solid #4B0082;
        }
    </style>
""", unsafe_allow_html=True)

# CABEÇALHO
image = Image.open('header.png')
st.image(image, use_container_width=True)

# TÍTULO PRINCIPAL
st.markdown("""
    <div class="main-header">
        <h1 style='margin:0;'>Avaliação de Projetos</h1>
        <p style='margin:0; font-size:1.1rem;'>CIP - Central de Inteligência  de Projetos</p>
    </div>
""", unsafe_allow_html=True)

# INSTRUÇÕES
with st.container():
    st.markdown("""
        <div class="custom-card">
            <h3 style='color: #4B0082;'>📋 Instruções de Avaliação</h3>
            <p>Nesta plataforma, sua tarefa é avaliar cada proposta de projeto em <strong>duas dimensões:</strong></p>
            <ol>
                <li><strong>O problema</strong> que o projeto busca resolver</li>
                <li><strong>A solução</strong> proposta</li>
            </ol>
            <p>Atribua <strong>uma nota de 0 a 5</strong> para cada critério:</p>
            <ul>
                <li>0 - Não atende ao critério (nota mínima)</li>
                <li>5 - Atende plenamente ao critério (nota máxima)</li>
            </ul>
            <p>A avaliação será calculada automaticamente conforme os pesos pré-definidos.</p>
        </div>
    """, unsafe_allow_html=True)

# LISTA DE PROJETOS
st.markdown("""
    <div style="margin-top: 2rem;">
        <h2 style='color: #4B0082; text-align: center;'>📌 Propostas de Projeto em Aberto</h2>
    </div>
""", unsafe_allow_html=True)

# Função para criar cards de projeto
def criar_card_projeto(numero, superintendencia, gerencia, proponente, link_forms):
    st.markdown(f"""
        <div class="project-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3 style='color: #011B70; margin:0;'>Projeto {numero}</h3>
                <a href="{link_forms}" target="_blank" style="text-decoration: none;">
                    <button style="background-color: #4B0082; color: white; border: none; border-radius: 5px; padding: 0.3rem 0.8rem; font-size: 0.9rem;">
                        📝 Ver o forms
                    </button>
                </a>
            </div>
            <p style="margin: 0.5rem 0;"><strong>Superintendência:</strong> {superintendencia}</p>
            <p style="margin: 0.5rem 0;"><strong>Gerência:</strong> {gerencia}</p>
            <p style="margin: 0.5rem 0 1rem 0;"><strong>Proponente:</strong> {proponente}</p>
            <div style="text-align: right;">
                <a href="pages/Avaliacao_Projeto_{numero}.py" target="_self" style="text-decoration: none;">
                    <button style="background-color: #4B0082; color: white; border: none; border-radius: 5px; padding: 0.5rem 1.5rem; font-size: 1rem;">
                        Avaliar Projeto {numero} →
                    </button>
                </a>
            </div>
        </div>
    """, unsafe_allow_html=True)

# PROJETOS (substitua com seus dados reais)
projetos = [
    {"numero": 1, "superintendencia": "SUP", "gerencia": "GER", "proponente": "Proponente", "link_forms": "https://forms/link1"},
    {"numero": 2, "superintendencia": "SUP", "gerencia": "GER", "proponente": "Proponente", "link_forms": "https://forms/link2"},
    {"numero": 3, "superintendencia": "SUP", "gerencia": "GER", "proponente": "Proponente", "link_forms": "https://forms/link3"},
    {"numero": 4, "superintendencia": "SUP", "gerencia": "GER", "proponente": "Proponente", "link_forms": "https://forms/link4"},
    {"numero": 5, "superintendencia": "SUP", "gerencia": "GER", "proponente": "Proponente", "link_forms": "https://forms/link5"},
    {"numero": 6, "superintendencia": "SUP", "gerencia": "GER", "proponente": "Proponente", "link_forms": "https://forms/link6"}
]

for projeto in projetos:
    criar_card_projeto(
        projeto["numero"],
        projeto["superintendencia"],
        projeto["gerencia"],
        projeto["proponente"],
        projeto["link_forms"]
    )

# RODAPÉ
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #6c757d; font-size: 0.9rem;">
        CIP - Central de Inovações e Projetos | Versão 2.0
""", unsafe_allow_html=True)