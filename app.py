import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

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
    .desc-box {
        background-color: #151B3B;
        border-left: 4px solid #5B9BD5;
        border-radius: 8px;
        padding: 10px 14px;
        margin: 4px 0 16px 0;
    }
    .takeaway-box {
        background-color: #151B3B;
        border-left: 4px solid #2ECC71;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 16px 0 8px 0;
    }
    </style>
""", unsafe_allow_html=True)

df = pd.read_csv("shopping_behavior_updated.csv")

def add_age_group(d):
    d = d.copy()
    d["Age Group"] = pd.cut(d["Age"], bins=[0,25,35,45,55,100], labels=["18-25","26-35","36-45","46-55","56+"])
    return d

def style(fig):
    fig.update_layout(
        paper_bgcolor="#0A0E27", plot_bgcolor="#0A0E27",
        font=dict(color="white", size=13),
        xaxis=dict(gridcolor="rgba(255,255,255,0.08)", tickfont=dict(color="white"), title_font=dict(color="white")),
        yaxis=dict(gridcolor="rgba(255,255,255,0.08)", tickfont=dict(color="white"), title_font=dict(color="white")),
        legend=dict(font=dict(color="white"), bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=20, b=40, l=20, r=20)
    )
    return fig

def desc(text):
    st.markdown(f"<div class='desc-box'><span style='color:#AAAAAA; font-size:13px;'>{text}</span></div>", unsafe_allow_html=True)

def takeaway(points):
    bullets = "".join([f"<li style='color:white; font-size:13px; margin-bottom:6px;'>{p}</li>" for p in points])
    st.markdown(f"<ul style='padding-left:20px; margin:8px 0 16px 0;'>{bullets}</ul>", unsafe_allow_html=True)

NT = {"displayModeBar": False}

freq_colors = {
    "Annually": "#5B9BD5", "Bi-Weekly": "#2ECC71", "Every 3 Months": "#F39C12",
    "Fortnightly": "#9B59B6", "Monthly": "#E74C3C", "Quarterly": "#1ABC9C", "Weekly": "#E67E22"
}

st.sidebar.markdown("## Filters")
st.sidebar.markdown("<p style='color:#AAAAAA; font-size:12px; margin-top:-8px;'>Adjust filters to explore specific segments</p>", unsafe_allow_html=True)
season_sel = st.sidebar.multiselect("Season", df["Season"].unique(), default=df["Season"].unique())
category_sel = st.sidebar.multiselect("Category", df["Category"].unique(), default=df["Category"].unique())
gender_sel = st.sidebar.multiselect("Gender", df["Gender"].unique(), default=df["Gender"].unique())
st.sidebar.divider()
st.sidebar.markdown("<p style='color:#AAAAAA; font-size:12px;'>Dataset: shopping_behavior_updated.csv</p>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color:#AAAAAA; font-size:12px;'>3,900 customers · 18 columns</p>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color:#AAAAAA; font-size:12px;'>Source: Kaggle</p>", unsafe_allow_html=True)

filtered = df[
    (df["Season"].isin(season_sel)) &
    (df["Category"].isin(category_sel)) &
    (df["Gender"].isin(gender_sel))
]
filtered = add_age_group(filtered)

# Top banner
st.markdown(f"""
    <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;'>
        <div>
            <h1 style='color:white; margin:0; font-size:2rem;'>Insights on Marketing and Discounts</h1>
            <p style='color:#AAAAAA; font-size:16px; margin:4px 0 0 0;'>Who should we market to — and is the discount actually worth it?</p>
        </div>
        <div style='text-align:right;'>
            <span style='color:#5B9BD5; font-size:12px; font-weight:500;'>Dataset: 3,900 customers · 18 variables</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Summary strip
