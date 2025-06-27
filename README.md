
# 🐍 Compilador Emojilanguage (CEm) 🚀

## 🎯 Funcionalidades Suportadas

O compilador atualmente oferece suporte a:

### 📌 Declaração de variáveis

```emj
🔢 idade 🟰 25 🛑
🔤 nome 🟰 👉Kaique👈 🛑
```

### 📌 Impressão na tela

```emj
👀 👉Olá, mundo!👈 🛑
👀 idade 🛑
```

### 📌 Estruturas de controle

#### IF / ELSE

```emj
🙂‍↕️ 🫸 idade ▶️ 18 🫷 🤜
    👀 👉Maior de idade👈 🛑
🤛 🙂‍↔️ 🤜
    👀 👉Menor de idade👈 🛑
🤛
```

#### WHILE

```emj
🔢 x 🟰 0 🛑
🤸‍♂️ 🫸 x ◀️ 3 🫷 🤜
    👀 x 🛑
    🔢 x 🟰 x ➕ 1 🛑
🤛
```

#### FOR

```emj
🔢 soma 🟰 0 🛑
🌀 i 🟰 1 ➡️ 5 🤜
    👀 i 🛑
    🔢 soma 🟰 soma ➕ i 🛑
🤛
```

---

## 🏗️ Estrutura do Projeto

| Arquivo            | Função                                                              |
|--------------------|---------------------------------------------------------------------|
| `main.py`          | Ponto de entrada. Executa as fases do compilador e interpreta o código |
| `lexer.py`         | Análise léxica: converte texto em tokens                           |
| `parser.py`        | Análise sintática: gera a árvore (AST) com base nos tokens         |
| `compiler_ast.py`  | Definições das classes da AST                                      |
| `interpreter.py`   | Executa o código a partir da AST (interpretação)                   |

---

## ▶️ Como Executar

Crie seu arquivo `.emj` com o código Emojilanguage:

### Exemplo (`exemplo.emj`):

```emj
🔢 x 🟰 0 🛑
🌀 i 🟰 1 ➡️ 3 🤜
    👀 👉Contador: 👈 🛑
    👀 i 🛑
🤛
```

### Execute o compilador:

```bash
python main.py exemplo.emj
```

---

## 📤 Exemplo de Saída

```
Compilação concluída com sucesso!

=== Árvore Sintática Abstrata (AST) ===
Programa
  Declaração de variável: x (Tipo: INT_TYPE)
    Número: 0
  ...

=== Saída do programa ===

Contador: 1
Contador: 2
Contador: 3

=== Fim da execução ===
```
