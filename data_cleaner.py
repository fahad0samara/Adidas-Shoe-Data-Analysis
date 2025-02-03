import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime
import os
import numpy as np

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
            return None
        df = pd.read_csv(file_path)
        if df.empty:
            return None
        return df
    except Exception as e:
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
    .element-container:has(div.stMarkdown):first-child {
        margin-top: -4rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.4rem;
    }
    div[data-testid="stMetricDelta"] {
        font-size: 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        border-radius: 4px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4CAF50;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def get_data():
    shoes_dim = load_data('shoes_dim.csv', 'shoes_dim.csv')
    shoes_fact = load_data('shoes_fact.csv', 'shoes_fact.csv')
    country_dim = load_data('country_dim.csv', 'country_dim.csv')
    return shoes_dim, shoes_fact, country_dim

# Load data silently
shoes_dim, shoes_fact, country_dim = get_data()

# Check if data loading was successful
if shoes_dim is None or shoes_fact is None or country_dim is None:
    st.error("Failed to load one or more required datasets. Please ensure all data files are present in the correct location.")
    st.stop()

# Create header with logo and title
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/2/20/Adidas_Logo.svg", width=100)
with col2:
    st.title("👟 Adidas Data Analysis Dashboard")
    st.markdown("### Comprehensive Data Analysis and Insights")

# Display dataset information in sidebar
with st.sidebar:
    st.header("Dataset Information")
    
    # Display dataset shapes
    st.subheader("Dataset Dimensions")
    cols = st.columns(2)
    cols[0].write("Shoes Dimension")
    cols[1].write(f"{shoes_dim.shape[0]} rows")
    cols = st.columns(2)
    cols[0].write("Shoes Facts")
    cols[1].write(f"{shoes_fact.shape[0]} rows")
    cols = st.columns(2)
    cols[0].write("Country Dimension")
    cols[1].write(f"{country_dim.shape[0]} rows")
    
    st.markdown("---")
    
    # Add filters
    st.subheader("Data Filters")
    
    # Gender filter
    if 'gender' in shoes_dim.columns:
        selected_genders = st.multiselect(
            "Gender",
            options=sorted(shoes_dim['gender'].unique()),
            default=sorted(shoes_dim['gender'].unique())
        )
    
    # Price range filter
    if 'price' in shoes_fact.columns:
        price_range = st.slider(
            "Price Range ($)",
            min_value=float(shoes_fact['price'].min()),
            max_value=float(shoes_fact['price'].max()),
            value=(float(shoes_fact['price'].min()), float(shoes_fact['price'].max()))
        )
    
    # Category filter
    if 'category' in shoes_fact.columns:
        selected_categories = st.multiselect(
            "Category",
            options=sorted(shoes_fact['category'].unique()),
            default=sorted(shoes_fact['category'].unique())
        )
    
    st.markdown("---")
    
    # Add data preview section
    if st.checkbox("Show Data Preview"):
        st.subheader("Data Preview")
        dataset = st.selectbox(
            "Select Dataset",
            ["Shoes Dimension", "Shoes Facts", "Country Dimension"]
        )
        
        if dataset == "Shoes Dimension":
            st.dataframe(shoes_dim.head(), use_container_width=True)
        elif dataset == "Shoes Facts":
            st.dataframe(shoes_fact.head(), use_container_width=True)
        else:
            st.dataframe(country_dim.head(), use_container_width=True)

# Apply filters
filtered_shoes_dim = shoes_dim.copy()
filtered_shoes_fact = shoes_fact.copy()

if 'gender' in shoes_dim.columns and selected_genders:
    filtered_shoes_dim = filtered_shoes_dim[filtered_shoes_dim['gender'].isin(selected_genders)]

if 'price' in shoes_fact.columns:
    filtered_shoes_fact = filtered_shoes_fact[
        (filtered_shoes_fact['price'] >= price_range[0]) &
        (filtered_shoes_fact['price'] <= price_range[1])
    ]

if 'category' in shoes_fact.columns and selected_categories:
    filtered_shoes_fact = filtered_shoes_fact[filtered_shoes_fact['category'].isin(selected_categories)]

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
        
        # Add summary metrics at the top
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_products = len(filtered_shoes_dim)
            delta_products = ((total_products - len(shoes_dim)) / len(shoes_dim)) * 100
            st.metric(
                "Total Products",
                f"{total_products:,}",
                f"{delta_products:.1f}% from total"
            )
            
        with col2:
            total_countries = len(country_dim)
            st.metric("Total Countries", f"{total_countries:,}")
            
        with col3:
            if 'price' in filtered_shoes_fact.columns:
                avg_price = filtered_shoes_fact['price'].mean()
                overall_avg = shoes_fact['price'].mean()
                price_delta = ((avg_price - overall_avg) / overall_avg) * 100
                st.metric(
                    "Average Price",
                    f"${avg_price:.2f}",
                    f"{price_delta:+.1f}% from overall"
                )
                
        with col4:
            if 'availability' in filtered_shoes_fact.columns:
                available = filtered_shoes_fact['availability'].sum()
                total_available = shoes_fact['availability'].sum()
                avail_delta = ((available - total_available) / total_available) * 100
                st.metric(
                    "Available Products",
                    f"{available:,}",
                    f"{avail_delta:+.1f}% from total"
                )
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'gender' in filtered_shoes_dim.columns:
                st.subheader("Gender Distribution")
                gender_dist = filtered_shoes_dim['gender'].value_counts()
                fig_gender = px.pie(
                    values=gender_dist.values,
                    names=gender_dist.index,
                    title="Gender Distribution",
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_gender.update_traces(textinfo='percent+label')
                st.plotly_chart(fig_gender, use_container_width=True)
                
                # Add gender statistics
                st.markdown("**Gender Breakdown:**")
                for gender, count in gender_dist.items():
                    st.write(f"- {gender}: {count:,} ({count/len(filtered_shoes_dim)*100:.1f}%)")
            
        with col2:
            if 'category' in filtered_shoes_fact.columns:
                st.subheader("Category Distribution")
                cat_dist = filtered_shoes_fact['category'].value_counts()
                fig_cat = px.pie(
                    values=cat_dist.values,
                    names=cat_dist.index,
                    title="Category Distribution",
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_cat.update_traces(textinfo='percent+label')
                st.plotly_chart(fig_cat, use_container_width=True)
                
                # Add category statistics
                st.markdown("**Category Breakdown:**")
                for cat, count in cat_dist.items():
                    st.write(f"- {cat}: {count:,} ({count/len(filtered_shoes_fact)*100:.1f}%)")
        
        st.markdown("---")
        
        # Time series analysis if date is available
        if 'date' in filtered_shoes_fact.columns:
            st.subheader("Products Over Time")
            
            try:
                # Convert date to datetime with European format (day first)
                filtered_shoes_fact['date'] = pd.to_datetime(
                    filtered_shoes_fact['date'],
                    format='%d/%m/%Y',
                    dayfirst=True
                )
                
                # Group by date and count products
                daily_products = filtered_shoes_fact.groupby('date').size().reset_index(name='count')
                daily_products = daily_products.sort_values('date')
                
                # Create time series plot
                fig_time = px.line(
                    daily_products,
                    x='date',
                    y='count',
                    title="Daily Product Count",
                    labels={'count': 'Number of Products', 'date': 'Date'}
                )
                
                # Customize the layout
                fig_time.update_layout(
                    xaxis=dict(
                        title="Date",
                        tickformat="%d %b %Y",
                        tickangle=45,
                        gridcolor='lightgray'
                    ),
                    yaxis=dict(
                        title="Number of Products",
                        gridcolor='lightgray'
                    ),
                    plot_bgcolor='white'
                )
                
                # Add range selector
                fig_time.update_xaxes(
                    rangeslider_visible=True,
                    rangeselector=dict(
                        buttons=list([
                            dict(count=7, label="1w", step="day", stepmode="backward"),
                            dict(count=1, label="1m", step="month", stepmode="backward"),
                            dict(count=3, label="3m", step="month", stepmode="backward"),
                            dict(step="all")
                        ])
                    )
                )
                
                st.plotly_chart(fig_time, use_container_width=True)
                
                # Add summary statistics
                st.markdown("**Time Series Statistics:**")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Average Daily Products",
                        f"{daily_products['count'].mean():.0f}"
                    )
                
                with col2:
                    st.metric(
                        "Maximum Daily Products",
                        f"{daily_products['count'].max():.0f}"
                    )
                
                with col3:
                    st.metric(
                        "Total Days",
                        f"{len(daily_products):,}"
                    )
                
            except Exception as e:
                st.error(f"Error processing time series data: {str(e)}")
                st.info("Please check the date format in your data.")
        else:
            st.warning("Date information not available in the dataset")

    with tab2:
        st.header("Data Quality Analysis")
        
        # Missing values analysis
        missing_shoes = filtered_shoes_dim.isnull().sum()
        missing_pct_shoes = (missing_shoes / len(filtered_shoes_dim)) * 100
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Missing Values Summary")
            missing_df = pd.DataFrame({
                'Missing Count': missing_shoes,
                'Missing Percentage': missing_pct_shoes.round(2)
            })
            st.dataframe(missing_df, use_container_width=True)
            
            # Data completeness score
            completeness = (1 - missing_shoes.sum() / (len(filtered_shoes_dim) * len(filtered_shoes_dim.columns))) * 100
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
        duplicates = filtered_shoes_dim.duplicated().sum()
        st.metric("Duplicate Records", duplicates)
        
        # Data consistency check
        st.subheader("Data Consistency Check")
        if 'gender' in filtered_shoes_dim.columns:
            invalid_gender = filtered_shoes_dim[~filtered_shoes_dim['gender'].isin(['M', 'W', 'U', 'K'])]['gender'].unique()
            st.write("Invalid gender values:", invalid_gender if len(invalid_gender) > 0 else "None")
        else:
            st.warning("Gender data not available for consistency check")

    with tab3:
        st.header("Price Analysis")
        
        if 'price' in filtered_shoes_fact.columns:
            col1, col2 = st.columns(2)
            
            with col1:
                # Price distribution
                fig_price = px.histogram(
                    filtered_shoes_fact,
                    x='price',
                    title="Price Distribution",
                    nbins=30
                )
                st.plotly_chart(fig_price, use_container_width=True)
                
                # Price statistics
                st.write("Price Statistics:")
                st.dataframe(filtered_shoes_fact['price'].describe().round(2), use_container_width=True)

            with col2:
                # Price by category
                if 'category' in filtered_shoes_fact.columns:
                    avg_price_cat = filtered_shoes_fact.groupby('category')['price'].mean().sort_values(ascending=False)
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
            if 'gender' in filtered_shoes_dim.columns and 'best_for_wear' in filtered_shoes_dim.columns:
                gender_usage = pd.crosstab(filtered_shoes_dim['gender'], filtered_shoes_dim['best_for_wear'])
                fig_gender_usage = px.bar(
                    gender_usage,
                    title="Gender Mix by Usage Category",
                    labels={'value': 'Count', 'gender': 'Gender'}
                )
                st.plotly_chart(fig_gender_usage, use_container_width=True)
            else:
                st.warning("Gender or usage category data not available")

        with col2:
            if 'dominant_color' in filtered_shoes_dim.columns and 'gender' in filtered_shoes_dim.columns:
                color_gender = pd.crosstab(filtered_shoes_dim['dominant_color'], filtered_shoes_dim['gender'])
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
        if 'release_date' in filtered_shoes_dim.columns and 'best_for_wear' in filtered_shoes_dim.columns:
            timeline = filtered_shoes_dim.groupby(['release_date', 'best_for_wear']).size().reset_index(name='count')
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
