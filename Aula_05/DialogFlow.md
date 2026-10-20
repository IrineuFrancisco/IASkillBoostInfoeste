

# 🤖 AULA: Interfaces Conversacionais com Google Dialogflow
**Disciplina:** Inteligência Artificial Aplicada  
**Objetivo:** Compreender e construir um Agente de IA para Automação de Pedidos.

---

## 🧠 1. A Base Teórica: O que acontece por trás do Chat?

Antes de clicar em botões, precisamos entender que o Dialogflow não é um simples "robô de perguntas e respostas". Ele é baseado em **NLU (Natural Language Understanding)**, uma subárea da IA que foca em como as máquinas interpretam a linguagem humana.

### O Fluxo da Inteligência:
1.  **Input (Entrada):** O usuário digita algo (ex: "Tô com fome, quero uma pizza").
2.  **Intent Classification (Classificação de Intenção):** A IA compara a frase com modelos matemáticos para descobrir *o que* o usuário quer.
3.  **Entity Extraction (Extração de Entidades):** A IA "limpa" a frase e extrai dados importantes (ex: "Calabresa", "Grande").
4.  **Fulfillment (Resposta):** O sistema gera uma resposta baseada na intenção identificada.

---

## 🛠️ 2. Glossário Técnico (Os Pilares)

> **Intents (Intenções):** O objetivo do usuário. É o "mapa" do bot.
> 
> **Training Phrases (Frases de Treino):** Exemplos de como as pessoas falam. A IA usa isso para aprender e generalizar (ela entende frases que você nunca escreveu, por similaridade vetorial).
> 
> **Entities (Entidades):** São as variáveis. Se a Intenção é o *verbo*, a Entidade é o *substantivo*.
> 
> **Contextos:** A memória de curto prazo do bot. Permite que o bot saiba que, quando o usuário diz "Sim", ele está confirmando o pedido de pizza, e não outra coisa.

---

## 🍕 3. Projeto Prático: Sistema de Delivery "IA-Pizza"

### Passo 1: Criando o Agente
1. Acesse [Dialogflow ES](https://dialogflow.cloud.google.com/).
2. Clique em **Create Agent**.
3. Nome: `Pizzaria_IA_Bot` | Língua: `Portuguese (pt-br)`.

### Passo 2: Construindo o "Cérebro" (Entities)
As entidades permitem que o bot reconheça dados específicos. Vamos criar três:

| Entidade | Valores (Exemplos) | Sinônimos |
| :--- | :--- | :--- |
| `@Sabor` | Calabresa | Linguiça, de carne, tradicional |
| `@Tamanho` | Grande | Família, 8 fatias, G |
| `@FormaPagamento` | Cartão | Crédito, Débito, Visa, Master |

*   **Como fazer:** Vá em `Entities` -> `Create Entity` -> Salve cada uma após preencher.

### Passo 3: Criando a Intenção Principal (`fazer_pedido`)
Nesta etapa, treinamos a IA para entender o desejo do usuário.

1.  Vá em **Intents** -> **Create Intent**.
2.  Nome: `pedido.pizza`.
3.  **Training Phrases:** Adicione pelo menos 10 frases, como:
    *   "Quero uma pizza"
    *   "Vou pedir uma redonda de pepperoni"
    *   "Me vê uma margherita média"
    *   "Estou com fome, quero calabresa"

### Passo 4: Parâmetros e Slot Filling (A Mágica dos Dados)
Para um pedido ser válido, precisamos de informações obrigatórias. Role até **Action and Parameters**.

| Required | Parameter Name | Entity | Value | Prompt (Se o usuário esquecer) |
| :--- | :--- | :--- | :--- | :--- |
| ✅ | `sabor` | `@Sabor` | `$sabor` | "Qual sabor você deseja?" |
| ✅ | `tamanho` | `@Tamanho` | `$tamanho` | "Qual o tamanho? (Broto, Média ou Grande)" |
| ✅ | `pagamento` | `@FormaPagamento` | `$pagamento` | "Como deseja pagar?" |
| ✅ | `endereco` | `@sys.address` | `$endereco` | "Onde devemos entregar?" |

> **Nota de IA:** O parâmetro `@sys.address` é uma **System Entity**. O Google já treinou a IA dele para reconhecer endereços automaticamente em qualquer lugar do mundo!

---

## 🔗 4. Gerindo o Contexto (A Lógica Avançada)

Imagine que o usuário diga: "Vou querer a de Calabresa". O bot pergunta: "Qual o tamanho?". O usuário responde: "Grande". 
Sem **Contexto**, o bot esquece que o assunto era Calabresa.

1. No topo da Intent `pedido.pizza`, em **Context**, adicione um **Output Context**: `pedido-em-andamento`.
2. Isso cria uma "tag" que acompanha a conversa por 5 interações (lifespan).

---

## 💬 5. Respostas Inteligentes

Na seção **Responses**, use os parâmetros capturados para confirmar o pedido:

> "Ótima escolha! 🍕 Registrei seu pedido de uma pizza de **$sabor**, tamanho **$tamanho**. O entregador levará para **$endereco** e o pagamento será no **$pagamento**. Posso confirmar?"

---

## 🚀 6. Testando e Integrando

### Teste de Stress:
No painel à direita (**Try it now**), tente confundir a IA:
- *Usuário:* "Quero uma de mussarela"
- *IA:* (Deve identificar o sabor e perguntar o tamanho)
- *Usuário:* "Pode ser grande e entrega na Avenida Paulista 1000"
- *IA:* (Deve pular as perguntas de tamanho e endereço e ir direto para o pagamento)

### Publicação:
#### Use o "Dialogflow Messenger" (A alternativa moderna)
Como o "Web Demo" está datado, o Google lançou o **Dialogflow Messenger**, que é mais bonito e funciona melhor.
1. No menu lateral esquerdo, clique em **Integrations**.
2. Procure por **Dialogflow Messenger** (geralmente fica no topo).
3. Clique em **Enable**.
4. Ele vai te dar um código e um botão "Try it now". Clique no botão. Ele abrirá um balão de chat no canto inferior direito que funciona perfeitamente.

---

## 📝 Exercício de Fixação

1.  **Personalização:** Adicione uma entidade para `Bebida` e integre-a à intenção de pedido.
2.  **Tratamento de Erros:** Edite a `Default Fallback Intent` para que o bot não diga apenas "Não entendi", mas dê opções do que ele sabe fazer (ex: "Desculpe, eu consigo anotar pedidos de pizza e informar o horário de funcionamento").
3.  **Inteligência Extra:** Crie uma intent `horario_funcionamento` que responda prontamente se a pizzaria está aberta.

---
**Dica do Professor:** No Dialogflow, o segredo não é a quantidade de frases, mas a qualidade e a diversidade delas. Pense em como pessoas de diferentes regiões falariam!

