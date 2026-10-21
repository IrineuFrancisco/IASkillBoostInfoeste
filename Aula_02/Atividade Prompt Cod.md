
## 💻 4. CÓDIGO FONTE FINAL CORRIGIDO

```python
# ==============================================================================
# SISTEMA DE GESTÃO ESCOLAR V1.0 (CORRIGIDO)
# ==============================================================================

print("--- Bem-vindo ao Sistema Escolar (Versão Homologada) ---")

# 1. Conversão explícita para float
nome_aluno = input("Digite o nome do aluno: ").strip()
nota1 = float(input("Nota 1: "))
nota2 = float(input("Nota 2: "))
nota3 = float(input("Nota 3: "))

# 2. Uso de parênteses para forçar a soma antes da divisão
media = (nota1 + nota2 + nota3) / 3

# 3. Estrutura condicional correta com if, elif e else
if media >= 7.0:
    situacao = "APROVADO"
elif media >= 5.0:
    situacao = "RECUPERAÇÃO"
else:
    situacao = "REPROVADO"

# 4. Sintaxe da f-string corrigida com chaves completas
print(f"\nO aluno {nome_aluno} obteve média {media:.2f} e está: {situacao}")

# --- SETOR FINANCEIRO ---
mensalidade_base = 1200.00
desconto_porcentagem = float(input("\nQuanto de desconto o aluno possui (%)? "))

# 5. Cálculo percentual e variáveis consistentes
valor_desconto = mensalidade_base * (desconto_porcentagem / 100.0)
valor_final = mensalidade_base - valor_desconto

print(f"Valor final da mensalidade com desconto: R$ {valor_final:.2f}")
```
