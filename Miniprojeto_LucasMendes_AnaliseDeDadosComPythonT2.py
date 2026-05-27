# =============================================================================
# ANÁLISE EXPLORATÓRIA DE DADOS - BASE VAREJO
# Mini-Projeto Avaliativo - Módulo 1 - Semana 07
# Disciplina: Análise de Dados com Python [T2]
# Aluno : Lucas Mendes | Turma: T2
# =============================================================================
# INSTRUÇÕES DE EXECUÇÃO:
#   1. Coloque o arquivo Base_Varejo.csv na mesma pasta deste script.
#   2. Abra o terminal no VS Code nessa pasta.
#   3. Execute: python Miniprojeto_LucasMendes_AnáliseDeDadosComPythonT2.py
#
# INTEGRAÇÃO COM DASHBOARD:
#   Este arquivo também funciona como módulo. O Dash_Streamlit.py importa a
#   função obter_dados() daqui para reutilizar o DataFrame já limpo.
#   Exemplo: from Miniprojeto_LucasMendes_AnáliseDeDadosComPythonT2 import obter_dados
# =============================================================================

import pandas as pd


# ===========================================================================
# FUNÇÃO PRINCIPAL DE LIMPEZA — usada tanto pelo script quanto pelo dashboard
# Retorna o DataFrame já limpo e pronto para análise.
# ===========================================================================

def obter_dados(caminho_csv: str = "Base_Varejo.csv") -> pd.DataFrame:
    """
    Carrega Base_Varejo.csv, executa todas as etapas de limpeza (Sprints 2-3)
    e retorna o DataFrame limpo.

    Parâmetros
    ----------
    caminho_csv : str
        Caminho para o arquivo CSV (padrão: mesma pasta do script).

    Retorna
    -------
    pd.DataFrame
        Base limpa com 10 colunas e sem duplicatas.
    """

    # Sprint 1 — Importação
    df = pd.read_csv(caminho_csv, sep=None, engine="python")

    # Sprint 3.1 — Remove colunas completamente nulas
    # Justificativa: artefatos do CSV exportado, sem nenhuma informação útil.
    colunas_vazias = [col for col in df.columns if df[col].isnull().all()]
    df.drop(columns=colunas_vazias, inplace=True)

    # Sprint 3.2 — Substitui categoria inválida '#N/D' por 'Sem Categoria'
    # Justificativa: '#N/D' é erro de preenchimento. Imputar 'Sem Categoria'
    # preserva os registros sem falsear agrupamentos por categoria.
    df["PR_CAT"] = df["PR_CAT"].apply(
        lambda x: "Sem Categoria" if x == "#N/D" else x
    )

    # Sprint 3.3 — Converte DATA de string para datetime (formato DD/MM/YYYY)
    df["DATA"] = pd.to_datetime(df["DATA"], format="%d/%m/%Y", errors="coerce")

    # Sprint 3.4 — Remove linhas completamente duplicadas
    # Justificativa: linhas idênticas em todos os campos indicam erro de
    # duplicação no registro, não compras repetidas legítimas.
    df.drop_duplicates(inplace=True)

    return df


# ===========================================================================
# BLOCO PRINCIPAL — executado apenas via `python script.py`, nunca via import
# ===========================================================================