male_pct = round(len(df[df["Gender"]=="Male"]) / len(df) * 100)
female_pct = 100 - male_pct
top_cat = df.groupby("Category")["Purchase Amount (USD)"].sum().idxmax()
top_age = "56+"
st.markdown(f"""
    <div style='display:flex; gap:12px; margin-bottom:16px; flex-wrap:wrap;'>
        <div style='background:#151B3B; border:1px solid #2A3060; border-radius:8px; padding:8px 16px; flex:1; text-align:center;'>
            <span style='color:#AAAAAA; font-size:11px; display:block;'>LARGEST SEGMENT</span>
            <span style='color:#2ECC71; font-size:16px; font-weight:600;'>{top_age} Males</span>
        </div>
        <div style='background:#151B3B; border:1px solid #2A3060; border-radius:8px; padding:8px 16px; flex:1; text-align:center;'>
            <span style='color:#AAAAAA; font-size:11px; display:block;'>HIGHEST VALUE BUYER</span>
            <span style='color:#2ECC71; font-size:16px; font-weight:600;'>Female ($60.25 avg)</span>
        </div>
        <div style='background:#151B3B; border:1px solid #2A3060; border-radius:8px; padding:8px 16px; flex:1; text-align:center;'>
            <span style='color:#AAAAAA; font-size:11px; display:block;'>TOP CATEGORY</span>
            <span style='color:#5B9BD5; font-size:16px; font-weight:600;'>{top_cat} (45%)</span>
        </div>
        <div style='background:#151B3B; border:1px solid #2A3060; border-radius:8px; padding:8px 16px; flex:1; text-align:center;'>
            <span style='color:#AAAAAA; font-size:11px; display:block;'>BEST CAMPAIGN WINDOW</span>
            <span style='color:#5B9BD5; font-size:16px; font-weight:600;'>Fall ($61.56 avg)</span>
        </div>
        <div style='background:#151B3B; border:1px solid #2A3060; border-radius:8px; padding:8px 16px; flex:1; text-align:center;'>
            <span style='color:#AAAAAA; font-size:11px; display:block;'>DISCOUNTS TO FEMALES</span>
            <span style='color:#E74C3C; font-size:16px; font-weight:600;'>0% — Zero</span>
        </div>
    </div>
""", unsafe_allow_html=True)
st.divider()

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Overview", "Finance", "Discounts", "Customer Behavior", "Selling Frequency", "Recommendations"
])

# ====================
# TAB 1 — OVERVIEW
# ====================
with tab1:
    st.markdown("<p style='color:#5B9BD5; font-size:13px;'>Covers: Age · Gender · Purchase Amount</p>", unsafe_allow_html=True)
    takeaway([
        "56+ males are your biggest customer group",
        "Female customers spend more per purchase — $60.25 vs $59.54 for males",
        "Target 56+ males for volume, females for value"
    ])

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Customers", f"{len(filtered):,}")
    col2.metric("Total Revenue", f"${filtered['Purchase Amount (USD)'].sum():,.0f}")
    col3.metric("Avg Spend", f"${filtered['Purchase Amount (USD)'].mean():.2f}")
    col4.metric("Avg Rating", f"{filtered['Review Rating'].mean():.2f}")
    col5.metric("Top Season", filtered.groupby("Season")["Purchase Amount (USD)"].mean().idxmax())

    st.divider()

    st.markdown("### Revenue: Based on Customer Age")
    age_rev = filtered.groupby("Age Group", observed=True)["Purchase Amount (USD)"].sum()
    total_rev = age_rev.sum()
    for age in ["56+","46-55","36-45","26-35","18-25"]:
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
    desc("56+ customers generate the most total revenue — more than any other age group.")

    st.divider()

    st.markdown("### Revenue: Based on Customer Gender")
    gender_rev = filtered.groupby("Gender")["Purchase Amount (USD)"].sum()
    total_gender = gender_rev.sum()
    for gender in ["Male","Female"]:
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
    desc("Males generate more total revenue — but only because there are twice as many male customers. Females spend more per individual purchase ($60.25 vs $59.54).")

    st.divider()

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### Number of Customers by Age")
        age_count = filtered.groupby("Age Group", observed=True).size().reset_index(name="Customers")
        f1 = px.bar(age_count, x="Age Group", y="Customers", color="Age Group",
            color_discrete_map={a: ("#E74C3C" if a == "56+" else "#5B9BD5") for a in age_count["Age Group"]})
        f1 = style(f1)
        f1.update_layout(showlegend=False)
        st.plotly_chart(f1, use_container_width=True, config=NT, key="ov_age_count")
        desc("56+ is the largest customer segment. Red highlights the dominant group.")

    with col_b:
        st.markdown("### Gender Split")
        gender_count = filtered.groupby("Gender").size().reset_index(name="Customers")
        f2 = px.pie(gender_count, names="Gender", values="Customers", color="Gender",
            color_discrete_map={"Male":"#5B9BD5","Female":"#2ECC71"}, hole=0.5)
        f2.update_layout(paper_bgcolor="#0A0E27", font=dict(color="white"), legend=dict(font=dict(color="white")))
        f2.update_traces(textfont=dict(color="white"))
        st.plotly_chart(f2, use_container_width=True, config=NT, key="ov_gender_split")
        desc("68% male customers, 32% female. Despite the gap, females outspend males per transaction.")


