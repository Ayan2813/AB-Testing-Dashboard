import pandas as pd
import numpy as np

# Parameters
n = 100  # total number of rows

np.random.seed(42)  # for reproducibility

# Generate random data
df = pd.DataFrame({
    'group_name': np.random.choice(['A', 'B'], size=n),
    'converted': np.random.choice([0, 1], size=n, p=[0.7, 0.3]),  # ~30% conversion rate
    'device': np.random.choice(['Mobile', 'Desktop', 'Tablet'], size=n),
    'country': np.random.choice(['USA', 'India', 'UK', 'Canada', 'Australia'], size=n),
    'traffic_source': np.random.choice(['Organic', 'Paid', 'Referral', 'Social', 'Direct'], size=n),
    'created_at': pd.date_range(start='2025-01-01', periods=n, freq='D')
})

# Save CSV
df.to_csv("sample_ab_test_data.csv", index=False)
print("CSV file 'sample_ab_test_data.csv' created successfully!")
