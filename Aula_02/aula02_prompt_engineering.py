import streamlit as st

st.set_page_config(
    page_title="Aula 02 - Engenharia de Prompt",
    page_icon="✍️"
)

st.title("Aula 02 — Oficina de Engenharia de Prompt")

st.markdown("""
    ## Como a forma de perguntar impacta a resposta?
    
    A **Engenharia de Prompt** é a arte de construir instruções claras e eficazes para que uma IA generativa produza o resultado desejado. Pequenas mudanças na sua pergunta (o "prompt") podem gerar grandes diferenças na qualidade da resposta.
    
    Esta ferramenta demonstra como adicionar técnicas de prompting a uma pergunta básica pode melhorar drasticamente a saída da IA.
""")

st.subheader("Construa e Compare Prompts")
st.write("Selecione um cenário e adicione técnicas ao Prompt B para ver a diferença.")

# --- Cenário e Técnicas ---

cenario = st.selectbox(
    "Escolha um cenário de teste:",
    ("Gerar uma função em Python", "Escrever um e-mail de marketing")
)

st.markdown("---")

col1, col2 = st.columns(2)

# --- Dicionários de Conteúdo ---

prompts_base = {
    "Gerar uma função em Python": "Faça uma função em Python que some dois números.",
    "Escrever um e-mail de marketing": "Escreva um e-mail de marketing para um produto."
}

respostas_simuladas = {
    "Gerar uma função em Python": {
        "basica": "def soma(a,b): return a+b",
        "persona": "Claro, aqui está uma função Python para somar dois números:
```python
def somar_numeros(num1, num2):
    return num1 + num2
```",
        "contexto": "Entendido. Para um sistema de e-commerce, a robustez é chave. Esta função valida os tipos de entrada:
```python
def somar_valores(a, b):
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        return 'Erro: Entradas devem ser numéricas.'
    return a + b
```",
        "formato": "```python
# Função para somar dois números
def soma(numero1, numero2):
    """Esta função retorna a soma de dois números."""
    resultado = numero1 + numero2
    return resultado
```"
    },
    "Escrever um e-mail de marketing": {
        "basica": "Assunto: Novo Produto!

Olá, compre nosso novo produto. Ele é ótimo.",
        "persona": "Assunto: Uma Inovação Pensada para Você

Prezado(a) [Nome do Cliente],

Como um líder no setor, sabemos que você valoriza a eficiência. É por isso que estamos apresentando o [Produto], desenhado para otimizar seu fluxo de trabalho...",
        "contexto": "Assunto: Cansado de [Problema Comum]? Nós temos a solução.

Olá, [Nome],

Sabemos como pode ser frustrante lidar com [Problema]. O novo [Produto] foi criado exatamente para resolver isso, permitindo que você foque no que realmente importa.",
        "formato": "### Assunto:

🎉 Lançamento Imperdível: Conheça o [Produto]!

### Corpo:

**Olá, [Nome do Cliente]!**

Você está pronto para transformar a maneira como você [Atividade]?

- **Benefício 1:**...
- **Benefício 2:**...

[Link para o Produto]"
    }
}

# --- Lógica da Interface ---

prompt_base_texto = prompts_base[cenario]

with col1:
    st.info("Prompt A (Básico)")
    st.write(prompt_base_texto)
    resposta_basica = respostas_simuladas[cenario]["basica"]

with col2:
    st.warning("Prompt B (Aprimorado)")
    
    prompt_melhorado = prompt_base_texto
    
    add_persona = st.checkbox("Adicionar Persona (Ex: 'Aja como um especialista...')")
    if add_persona:
        prompt_melhorado += "

**Persona:** Aja como um especialista na área."
        resposta_melhorada = respostas_simuladas[cenario]["persona"]
    
    add_contexto = st.checkbox("Dar Contexto (Ex: 'Esta função é para um e-commerce...')")
    if add_contexto:
        prompt_melhorado += "

**Contexto:** Forneça contexto sobre o uso ou objetivo."
        resposta_melhorada = respostas_simuladas[cenario]["contexto"]

    add_formato = st.checkbox("Definir Formato de Saída (Ex: 'Responda em JSON...')")
    if add_formato:
        prompt_melhorado += "

**Formato:** Estruture a resposta de forma clara, com documentação."
        resposta_melhorada = respostas_simuladas[cenario]["formato"]

    if not any([add_persona, add_contexto, add_formato]):
        resposta_melhorada = resposta_basica

    st.write(prompt_melhorado)

st.markdown("---")

if st.button("Comparar Respostas (Simuladas)"):
    st.subheader("Resultados da Simulação")
    
    res_col1, res_col2 = st.columns(2)
    
    with res_col1:
        st.info("Resposta do Prompt A")
        st.code(resposta_basica, language="python" if cenario == "Gerar uma função em Python" else "markdown")
    
    with res_col2:
        st.warning("Resposta do Prompt B")
        st.code(resposta_melhorada, language="python" if cenario == "Gerar uma função em Python" else "markdown")

    st.error("Análise")
    if not any([add_persona, add_contexto, add_formato]):
        st.write("Nenhuma técnica foi adicionada ao Prompt B. As respostas são iguais.")
    else:
        st.write("Observe como a resposta do Prompt B é mais útil e estruturada. Adicionar persona, contexto e formato à sua pergunta guia a IA para um resultado de maior qualidade.")