# ====================
# TAB 2 — FINANCE
# ====================
with tab2:
    st.markdown("<p style='color:#5B9BD5; font-size:13px;'>Covers: Age · Gender · Purchase Amount · Category · Payment Method · Shipping Type</p>", unsafe_allow_html=True)
    st.markdown("### Where is the money coming from?")
    takeaway([
        "56+ males generate the most money",
        "Females spend more per trip — they are your highest value buyer per transaction",
        "Clothing is your top category",
        "Payment method and shipping type do not affect how much customers spend"
    ])
    st.divider()

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### Age vs Purchase Amount")
        f3 = px.scatter(filtered, x="Age", y="Purchase Amount (USD)", color="Gender",
            color_discrete_map={"Male":"#5B9BD5","Female":"#2ECC71"}, opacity=0.5)
        f3 = style(f3)
        st.plotly_chart(f3, use_container_width=True, config=NT, key="fi_age_scatter")
        desc("No pattern between age and spend — purchases spread evenly across all ages. Age alone should not drive targeting strategy.")

    with col_b:
        st.markdown("### Spend Distribution by Gender")
        f4 = px.box(filtered, x="Gender", y="Purchase Amount (USD)", color="Gender",
            color_discrete_map={"Male":"#5B9BD5","Female":"#2ECC71"})
        f4 = style(f4)
        f4.update_layout(showlegend=False, yaxis=dict(range=[30,100]))
        st.plotly_chart(f4, use_container_width=True, config=NT, key="fi_gender_box")
        desc("Female customers have a higher median and Q3. The top spenders in this dataset are female.")

    st.divider()

    col_c, col_d = st.columns(2)
    with col_c:
        st.markdown("### Total Revenue by Age Group")
        age_rev2 = filtered.groupby("Age Group", observed=True)["Purchase Amount (USD)"].sum().reset_index()
        age_rev2.columns = ["Age Group","Total Revenue ($)"]
        f5 = px.bar(age_rev2, x="Age Group", y="Total Revenue ($)", color="Age Group",
            color_discrete_map={a: ("#E74C3C" if a == "56+" else "#5B9BD5") for a in age_rev2["Age Group"]})
        f5 = style(f5)
        f5.update_layout(showlegend=False)
        st.plotly_chart(f5, use_container_width=True, config=NT, key="fi_age_rev")
        desc("56+ generates the most total revenue. The gap between 56+ and all other groups is significant.")

    with col_d:
        st.markdown("### Revenue by Category and Gender")
        gender_cat = filtered.groupby(["Category","Gender"])["Purchase Amount (USD)"].sum().reset_index()
        gender_cat.columns = ["Category","Gender","Total Revenue ($)"]
        f6 = px.treemap(gender_cat, path=["Gender","Category"], values="Total Revenue ($)",
            color="Gender", color_discrete_map={"Male":"#5B9BD5","Female":"#2ECC71"})
        f6.update_layout(paper_bgcolor="#0A0E27", font=dict(color="white"), margin=dict(t=20,b=20,l=20,r=20))
        f6.update_traces(textfont=dict(color="white"))
        st.plotly_chart(f6, use_container_width=True, config=NT, key="fi_treemap")
        desc("Clothing dominates revenue for both genders. Males lead by volume in every category.")

    st.divider()

    col_e, col_f = st.columns(2)
    with col_e:
        st.markdown("### Revenue by Payment Method")
        pay_rev = filtered.groupby("Payment Method")["Purchase Amount (USD)"].sum().reset_index()
        pay_rev.columns = ["Payment Method","Total Revenue ($)"]
        pay_rev = pay_rev.sort_values("Total Revenue ($)", ascending=True)
        f7 = px.bar(pay_rev, x="Total Revenue ($)", y="Payment Method", orientation="h",
            color_discrete_sequence=["#5B9BD5"])
        f7 = style(f7)
        f7.update_layout(showlegend=False)
        st.plotly_chart(f7, use_container_width=True, config=NT, key="fi_payment")
        desc("All six payment methods generate roughly equal revenue. No single method dominates.")

    with col_f:
        st.markdown("### Revenue by Shipping Type")
        ship_rev = filtered.groupby("Shipping Type")["Purchase Amount (USD)"].sum().reset_index()
        ship_rev.columns = ["Shipping Type","Total Revenue ($)"]
        ship_rev = ship_rev.sort_values("Total Revenue ($)", ascending=True)
        f8 = px.bar(ship_rev, x="Total Revenue ($)", y="Shipping Type", orientation="h",
            color_discrete_sequence=["#5B9BD5"])
        f8 = style(f8)
        f8.update_layout(showlegend=False)
        st.plotly_chart(f8, use_container_width=True, config=NT, key="fi_shipping")
        desc("Shipping type does not significantly affect spend. Free Shipping leads slightly but not enough to drive strategy.")


