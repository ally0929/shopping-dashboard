import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Insights on Marketing and Discounts", layout="wide")

st.markdown("""
    <style>
    header[data-testid="stHeader"] { background-color: #0A0E27; }
    .stApp { background-color: #0A0E27; color: white; }
    [data-testid="stSidebar"] { background-color: #151B3B; }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="metric-container"] {
        background-color: #151B3B;
        border: 1px solid #2A3060;
        border-radius: 10px;
        padding: 15px;
    }
    [data-testid="stMetricValue"] { color: #5B9BD5 !important; font-size: 2rem !important; }
    [data-testid="stMetricLabel"] { color: #AAAAAA !important; }
    h1, h2, h3, p, label, .stMarkdown { color: white !important; }
    hr { border-color: #2A3060; }
    .stMultiSelect span { background-color: #2A3060 !important; color: white !important; }
    .modebar { display: none !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #151B3B; border-radius: 10px; padding: 4px; }
    .stTabs [data-baseweb="tab"] { color: #AAAAAA !important; background-color: transparent; border-radius: 8px; padding: 8px 20px; }
    .stTabs [aria-selected="true"] { background-color: #5B9BD5 !important; color: white !important; }
    .insight-box {
        background-color: #151B3B;
        border-left: 4px solid #2ECC71;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 8px 0 16px 0;
    }
    .warning-box {
        background-color: #151B3B;
        border-left: 4px solid #E74C3C;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 8px 0 16px 0;
    }
    </style>
""", unsafe_allow_html=True)

df = pd.read_csv("shopping_behavior_updated.csv")

def add_age_group(dataframe):
    dataframe = dataframe.copy()
    dataframe["Age Group"] = pd.cut(
        dataframe["Age"],
        bins=[0, 25, 35, 45, 55, 100],
        labels=["18-25", "26-35", "36-45", "46-55", "56+"]
    )
    return dataframe

def style(fig):
    fig.update_layout(
        paper_bgcolor="#0A0E27",
        plot_bgcolor="#0A0E27",
        font=dict(color="white", size=13),
        xaxis=dict(gridcolor="rgba(255,255,255,0.08)", tickfont=dict(color="white"), title_font=dict(color="white")),
        yaxis=dict(gridcolor="rgba(255,255,255,0.08)", tickfont=dict(color="white"), title_font=dict(color="white")),
        legend=dict(font=dict(color="white"), bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=20, b=40, l=20, r=20)
    )
    return fig

no_toolbar = {"displayModeBar": False}

st.sidebar.markdown("## Filters")
season_sel = st.sidebar.multiselect("Season", df["Season"].unique(), default=df["Season"].unique())
category_sel = st.sidebar.multiselect("Category", df["Category"].unique(), default=df["Category"].unique())
gender_sel = st.sidebar.multiselect("Gender", df["Gender"].unique(), default=df["Gender"].unique())

filtered = df[
    (df["Season"].isin(season_sel)) &
    (df["Category"].isin(category_sel)) &
    (df["Gender"].isin(gender_sel))
]
filtered = add_age_group(filtered)

st.markdown("<h1>Insights on Marketing and Discounts</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#AAAAAA; font-size:18px;'>Who should we market to — and is the discount actually worth it?</p>", unsafe_allow_html=True)
st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview",
    "Finance",
    "Discounts",
    "Selling Frequency",
    "Recommendations"
])

