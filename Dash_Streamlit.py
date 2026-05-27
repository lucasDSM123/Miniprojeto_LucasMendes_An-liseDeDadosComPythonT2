# =============================================================================
# DASHBOARD — ANÁLISE EXPLORATÓRIA DE DADOS | BASE VAREJO
# Aluno  : Lucas Mendes | Turma: T2 — Análise de Dados com Python
# Execução: streamlit run Dash_Streamlit.py
#
# DEPENDÊNCIA: Miniprojeto_LucasMendes_AnáliseDeDadosComPythonT2.py
#   O DataFrame é obtido pela função obter_dados() definida naquele módulo.
#   Ambos os arquivos devem estar na mesma pasta que Base_Varejo.csv.
# =============================================================================

import sys
import os
import pandas as pd
import plotly.express as px
import streamlit as st

# ── Importa a função de limpeza do script principal ──────────────────────────
# Adiciona o diretório atual ao path para garantir o import independente
# de onde o streamlit for executado.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Miniprojeto_LucasMendes_AnáliseDeDadosComPythonT2 import obter_dados

# ── Configuração da página ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard Varejo",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS customizado ───────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0f1117; }

    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #1e2130, #252a3d);
        border: 1px solid #2e3555;
        border-radius: 12px;
        padding: 16px 20px;
    }
    [data-testid="metric-container"] label {
        color: #8b92b8 !important;
        font-size: 0.78rem !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #e8eaf6 !important;
        font-size: 1.7rem !important;
        font-weight: 700;
    }
    [data-testid="metric-container"] [data-testid="stMetricDelta"] {
        color: #64b5f6 !important;
    }
    [data-testid="stSidebar"] {
        background-color: #131621;
        border-right: 1px solid #1e2130;
    }
    .section-title {
        font-size: 0.72rem;
        font-weight: 700;
        color: #5c6bc0;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin: 24px 0 8px 0;
    }
    .hero {
        background: linear-gradient(135deg, #1a1f35 0%, #1e2545 50%, #1a2035 100%);
        border: 1px solid #2e3a6e;
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 24px;
    }
    .hero h1 { color: #e8eaf6; font-size: 1.8rem; margin: 0 0 4px 0; }
    .hero p  { color: #7986cb; margin: 0; font-size: 0.95rem; }
    hr { border-color: #1e2545 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CARREGAMENTO — delega toda a limpeza ao script principal
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Carregando base via Miniprojeto_LucasMendes…")
def carregar_dados() -> pd.DataFrame:
    """
    Chama obter_dados() do script principal para obter o DataFrame já limpo
    (sem duplicatas, sem colunas vazias, DATA como datetime, #N/D tratado).
    Adiciona colunas auxiliares de label e período para uso nos gráficos.
    """
    df = obter_dados("Base_Varejo.csv")

    # Colunas auxiliares para exibição
    df["ANO"]          = df["DATA"].dt.year
    df["MES"]          = df["DATA"].dt.month
    df["GENERO_LABEL"] = df["CL_GENERO"].map({"F": "Feminino", "M": "Masculino"})
    df["SEG_LABEL"]    = df["CL_SEG"].map(
        {"A": "Premium (A)", "B": "Padrão (B)", "C": "Básico (C)"}
    )
    return df

df = carregar_dados()

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — FILTROS
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛒 Base Varejo")
    st.markdown("---")

    st.markdown('<p class="section-title">Período</p>', unsafe_allow_html=True)
    anos_disp = sorted(df["ANO"].dropna().unique())
    anos_sel  = st.multiselect("Ano", anos_disp, default=[])

    st.markdown('<p class="section-title">Gênero</p>', unsafe_allow_html=True)
    generos_disp = sorted(df["GENERO_LABEL"].unique())
    generos_sel  = st.multiselect("Gênero", generos_disp, default=[])

    st.markdown('<p class="section-title">Segmento</p>', unsafe_allow_html=True)
    segs_disp = sorted(df["SEG_LABEL"].dropna().unique())
    segs_sel  = st.multiselect("Segmento", segs_disp, default=[])

    st.markdown('<p class="section-title">Categoria</p>', unsafe_allow_html=True)
    cats_disp = sorted(df["PR_CAT"].unique())
    cats_sel  = st.multiselect("Categoria", cats_disp, default=[])

    st.markdown("---")
    st.caption("Mini-Projeto · Lucas Mendes · T2")

# ─────────────────────────────────────────────────────────────────────────────
# APLICAR FILTROS
# Regra: seleção vazia = sem restrição nessa dimensão (mostra todos)
# ─────────────────────────────────────────────────────────────────────────────
anos_ativos    = anos_sel    if anos_sel    else anos_disp
generos_ativos = generos_sel if generos_sel else generos_disp
segs_ativos    = segs_sel    if segs_sel    else segs_disp
cats_ativas    = cats_sel    if cats_sel    else cats_disp

dff = df[
    df["ANO"].isin(anos_ativos) &
    df["GENERO_LABEL"].isin(generos_ativos) &
    df["SEG_LABEL"].isin(segs_ativos) &
    df["PR_CAT"].isin(cats_ativas)
]

# ─────────────────────────────────────────────────────────────────────────────
# CABEÇALHO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>🛒 Dashboard · Análise de Varejo</h1>
  <p>Análise Exploratória de Dados — Mini-Projeto Avaliativo · Módulo 1 · Lucas Mendes · T2</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# KPIs
# ─────────────────────────────────────────────────────────────────────────────
total_registros = len(dff)
total_clientes  = dff["CL_ID"].nunique()
total_compras   = dff["CO_ID"].nunique()
media_filhos    = dff["CL_FHL"].mean() if total_registros else 0
cat_top         = dff["PR_CAT"].value_counts().idxmax() if total_registros else "—"
genero_top      = dff["GENERO_LABEL"].value_counts().idxmax() if total_registros else "—"

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("📋 Registros",    f"{total_registros:,}")
k2.metric("👤 Clientes",     f"{total_clientes:,}")
k3.metric("🛍️ Compras",     f"{total_compras:,}")
k4.metric("👶 Média Filhos", f"{media_filhos:.2f}")
k5.metric("🏆 Cat. Líder",   cat_top)
k6.metric("⭐ Gênero Líder", genero_top)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# LINHA 2 — Compras por Categoria | Compras por Gênero
# ─────────────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<p class="section-title">Compras por Categoria de Produto</p>', unsafe_allow_html=True)
    cat_data = (
        dff["PR_CAT"].value_counts().reset_index()
        .rename(columns={"PR_CAT": "Categoria", "count": "Compras"})
    )
    fig_cat = px.bar(
        cat_data, x="Compras", y="Categoria", orientation="h",
        color="Compras",
        color_continuous_scale=["#1e2545", "#3949ab", "#7986cb", "#c5cae9"],
        text="Compras",
    )
    fig_cat.update_traces(texttemplate="%{text:,}", textposition="outside")
    fig_cat.update_layout(
        plot_bgcolor="#0f1117", paper_bgcolor="#0f1117",
        font_color="#c5cae9", showlegend=False, coloraxis_showscale=False,
        margin=dict(l=10, r=40, t=10, b=10),
        xaxis=dict(showgrid=False, color="#3a4060"),
        yaxis=dict(showgrid=False, categoryorder="total ascending"),
        height=320,
    )
    st.plotly_chart(fig_cat, use_container_width=True)

with col2:
    st.markdown('<p class="section-title">Compras por Gênero</p>', unsafe_allow_html=True)
    gen_data = dff["GENERO_LABEL"].value_counts().reset_index()
    gen_data.columns = ["Gênero", "Compras"]
    fig_gen = px.pie(
        gen_data, names="Gênero", values="Compras", hole=0.55,
        color_discrete_sequence=["#5c6bc0", "#9fa8da"],
    )
    fig_gen.update_traces(textinfo="percent+label", textfont_color="#e8eaf6")
    fig_gen.update_layout(
        plot_bgcolor="#0f1117", paper_bgcolor="#0f1117",
        font_color="#c5cae9", showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        height=320,
    )
    st.plotly_chart(fig_gen, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# LINHA 3 — Evolução temporal | Distribuição de Filhos
# ─────────────────────────────────────────────────────────────────────────────
col3, col4 = st.columns([3, 2])

with col3:
    st.markdown('<p class="section-title">Evolução de Compras ao Longo do Tempo</p>', unsafe_allow_html=True)
    tempo = (
        dff.groupby(dff["DATA"].dt.to_period("M"))
        .size().reset_index(name="Compras")
    )
    tempo["DATA"] = tempo["DATA"].astype(str)
    fig_tempo = px.area(
        tempo, x="DATA", y="Compras",
        color_discrete_sequence=["#5c6bc0"],
    )
    fig_tempo.update_traces(
        fill="tozeroy", line_color="#7986cb",
        fillcolor="rgba(92,107,192,0.15)"
    )
    fig_tempo.update_layout(
        plot_bgcolor="#0f1117", paper_bgcolor="#0f1117",
        font_color="#c5cae9",
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(showgrid=False, color="#3a4060", tickangle=-35),
        yaxis=dict(showgrid=True, gridcolor="#1e2545", color="#3a4060"),
        height=300,
    )
    st.plotly_chart(fig_tempo, use_container_width=True)

with col4:
    st.markdown('<p class="section-title">Distribuição — Nº de Filhos dos Clientes</p>', unsafe_allow_html=True)
    filhos_data = dff["CL_FHL"].value_counts().sort_index().reset_index()
    filhos_data.columns = ["Filhos", "Clientes"]
    fig_filhos = px.bar(
        filhos_data, x="Filhos", y="Clientes",
        color="Clientes",
        color_continuous_scale=["#1e2545", "#3949ab", "#7986cb"],
        text="Clientes",
    )
    fig_filhos.update_traces(texttemplate="%{text:,}", textposition="outside")
    fig_filhos.update_layout(
        plot_bgcolor="#0f1117", paper_bgcolor="#0f1117",
        font_color="#c5cae9", showlegend=False, coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(showgrid=False, color="#3a4060", tickmode="linear"),
        yaxis=dict(showgrid=False),
        height=300,
    )
    st.plotly_chart(fig_filhos, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# LINHA 4 — Compras por Segmento | Estatísticas Descritivas
# ─────────────────────────────────────────────────────────────────────────────
col5, col6 = st.columns([1, 1])

with col5:
    st.markdown('<p class="section-title">Compras por Segmento de Cliente</p>', unsafe_allow_html=True)
    seg_data = (
        dff[dff["SEG_LABEL"].notna()]
        .groupby("SEG_LABEL")["CO_ID"].count().reset_index()
        .rename(columns={"CO_ID": "Compras", "SEG_LABEL": "Segmento"})
        .sort_values("Compras", ascending=False)
    )
    seg_data["Segmento"] = seg_data["Segmento"].astype(str)
    fig_seg = px.bar(
        seg_data, x="Segmento", y="Compras",
        color="Compras",
        color_continuous_scale=["#1e2545", "#3949ab", "#9fa8da"],
        text="Compras",
    )
    fig_seg.update_traces(texttemplate="%{text:,}", textposition="outside")
    fig_seg.update_layout(
        plot_bgcolor="#0f1117", paper_bgcolor="#0f1117",
        font_color="#c5cae9", showlegend=False, coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=10, b=30),
        xaxis=dict(showgrid=False, color="#3a4060"),
        yaxis=dict(showgrid=False),
        height=300,
    )
    st.plotly_chart(fig_seg, use_container_width=True)

with col6:
    st.markdown('<p class="section-title">📊 Estatísticas Descritivas — Nº de Filhos (CL_FHL)</p>', unsafe_allow_html=True)
    s = dff["CL_FHL"]

    # Helpers seguros para Series que podem ser vazias ou ter 1 elemento
    def _fmt(val, fmt):
        try:
            return format(val, fmt) if pd.notna(val) else "—"
        except Exception:
            return "—"

    moda_val  = s.mode().iloc[0] if not s.mode().empty else "—"
    std_val   = s.std() if len(s) > 1 else "—"

    stats = pd.DataFrame({
        "Parâmetro": ["Contagem", "Mínimo", "Máximo", "Média", "Mediana",
                      "Moda", "Desvio Padrão", "Q1 (25%)", "Q3 (75%)"],
        "Valor": [
            f"{s.count():,}",
            _fmt(s.min(), ""),
            _fmt(s.max(), ""),
            _fmt(s.mean(), ".4f"),
            _fmt(s.median(), ".1f"),
            str(moda_val),
            _fmt(std_val, ".4f"),
            _fmt(s.quantile(0.25), ".1f"),
            _fmt(s.quantile(0.75), ".1f"),
        ]
    })
    st.dataframe(stats, use_container_width=True, hide_index=True, height=338)

# ─────────────────────────────────────────────────────────────────────────────
# LINHA 5 — Heatmap Categoria x Gênero
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">Heatmap — Compras por Categoria e Gênero</p>', unsafe_allow_html=True)

heat_data = (
    dff.groupby(["PR_CAT", "GENERO_LABEL"])["CO_ID"]
    .count().reset_index().rename(columns={"CO_ID": "Compras"})
)
heat_pivot = heat_data.pivot(
    index="PR_CAT", columns="GENERO_LABEL", values="Compras"
).fillna(0)

fig_heat = px.imshow(
    heat_pivot,
    color_continuous_scale=["#0f1117", "#1e2545", "#3949ab", "#7986cb", "#c5cae9"],
    text_auto=True, aspect="auto",
)
fig_heat.update_layout(
    plot_bgcolor="#0f1117", paper_bgcolor="#0f1117",
    font_color="#c5cae9", coloraxis_showscale=False,
    margin=dict(l=10, r=10, t=10, b=10),
    xaxis=dict(showgrid=False, color="#3a4060"),
    yaxis=dict(showgrid=False, color="#3a4060"),
    height=280,
)
st.plotly_chart(fig_heat, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# RODAPÉ
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#3a4060; font-size:0.8rem;'>"
    "Mini-Projeto Avaliativo · Módulo 1 · Lucas Mendes · T2 · Análise de Dados com Python"
    "</p>",
    unsafe_allow_html=True,
)