import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (14, 6)

orders_df = pd.read_csv('outputs/cleaned/orders.csv')
returns_df = pd.read_csv('outputs/cleaned/returns.csv')
sponsored_df = pd.read_csv('outputs/cleaned/sponsored_products.csv')
sku_metrics_df = pd.read_csv('outputs/cleaned/sku_metrics.csv')

orders_df['purchase_ts'] = pd.to_datetime(orders_df['purchase_ts'])
orders_df['month'] = orders_df['purchase_ts'].dt.to_period('M')

sku_data = sku_metrics_df[sku_metrics_df['sku'] != 'UNKNOWN'].copy()

sku_summary = sku_data.groupby('sku').agg({
    'orders_cnt': 'sum',
    'units_sold': 'sum',
    'gross_sales': 'sum',
    'ad_spend_sp': 'sum',
    'net_profit': 'sum'
}).reset_index()

sku_summary['acos'] = (sku_summary['ad_spend_sp'] / sku_summary['gross_sales'] * 100).round(2)
sku_summary['tacos'] = (sku_summary['ad_spend_sp'] / sku_summary['gross_sales'] * 100).round(2)
sku_summary['net_margin'] = (sku_summary['net_profit'] / sku_summary['gross_sales'] * 100).round(2)

total_sales = sku_summary['gross_sales'].sum()
total_ad_spend = sku_summary['ad_spend_sp'].sum()
total_profit = sku_summary['net_profit'].sum()

overall_acos = (total_ad_spend / total_sales * 100)
overall_tacos = (total_ad_spend / total_sales * 100)
overall_margin = (total_profit / total_sales * 100)

print("=" * 80)
print("AMAZON ECOMMERCE PERFORMANCE ANALYSIS")
print("=" * 80)

print("\nAGGREGATE METRICS")
print("-" * 80)
print(f"Total Sales:        ${total_sales:,.2f}")
print(f"Total Ad Spend:     ${total_ad_spend:,.2f}")
print(f"Net Profit:         ${total_profit:,.2f}")
print(f"Net Margin:         {overall_margin:.2f}%")
print(f"ACoS:               {overall_acos:.2f}%")
print(f"TACoS:              {overall_tacos:.2f}%")

print("\n\nSKU PERFORMANCE")
print("-" * 80)
print(f"{'SKU':<10} {'Sales':<12} {'Ad Spend':<12} {'ACoS':<8} {'TACoS':<8} {'Net Profit':<12} {'Net Margin':<10}")
print("-" * 80)

for idx, row in sku_summary.iterrows():
    print(f"{row['sku']:<10} ${row['gross_sales']:<11,.2f} ${row['ad_spend_sp']:<11,.2f} {row['acos']:<7.2f}% {row['tacos']:<7.2f}% ${row['net_profit']:<11,.2f} {row['net_margin']:<9.2f}%")

print("-" * 80)
print(f"{'TOTAL':<10} ${total_sales:<11,.2f} ${total_ad_spend:<11,.2f} {overall_acos:<7.2f}% {overall_tacos:<7.2f}% ${total_profit:<11,.2f} {overall_margin:<9.2f}%")

monthly_data = orders_df.groupby('month').agg({
    'item_price': 'sum',
    'amazon_order_id': 'count'
}).rename(columns={'item_price': 'sales', 'amazon_order_id': 'orders'})

ad_monthly = sponsored_df.groupby(sponsored_df['start_date'].str[:7]).agg({
    'spend': 'sum',
    '7_day_total_sales': 'sum'
}).reset_index()
ad_monthly.columns = ['month', 'ad_spend', 'ad_sales']

print("\n\nMONTHLY BREAKDOWN")
print("-" * 80)
print(f"{'Month':<15} {'Gross Sales':<15} {'Ad Spend':<15} {'Ad Sales':<15}")
print("-" * 80)

for idx, row in ad_monthly.iterrows():
    print(f"{row['month']:<15} ${row['ad_sales']:<14,.2f} ${row['ad_spend']:<14,.2f} ${row['ad_sales']:<14,.2f}")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

sku_order = sku_summary.sort_values('ad_spend_sp', ascending=True)
colors = ['#d62728' if x > 2000 else '#1f77b4' for x in sku_order['ad_spend_sp']]
axes[0].barh(sku_order['sku'], sku_order['ad_spend_sp'], color=colors)
axes[0].set_xlabel('Ad Spend ($)', fontsize=11, fontweight='bold')
axes[0].set_title('Total Ad Spend by SKU', fontsize=12, fontweight='bold')
axes[0].grid(axis='x', alpha=0.3)

for i, v in enumerate(sku_order['ad_spend_sp']):
    axes[0].text(v + 50, i, f'${v:,.0f}', va='center', fontweight='bold')

months = ad_monthly['month'].astype(str)
ax1 = axes[1]
ax2 = ax1.twinx()

ax1.plot(months, ad_monthly['ad_sales'], marker='o', color='#1f77b4', linewidth=2.5, markersize=8, label='Sales')
ax2.plot(months, ad_monthly['ad_spend'], marker='s', color='#d62728', linewidth=2.5, markersize=8, label='Ad Spend')

ax1.set_xlabel('Month', fontsize=11, fontweight='bold')
ax1.set_ylabel('Sales ($)', fontsize=11, fontweight='bold', color='#1f77b4')
ax2.set_ylabel('Ad Spend ($)', fontsize=11, fontweight='bold', color='#d62728')
ax1.set_title('Monthly Sales vs Ad Spend', fontsize=12, fontweight='bold')
ax1.grid(alpha=0.3)
ax1.tick_params(axis='y', labelcolor='#1f77b4')
ax2.tick_params(axis='y', labelcolor='#d62728')

plt.tight_layout()
plt.savefig('outputs/analysis_dashboard.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n\nVisualization saved to outputs/analysis_dashboard.png")
print("=" * 80)
