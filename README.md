# Amazon E-Commerce Data Analysis

Analysis of BlissBaby product performance on Amazon (October-November 2025).

## Analysis Workflow

**Data Pipeline:**
1. Raw data sampled and imported to Power BI for initial exploration
2. Database cleaned using SQL views and queries
3. Detailed metrics calculated and analyzed
4. Key insights identified through exploratory analysis

**Deliverables:**
- `detailed_analysis.py` - SQL-cleaned data with detailed calculations
- `KeyInsights.ipynb` - Business question analysis with visualizations

## Business Questions & Findings

### 1. When are products most returned?
November shows 82% of returns (28 of 34 total). Fridays peak with 7 returns.

### 2. Product with most ads and clicks?
UB0101 leads with 2,328 clicks and $645 ad spend. Highest impressions at 532,365.

### 3. Is the most advertised product also the best seller?
Yes. UB0101 has both highest ad volume and 524 units sold. The 49% organic sales component indicates strong brand recognition beyond paid channels.

### 4. Least performing products?
UBW101 ($1.72 ROAS), UBL101 (172 clicks), USP101 (6.52% return rate) need optimization.

## Running the Analysis

### Detailed Metrics (Python)
```bash
python detailed_analysis.py
```
Outputs:
- Aggregate KPIs (Total Sales, Ad Spend, ACoS, TACoS, Net Margin)
- SKU-level performance breakdown
- Monthly trends
- Visualization dashboard (PNG export)

### Key Insights (Jupyter)
```bash
jupyter notebook KeyInsights.ipynb
```
Covers:
- Return timing and patterns
- Advertising performance comparison
- Sales vs ad correlation
- Weak performer analysis with visualizations
