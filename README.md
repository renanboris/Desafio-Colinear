# 📊 Accounting Dataset Generator

Ferramenta de Engenharia de Dados desenvolvida para processar, limpar e padronizar arquivos contábeis brutos (CSV) visando o treinamento de modelos de Machine Learning.

## 🚀 Como executar

1. **Pré-requisitos**
- Certifique-se de ter o Python instalado. Instale as dependências:
```bash
   pip install pandas
```

- Estrutura de Pastas Coloque os arquivos CSV brutos dentro de uma pasta chamada input/ na raiz do projeto.

*Plaintext*

/
├── input/
│   ├── lancamentos_11.csv
│   ├── lancamentos_106.csv
│   └── lancamentos_109.csv
├── services/
│   ├── parser.py
│   └── text_cleaning_tool.py
└── main.py

*Execução - Rode o script principal:*

```bash
python main.py
```

*Resultado O arquivo consolidado dataset_final.csv será gerado na raiz do projeto.*

## 🛠️ O que o projeto faz

- Input: Lê múltiplos arquivos CSV contábeis com layouts hierárquicos (Pai: Conta -> Filho: Lançamentos).

- Parsing Inteligente:

- Detecta automaticamente a posição das colunas (Data, Histórico, Débito, Crédito).

- Associa cada lançamento à sua conta contábil pai correspondente.

- Sanitização (Limpeza):

- Remove acentos, pontuação e stopwords (ex: "de", "para").

- Converte tudo para minúsculo.

- Formata valores numéricos e define tipo Débito (d) ou Crédito (c).

*Consolidação: Gera um dataset único, sem informações duplicadas e formatado conforme a regra de negócio: [descrição limpa] valor [0.00] [d/c]*

## 🧠 Decisões Técnicas

Biblioteca CSV ou Pandas na leitura: Optei por usar a biblioteca nativa csv para o parsing linha-a-linha.

*Motivo:* Os arquivos originais possuem estrutura hierárquica (cabeçalhos de conta intercalados com dados) que dificultaria o uso direto do *pd.read_csv*.

*Detecção Dinâmica de Colunas:* O script varre o cabeçalho procurando por palavras-chave ("Histórico", "Débito"). Isso torna o código resiliente a mudanças de layout.

*Pandas no Final:* Utilizado apenas na etapa de consolidação para garantir a estrutura do CSV final e remover duplicatas de forma performática.

*Arquitetura Modular:* Separação clara de responsabilidades:

*main.py:* Orquestrador.
*services/parser.py:* Lógica de extração.
*services/text_cleaning_tool.py:* Regras de Limpeza.

## ⚠️ Dificuldades Superadas

*Encoding e Caracteres Especiais:* Arquivos com codificação e muita sujeira quebravam a leitura inicial. Resolvido com tratamento de erros (replace) e encoding correto.

*Variação de Layout:* Arquivos onde a coluna "Histórico" poderia mudar de posição. Resolvido com a lógica de header_found e busca por índices baseada em strings.

*Estrutura Hierárquica:* Manter o estado da "Conta Atual" (account_code_current) enquanto lia as linhas filhas (transações).

## 🔮 Próximos Passos (Melhorias Futuras)

*Agrupamento de Classes Raras:* Implementar a regra de negócio para transformar contas com menos de 20% da média de registros em uma categoria "OUTROS".

*Validação Semântica:* Garantir relação 1:1 estrita entre Código da Conta e Descrição da Conta (normalizar nomes de bancos, por exemplo).

*Testes Unitários:* Criar testes automatizados para validar o regex de limpeza e o parser.