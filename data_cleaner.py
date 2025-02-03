import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime
import os

# Set page configuration
st.set_page_config(
    page_title="Adidas Data Analysis Dashboard",
    page_icon="👟",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_data(file_path, file_name):
    """Load data with error handling"""
    try:
        if not os.path.exists(file_path):
            st.error(f"Error: {file_name} not found in the current directory.")
            return None
        return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Error loading {file_name}: {str(e)}")
        return None

# Add custom CSS to improve the UI
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .st-emotion-cache-1v0mbdj {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("👟 Adidas Data Analysis Dashboard")
st.markdown("### Comprehensive Data Analysis and Insights")

# Load the data with error handling
@st.cache_data
def get_data():
    shoes_dim = load_data('shoes_dim.csv', 'shoes_dim.csv')
    shoes_fact = load_data('shoes_fact.csv', 'shoes_fact.csv')
    country_dim = load_data('country_dim.csv', 'country_dim.csv')
    return shoes_dim, shoes_fact, country_dim

shoes_dim, shoes_fact, country_dim = get_data()

# Check if data loading was successful
if shoes_dim is None or shoes_fact is None or country_dim is None:
    st.error("Failed to load one or more required datasets. Please ensure all data files are present in the correct location.")
    st.stop()

try:
    # Create tabs for different analyses
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Basic Statistics", 
        "🔍 Data Quality", 
        "💰 Price Analysis", 
        "🌍 Geographic Analysis",
        "🎯 Market Insights"
    ])

    with tab1:
        st.header("Basic Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Unique Shoes", len(shoes_dim))
            
            # Gender distribution
            if 'gender' in shoes_dim.columns:
                gender_dist = shoes_dim['gender'].value_counts()
                fig_gender = px.pie(
                    values=gender_dist.values,
                    names=gender_dist.index,
                    title="Gender Distribution"
                )
                st.plotly_chart(fig_gender, use_container_width=True)
            else:
                st.warning("Gender data not available")

        with col2:
            if 'best_for_wear' in shoes_dim.columns:
                st.metric("Usage Categories", shoes_dim['best_for_wear'].nunique())
                
                # Usage distribution
                wear_dist = shoes_dim['best_for_wear'].value_counts()
                fig_wear = px.pie(
                    values=wear_dist.values,
                    names=wear_dist.index,
                    title="Usage Distribution"
                )
                st.plotly_chart(fig_wear, use_container_width=True)
            else:
                st.warning("Usage category data not available")

        with col3:
            if 'dominant_color' in shoes_dim.columns:
                st.metric("Color Variations", shoes_dim['dominant_color'].nunique())
                
                # Color distribution
                color_dist = shoes_dim['dominant_color'].value_counts().head(10)
                fig_color = px.bar(
                    x=color_dist.index,
                    y=color_dist.values,
                    title="Top 10 Dominant Colors"
                )
                st.plotly_chart(fig_color, use_container_width=True)
            else:
                st.warning("Color data not available")

    with tab2:
        st.header("Data Quality Analysis")
        
        # Missing values analysis
        missing_shoes = shoes_dim.isnull().sum()
        missing_pct_shoes = (missing_shoes / len(shoes_dim)) * 100
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Missing Values Summary")
            missing_df = pd.DataFrame({
                'Missing Count': missing_shoes,
                'Missing Percentage': missing_pct_shoes.round(2)
            })
            st.dataframe(missing_df, use_container_width=True)
            
            # Data completeness score
            completeness = (1 - missing_shoes.sum() / (len(shoes_dim) * len(shoes_dim.columns))) * 100
            st.metric("Data Completeness Score", f"{completeness:.2f}%")

        with col2:
            fig = px.bar(
                x=missing_shoes.index,
                y=missing_shoes.values,
                title="Missing Values by Column"
            )
            st.plotly_chart(fig, use_container_width=True)

        # Duplicate analysis
        st.subheader("Duplicate Analysis")
        duplicates = shoes_dim.duplicated().sum()
        st.metric("Duplicate Records", duplicates)
        
        # Data consistency check
        st.subheader("Data Consistency Check")
        if 'gender' in shoes_dim.columns:
            invalid_gender = shoes_dim[~shoes_dim['gender'].isin(['M', 'W', 'U', 'K'])]['gender'].unique()
            st.write("Invalid gender values:", invalid_gender if len(invalid_gender) > 0 else "None")
        else:
            st.warning("Gender data not available for consistency check")

    with tab3:
        st.header("Price Analysis")
        
        if 'price' in shoes_fact.columns:
            col1, col2 = st.columns(2)
            
            with col1:
                # Price distribution
                fig_price = px.histogram(
                    shoes_fact,
                    x='price',
                    title="Price Distribution",
                    nbins=30
                )
                st.plotly_chart(fig_price, use_container_width=True)
                
                # Price statistics
                st.write("Price Statistics:")
                st.dataframe(shoes_fact['price'].describe().round(2), use_container_width=True)

            with col2:
                # Price by category
                if 'category' in shoes_fact.columns:
                    avg_price_cat = shoes_fact.groupby('category')['price'].mean().sort_values(ascending=False)
                    fig_price_cat = px.bar(
                        x=avg_price_cat.index,
                        y=avg_price_cat.values,
                        title="Average Price by Category"
                    )
                    st.plotly_chart(fig_price_cat, use_container_width=True)
        else:
            st.warning("Price data not available in the dataset")

    with tab4:
        st.header("Geographic Analysis")
        
        # Country distribution
        st.subheader("Country Distribution")
        country_stats = pd.DataFrame({
            'Currency': country_dim['currency'].value_counts(),
            'Shoe Metric': country_dim['shoe_metric'].value_counts()
        })
        st.dataframe(country_stats, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Currency distribution
            fig_currency = px.pie(
                values=country_dim['currency'].value_counts(),
                names=country_dim['currency'].value_counts().index,
                title="Currency Distribution"
            )
            st.plotly_chart(fig_currency, use_container_width=True)
            
        with col2:
            # Shoe metric distribution
            fig_metric = px.pie(
                values=country_dim['shoe_metric'].value_counts(),
                names=country_dim['shoe_metric'].value_counts().index,
                title="Shoe Metric Distribution"
            )
            st.plotly_chart(fig_metric, use_container_width=True)

    with tab5:
        st.header("Market Insights")
        
        # Product mix analysis
        st.subheader("Product Mix Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'gender' in shoes_dim.columns and 'best_for_wear' in shoes_dim.columns:
                gender_usage = pd.crosstab(shoes_dim['gender'], shoes_dim['best_for_wear'])
                fig_gender_usage = px.bar(
                    gender_usage,
                    title="Gender Mix by Usage Category",
                    labels={'value': 'Count', 'gender': 'Gender'}
                )
                st.plotly_chart(fig_gender_usage, use_container_width=True)
            else:
                st.warning("Gender or usage category data not available")

        with col2:
            if 'dominant_color' in shoes_dim.columns and 'gender' in shoes_dim.columns:
                color_gender = pd.crosstab(shoes_dim['dominant_color'], shoes_dim['gender'])
                fig_color_gender = px.bar(
                    color_gender.head(10),
                    title="Top 10 Colors by Gender",
                    labels={'value': 'Count', 'dominant_color': 'Color'}
                )
                st.plotly_chart(fig_color_gender, use_container_width=True)
            else:
                st.warning("Color or gender data not available")

        # Trend analysis
        st.subheader("Product Categories Over Time")
        if 'release_date' in shoes_dim.columns and 'best_for_wear' in shoes_dim.columns:
            timeline = shoes_dim.groupby(['release_date', 'best_for_wear']).size().reset_index(name='count')
            fig_timeline = px.line(
                timeline,
                x='release_date',
                y='count',
                color='best_for_wear',
                title="Product Categories Timeline"
            )
            st.plotly_chart(fig_timeline, use_container_width=True)
        else:
            st.warning("Release date or usage category data not available")

except Exception as e:
    st.error(f"An error occurred while processing the data: {str(e)}")
    st.info("Please check the data format and try again.")
