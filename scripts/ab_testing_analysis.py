import mysql.connector
import pandas as pd
from statsmodels.stats.proportion import proportions_ztest
import matplotlib.pyplot as plt
import seaborn as sns

# --- MySQL Connection ---
conn = mysql.connector.connect(
    host="localhost",
    user="root",             # replace with your MySQL username
    password="",# replace with your password
    database="ab_testing_db"
)

# --- Fetch Data ---
query = "SELECT * FROM experiment_data;"
df = pd.read_sql(query, conn)
conn.close()

# --- Basic Metrics ---
metrics = df.groupby('group_name')['converted'].agg(['count','sum']).rename(columns={'count':'total_users','sum':'conversions'})
metrics['conversion_rate'] = metrics['conversions'] / metrics['total_users']

# --- Uplift Calculation ---
uplift = metrics.loc['B','conversion_rate'] - metrics.loc['A','conversion_rate']

# --- Statistical Significance (z-test) ---
count = metrics['conversions'].values
nobs = metrics['total_users'].values
z_stat, p_value = proportions_ztest(count, nobs)

# --- Print Results ---
print("=== A/B Test Metrics ===")
print(metrics)
print(f"\nUplift (B - A): {uplift:.4f}")
print(f"Z-statistic: {z_stat:.4f}, P-value: {p_value:.4f}")

# --- Visualization ---
sns.barplot(x=metrics.index, y=metrics['conversion_rate']*100)
plt.ylabel("Conversion Rate (%)")
plt.title("A/B Test Conversion Rates")
plt.show()
