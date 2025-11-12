import pandas as pd
import streamlit as st
from pathlib import Path
import plotly.express as px

# -------------------- CONFIGURATION --------------------
st.set_page_config(
    page_title="🌞 Solar Data Dashboard",
    layout="wide",
    page_icon="🌍",
)

DATA_DIR = Path("data")

# -------------------- PAGE STYLES --------------------
st.markdown("""
    <style>
        /* Overall dark theme */
        .main {
            background-color: #0e1117;
            color: #fafafa;
            font-family: 'Inter', sans-serif;
        }

        /* Sidebar style */
        section[data-testid="stSidebar"] {
            background-color: #1c1f26 !important;
            padding: 20px;
        }

        h1, h2, h3, h4 {
            color: #f5c542;
            font-weight: 700;
        }

        .metric-label {
            font-size: 16px;
            color: #cccccc;
        }

        .metric-value {
            font-size: 28px;
            color: #ffffff;
        }

        .stButton>button {
            background-color: #f5c542;
            color: black;
            border-radius: 10px;
            font-weight: 600;
        }

        .stDownloadButton>button {
            background-color: #f5c542;
            color: black;
            border-radius: 10px;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------- FUNCTIONS --------------------
def list_available_countries():
    try:
        files = sorted(DATA_DIR.glob("*_clean.csv"))
        return [f.stem.replace('_clean','') for f in files]
    except Exception as e:
        st.error(f"Error accessing data directory: {e}")
        return []

def load_country_df(country_key):
    p = DATA_DIR / f"{country_key}_clean.csv"
    if not p.exists():
        raise FileNotFoundError(f"Data file not found: {p}")
    df = pd.read_csv(p, parse_dates=['Timestamp'])
    if 'country' not in df.columns:
        df['country'] = country_key
    return df

def combine_countries(country_keys):
    frames = []
    for c in country_keys:
        try:
            frames.append(load_country_df(c))
        except FileNotFoundError as e:
            st.warning(f"Data not found for {c}: {e}")
    if not frames:
        raise ValueError("No valid country data found")
    return pd.concat(frames, ignore_index=True)

def fig_boxplot(df, metric='GHI', by='country', sample_n=5000):
    if sample_n and len(df) > sample_n:
        df_plot = df.sample(sample_n, random_state=1)
    else:
        df_plot = df
    fig = px.box(
        df_plot, x=by, y=metric, points='outliers',
        color=by, title=f"{metric} Distribution by {by}",
        color_discrete_sequence=px.colors.qualitative.Safe,
        template="plotly_dark"
    )
    fig.update_layout(yaxis_title=f"{metric} (W/m²)", xaxis_title=str(by))
    return fig

def fig_bar_ranking(df, metric='GHI'):
    mean_vals = df.groupby('country')[metric].mean().sort_values(ascending=False).reset_index()
    fig = px.bar(
        mean_vals, x='country', y=metric,
        title=f"Mean {metric} by Country",
        color='country', text_auto=".1f",
        color_discrete_sequence=px.colors.qualitative.Bold,
        template="plotly_dark"
    )
    fig.update_layout(yaxis_title=f"{metric} (W/m²)", xaxis_title="Country")
    return fig

def top_regions_table(df, metric='GHI', top_n=10):
    group_col = 'Comments' if 'Comments' in df.columns and df['Comments'].notna().any() else 'country'
    table = (
        df.groupby(group_col)[metric]
          .agg(['count','mean','median','std'])
          .rename(columns={'count':'n'})
          .sort_values('mean', ascending=False)
    )
    return table.reset_index().head(top_n)

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.markdown("## 🌍 Dashboard Controls")
    available = list_available_countries()
    countries = st.multiselect("Select Countries", options=available, default=available[:2] if available else [])
    metric = st.selectbox("Select Metric", options=['GHI', 'DNI', 'DHI'], index=0)
    sample_n = st.slider("Sample Size", 1000, 20000, 5000, 1000)
    st.markdown("---")
    st.markdown("### 🔄 Refresh Data")
    if st.button("Refresh"):
        st.rerun()

# -------------------- MAIN DASHBOARD --------------------
st.markdown("# ☀️ Solar Data Dashboard")
if not countries:
    st.info("👈 Select at least one country to display results.")
    st.stop()

@st.cache_data(ttl=600)
def load_and_prepare(keys):
    return combine_countries(tuple(keys))

try:
    df_all = load_and_prepare(tuple(countries))
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

st.markdown(f"### 📊 Comparing {', '.join(countries)} on {metric}")

# ---- Metrics Section ----
col1, col2, col3 = st.columns(3)
col1.metric("🌎 Total Records", f"{len(df_all):,}")
col2.metric(f"⚡ Avg {metric}", f"{df_all[metric].mean():.2f} W/m²")
col3.metric("📅 Date Range", f"{df_all['Timestamp'].min().date()} → {df_all['Timestamp'].max().date()}")

# ---- Visuals ----
st.markdown("## 📈 Metric Distributions")
col4, col5 = st.columns([2,1])

with col4:
    fig_box = fig_boxplot(df_all, metric=metric, by='country', sample_n=sample_n)
    st.plotly_chart(fig_box, use_container_width=True)

with col5:
    fig_bar = fig_bar_ranking(df_all, metric=metric)
    st.plotly_chart(fig_bar, use_container_width=True)

# ---- Table ----
st.markdown("## 🧾 Top Regions by Mean Value")
top_n = st.number_input("Top N", 3, 50, 10)
table = top_regions_table(df_all, metric=metric, top_n=top_n)
st.dataframe(table.style.background_gradient(cmap="YlOrBr").format({
    'mean': "{:.2f}", 'median': "{:.2f}", 'std': "{:.2f}"
}))

# ---- Download ----
st.markdown("## 💾 Download Filtered Data")
csv = df_all.to_csv(index=False)
st.download_button("Download CSV", csv, "filtered_data.csv", "text/csv")