# ====================
# TAB 3 — DISCOUNTS
# ====================
with tab3:
    st.markdown("<p style='color:#5B9BD5; font-size:13px;'>Covers: Discount Applied · Promo Code Used · Subscription Status · Gender</p>", unsafe_allow_html=True)
    st.markdown("### Are discounts working — and who is getting them?")
    takeaway([
        "56+ males receive the most discounts yet spend less than customers who receive none",
        "Females received zero discounts yet still spent more than discounted males",
        "Discounts lower your margin without changing customer behavior",
        "Move discount budget into ads targeting female customers"
    ])
    st.divider()

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### Discount Distribution by Gender")
        disc_gender = filtered.groupby(["Gender","Discount Applied"]).size().reset_index(name="Count")
        f9 = px.bar(disc_gender, x="Gender", y="Count", color="Discount Applied", barmode="group",
            color_discrete_map={"Yes":"#E74C3C","No":"#5B9BD5"})
        f9 = style(f9)
        st.plotly_chart(f9, use_container_width=True, config=NT, key="di_gender_disc")
        desc("100% of discounts went to male customers. Female customers received zero discounts — yet spent more per purchase.")

    with col_b:
        st.markdown("### Spend Distribution — Discount vs No Discount")
        f10 = px.box(filtered, x="Discount Applied", y="Purchase Amount (USD)", color="Discount Applied",
            color_discrete_map={"Yes":"#E74C3C","No":"#2ECC71"})
        f10 = style(f10)
        f10.update_layout(showlegend=False, yaxis=dict(range=[30,100]))
        st.plotly_chart(f10, use_container_width=True, config=NT, key="di_disc_box")
        desc("Customers without discounts spent more. Discounts are not driving higher purchases — they are reducing margin on sales that would have happened anyway.")

    st.divider()

    col_c, col_d = st.columns(2)
    with col_c:
        st.markdown("### Promo Code Usage")
        promo_count = filtered.groupby("Promo Code Used").size().reset_index(name="Count")
        f11 = px.pie(promo_count, names="Promo Code Used", values="Count", color="Promo Code Used",
            color_discrete_map={"Yes":"#E74C3C","No":"#2ECC71"}, hole=0.5)
        f11.update_layout(paper_bgcolor="#0A0E27", font=dict(color="white"), legend=dict(font=dict(color="white")))
        f11.update_traces(textfont=dict(color="white"))
        st.plotly_chart(f11, use_container_width=True, config=NT, key="di_promo_pie")
        desc("43% of customers used a promo code. Like discounts, promo codes do not correlate with higher spending.")

    with col_d:
        st.markdown("### Discount Usage by Age Group")
        disc_age = filtered.groupby(["Age Group","Discount Applied"], observed=True).size().reset_index(name="Count")
        f12 = px.bar(disc_age, x="Age Group", y="Count", color="Discount Applied", barmode="group",
            color_discrete_map={"Yes":"#E74C3C","No":"#5B9BD5"})
        f12 = style(f12)
        st.plotly_chart(f12, use_container_width=True, config=NT, key="di_age_disc")
        desc("56+ receives the most discounts of any age group — yet they are already your largest spending segment without needing the incentive.")

    st.divider()

    col_e, col_f = st.columns(2)
    with col_e:
        st.markdown("### Subscription Status Split")
        sub_count = filtered.groupby("Subscription Status").size().reset_index(name="Count")
        f13 = px.pie(sub_count, names="Subscription Status", values="Count", color="Subscription Status",
            color_discrete_map={"Yes":"#2ECC71","No":"#5B9BD5"}, hole=0.5)
        f13.update_layout(paper_bgcolor="#0A0E27", font=dict(color="white"), legend=dict(font=dict(color="white")))
        f13.update_traces(textfont=dict(color="white"))
        st.plotly_chart(f13, use_container_width=True, config=NT, key="di_sub_pie")
        desc("Only 27% of customers are subscribers. Growing the subscriber base is a potential loyalty opportunity.")

    with col_f:
        st.markdown("### Avg Spend — Subscribers vs Non-Subscribers")
        sub_spend = filtered.groupby("Subscription Status")["Purchase Amount (USD)"].mean().reset_index()
        sub_spend.columns = ["Subscription Status","Avg Spend ($)"]
        f14 = px.bar(sub_spend, x="Subscription Status", y="Avg Spend ($)", color="Subscription Status",
            color_discrete_map={"Yes":"#2ECC71","No":"#5B9BD5"})
        f14 = style(f14)
        f14.update_layout(showlegend=False, yaxis=dict(range=[58,61]))
        st.plotly_chart(f14, use_container_width=True, config=NT, key="di_sub_spend")
        desc("Subscribers and non-subscribers spend virtually the same. Subscription status alone does not predict higher spending.")


