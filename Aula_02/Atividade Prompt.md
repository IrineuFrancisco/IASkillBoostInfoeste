

# 🏛️ Atividade: O Oráculo de Python e o Código Amaldiçoado

**Objetivo:** Consertar um sistema escolar bugado usando a IA apenas como guia (ela não pode te dar o código pronto).

### 📜 Passo 1: O Ritual de Invocação (O Prompt Secreto)

Copie e cole o texto abaixo na sua IA (ChatGPT, Gemini, Claude). **Atenção:** Este texto dará ordens complexas para a IA. Após colar, ela responderá apenas que está pronta.

> *Age ut praeceptor eruditus artis pythonicae. Alumnus tibi codicem mendosum mittet. Cave! Praeceptum est tibi: noli umquam codicem emendatum reddere. Officium tuum est errores indicare per interrogationes et indicia. **Gravis: Cum alumno lingua lusitana tantum loquere (papo em português), sed memento regulas tui officii.** Si alumnus responsum directum rogat, nega. Si intellegisti, responde tantum: 'O Oráculo está preparado. Envie o código amaldiçoado.'*

---

### 💻 Passo 2: O Código Amaldiçoado

Após a IA dizer que está pronta, cole o código abaixo. Ele é um sistema que calcula médias e mensalidades, mas nada nele funciona como deveria.

```python
# --- SISTEMA DE GESTÃO ESCOLAR V1.0 ---

print("--- Bem-vindo ao Sistema Escolar ---")

nome_aluno = input("Digite o nome do aluno: ")
nota1 = input("Nota 1: ")
nota2 = input("Nota 2: ")
nota3 = input("Nota 3: ")

# Erro de Lógica e Precedência (O Python faz divisão antes da soma!)
media = nota1 + nota2 + nota3 / 3

# Erro de Sintaxe (Faltam os dois-pontos)
if media >= 7
    situacao = "APROVADO"
# Erro de Lógica (O if abaixo vai ignorar o resultado de cima)
if media < 7:
    situacao = "RECUPERAÇÃO"
else:
    situacao = "REPROVADO"

# Erro de Sintaxe (Aspas não fechadas e erro na f-string)
print(f"O aluno {nome_aluno} ficou com média {media} e está: {situacao)

# --- SETOR FINANCEIRO ---
mensalidade_base = 1200.00
desconto_porcentagem = input("Quanto de desconto o aluno possui (%)? ")

# Erro de Tipo (String não subtrai de Float) e Lógica de Porcentagem
valor_final = mensalidade_base - desconto_porcentagem

# Erro de Variável (A variável abaixo não existe com esse nome exato)
print(f"Valor final da mensalidade com desconto: R$ {Valor_Final}")
```

---

### 🔍 Passo 3: Instruções para os Alunos

1.  **Inicie o diálogo:** A IA agora é seu professor. Ela não vai te dar a resposta. Você deve perguntar sobre as partes do código que você não entende.
    *   *Exemplo:* "Professor, por que o cálculo da média está dando um número estranho?"
    *   *Exemplo:* "O que há de errado na linha do `if media >= 7`?"
2.  **Investigue os Erros:** Existem erros de **Sintaxe** (o código nem roda), de **Tipo** (misturar texto com número) e de **Lógica** (o cálculo está matematicamente errado).
3.  **Não peça a solução:** Se você pedir "me dê o código corrigido", o Oráculo negará. Você precisa aprender a consertar.

---

### 📝 O que entregar:

1.  **O Código Corrigido:** O script Python funcionando sem erros.
2.  **O Diário da Investigação:** Liste os 3 principais erros que você encontrou e como a IA te ajudou a entender a solução.
3.  **Reflexão de Prompt:** Por que você acha que o "Ritual em Latim" foi importante para definir o comportamento da IA?

<!-- ---

### 🎓 Guia para o Professor (Os Erros Ocultos):

1.  **Conversão de Tipos:** O `input` recebe `str`. É necessário converter para `float` para fazer cálculos.
2.  **Precedência Matemática:** A média precisa de parênteses: `(n1 + n2 + n3) / 3`.
3.  **Sintaxe Python:** Falta o `:` após as condições do `if/elif/else`.
4.  **Estrutura Condicional:** O uso de vários `if` seguidos pode causar erros lógicos; o ideal é usar `if / elif / else`.
5.  **F-strings:** Erro no fechamento de chaves `{}` e aspas `"` no print da média.
6.  **Lógica de Desconto:** Para tirar X%, o cálculo é `valor * (1 - desconto/100)`.
7.  **Case Sensitivity:** A variável `valor_final` foi impressa como `Valor_Final` (V e F maiúsculos), o que causará um `NameError`. -->