# TAB 1 — OVERVIEW
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Customers", f"{len(filtered):,}")
    col2.metric("Total Revenue", f"${filtered['Purchase Amount (USD)'].sum():,.0f}")
    col3.metric("Avg Spent Per Customer", f"${filtered['Purchase Amount (USD)'].mean():.2f}")
    col4.metric("Top Season", filtered.groupby("Season")["Purchase Amount (USD)"].mean().idxmax())

    st.divider()

    st.markdown("""
        <div class='warning-box'>
        <b style='color:#E74C3C; font-size:16px;'>Why this research matters:</b><br><br>
        <span style='color:white; font-size:15px;'>
        Retail marketers waste budget by treating all customers the same.
        This data shows that your highest volume customers are 56+ males —
        but your highest value customers per purchase are female.
        Despite this, 100% of discounts in this dataset went exclusively to male customers.
        The budget is being spent on the wrong people.
        </span>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### Revenue: Based on Customer Age")
    age_rev = filtered.groupby("Age Group", observed=True)["Purchase Amount (USD)"].sum()
    total_rev = age_rev.sum()
    for age in ["56+", "46-55", "36-45", "26-35", "18-25"]:
        if age in age_rev.index:
            pct = age_rev[age] / total_rev
            color = "#2ECC71" if age == "56+" else "#5B9BD5"
            st.markdown(f"""
                <div style='display:flex; align-items:center; margin-bottom:10px;'>
                    <div style='width:80px; color:white; font-size:14px; font-weight:500;'>{age}</div>
                    <div style='flex:1; background:#1E2A45; border-radius:6px; height:24px; margin:0 12px;'>
                        <div style='width:{pct*100:.1f}%; background:{color}; height:24px; border-radius:6px;'></div>
                    </div>
                    <div style='width:50px; color:white; font-size:14px; text-align:right;'>{pct*100:.1f}%</div>
                </div>
            """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### Revenue: Based on Customer Gender")
    gender_rev = filtered.groupby("Gender")["Purchase Amount (USD)"].sum()
    total_gender = gender_rev.sum()
    for gender in ["Male", "Female"]:
        if gender in gender_rev.index:
            pct = gender_rev[gender] / total_gender
            color = "#5B9BD5" if gender == "Male" else "#2ECC71"
            st.markdown(f"""
                <div style='display:flex; align-items:center; margin-bottom:10px;'>
                    <div style='width:80px; color:white; font-size:14px; font-weight:500;'>{gender}</div>
                    <div style='flex:1; background:#1E2A45; border-radius:6px; height:24px; margin:0 12px;'>
                        <div style='width:{pct*100:.1f}%; background:{color}; height:24px; border-radius:6px;'></div>
                    </div>
                    <div style='width:50px; color:white; font-size:14px; text-align:right;'>{pct*100:.1f}%</div>
                </div>
            """, unsafe_allow_html=True)

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Number of Customers by Age")
        age_count = filtered.groupby("Age Group", observed=True).size().reset_index(name="Customers")
        bar_colors = ["#E74C3C" if a == "56+" else "#5B9BD5" for a in age_count["Age Group"]]
        fig = px.bar(age_count, x="Age Group", y="Customers", color="Age Group",
            color_discrete_map={a: ("#E74C3C" if a == "56+" else "#5B9BD5") for a in age_count["Age Group"]})
        fig = style(fig)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True, config=no_toolbar)

    with col2:
        st.markdown("### Gender Split")
        gender_count = filtered.groupby("Gender").size().reset_index(name="Customers")
        fig2 = px.pie(gender_count, names="Gender", values="Customers", color="Gender",
            color_discrete_map={"Male": "#5B9BD5", "Female": "#2ECC71"}, hole=0.5)
        fig2.update_layout(paper_bgcolor="#0A0E27", font=dict(color="white"), legend=dict(font=dict(color="white")))
        fig2.update_traces(textfont=dict(color="white"))
        st.plotly_chart(fig2, use_container_width=True, config=no_toolbar)

# TAB 2 — FINANCE
with tab2:
    st.markdown("### Where is the money coming from?")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Age vs Purchase Amount")
        fig3 = px.scatter(filtered, x="Age", y="Purchase Amount (USD)", color="Gender",
            color_discrete_map={"Male": "#5B9BD5", "Female": "#2ECC71"}, opacity=0.5)
        fig3 = style(fig3)
        st.plotly_chart(fig3, use_container_width=True, config=no_toolbar)

    with col2:
        st.markdown("### Spend Distribution by Gender")
        fig4 = px.box(filtered, x="Gender", y="Purchase Amount (USD)", color="Gender",
            color_discrete_map={"Male": "#5B9BD5", "Female": "#2ECC71"})
        fig4 = style(fig4)
        fig4.update_layout(showlegend=False, yaxis=dict(range=[30, 100]))
        st.plotly_chart(fig4, use_container_width=True, config=no_toolbar)

    st.divider()

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("### Total Revenue by Age Group")
        age_rev2 = filtered.groupby("Age Group", observed=True)["Purchase Amount (USD)"].sum().reset_index()
        age_rev2.columns = ["Age Group", "Total Revenue ($)"]
        fig5 = px.bar(age_rev2, x="Age Group", y="Total Revenue ($)", color="Age Group",
            color_discrete_map={a: ("#E74C3C" if a == "56+" else "#5B9BD5") for a in age_rev2["Age Group"]})
        fig5 = style(fig5)
        fig5.update_layout(showlegend=False)
        st.plotly_chart(fig5, use_container_width=True, config=no_toolbar)

    with col4:
        st.markdown("### Revenue by Category and Gender")
        gender_cat = filtered.groupby(["Category", "Gender"])["Purchase Amount (USD)"].sum().reset_index()
        gender_cat.columns = ["Category", "Gender", "Total Revenue ($)"]
        fig6 = px.treemap(gender_cat, path=["Gender", "Category"], values="Total Revenue ($)",
            color="Gender", color_discrete_map={"Male": "#5B9BD5", "Female": "#2ECC71"})
        fig6.update_layout(paper_bgcolor="#0A0E27", font=dict(color="white"), margin=dict(t=20, b=20, l=20, r=20))
        fig6.update_traces(textfont=dict(color="white"))
        st.plotly_chart(fig6, use_container_width=True, config=no_toolbar)

# TAB 3 — DISCOUNTS
with tab3:
    st.markdown("### Are discounts working — and who is getting them?")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Discount Distribution by Gender")
        disc_gender = filtered.groupby(["Gender", "Discount Applied"]).size().reset_index(name="Count")
        fig7 = px.bar(disc_gender, x="Gender", y="Count", color="Discount Applied", barmode="group",
            color_discrete_map={"Yes": "#E74C3C", "No": "#5B9BD5"})
        fig7 = style(fig7)
        st.plotly_chart(fig7, use_container_width=True, config=no_toolbar)

    with col2:
        st.markdown("### Spend Distribution — Discount vs No Discount")
        fig8 = px.box(filtered, x="Discount Applied", y="Purchase Amount (USD)", color="Discount Applied",
            color_discrete_map={"Yes": "#E74C3C", "No": "#2ECC71"})
        fig8 = style(fig8)
        fig8.update_layout(showlegend=False, yaxis=dict(range=[30, 100]))
        st.plotly_chart(fig8, use_container_width=True, config=no_toolbar)

    st.divider()

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("### Promo Code Usage")
        promo_count = filtered.groupby("Promo Code Used").size().reset_index(name="Count")
        fig9 = px.pie(promo_count, names="Promo Code Used", values="Count", color="Promo Code Used",
            color_discrete_map={"Yes": "#E74C3C", "No": "#2ECC71"}, hole=0.5)
        fig9.update_layout(paper_bgcolor="#0A0E27", font=dict(color="white"), legend=dict(font=dict(color="white")))
        fig9.update_traces(textfont=dict(color="white"))
        st.plotly_chart(fig9, use_container_width=True, config=no_toolbar)

    with col4:
        st.markdown("### Discount Usage by Age Group")
        disc_age = filtered.groupby(["Age Group", "Discount Applied"], observed=True).size().reset_index(name="Count")
        fig10 = px.bar(disc_age, x="Age Group", y="Count", color="Discount Applied", barmode="group",
            color_discrete_map={"Yes": "#E74C3C", "No": "#5B9BD5"})
        fig10 = style(fig10)
        st.plotly_chart(fig10, use_container_width=True, config=no_toolbar)

# TAB 4 — SELLING FREQUENCY
with tab4:
    st.markdown("### What is selling — and when?")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Category Breakdown")
        cat_count = filtered.groupby("Category").size().reset_index(name="Number of Purchases")
        fig11 = px.treemap(cat_count, path=["Category"], values="Number of Purchases",
            color="Number of Purchases", color_continuous_scale=["#1E2A45", "#5B9BD5"])
        fig11.update_layout(paper_bgcolor="#0A0E27", font=dict(color="white"), margin=dict(t=20, b=20, l=20, r=20))
        fig11.update_traces(textfont=dict(color="white"))
        st.plotly_chart(fig11, use_container_width=True, config=no_toolbar)

    with col2:
        st.markdown("### Average Spend by Season")
        season_spend = filtered.groupby("Season")["Purchase Amount (USD)"].mean().reset_index()
        season_spend.columns = ["Season", "Avg Spend ($)"]
        season_spend = season_spend.sort_values("Avg Spend ($)", ascending=False)
        top_season = season_spend.iloc[0]["Season"]
        colors = ["#2ECC71" if s == top_season else "#5B9BD5" for s in season_spend["Season"]]
        fig12 = px.bar(season_spend, x="Season", y="Avg Spend ($)", color="Season", color_discrete_sequence=colors)
        fig12 = style(fig12)
        fig12.update_layout(showlegend=False)
        st.plotly_chart(fig12, use_container_width=True, config=no_toolbar)

    st.divider()

    st.markdown("### Purchase Frequency by Age Group")
    freq_age = filtered.groupby(["Age Group", "Frequency of Purchases"], observed=True).size().reset_index(name="Count")
    freq_pivot = freq_age.pivot(index="Frequency of Purchases", columns="Age Group", values="Count").fillna(0)
    fig13 = px.imshow(freq_pivot, color_continuous_scale=["#1E2A45", "#5B9BD5", "#2ECC71"], aspect="auto")
    fig13.update_layout(paper_bgcolor="#0A0E27", font=dict(color="white"),
        xaxis=dict(tickfont=dict(color="white"), title_font=dict(color="white")),
        yaxis=dict(tickfont=dict(color="white"), title_font=dict(color="white")),
        coloraxis_colorbar=dict(tickfont=dict(color="white"), title=dict(font=dict(color="white"))),
        margin=dict(t=20, b=40, l=20, r=20))
    st.plotly_chart(fig13, use_container_width=True, config=no_toolbar)

# TAB 5 — RECOMMENDATIONS
with tab5:
    st.markdown("### What should you actually do with this?")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='insight-box'>
        <b style='color:#2ECC71; font-size:16px;'>1. Start marketing to your female customer</b><br><br>
        <span style='color:white;'>Female customers spend more per purchase than males and receive zero discounts —
        yet they still buy. They are your most valuable buyer per transaction and you are
        not targeting them at all. Start running campaigns specifically aimed at women.</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='insight-box'>
        <b style='color:#2ECC71; font-size:16px;'>2. Stop giving discounts to everyone</b><br><br>
        <span style='color:white;'>Every discount in this dataset went to male customers who then spent less than
        non-discounted customers. Discounts are not changing behavior — they are just
        reducing your margin. Redirect that budget into targeted campaigns instead.</span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### Raw Data")
    st.dataframe(filtered.drop(columns=["Age Group"]).reset_index(drop=True), use_container_width=True, height=300)
