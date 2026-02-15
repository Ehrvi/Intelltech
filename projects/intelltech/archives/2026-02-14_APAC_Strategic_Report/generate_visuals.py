#!/usr/bin/env python3
"""
Generate all visualizations for IntellTech APAC Strategic Report
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle
import seaborn as sns

# Set professional style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# IntellTech color scheme (professional blues and grays)
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e', 
    'accent': '#2ca02c',
    'neutral': '#7f7f7f',
    'highlight': '#d62728'
}

def save_fig(filename, dpi=300):
    """Save figure with high quality"""
    plt.tight_layout()
    plt.savefig(f'/home/ubuntu/final_report/images/{filename}', dpi=dpi, bbox_inches='tight')
    plt.close()

# 1. CHAPTER 2: Country Market Size Comparison
def country_market_size():
    countries = ['India', 'Australia', 'Indonesia', 'Malaysia', 'Japan', 
                 'Singapore', 'Vietnam', 'Philippines', 'South Korea', 'Thailand', 'New Zealand']
    market_size = [240, 280, 200, 130, 150, 70, 110, 100, 90, 80, 50]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = [COLORS['highlight'] if x in ['India', 'Australia'] else COLORS['primary'] for x in countries]
    bars = ax.barh(countries, market_size, color=colors)
    
    ax.set_xlabel('Addressable SHM Market 2025 (USD Millions)', fontsize=12, fontweight='bold')
    ax.set_title('APAC Market Opportunity by Country', fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3)
    
    # Add value labels
    for i, (country, value) in enumerate(zip(countries, market_size)):
        ax.text(value + 5, i, f'${value}M', va='center', fontsize=10)
    
    save_fig('country_market_size.png')

# 2. CHAPTER 2: Attractiveness vs Ease of Entry Matrix
def attractiveness_matrix():
    countries_data = {
        'Australia': (9, 8.5),
        'India': (9.5, 4),
        'Indonesia': (8.5, 3),
        'Singapore': (6, 9),
        'Malaysia': (7, 7),
        'Japan': (7.5, 5),
        'Vietnam': (7, 5.5),
        'Philippines': (6.5, 4.5),
        'South Korea': (6.5, 6),
        'Thailand': (5.5, 6),
        'New Zealand': (4.5, 8.5)
    }
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Plot countries
    for country, (attract, ease) in countries_data.items():
        color = COLORS['highlight'] if country in ['Australia', 'India'] else COLORS['primary']
        ax.scatter(ease, attract, s=300, alpha=0.6, color=color, edgecolors='black', linewidth=1.5)
        ax.annotate(country, (ease, attract), fontsize=9, ha='center', va='center', fontweight='bold')
    
    # Add quadrant lines
    ax.axhline(y=7, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    ax.axvline(x=6, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    
    # Quadrant labels
    ax.text(8.5, 9.5, 'Strategic\nEntry', fontsize=11, ha='center', fontweight='bold', 
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))
    ax.text(3, 9.5, 'High\nPotential', fontsize=11, ha='center', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.3))
    ax.text(8.5, 4.5, 'Easy\nWins', fontsize=11, ha='center', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
    ax.text(3, 4.5, 'Low\nPriority', fontsize=11, ha='center', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.3))
    
    ax.set_xlabel('Ease of Entry Score', fontsize=12, fontweight='bold')
    ax.set_ylabel('Market Attractiveness Score', fontsize=12, fontweight='bold')
    ax.set_title('Country Attractiveness Matrix', fontsize=14, fontweight='bold', pad=20)
    ax.set_xlim(2, 10)
    ax.set_ylim(4, 10)
    ax.grid(True, alpha=0.3)
    
    save_fig('attractiveness_matrix.png')

# 3. CHAPTER 2: Regulatory Pressure Heatmap
def regulatory_heatmap():
    countries = ['Australia', 'India', 'Indonesia', 'Malaysia', 'Singapore', 
                 'Japan', 'Vietnam', 'Philippines', 'South Korea', 'Thailand', 'New Zealand']
    regulations = ['GISTM', 'Dam Safety', 'Infrastructure\nCodes', 'Seismic\nCodes']
    
    # Pressure levels: 3=High, 2=Medium, 1=Low
    data = np.array([
        [3, 3, 3, 2],  # Australia
        [3, 3, 2, 2],  # India
        [3, 2, 2, 3],  # Indonesia
        [2, 2, 2, 1],  # Malaysia
        [1, 2, 3, 1],  # Singapore
        [1, 2, 3, 3],  # Japan
        [2, 2, 2, 2],  # Vietnam
        [2, 2, 2, 3],  # Philippines
        [1, 2, 3, 3],  # South Korea
        [2, 2, 2, 2],  # Thailand
        [2, 2, 3, 3],  # New Zealand
    ])
    
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(data, cmap='RdYlGn_r', aspect='auto', vmin=1, vmax=3)
    
    ax.set_xticks(np.arange(len(regulations)))
    ax.set_yticks(np.arange(len(countries)))
    ax.set_xticklabels(regulations, fontsize=10, fontweight='bold')
    ax.set_yticklabels(countries, fontsize=10)
    
    # Add text annotations
    for i in range(len(countries)):
        for j in range(len(regulations)):
            text_color = 'white' if data[i, j] == 3 else 'black'
            label = ['Low', 'Medium', 'High'][int(data[i, j])-1]
            ax.text(j, i, label, ha='center', va='center', color=text_color, fontweight='bold', fontsize=9)
    
    ax.set_title('Regulatory Pressure Across APAC', fontsize=14, fontweight='bold', pad=20)
    plt.colorbar(im, ax=ax, label='Urgency Level', ticks=[1, 2, 3])
    
    save_fig('regulatory_heatmap.png')

# 4. CHAPTER 3: Sector Market Size Evolution
def sector_market_evolution():
    sectors = ['Mining', 'Infrastructure', 'Energy', 'Railways', 'Dams']
    years = [2020, 2022, 2024, 2026, 2028, 2030]
    
    # Market size data (millions USD)
    mining = [400, 480, 550, 600, 640, 650]
    infrastructure = [250, 290, 330, 360, 370, 375]
    energy = [120, 150, 180, 210, 220, 225]
    railways = [200, 240, 280, 300, 310, 312]
    dams = [180, 210, 240, 260, 268, 270]
    
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.plot(years, mining, marker='o', linewidth=2.5, label='Mining', color=COLORS['highlight'])
    ax.plot(years, infrastructure, marker='s', linewidth=2.5, label='Infrastructure', color=COLORS['primary'])
    ax.plot(years, energy, marker='^', linewidth=2.5, label='Energy (Offshore Wind)', color=COLORS['accent'])
    ax.plot(years, railways, marker='d', linewidth=2.5, label='Railways', color=COLORS['secondary'])
    ax.plot(years, dams, marker='*', linewidth=2.5, label='Dams & Reservoirs', color=COLORS['neutral'])
    
    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Market Size (USD Millions)', fontsize=12, fontweight='bold')
    ax.set_title('APAC Sector Market Size Evolution (2020-2030)', fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper left', fontsize=10, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    
    save_fig('sector_evolution.png')

# 5. CHAPTER 3: Sector Prioritization Bubble Chart
def sector_bubble_chart():
    sectors_data = {
        'Mining': (650, 9, 9),
        'Infrastructure': (375, 7, 8.5),
        'Energy': (225, 8.5, 8),
        'Railways': (312, 6.5, 7.5),
        'Dams': (270, 8, 7),
        'Ports': (120, 6, 7),
        'Oil & Gas': (100, 5, 7.5),
        'Construction': (200, 5, 6),
        'Water': (90, 5.5, 6),
        'Solar': (60, 6.5, 5.5),
        'Environmental': (37, 5, 5)
    }
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    for sector, (market, urgency, profit) in sectors_data.items():
        size = profit * 100
        color = COLORS['highlight'] if sector in ['Mining', 'Infrastructure'] else COLORS['primary']
        ax.scatter(market, urgency, s=size, alpha=0.6, color=color, edgecolors='black', linewidth=1.5)
        ax.annotate(sector, (market, urgency), fontsize=9, ha='center', va='center', fontweight='bold')
    
    ax.set_xlabel('Market Size (USD Millions)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Growth / Urgency Score', fontsize=12, fontweight='bold')
    ax.set_title('APAC Sector Opportunity Matrix\n(Bubble size = Profitability)', fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 700)
    ax.set_ylim(4, 10)
    
    save_fig('sector_bubble.png')

# 6. CHAPTER 4: Competitive Positioning Matrix
def competitive_positioning():
    competitors = {
        'Fugro': (8, 9),
        'Keller': (7, 8.5),
        'COWI': (8.5, 8),
        'SIXENSE': (7.5, 6),
        'Ackcio': (6, 5),
        'Campbell Sci': (5, 7),
        'Local Players': (4, 4),
        'IntellTech\n(Target)': (8, 6.5)
    }
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    for company, (features, price) in competitors.items():
        if 'IntellTech' in company:
            color = COLORS['highlight']
            size = 400
        else:
            color = COLORS['primary']
            size = 250
        
        ax.scatter(features, price, s=size, alpha=0.6, color=color, edgecolors='black', linewidth=2)
        ax.annotate(company, (features, price), fontsize=9, ha='center', va='center', fontweight='bold')
    
    # Quadrant lines
    ax.axhline(y=7, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    ax.axvline(x=6.5, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    
    # Quadrant labels
    ax.text(8.5, 9.5, 'Premium', fontsize=11, ha='center', fontweight='bold')
    ax.text(5, 9.5, 'Overpriced', fontsize=11, ha='center', fontweight='bold')
    ax.text(8.5, 4.5, 'Value', fontsize=11, ha='center', fontweight='bold')
    ax.text(5, 4.5, 'Commodity', fontsize=11, ha='center', fontweight='bold')
    
    ax.set_xlabel('Features / Capabilities Score', fontsize=12, fontweight='bold')
    ax.set_ylabel('Price Point Score', fontsize=12, fontweight='bold')
    ax.set_title('Competitive Positioning Matrix', fontsize=14, fontweight='bold', pad=20)
    ax.set_xlim(3, 10)
    ax.set_ylim(3, 10)
    ax.grid(True, alpha=0.3)
    
    save_fig('competitive_positioning.png')

# 7. Market Opportunity Waterfall
def market_waterfall():
    categories = ['TAM\nGlobal', 'APAC\nFilter', 'SAM\nAPAC', 'Capability\nFilter', 'SOM\n(3-Year)']
    values = [12000, -8500, 3500, -3300, 200]
    cumulative = np.cumsum([12000, -8500, 0, -3300, 0])
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    colors = [COLORS['primary'] if v > 0 else COLORS['neutral'] for v in values]
    colors[2] = COLORS['accent']  # SAM
    colors[4] = COLORS['highlight']  # SOM
    
    for i, (cat, val, cum) in enumerate(zip(categories, values, cumulative)):
        if val > 0:
            ax.bar(i, val, bottom=cum-val, color=colors[i], edgecolor='black', linewidth=1.5)
        else:
            ax.bar(i, abs(val), bottom=cum, color=colors[i], alpha=0.7, edgecolor='black', linewidth=1.5)
        
        # Add value labels
        if i in [0, 2, 4]:
            ax.text(i, cum if val < 0 else cum, f'${cum:,.0f}M', ha='center', va='bottom', 
                   fontsize=11, fontweight='bold')
    
    ax.set_xticks(range(len(categories)))
    ax.set_xticklabels(categories, fontsize=11, fontweight='bold')
    ax.set_ylabel('Market Size (USD Millions)', fontsize=12, fontweight='bold')
    ax.set_title('Market Opportunity Waterfall: TAM → SAM → SOM', fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3)
    
    save_fig('market_waterfall.png')

# Generate all visualizations
if __name__ == '__main__':
    print("Generating visualizations...")
    country_market_size()
    print("✓ Country market size")
    attractiveness_matrix()
    print("✓ Attractiveness matrix")
    regulatory_heatmap()
    print("✓ Regulatory heatmap")
    sector_market_evolution()
    print("✓ Sector evolution")
    sector_bubble_chart()
    print("✓ Sector bubble chart")
    competitive_positioning()
    print("✓ Competitive positioning")
    market_waterfall()
    print("✓ Market waterfall")
    print("\nAll visualizations generated successfully!")
