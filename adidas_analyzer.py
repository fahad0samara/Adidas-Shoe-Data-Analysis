import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Adidas Shoe Data Analyzer",
    page_icon="👟",
    layout="wide"
)

# Add title and description
st.title("👟 Adidas Shoe Data Analyzer")
st.markdown("Analyze and explore Adidas shoe data interactively!")

# Load the data
@st.cache_data
def load_data():
    shoes_dim = pd.read_csv('shoes_dim.csv')
    shoes_fact = pd.read_csv('shoes_fact.csv')
    country_dim = pd.read_csv('country_dim.csv')
    return shoes_dim, shoes_fact, country_dim

try:
    shoes_dim, shoes_fact, country_dim = load_data()
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Gender filter
    gender_options = ['All'] + sorted(shoes_dim['gender'].unique().tolist())
    selected_gender = st.sidebar.selectbox('Select Gender', gender_options)
    
    # Best for wear filter
    wear_options = ['All'] + sorted(shoes_dim['best_for_wear'].unique().tolist())
    selected_wear = st.sidebar.selectbox('Best For', wear_options)
    
    # Apply filters
    filtered_shoes = shoes_dim.copy()
    if selected_gender != 'All':
        filtered_shoes = filtered_shoes[filtered_shoes['gender'] == selected_gender]
    if selected_wear != 'All':
        filtered_shoes = filtered_shoes[filtered_shoes['best_for_wear'] == selected_wear]
    
    # Main content area
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Data Statistics")
        st.write(f"Total Shoes: {len(filtered_shoes)}")
        
        # Gender distribution
        gender_dist = filtered_shoes['gender'].value_counts()
        fig_gender = px.pie(
            values=gender_dist.values,
            names=gender_dist.index,
            title="Gender Distribution"
        )
        st.plotly_chart(fig_gender)
    
    with col2:
        st.subheader("🎯 Usage Categories")
        wear_dist = filtered_shoes['best_for_wear'].value_counts()
        fig_wear = px.bar(
            x=wear_dist.index,
            y=wear_dist.values,
            title="Shoes by Category"
        )
        st.plotly_chart(fig_wear)
    
    # Show filtered shoe data
    st.subheader("🔍 Shoe Catalog")
    
    # Search functionality
    search_term = st.text_input("Search shoes by name:")
    if search_term:
        filtered_shoes = filtered_shoes[filtered_shoes['name'].str.contains(search_term, case=False, na=False)]
    
    # Display the data
    st.dataframe(
        filtered_shoes[['name', 'gender', 'best_for_wear', 'dominant_color', 'sub_color1', 'sub_color2']],
        use_container_width=True
    )
    
    # Show selected shoe details
    if st.checkbox("Show detailed view of shoes"):
        for _, shoe in filtered_shoes.iterrows():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(shoe['image_url'], width=200)
            with col2:
                st.write(f"**{shoe['name']}**")
                st.write(f"Gender: {shoe['gender']}")
                st.write(f"Best for: {shoe['best_for_wear']}")
                st.write(f"Colors: {shoe['dominant_color']} / {shoe['sub_color1']} / {shoe['sub_color2']}")
            st.divider()

except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.info("Please make sure all data files (shoes_dim.csv, shoes_fact.csv, country_dim.csv) are in the same directory as this script.")