# ====================
# TAB 4 — CUSTOMER BEHAVIOR
# ====================
with tab4:
    st.markdown("<p style='color:#5B9BD5; font-size:13px;'>Covers: Review Rating · Previous Purchases · Size · Color · Item Purchased · Location</p>", unsafe_allow_html=True)
    st.markdown("### How do customers behave beyond what they buy?")
    takeaway([
        "56+ customers come back the most — they are your most loyal returners",
        "Medium and Large are your top sizes — stock accordingly",
        "Blouses and pants are your best selling items — lead with these in campaigns",
        "Color and location do not predict purchasing behavior"
    ])
    st.divider()

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### Review Rating Distribution")
        f15 = px.histogram(filtered, x="Review Rating", nbins=20, color_discrete_sequence=["#5B9BD5"])
        f15 = style(f15)
        f15.update_layout(bargap=0.1)
        st.plotly_chart(f15, use_container_width=True, config=NT, key="cb_rating_hist")
        desc("Most ratings fall between 3.1 and 4.4. Average is 3.75. There is room to improve the experience and push ratings higher.")

    with col_b:
        st.markdown("### Previous Purchases by Age Group")
        prev_age = filtered.groupby("Age Group", observed=True)["Previous Purchases"].mean().reset_index()
        prev_age.columns = ["Age Group","Avg Previous Purchases"]
        f16 = px.bar(prev_age, x="Age Group", y="Avg Previous Purchases", color="Age Group",
            color_discrete_map={a: ("#E74C3C" if a == "56+" else "#5B9BD5") for a in prev_age["Age Group"]})
        f16 = style(f16)
        f16.update_layout(showlegend=False)
        st.plotly_chart(f16, use_container_width=True, config=NT, key="cb_prev_age")
        desc("56+ customers have the most previous purchases — confirming they are your most loyal returning buyers.")

    st.divider()

    col_c, col_d = st.columns(2)
    with col_c:
        st.markdown("### Size Preference")
        size_count = filtered.groupby("Size").size().reset_index(name="Count")
        size_order = ["S","M","L","XL"]
        size_count["Size"] = pd.Categorical(size_count["Size"], categories=size_order, ordered=True)
        size_count = size_count.sort_values("Size")
        f17 = px.bar(size_count, x="Size", y="Count", color_discrete_sequence=["#5B9BD5"])
        f17 = style(f17)
        f17.update_layout(showlegend=False)
        st.plotly_chart(f17, use_container_width=True, config=NT, key="cb_size")
        desc("Medium is the most purchased size followed by Large. Inventory and campaigns should focus on M and L.")

    with col_d:
        st.markdown("### Top 10 Colors Purchased")
        color_count = filtered.groupby("Color").size().reset_index(name="Count")
        color_count = color_count.sort_values("Count", ascending=False).head(10)
        f18 = px.bar(color_count, x="Color", y="Count", color_discrete_sequence=["#5B9BD5"])
        f18 = style(f18)
        f18.update_layout(showlegend=False)
        st.plotly_chart(f18, use_container_width=True, config=NT, key="cb_color")
        desc("Colors are spread fairly evenly. No single color dominates — color preference is not a strong targeting signal.")

    st.divider()

    st.markdown("### Top 10 Items Purchased")
    item_count = filtered.groupby("Item Purchased").size().reset_index(name="Count")
    item_count = item_count.sort_values("Count", ascending=False).head(10)
    f19 = px.bar(item_count, x="Item Purchased", y="Count", color_discrete_sequence=["#5B9BD5"])
    f19 = style(f19)
    f19.update_layout(showlegend=False)
    st.plotly_chart(f19, use_container_width=True, config=NT, key="cb_items")
    desc("Blouses, jewelry and pants are the top purchased items. These should be prioritized in campaign creative and inventory planning.")

    st.divider()

    st.markdown("### Customers by Location (Top 15 States)")
    loc_count = filtered.groupby("Location").size().reset_index(name="Customers")
    loc_count = loc_count.sort_values("Customers", ascending=False).head(15)
    f20 = px.bar(loc_count, x="Location", y="Customers", color_discrete_sequence=["#5B9BD5"])
    f20 = style(f20)
    f20.update_layout(showlegend=False)
    st.plotly_chart(f20, use_container_width=True, config=NT, key="cb_location")
    desc("Customers spread across many states with no single location dominating. Geographic targeting should be broad rather than hyper-local.")


