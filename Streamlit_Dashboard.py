import streamlit as st
import pandas as pd
import plotly.express as px
import calendar
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(page_title="Restaurant Management Dashboard", page_icon=":bar_chart:", layout="wide")

# Title of the web application
st.title("🍴 Restaurant Management Dashboard")
st.markdown("---")

# Load the CSV file
@st.cache_data
def load_data():
    try:
        data = pd.read_csv("test_data.csv")
        # Pre-processing dates
        data['Order_Time'] = pd.to_datetime(data['Order_Time'], format='%d/%m/%Y %H:%M', errors='coerce')
        data['Date'] = data['Order_Time'].dt.date
        data['Hour'] = data['Order_Time'].dt.hour
        data['Month'] = data['Order_Time'].dt.month
        # Filter out rows where date parsing failed
        data = data.dropna(subset=['Order_Time'])
        data['Month_Text'] = data['Month'].apply(lambda x: calendar.month_name[int(x)])
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # --- Layout: Column 1 & 2 ---
    col1, col2 = st.columns(2)

    with col1:
        selected_month = st.selectbox("📅 Select a Month", df['Month_Text'].unique())
        filtered_month_df = df[df['Month_Text'] == selected_month]
        total_sale_month = filtered_month_df['Price'].sum()
        
        st.metric(label=f"Total Sale ({selected_month})", value=f"${total_sale_month:,.2f}")
        
        monthly_sale = filtered_month_df.groupby('Menu')['Price'].sum().reset_index()
        fig1 = px.bar(monthly_sale, x='Menu', y='Price', color='Menu', 
                      title=f'Revenue by Menu Item ({selected_month})',
                      labels={'Price': 'Sale (Baht)'})
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        selected_category = st.selectbox("📂 Select a Category", df['Category'].unique())
        filtered_cat_df = df[df['Category'] == selected_category]
        total_sale_cat = filtered_cat_df['Price'].sum()
        
        st.metric(label=f"Total {selected_category.title()} Sales", value=f"${total_sale_cat:,.2f}")
        
        daily_sales = filtered_cat_df.groupby('Day_Of_Week')['Category'].count().reset_index()
        custom_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_sales['Day_Of_Week'] = pd.Categorical(daily_sales['Day_Of_Week'], categories=custom_order, ordered=True)
        daily_sales = daily_sales.sort_values('Day_Of_Week')
        
        fig2 = px.bar(daily_sales, x='Day_Of_Week', y='Category', color='Day_Of_Week',
                      title=f'Order Volume: {selected_category} by Day',
                      labels={'Category': 'Order Count'})
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # --- Layout: Column 3 & 4 (Staff Performance) ---
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("⏱️ Drinks Staff Efficiency")
        # Ensure Serve_Time is numeric for 'min' calculation
        # If Serve_Time is M:S, we convert to total seconds for plotting
        temp_df = df.copy()
        pivot_drinks = pd.pivot_table(temp_df, values='Serve_Time', index='Menu', columns='Drinks_Staff', aggfunc='min').reset_index()
        melted_drinks = pd.melt(pivot_drinks, id_vars=['Menu'], var_name='Drinks_Staff', value_name='Min_Time')
        
        fig3 = px.bar(melted_drinks, x='Menu', y='Min_Time', color='Drinks_Staff', barmode='group',
                      title='Min Serve Time per Drink Staff')
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.subheader("🍳 Kitchen Staff Efficiency")
        pivot_kitchen = pd.pivot_table(temp_df, values='Serve_Time', index='Menu', columns='Kitchen_Staff', aggfunc='min').reset_index()
        melted_kitchen = pd.melt(pivot_kitchen, id_vars=['Menu'], var_name='Kitchen_Staff', value_name='Min_Time')
        
        fig4 = px.bar(melted_kitchen, x='Menu', y='Min_Time', color='Kitchen_Staff', barmode='group',
                      title='Min Serve Time per Kitchen Staff')
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")

    # --- Layout: Column 5 & 6 (Top Items & Distribution) ---
    col5, col6 = st.columns(2)

    with col5:
        top_food = df[df['Category'] == 'food'].groupby('Menu')['Price'].sum().nlargest(5).reset_index()
        top_food['Category'] = 'Food'
        top_drink = df[df['Category'] == 'drink'].groupby('Menu')['Price'].sum().nlargest(5).reset_index()
        top_drink['Category'] = 'Drink'
        top_items = pd.concat([top_food, top_drink])
        
        fig5 = px.bar(top_items, x='Menu', y='Price', color='Category', 
                      title='Top 5 Food vs Top 5 Drinks (By Revenue)')
        st.plotly_chart(fig5, use_container_width=True)

    with col6:
        # Pie Chart Subplots
        fig6 = make_subplots(rows=1, cols=2, specs=[[{'type':'pie'}, {'type':'pie'}]], 
                             subplot_titles=['Drinks Distribution', 'Food Distribution'])
        
        cat_counts = df.groupby(['Category', 'Menu']).size().reset_index(name='Count')
        
        fig6.add_trace(go.Pie(labels=cat_counts[cat_counts['Category']=='drink']['Menu'], 
                              values=cat_counts[cat_counts['Category']=='drink']['Count']), row=1, col=1)
        
        fig6.add_trace(go.Pie(labels=cat_counts[cat_counts['Category']=='food']['Menu'], 
                              values=cat_counts[cat_counts['Category']=='food']['Count']), row=1, col=2)
        
        fig6.update_layout(title_text='Menu Item Popularity')
        st.plotly_chart(fig6, use_container_width=True)

else:
    st.warning("Please ensure 'test_data.csv' is in the same directory and contains the required columns.")
