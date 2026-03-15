from agent import *
from dbOps import query_db
import pandas as pd
import streamlit as st
import plotly.express as px
 

# page settings
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon=":bar_chart:",
    layout="wide"
)

query = "SELECT * FROM Global_Superstore2"
df = query_db(query)
agent = Agent()

# ---- Transform SQL dataset to match dashboard schema ----
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

df["Year"] = df["Order_Date"].dt.year
df["Month_Name"] = df["Order_Date"].dt.strftime("%b")

df["Item_Category"] = df["Category"]
df["Tota_Selling_Value"] = df["Sales"]
df["Quantity_Sold_kilo"] = df["Quantity"]

# superstore dataset has no returns, so mark all as sales
df["Sale_or_Return"] = "sale"

# Initialize session state for filters
if "filters" not in st.session_state:
    st.session_state.filters = {
        "year": df["Year"].unique().tolist(),
        "item_category": df["Item_Category"].unique().tolist(),
    }

# Initializing session state for chat
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# Sidebar for filters
st.sidebar.header("Select Filters Here")

# Update filters state independently
year = st.sidebar.multiselect(
    "Select Year.",
    options=df["Year"].unique(),
    default=st.session_state.filters["year"],
    on_change=lambda: st.session_state.filters.update({"year": year})
)

item_category = st.sidebar.multiselect(
    "Select Product Category.",
    options=df["Item_Category"].unique(),
    default=st.session_state.filters["item_category"],
    on_change=lambda: st.session_state.filters.update({"item_category": item_category})
)


# Sidebar for chat
with st.sidebar:
    st.title("🤖 AI Assistant Manager")

    # Chat container
    messages = st.container(height=300)
    for msg in st.session_state.chat_messages:
        if msg["role"] == "user":
            messages.chat_message("user").write(msg["content"])
        elif msg["role"] == "assistant":
            messages.chat_message("assistant").write(msg["content"])

    # Chat input
    if new_prompt := st.chat_input("How can I assist?"):
        
        # state magangment...
        st.session_state.chat_messages.append({"role": "user", "content": new_prompt})
 
        # display output instantly for chat history
        messages.chat_message("user").write(new_prompt)

        # generate RAG AI response & add to sesion state as well
        answer = agent.answer(new_prompt).get("output","Currently on my break... I'll respond shortly")
        st.session_state.chat_messages.append({"role": "assistant", "content": answer})
        messages.chat_message("assistant").write(answer)


# df filter affecting by year and category selection
df_selection_year_and_category = df.query(
    "Year == @year & Item_Category == @item_category"
)
# only affected by year selection
df_selection_year = df.query(
    "Year == @year"
)


st.title("📊 Sales Dashboard")
st.markdown("##")

no_of_orders = len(df_selection_year_and_category)

total_sales_revenue = df_selection_year_and_category["Tota_Selling_Value"].sum()

total_profit = df_selection_year_and_category["Profit"].sum()

avg_order_value = total_sales_revenue / no_of_orders if no_of_orders > 0 else 0

# Display Columns for KPIs
first_col, second_col, third_col, forth_col = st.columns(4)

with first_col:
    st.subheader("No. of Orders")
    st.subheader(f"{no_of_orders:,}")

with second_col:
    st.subheader("Total Profit")
    st.subheader(f"(US $) {total_profit:,.2f}")

with third_col:
    st.subheader("Total Sales Revenue")
    st.subheader(f"(US $) {total_sales_revenue:,.2f}")

with forth_col:
    st.subheader("Average Order Value")
    st.subheader(f"(US $) {avg_order_value:,.2f}")


# Graphs building.
# 1. Line Graph Revenue/month
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
df_grouped = (
    df_selection_year_and_category
    .groupby("Month_Name")["Tota_Selling_Value"]
    .sum()
    .reindex(month_order)
)

# Create the line chart
revenue_by_month_fig = px.line(
    x=df_grouped.keys(),
    y=df_grouped.values,
    title="Monthly Revenue"
)

revenue_by_month_fig.update_layout(
    title=dict(
        text="Monthly Revenue",
        x=0.5, # Centering
        font=dict(size=15)
    ),
    xaxis_title="Month",
    yaxis_title="Total Revenue ($)",
    width=400,
    height=300,
    margin=dict(t=20, b=0, l=0, r=0),
    showlegend=False,
)

# Remove grid lines from both axes
revenue_by_month_fig.update_xaxes(
    showgrid=False,
    tickangle=45,
    tickfont=dict(size=12),
)
revenue_by_month_fig.update_yaxes(
    showgrid=False,
    tickfont=dict(size=12),
)

# ------------------------------------------------------------
# Defining color mapping
color_mapping = {
    "Aquatic Tuberous Veg.": "#1E90FF", # Soft blue
    "Cabbage": "#32CD32",               # Fresh green
    "Capsicum": "#FF4500",              # Vibrant Orange
    "Edible Mushroom": "#D2B48C",       # Light beige
    "Flower/Leaf/Veg.": "#9ACD32",      # Bright yellow-green
    "Solanum": "#6A5ACD"                # Deep purple
}

# Defining month order
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
# ------------------------------------------------------------

# 2. Stacked Bar Graph Revenue(per category)/month
# Ensure Month_Name is in the desired order
df_selection_year["Month_Name"] = pd.Categorical(df_selection_year["Month_Name"], categories=month_order, ordered=True)
df_grouped = (
    df_selection_year
    .groupby(["Month_Name", "Item_Category"])["Tota_Selling_Value"]
    .sum()
    .reset_index()
)

stacked_bar_graph_fig = px.bar(
    df_grouped,
    y="Month_Name",
    x="Tota_Selling_Value", 
    color="Item_Category",
    color_discrete_map=color_mapping,
    labels={"Revenue": "Sales Revenue ($)", "Month": "Month"},
    barmode="stack",
    orientation='h'
)

stacked_bar_graph_fig.update_yaxes(
    categoryorder="array",            # Use explicit ordering
    categoryarray=month_order[::-1]   # Reverse the custom order
)

# Customize layout
stacked_bar_graph_fig.update_layout(
    width=400,
    height=300,
    title=dict(
        text="Monthly Sales Revenue by Product Category",
        x=0.2,
        font=dict(size=15)
    ),
    yaxis_title="Month",
    xaxis_title="Total Revenue ($)",
    legend_title="Category",
    margin=dict(t=20, b=0, l=0, r=0),
)
# ------------------------------------------------------------


# 3. Tree graph of product categories and sales numbers
data = df_selection_year.groupby("Item_Category").count()["Quantity_Sold_kilo"]
data = {
    "Category": data.keys(),
    "Value": data.values,
}

# Create a treemap
treemap_fig = px.treemap(
    data,
    path=["Category"],
    values="Value",
    color= "Category",
    color_discrete_map=color_mapping,
)

treemap_fig.update_traces(
    hovertemplate ="Category: %{label}<br>Quantity(KG): %{value}<extra></extra>"
)

treemap_fig.update_layout(
    title=dict(
        text="Annual Sales By Category",
        x=0.3,
        font=dict(size=15)
    ),
    width=400,
    height=300,
    margin=dict(t=20, b=0, l=0, r=0),
)
# ------------------------------------------------------------


# Visualisations: Graphs
st.markdown("---")
second_first_col, second_second_col, second_third_col = st.columns(3)

with second_first_col:
    st.plotly_chart(revenue_by_month_fig)
with second_second_col:
    st.plotly_chart(stacked_bar_graph_fig)
with second_third_col:
    st.plotly_chart(treemap_fig)
# ------------------------------------------------------------