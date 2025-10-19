
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

import os

# Make path relative to this script file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)



# Number of users to simulate
n = 5000

# Simulated data
np.random.seed(42)
user_ids = np.arange(1, n + 1)
groups = np.random.choice(['A', 'B'], size=n)
devices = np.random.choice(['Mobile', 'Desktop'], size=n, p=[0.7, 0.3])
countries = np.random.choice(['India', 'USA', 'UK', 'Germany'], size=n)
traffic_source = np.random.choice(['Organic', 'Paid', 'Referral', 'Social'], size=n)

# Conversion probabilities
conversion_rate_A = 0.12
conversion_rate_B = 0.15

conversions = [
    1 if (group == 'A' and np.random.rand() < conversion_rate_A) or
         (group == 'B' and np.random.rand() < conversion_rate_B)
    else 0
    for group in groups
]

# Generate timestamps
start_date = datetime.now() - timedelta(days=30)
timestamps = [start_date + timedelta(minutes=i) for i in range(n)]

# Create DataFrame
df = pd.DataFrame({
    'user_id': user_ids,
    'group': groups,
    'converted': conversions,
    'device': devices,
    'country': countries,
    'traffic_source': traffic_source,
    'timestamp': timestamps
})

# Save to CSV
df.to_csv(os.path.join(DATA_DIR, 'experiment_data.csv'), index=False)
print("Experiment data generated and saved to data/experiment_data.csv")