# ====================
# TAB 5 — SELLING FREQUENCY
# ====================
with tab5:
    st.markdown("<p style='color:#5B9BD5; font-size:13px;'>Covers: Category · Season · Frequency of Purchases</p>", unsafe_allow_html=True)
    st.markdown("### What is selling — and when?")
    takeaway([
        "Clothing is 45% of all purchases — it is your number one product",
        "Fall is when customers spend the most — run your biggest campaigns then",
        "All age groups shop at the same frequency — do not use frequency to pick who to target"
    ])
    st.divider()

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### Category Breakdown")
        cat_count = filtered.groupby("Category").size().reset_index(name="Number of Purchases")
        f21 = px.treemap(cat_count, path=["Category"], values="Number of Purchases",
            color="Number of Purchases", color_continuous_scale=["#1E2A45","#5B9BD5"])
        f21.update_layout(paper_bgcolor="#0A0E27", font=dict(color="white"), margin=dict(t=20,b=20,l=20,r=20))
        f21.update_traces(textfont=dict(color="white"))
        st.plotly_chart(f21, use_container_width=True, config=NT, key="sf_category")
        desc("Clothing drives 45% of all purchases. Focus campaign spend on Clothing first.")

    with col_b:
        st.markdown("### Average Spend by Season")
        season_spend = filtered.groupby("Season")["Purchase Amount (USD)"].mean().reset_index()
        season_spend.columns = ["Season","Avg Spend ($)"]
        season_spend = season_spend.sort_values("Avg Spend ($)", ascending=False)
        top_season = season_spend.iloc[0]["Season"]
        colors = ["#2ECC71" if s == top_season else "#5B9BD5" for s in season_spend["Season"]]
        f22 = px.bar(season_spend, x="Season", y="Avg Spend ($)", color="Season", color_discrete_sequence=colors)
        f22 = style(f22)
        f22.update_layout(showlegend=False)
        st.plotly_chart(f22, use_container_width=True, config=NT, key="sf_season")
        desc("Fall drives the highest average spend. This is your best window to run major campaigns.")

    st.divider()

    st.markdown("### Purchase Frequency by Age Group")
    freq_age = filtered.groupby(["Age Group","Frequency of Purchases"], observed=True).size().reset_index(name="Count")
    freq_pivot = freq_age.pivot(index="Frequency of Purchases", columns="Age Group", values="Count").fillna(0)
    f23 = px.imshow(freq_pivot, color_continuous_scale=["#1E2A45","#5B9BD5","#2ECC71"], aspect="auto")
    f23.update_layout(
        paper_bgcolor="#0A0E27", font=dict(color="white"),
        xaxis=dict(tickfont=dict(color="white"), title_font=dict(color="white")),
        yaxis=dict(tickfont=dict(color="white"), title_font=dict(color="white")),
        coloraxis_colorbar=dict(tickfont=dict(color="white"), title=dict(font=dict(color="white"))),
        margin=dict(t=20,b=40,l=20,r=20)
    )
    st.plotly_chart(f23, use_container_width=True, config=NT, key="sf_heatmap")
    desc("Purchase frequency is evenly distributed across all age groups. No group shops significantly more often than another — frequency is not a useful targeting variable.")


