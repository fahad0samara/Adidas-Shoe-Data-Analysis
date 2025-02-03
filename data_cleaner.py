import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Adidas Data Analysis Dashboard",
    page_icon="👟",
    layout="wide"
)

st.title("👟 Adidas Data Analysis Dashboard")
st.markdown("### Comprehensive Data Analysis and Insights")

# Load the data
try:
    # Load all datasets
    shoes_dim = pd.read_csv('shoes_dim.csv')
    country_dim = pd.read_csv('country_dim.csv')
    shoes_fact = pd.read_csv('shoes_fact.csv')

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
            gender_dist = shoes_dim['gender'].value_counts()
            fig_gender = px.pie(
                values=gender_dist.values,
                names=gender_dist.index,
                title="Gender Distribution"
            )
            st.plotly_chart(fig_gender)

        with col2:
            st.metric("Usage Categories", shoes_dim['best_for_wear'].nunique())
            
            # Usage distribution
            wear_dist = shoes_dim['best_for_wear'].value_counts()
            fig_wear = px.pie(
                values=wear_dist.values,
                names=wear_dist.index,
                title="Usage Distribution"
            )
            st.plotly_chart(fig_wear)

        with col3:
            st.metric("Color Variations", shoes_dim['dominant_color'].nunique())
            
            # Color distribution
            color_dist = shoes_dim['dominant_color'].value_counts().head(10)
            fig_color = px.bar(
                x=color_dist.index,
                y=color_dist.values,
                title="Top 10 Dominant Colors"
            )
            st.plotly_chart(fig_color)

    with tab2:
        st.header("Data Quality Analysis")
        
        # Missing values analysis
        missing_shoes = shoes_dim.isnull().sum()
        missing_pct_shoes = (missing_shoes / len(shoes_dim)) * 100
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Missing Values Summary")
            st.write(pd.DataFrame({
                'Missing Count': missing_shoes,
                'Missing Percentage': missing_pct_shoes.round(2)
            }))
            
            # Data completeness score
            completeness = (1 - missing_shoes.sum() / (len(shoes_dim) * len(shoes_dim.columns))) * 100
            st.metric("Data Completeness Score", f"{completeness:.2f}%")

        with col2:
            fig = px.bar(
                x=missing_shoes.index,
                y=missing_shoes.values,
                title="Missing Values by Column"
            )
            st.plotly_chart(fig)

        # Duplicate analysis
        st.subheader("Duplicate Analysis")
        duplicates = shoes_dim.duplicated().sum()
        st.metric("Duplicate Records", duplicates)
        
        # Data consistency check
        st.subheader("Data Consistency Check")
        invalid_gender = shoes_dim[~shoes_dim['gender'].isin(['M', 'W', 'U', 'K'])]['gender'].unique()
        st.write("Invalid gender values:", invalid_gender if len(invalid_gender) > 0 else "None")

    with tab3:
        st.header("Price Analysis")
        
        if 'price' in shoes_fact.columns:
            col1, col2 = st.columns(2)
            
            with col1:
                # Price distribution
                fig_price = px.histogram(
                    shoes_fact,
                    x='price',
                    title="Price Distribution"
                )
                st.plotly_chart(fig_price)
                
                # Price statistics
                st.write("Price Statistics:")
                st.write(shoes_fact['price'].describe())

            with col2:
                # Price by category
                if 'category' in shoes_fact.columns:
                    avg_price_cat = shoes_fact.groupby('category')['price'].mean().sort_values(ascending=False)
                    fig_price_cat = px.bar(
                        x=avg_price_cat.index,
                        y=avg_price_cat.values,
                        title="Average Price by Category"
                    )
                    st.plotly_chart(fig_price_cat)

    with tab4:
        st.header("Geographic Analysis")
        
        # Country distribution
        st.subheader("Country Distribution")
        country_stats = pd.DataFrame({
            'Currency': country_dim['currency'].value_counts(),
            'Shoe Metric': country_dim['shoe_metric'].value_counts()
        })
        st.write(country_stats)
        
        # Currency distribution
        fig_currency = px.pie(
            values=country_dim['currency'].value_counts(),
            names=country_dim['currency'].value_counts().index,
            title="Currency Distribution"
        )
        st.plotly_chart(fig_currency)

    with tab5:
        st.header("Market Insights")
        
        # Product mix analysis
        st.subheader("Product Mix Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gender mix by usage
            gender_usage = pd.crosstab(shoes_dim['gender'], shoes_dim['best_for_wear'])
            fig_gender_usage = px.bar(
                gender_usage,
                title="Gender Mix by Usage Category"
            )
            st.plotly_chart(fig_gender_usage)

        with col2:
            # Color popularity by gender
            color_gender = pd.crosstab(shoes_dim['dominant_color'], shoes_dim['gender'])
            fig_color_gender = px.bar(
                color_gender.head(10),
                title="Top 10 Colors by Gender"
            )
            st.plotly_chart(fig_color_gender)

        # Trend analysis
        st.subheader("Product Categories Over Time")
        if 'release_date' in shoes_dim.columns:
            timeline = shoes_dim.groupby(['release_date', 'best_for_wear']).size().reset_index(name='count')
            fig_timeline = px.line(
                timeline,
                x='release_date',
                y='count',
                color='best_for_wear',
                title="Product Categories Timeline"
            )
            st.plotly_chart(fig_timeline)

except Exception as e:
    st.error(f"Error loading or processing data: {str(e)}")
    st.info("Please make sure all data files (shoes_dim.csv, shoes_fact.csv, country_dim.csv) are in the same directory as this script.")
