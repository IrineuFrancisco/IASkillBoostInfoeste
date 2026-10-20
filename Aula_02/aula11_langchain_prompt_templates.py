import streamlit as st
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

st.set_page_config(
    page_title="Aula 11 - LangChain e Prompt Templates",
    page_icon="🔗"
)

st.title("🔗 Aula 11 — LangChain e Prompt Templates")

st.markdown("""
    ## Padronizando Entradas com `PromptTemplate`
    
    À medida que nossas aplicações de IA se tornam mais complexas, construir prompts manualmente concatenando strings se torna confuso e propenso a erros. O **LangChain** resolve isso com `PromptTemplate`.

    Um `PromptTemplate` nos permite:
    - Definir um modelo de texto com variáveis (placeholders).
    - Garantir que todas as variáveis necessárias sejam preenchidas.
    - Reutilizar prompts de forma limpa e organizada.

    Vamos ver como isso funciona na prática.
""")

# --- 1. Configuração da Chave da API (reutilizado da aula 10) ---
api_key = None
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except (KeyError, FileNotFoundError):
    st.warning("Chave da API não encontrada. A execução com o modelo real está desabilitada.")
    api_key_input = st.text_input(
        "Opcional: Cole sua chave da API da OpenAI aqui para habilitar a execução:",
        type="password"
    )
    if api_key_input:
        api_key = api_key_input

# --- 2. Seleção de Cenário e Definição dos Templates ---
st.subheader("1. Escolha um Cenário")

cenarios = {
    "Tradutor de Idiomas": {
        "template": "Traduza o seguinte texto de {idioma_origem} para {idioma_destino}:

Texto: {texto}",
        "variaveis": ["idioma_origem", "idioma_destino", "texto"],
        "defaults": {"idioma_origem": "Português", "idioma_destino": "Inglês", "texto": "Inteligência Artificial é fascinante."}
    },
    "Gerador de E-mail Marketing": {
        "template": "Escreva um e-mail de marketing com um tom {tom} para o produto '{produto}'. O público-alvo são {publico_alvo}. Destaque o seguinte benefício: {beneficio}.",
        "variaveis": ["tom", "produto", "publico_alvo", "beneficio"],
        "defaults": {"tom": "entusiasmado", "produto": "Caneta Mágica", "publico_alvo": "estudantes", "beneficio": "nunca fica sem tinta"}
    }
}

cenario_selecionado = st.selectbox("Selecione um template pré-definido:", list(cenarios.keys()))
info_cenario = cenarios[cenario_selecionado]
template_str = info_cenario["template"]

st.write("Template Selecionado:")
st.code(template_str, language="text")

# --- 3. Formulário Dinâmico para as Variáveis ---
st.subheader("2. Preencha as Variáveis do Template")

# Usando st.form para agrupar as entradas
with st.form(key="variaveis_form"):
    inputs_usuario = {}
    for var in info_cenario["variaveis"]:
        default_value = info_cenario["defaults"].get(var, "")
        inputs_usuario[var] = st.text_input(f"Variável `{var}`:", value=default_value)
    
    submit_button = st.form_submit_button("Montar Prompt Final")

# --- 4. Visualização do Prompt e Execução ---
if submit_button:
    st.subheader("3. Prompt Final e Execução")
    
    # Cria o PromptTemplate com LangChain
    prompt_template = PromptTemplate(
        template=template_str,
        input_variables=info_cenario["variaveis"]
    )
    
    # Formata o prompt com as entradas do usuário
    prompt_final = prompt_template.format(**inputs_usuario)
    
    st.write("O prompt final, pronto para ser enviado ao modelo, é:")
    st.success(prompt_final)
    
    # --- Execução com LLMChain (se a chave existir) ---
    if api_key:
        st.markdown("---")
        st.write("Executando com o modelo real...")
        
        try:
            # Inicializa o modelo e a chain
            llm = ChatOpenAI(openai_api_key=api_key, model_name="gpt-3.5-turbo")
            chain = LLMChain(llm=llm, prompt=prompt_template)
            
            with st.spinner("Aguardando a resposta da IA..."):
                # Roda a chain com as entradas do usuário
                resultado = chain.run(inputs_usuario)
                st.info("Resposta do Modelo:")
                st.write(resultado)
                
        except Exception as e:
            st.error(f"Ocorreu um erro durante a execução: {e}")
    else:
        st.warning("A execução com o modelo real está desabilitada. Insira uma chave de API para testar.")