# ====================
# TAB 6 — RECOMMENDATIONS
# ====================
with tab6:
    st.markdown("<p style='color:#5B9BD5; font-size:13px;'>Covers: Gender · Discount Applied · Purchase Amount</p>", unsafe_allow_html=True)
    st.markdown("### What should you actually do with this?")
    st.divider()

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        <div class='insight-box'>
        <b style='color:#2ECC71; font-size:16px;'>1. Start marketing to your female customer</b><br><br>
        <span style='color:white;'>Female customers spend more per purchase than males and receive zero discounts yet they still buy. They are your most valuable buyer per transaction and your marketing is completely invisible to them. Start running campaigns specifically aimed at women.</span>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class='insight-box'>
        <b style='color:#2ECC71; font-size:16px;'>2. Stop giving discounts to everyone</b><br><br>
        <span style='color:white;'>Every discount went to male customers who then spent less than non-discounted customers. Discounts are not changing behavior — they are reducing your margin. Redirect that budget into targeted campaigns instead.</span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### Supporting Evidence")

    col_c, col_d = st.columns(2)
    with col_c:
        st.markdown("### Female vs Male Avg Spend")
        gender_spend = filtered.groupby("Gender")["Purchase Amount (USD)"].mean().reset_index()
        gender_spend.columns = ["Gender","Avg Spend ($)"]
        f24 = px.bar(gender_spend, x="Gender", y="Avg Spend ($)", color="Gender",
            color_discrete_map={"Male":"#5B9BD5","Female":"#2ECC71"})
        f24 = style(f24)
        f24.update_layout(showlegend=False, yaxis=dict(range=[59,61]))
        st.plotly_chart(f24, use_container_width=True, config=NT, key="re_gender_spend")
        desc("Females spend $60.25 vs males at $59.54 — outspending males on every transaction without any promotional incentive.")

    with col_d:
        st.markdown("### Who Receives Discounts")
        disc_g = filtered.groupby(["Gender","Discount Applied"]).size().reset_index(name="Count")
        f25 = px.bar(disc_g, x="Gender", y="Count", color="Discount Applied", barmode="group",
            color_discrete_map={"Yes":"#E74C3C","No":"#5B9BD5"})
        f25 = style(f25)
        st.plotly_chart(f25, use_container_width=True, config=NT, key="re_disc_gender")
        desc("Zero discounts went to female customers. Every discount went to male customers who spent less because of it.")

    st.divider()
    st.markdown("### Raw Data")
    st.dataframe(filtered.drop(columns=["Age Group"]).reset_index(drop=True), use_container_width=True, height=300)
