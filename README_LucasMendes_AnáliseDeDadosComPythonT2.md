# Mini-Projeto Avaliativo — Análise Exploratória de Dados (Varejo)
**Disciplina:** Análise de Dados com Python [T2] — Módulo 1, Semana 07  
**Aluno:** Lucas Mendes  
**Turma:** T2  

---

## Como executar

### 1. Pré-requisitos

Instale as dependências antes de rodar qualquer arquivo:

```bash
pip install pandas plotly streamlit
```

> **Requisito:** Python 3.8+. Todos os arquivos e o `Base_Varejo.csv` devem estar na **mesma pasta**.

---

### 2. Script de Análise Exploratória

Executa as 5 sprints no terminal (importação, verificação, limpeza, estatísticas e agrupamentos):

```bash
python Miniprojeto_LucasMendes_AnáliseDeDadosComPythonT2.py
```

---

### 3. Dashboard Interativo (Streamlit)

Abre o dashboard visual no navegador com filtros interativos:

```bash
streamlit run Dash_Streamlit.py
```

> O Streamlit abrirá automaticamente em `http://localhost:8501`.  
> O dashboard importa a função `obter_dados()` do script principal — **não duplica a limpeza**.

---

## Estrutura do projeto

```
📁 Miniprojeto_LucasMendes_AnáliseDeDadosComPythonT2/
│
├── Miniprojeto_LucasMendes_AnáliseDeDadosComPythonT2.py  # Script principal (AED + módulo de limpeza)
├── Dash_Streamlit.py                                      # Dashboard interativo (importa o script principal)
├── Base_Varejo.csv                                        # Base de dados (não versionar se grande)
└── README_LucasMendes_AnáliseDeDadosComPythonT2.md        # Este arquivo
```

> **Importante:** `Dash_Streamlit.py` depende do script principal. Ambos devem estar na mesma pasta.

---

## O que o script faz (Sprints)

| Sprint | Descrição |
|--------|-----------|
| 1 | Importação do CSV e exibição de shape, colunas e tipos |
| 2 | Verificação de problemas: nulos, duplicatas, categorias inválidas, tipo de data |
| 3 | Limpeza: remoção de colunas vazias, imputação de `#N/D`, conversão de `DATA` para datetime, remoção de duplicatas |
| 4 | Estatística descritiva da coluna `CL_FHL` (nº de filhos) |
| 5 | Agrupamentos com `groupby` e `pivot_table` + bloco de conclusões |

---

## O que o dashboard exibe

| Seção | Conteúdo |
|-------|----------|
| KPIs (topo) | Registros, clientes únicos, compras, média de filhos, categoria líder, gênero líder |
| Gráfico de barras | Compras por categoria de produto |
| Gráfico de rosca | Distribuição de compras por gênero |
| Gráfico de área | Evolução de compras ao longo do tempo (mês a mês) |
| Gráfico de barras | Distribuição do número de filhos dos clientes |
| Gráfico de barras | Compras por segmento de cliente (A / B / C) |
| Tabela | Estatísticas descritivas completas de `CL_FHL` |
| Heatmap | Cruzamento de compras por categoria e gênero |
| Sidebar | Filtros interativos por Ano, Gênero, Segmento e Categoria |

---

## Insights obtidos (3–6 tópicos)

1. **Qualidade dos dados:** A base bruta continha 4 colunas 100% vazias e 96.553 linhas duplicadas — ambos removidos na etapa de limpeza, resultando em 733.447 registros únicos.

2. **Categoria inválida (`#N/D`):** 3.650 registros não possuíam categoria de produto definida. Foram reclassificados como `"Sem Categoria"` para manter os registros na análise sem falsear os agrupamentos.

3. **Perfil de filhos dos clientes:** A maioria dos clientes não tem filhos (mediana = moda = 0). A média de 1,15 com desvio padrão de 1,42 revela distribuição assimétrica — uma minoria de clientes com 3–4 filhos eleva a média.

4. **Gênero e compras:** Clientes do gênero Feminino (F) realizaram mais compras (382.427) do que o Masculino (M) (351.020), representando aproximadamente 52% das transações.

5. **Categoria mais vendida:** ALIMENTOS lidera com 384.197 compras (>52% do total), seguida por HIGIENE e LIMPEZA. ACESSORIOS registra o menor volume (12.871).

6. **Limitações remanescentes:** A base não contém coluna de valor monetário (preço/receita), o que impede análises de faturamento. As colunas `CL_EC` e `CL_SEG` carecem de dicionário de dados oficial.

---

## Reflexão teórica — ETL e Qualidade de Dados

**ETL** (*Extract, Transform, Load*) é o processo de extrair dados de uma fonte, transformá-los para garantir consistência e qualidade, e carregá-los em um destino (banco de dados, dashboard, modelo etc.). Neste projeto, as três etapas estiveram presentes:

- **Extract:** leitura do arquivo `Base_Varejo.csv` com `pd.read_csv()`.
- **Transform:** remoção de colunas vazias, tratamento de categorias inválidas, conversão do tipo da coluna `DATA` e eliminação de duplicatas — encapsulados na função `obter_dados()`.
- **Load:** o DataFrame limpo é consumido tanto pelo script de análise quanto pelo dashboard Streamlit, que o utiliza para gerar visualizações interativas em tempo real.

**Qualidade de dados** é um fator crítico em projetos de BI e ciência de dados. Dados de baixa qualidade geram análises incorretas e decisões equivocadas. Os principais problemas encontrados nesta base — duplicatas, categorias inconsistentes (`#N/D`) e tipo de dado incorreto em `DATA` — são exemplos clássicos de problemas de qualidade que precisam ser tratados antes de qualquer análise. Adotar práticas sistemáticas de verificação e limpeza (como as realizadas nas Sprints 2 e 3) é essencial para garantir que os resultados sejam confiáveis e reproduzíveis.