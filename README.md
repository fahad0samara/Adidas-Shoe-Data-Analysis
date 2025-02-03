# 👟 Adidas Shoe Data Analysis

This project provides comprehensive analysis tools for Adidas shoe data, including interactive visualizations, data quality checks, and market insights.

## 📊 Features

- **Interactive Dashboard** (`adidas_analyzer.py`)
  - Basic shoe statistics
  - Gender and category distributions
  - Color analysis
  - Geographic insights

- **Data Quality Analysis** (`data_cleaner.py`)
  - Missing value detection
  - Data completeness scoring
  - Duplicate record identification
  - Data consistency checks

- **Jupyter Notebook Analysis** (`adidas_analysis.ipynb`)
  - Detailed data exploration
  - Statistical analysis
  - Visual insights
  - Cross-category analysis

## 🛠️ Installation

1. Clone this repository:
```bash
git clone https://github.com/[your-username]/adidas-shoe-analysis.git
cd adidas-shoe-analysis
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## 📋 Data Files

The project uses three main data files:
- `shoes_dim.csv`: Shoe dimension data (features, categories, colors)
- `shoes_fact.csv`: Shoe facts and metrics
- `country_dim.csv`: Country-specific information

## 🚀 Usage

### Interactive Dashboard
Run the Streamlit dashboard:
```bash
streamlit run adidas_analyzer.py
```

### Data Quality Analysis
Run the data quality checker:
```bash
streamlit run data_cleaner.py
```

### Jupyter Notebook
Launch Jupyter and open `adidas_analysis.ipynb`:
```bash
jupyter notebook adidas_analysis.ipynb
```

## 📈 Analysis Features

1. **Basic Statistics**
   - Total product count
   - Gender distribution
   - Usage categories
   - Color variations

2. **Data Quality**
   - Missing value analysis
   - Completeness scoring
   - Duplicate detection
   - Consistency checks

3. **Price Analysis**
   - Price distribution
   - Category-wise pricing
   - Price trends

4. **Geographic Analysis**
   - Country distribution
   - Currency analysis
   - Regional preferences

5. **Market Insights**
   - Product mix analysis
   - Gender preferences
   - Color popularity
   - Category trends

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Data source: Adidas Webstore
- Built with Python, Pandas, Streamlit, and Plotly