if __name__ == "__main__":

    # ── Sprint 1 — Importação ────────────────────────────────────────────────
    print("=" * 65)
    print("SPRINT 1 — IMPORTAÇÃO DOS DADOS")
    print("=" * 65)

    df_raw = pd.read_csv("Base_Varejo.csv", sep=None, engine="python")

    print(f"\nNúmero de registros : {df_raw.shape[0]:,}")
    print(f"Número de colunas   : {df_raw.shape[1]}")
    print("\nColunas e tipos de dados:")
    print(df_raw.dtypes.to_string())
    print("\nPrimeiras 3 linhas da base:")
    print(df_raw.head(3).to_string())

    # ── Sprint 2 — Verificação de Problemas ──────────────────────────────────
    print("\n" + "=" * 65)
    print("SPRINT 2 — VERIFICAÇÃO DE PROBLEMAS")
    print("=" * 65)

    colunas_vazias = [col for col in df_raw.columns if df_raw[col].isnull().all()]
    print(f"\n[PROBLEMA 1] Colunas 100% nulas (serão removidas): {colunas_vazias}")

    nulos = df_raw.drop(columns=colunas_vazias).isnull().sum()
    print("\n[PROBLEMA 2] Valores nulos por coluna (colunas úteis):")
    print(nulos.to_string())

    total_duplicatas = df_raw.duplicated().sum()
    print(f"\n[PROBLEMA 3] Linhas completamente duplicadas: {total_duplicatas:,}")

    cats_invalidas = df_raw[df_raw["PR_CAT"] == "#N/D"].shape[0]
    print(f"\n[PROBLEMA 4] Registros com categoria '#N/D' (inválida): {cats_invalidas:,}")

    print(f"\n[PROBLEMA 5] Tipo da coluna DATA: '{df_raw['DATA'].dtype}' "
          f"(deve ser datetime)")

    # ── Sprint 3 — Limpeza ───────────────────────────────────────────────────
    print("\n" + "=" * 65)
    print("SPRINT 3 — LIMPEZA DOS DADOS")
    print("=" * 65)

    # Usa a função obter_dados() para executar toda a limpeza
    df = obter_dados("Base_Varejo.csv")

    print(f"\n[3.1] Colunas nulas removidas: {colunas_vazias}")
    print(f"[3.2] Categoria '#N/D' substituída por 'Sem Categoria'.")
    print(f"      Categorias únicas agora: {df['PR_CAT'].unique().tolist()}")
    print(f"[3.3] Coluna DATA convertida para datetime.")
    print(f"      Datas inválidas (NaT): {df['DATA'].isnull().sum():,}")
    print(f"[3.4] Duplicatas removidas: {df_raw.shape[0] - df.shape[0]:,} linhas "
          f"({df_raw.shape[0]:,} → {df.shape[0]:,} registros)")

    print(f"\n[RESUMO] Base após limpeza: {df.shape[0]:,} registros, "
          f"{df.shape[1]} colunas.")
    print("Tipos finais das colunas:")
    print(df.dtypes.to_string())

    # ── Sprint 4 — Estatística Descritiva ────────────────────────────────────
    print("\n" + "=" * 65)
    print("SPRINT 4 — ESTATÍSTICA DESCRITIVA: Nº DE FILHOS (CL_FHL)")
    print("=" * 65)

    filhos     = df["CL_FHL"]
    media      = filhos.mean()
    mediana    = filhos.median()
    desvio_pad = filhos.std()
    moda       = filhos.mode()[0]
    maximo     = filhos.max()
    minimo     = filhos.min()
    contagem   = filhos.count()
    q1         = filhos.quantile(0.25)
    q3         = filhos.quantile(0.75)

    print(f"\n  Contagem  : {contagem:,}")
    print(f"  Mínimo    : {minimo}")
    print(f"  Máximo    : {maximo}")
    print(f"  Média     : {media:.4f}")
    print(f"  Mediana   : {mediana}")
    print(f"  Moda      : {moda}")
    print(f"  Desvio Pad: {desvio_pad:.4f}")
    print(f"  Q1 (25%)  : {q1}")
    print(f"  Q3 (75%)  : {q3}")

    print("\n  [Interpretação]")
    print(f"  A maioria dos clientes não tem filhos (mediana e moda = {int(moda)}).")
    print(f"  A média de {media:.2f} filhos indica que poucos clientes puxam a média")
    print(f"  para cima, com máximo de {int(maximo)} filhos registrados.")

    # ── Sprint 5 — Padrões de Agrupamento ────────────────────────────────────
    print("\n" + "=" * 65)
    print("SPRINT 5 — PADRÕES DE AGRUPAMENTO")
    print("=" * 65)

    compras_genero = (
        df.groupby("CL_GENERO")["CO_ID"]
        .count().reset_index()
        .rename(columns={"CO_ID": "QTD_COMPRAS"})
        .sort_values("QTD_COMPRAS", ascending=False)
    )
    print("\n[AGRUPAMENTO 1] Total de compras por Gênero:")
    print(compras_genero.to_string(index=False))
    print(f"\n  → Gênero com mais compras: '{compras_genero.iloc[0]['CL_GENERO']}'")

    compras_cat = (
        df.groupby("PR_CAT")["CO_ID"]
        .count().reset_index()
        .rename(columns={"CO_ID": "QTD_COMPRAS"})
        .sort_values("QTD_COMPRAS", ascending=False)
    )
    print("\n[AGRUPAMENTO 2] Total de compras por Categoria de Produto:")
    print(compras_cat.to_string(index=False))
    print(f"\n  → Categoria com mais vendas: '{compras_cat.iloc[0]['PR_CAT']}'")

    pivot_seg = pd.pivot_table(
        df, values="CL_FHL", index="CL_SEG",
        aggfunc=["mean", "count"]
    )
    pivot_seg.columns = ["Media_Filhos", "Qtd_Registros"]
    pivot_seg = pivot_seg.sort_values("Qtd_Registros", ascending=False)
    print("\n[AGRUPAMENTO 3 - pivot_table] Segmento de Cliente x Média de Filhos:")
    print(pivot_seg.round(2).to_string())

    # ── Conclusões ────────────────────────────────────────────────────────────
    print("\n" + "=" * 65)
    print("CONCLUSÕES E INSIGHTS DA ANÁLISE")
    print("=" * 65)
    print("""
  1. QUALIDADE DOS DADOS
     A base continha 4 colunas completamente vazias (artefatos do CSV)
     e 96.553 linhas duplicadas, que foram removidos antes da análise.
     Após limpeza, a base ficou com registros únicos e bem estruturados.

  2. CATEGORIA INVÁLIDA
     3.650 registros tinham a categoria '#N/D' (dado ausente/inválido).
     Foram classificados como 'Sem Categoria' para preservar os registros
     sem comprometer agrupamentos por categoria.

  3. FILHOS DOS CLIENTES
     A maioria dos clientes não possui filhos (mediana = moda = 0).
     A média de ~1.15 filhos e desvio padrão de ~1.42 indicam distribuição
     assimétrica à direita — poucos clientes com muitos filhos elevam a média.

  4. GÊNERO E COMPRAS
     Clientes do gênero Feminino realizaram mais compras que o Masculino
     na base analisada, representando a maior fatia de transações.

  5. CATEGORIA MAIS VENDIDA
     ALIMENTOS lidera com ampla margem (>50% das compras), seguida de
     HIGIENE e LIMPEZA. ACESSORIOS tem o menor volume de vendas.

  6. PROBLEMAS REMANESCENTES
     - A coluna DATA foi convertida com sucesso, mas análises temporais
       (sazonalidade, tendências) ainda não foram exploradas.
     - Não há coluna de valor monetário (preço/receita) na base fornecida,
       o que limita análises de faturamento e ticket médio.
     - O significado de CL_EC (estado civil?) e CL_SEG (segmento A/B/C)
       não foi documentado na base — confirmar com a origem dos dados.
""")
    print("=" * 65)
    print("FIM DA ANÁLISE EXPLORATÓRIA")
    print("=" * 65)
