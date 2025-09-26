from tabulate import tabulate
import pandas as pd
import numpy as np

# Assume you have a DataFrame named 'stage1_usefulness'
# and you want to create a summary table for the 'usefulness' column
summary_stats = stage1_usefulness.describe()
custom_row = stage1_usefulness.quantile(0.35)
summary_stats.loc['35%'] = custom_row
summary_stats.columns = summary_stats.columns.str.replace('<br>', ' ')
transposed_stats = summary_stats.transpose()

# Calculate the confidence interval for each column
conf_int = stage1_usefulness.apply(lambda x: (np.percentile(x, 2.5), np.percentile(x, 97.5)))

# Sort the DataFrame by the 'mean' column
transposed_stats.sort_values(by='mean', inplace=True)

# Format the 'count', 'mean', and 'std' columns
transposed_stats['count'] = transposed_stats['count'].apply(lambda x: f"{x:.0f}")
transposed_stats['mean'] = transposed_stats['mean'].apply(lambda x: f"{x:.2f}")
transposed_stats['std'] = transposed_stats['std'].apply(lambda x: f"{x:.2f}")
transposed_stats['min'] = transposed_stats['min'].apply(lambda x: f"{x:.0f}")
transposed_stats['max'] = transposed_stats['max'].apply(lambda x: f"{x:.0f}")
transposed_stats['35%'] = transposed_stats['35%'].apply(lambda x: f"{x:.0f}")
transposed_stats['50%'] = transposed_stats['50%'].apply(lambda x: f"{x:.0f}")

# Add a new row for confidence intervals
transposed_stats.loc['95% CI'] = conf_int.apply(lambda x: f"({x[0]:.2f}, {x[1]:.2f})")

# Remove '25%' and '75%' columns
transposed_stats = transposed_stats[['count', 'mean', 'std', 'min', '35%', '50%', 'max']]

# Create HTML table with styling
html_table = transposed_stats.to_html(classes='table', border=0, index=True)

# Add a CSS style for improved appearance
css_style = '<style>body { font-family: Arial, sans-serif; font-size: 14px; } .table { border-collapse: collapse; width: 60%; margin: auto; } th, td { padding: 10px; text-align: center; background-color: #f2f2f2; } th:first-child, td:first-child { text-align: left; } td { font-size: 12px; } th { font-size: 12px; } h2 { font-size: 14px; }</style>\n'

# Add the title to the HTML string
html_with_title = f'<h4 style="text-align: center;">Stage 1 - Usefulness</h4>\n{css_style}\n{html_table}'

# Save the HTML to a file or display it
with open('summary_stats.html', 'w') as f:
    f.write(html_with_title)
