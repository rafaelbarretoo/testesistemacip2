import streamlit as st
import pandas as pd
import os
from PIL import Image

# Configuração da página com layout mais amplo
st.set_page_config(
    page_title="Ícone + Projeto Nome do Projeto", 
    page_icon="🔐",
    layout="wide"
)

def calcular_media(notas, pesos):
    return sum(n * p for n, p in zip(notas, pesos))

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
        
        /* Sliders */
        .stSlider {
            margin-bottom: 1.5rem;
        }
        
        /* Botões */
        .stButton>button {
            background-color: #4B0082;
            color: white;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            margin-top: 1rem;
        }
        
        /* Expanders */
        .stExpander {
            margin-bottom: 1rem;
        }
        
        /* Métricas */
        .stMetric {
            border-radius: 5px;
            padding: 1rem;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# CABEÇALHO


# Imagem de cabeçalho
image = Image.open('headerav.png')
st.image(image, use_container_width=True)

# Título principal com destaque - Inserir nome e ícone que represente o projeto
st.markdown("""
    <div class="main-header">
        <h1 style='margin:0;'>Ícone Projeto</h1> 
        <p style='margin:0; font-size:1.1rem;'>SUP - Ger - Proponente</p>
    </div>
""", unsafe_allow_html=True)

# SEÇÃO DE INFORMAÇÕES DO PROJETO

col1, col2, col3 = st.columns([1, 1, 0.5])

with col1:
    with st.expander("📋 **Resumo do Projeto**", expanded=False):
        st.markdown("""
            **Problema Identificado:**  
            **Recursos financeiros previstos:**  
            **Prazo estimado de execução:**  
            **Resultados esperados:**  
            • Item 1  
            • Item 2  
            • Item 3  
            **Áreas envolvidas:**  
        """)

with col2:
    with st.expander("🗺️ **Roadmap do Projeto**", expanded=False):
        st.markdown("""
            **Início do Projeto:**  
            • Etapa 1  
            • Etapa 2  
            • Etapa 3  
            **Término do Projeto:**  
        """)

with col3:
    st.link_button("📝 Acessar Forms do Projeto", "https://docs.google.com/spreadsheets/d/1EOTViNNpObQ7Yz4kqWLp_S_lLkdlzqf3-3qhh_KULbA/edit?gid=1884140145#gid=1884140145",
                  use_container_width=True)

# SEÇÃO DE AVALIAÇÃO

st.markdown("""
    <div class="custom-card">
        <h2 style='color: #4B0082; text-align: center;'>🎯 Avaliação do Projeto </h2>
    </div>
""", unsafe_allow_html=True)

# Seleção de avaliador
nomes_usuarios = ["Aline Oliveira","André Diniz", "Guilherme Carrijo","Leonardo Briza", 
                 "Marcelo Gallo","Monica Vargas", "Patricia Testai", "Paulo Ravagnani"]
avaliador = st.selectbox("**Selecione seu nome:**", nomes_usuarios, index=None, placeholder="Escolha seu nome...")

# CRITÉRIOS - PROBLEMA

st.markdown("""
    <div class="custom-card">
        <h3 style='color: #011B70; text-align: center;'>Critérios - Problema</h3>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    gravidade = st.slider(
        "**Gravidade do problema - Peso: 0,50**\n"
        "\nO problema é sério? Pode traver impactos relevantes se não for resolvido?",
        0.0, 5.0, 0.0, step=0.5,
        help="0 = Baixa gravidade | 5 = Extremamente grave"
    )

with col2:
    urgencia = st.slider(
        "**Urgência de Solução do Problema - Peso: 0,30**\n"
        "\nEssa é uma situação que exige ação imediata ou pode esperar?",
        0.0, 5.0, 0.0, step=0.5,
        help="0 = Baixa urgência | 5 = Muita urgência"
    )

with col3:
    tendencia = st.slider(
        "**Tendência do Problema - Peso: 0,20**\n"
        "\nSe nada for feito, o problema tende a piorar, estagnar ou se resolver?",
        0.0, 5.0, 0.0, step=0.5,
        help="0 = Baixa tendência de piora | 5 = Alta tendência de piora"
    )

# Cálculo da média do problema
notas_problema = [gravidade, urgencia, tendencia]
pesos_problema = [0.50, 0.30, 0.20]
media_problema = calcular_media(notas_problema, pesos_problema)

# Exibição com estilo
st.markdown(f"""
    <div class="custom-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h4 style="margin:0;">Média - Problema</h4>
            <div style="font-size: 1.5rem; font-weight: bold; color: {"#28a745" if media_problema >= 4 else "#ffc107" if media_problema >= 2 else "#dc3545"}">
                {media_problema:.2f}
            </div>
        </div>
        <div style="margin-top: 0.5rem;">
            <progress value="{media_problema}" max="5" style="width:100%; height:10px; border-radius:5px; color: {"#28a745" if media_problema >= 4 else "#ffc107" if media_problema >= 2 else "#dc3545"}"></progress>
        </div>
    </div>
""", unsafe_allow_html=True)

# CRITÉRIOS - SOLUÇÃO

st.markdown("""
    <div class="custom-card">
        <h3 style='color: #011B70; text-align: center;'>Critérios - Solução</h3>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    viabilidade_solucao = st.slider(
        "**Viabilidade da Solução - Peso: 0,30**\n"
        "\nA proposta é realista? Considera bem custos, prazos e riscos?",
        0.0, 5.0, 0.0, step=0.5,
        help="0 = Inviável | 5 = Totalmente viável"
    )

    resultados_esperados = st.slider(
        "**Resultados Esperados - Peso: 0,30**\n"
        "\nOs resultados estão bem descritos? São mensuráveis?",
        0.0, 5.0, 0.0, step=0.5,
        help="0 = Indefinidos | 5 = Bem definidos e mensuráveis"
    )

    impacto_solucao = st.slider(
        "**Impacto da Solução - Peso 0,20**\n"
        "\nA solução trará benefícios concretos para o CIEE?",
        0.0, 5.0, 0.0, step=0.5,
        help="0 = Baixo impacto | 5 = Alto impacto "
    )

with col2:
    alinhamento_estrategico = st.slider(
        "**Alinhamento Estratégico - Peso 0,10**\n"
        "\nConectada com planejamento estratégico ou compromissos institucionais?",
        0.0, 5.0, 0.0, step=0.5,
        help="0 = Sem alinhamento | 5 = Totalmente alinhado"
    )

    abrangencia = st.slider(
        "**Abrangência (Público e Território) - Peso: 0,10**\n"
        "\nO projeto atinge muitas pessoas/áreas ou tem escopo limitado?",
        0.0, 5.0, 0.0, step=0.5,
        help="0 = Baixa abrangência | 5 = Alta abrangência"
    )

# Cálculo da média da solução
notas_solucao = [viabilidade_solucao, resultados_esperados, impacto_solucao, alinhamento_estrategico, abrangencia]
pesos_solucao = [0.30, 0.30, 0.20, 0.10, 0.10]
media_solucao = calcular_media(notas_solucao, pesos_solucao)

# Exibição com estilo
st.markdown(f"""
    <div class="custom-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h4 style="margin:0;">Média - Solução</h4>
            <div style="font-size: 1.5rem; font-weight: bold; color: {"#28a745" if media_solucao >= 4 else "#ffc107" if media_solucao >= 2 else "#dc3545"}">
                {media_solucao:.2f}
            </div>
        </div>
        <div style="margin-top: 0.5rem;">
            <progress value="{media_solucao}" max="5" style="width:100%; height:10px; border-radius:5px; color: {"#28a745" if media_solucao >= 4 else "#ffc107" if media_solucao >= 2 else "#dc3545"}"></progress>
        </div>
    </div>
""", unsafe_allow_html=True)

# OBSERVAÇÕES

observacoes = st.text_area(
    "**Deixe sua opinião sobre o projeto avaliado:**",
    placeholder="Descreva aqui suas observações, sugestões ou considerações adicionais...",
    height=200
)

# RESULTADO FINAL

media_geral = calcular_media([media_problema, media_solucao], [0.50, 0.50])

# Definir cor e status com base na média
if media_geral < 2:
    cor_status = "#dc3545"
    status = "REPROVADO"
elif media_geral < 4:
    cor_status = "#ffd900f6"
    status = "REVISÃO NECESSÁRIA"
else:
    cor_status = "#28a745"
    status = "APROVADO"

st.markdown(f"""
    <div class="custom-card">
        <h3 style='text-align: center;'>Resultado Final Individual</h3>
        <div style="text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 2rem; font-weight: bold; color: {cor_status};">
                {media_geral:.2f}
            </div>
            <div style="font-size: 1.5rem; font-weight: bold; color: {cor_status}; margin-top: 0.5rem;">
                {status}
            </div>
            <progress value="{media_geral}" max="5" style="width:80%; height:15px; border-radius:5px; margin-top:1rem;"></progress>
        </div>
    </div>
""", unsafe_allow_html=True)

# SALVAR AVALIAÇÃO

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("💾 Salvar Avaliação", use_container_width=True):
        criterios = [gravidade, urgencia, tendencia, viabilidade_solucao, resultados_esperados,
                    impacto_solucao, alinhamento_estrategico, abrangencia]
        
        if any(valor == 0.0 for valor in criterios):
            st.error("Por favor, preencha todos os critérios com notas maiores que 0,0!")
        elif not avaliador:
            st.error("Por favor, selecione seu nome antes de salvar.")
        else:
            dados = {
                "Avaliador": [avaliador],
                "Gravidade": [gravidade],
                "Urgência": [urgencia],
                "Tendência": [tendencia],
                "Média Problema": [media_problema],
                "Viabilidade da Solução": [viabilidade_solucao],
                "Resultados Esperados": [resultados_esperados],
                "Impacto da Solução": [impacto_solucao],
                "Alinhamento Estratégico": [alinhamento_estrategico],
                "Abrangência": [abrangencia],
                "Média Solução": [media_solucao],
                "Média Final": [media_geral],
                "Observação": [observacoes]
            }

            df = pd.DataFrame(dados)
            arquivo = "avaliacoes02.xlsx"

            if os.path.exists(arquivo):
                df_existente = pd.read_excel(arquivo)

                if avaliador in df_existente["Avaliador"].values:
                    st.error("Este avaliador já preencheu a avaliação. Cada avaliador só pode avaliar cada projeto uma vez.")
                else:
                    df = pd.concat([df_existente, df], ignore_index=True)
                    df.to_excel(arquivo, index=False)
                    st.success("✅ Avaliação salva com sucesso!")
            else:
                df.to_excel(arquivo, index=False)
                st.success("✅ Avaliação salva com sucesso!")

# RODAPÉ

st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #6c757d; font-size: 0.9rem;">
        CIP - Central de Inovações e Projetos | Versão 2.0
    </div>
""", unsafe_allow_html=True)