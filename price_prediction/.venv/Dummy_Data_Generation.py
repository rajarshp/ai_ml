#!/usr/bin/env python
# coding: utf-8

# ### Data Generation

# In[2]:


import pandas as pd
import numpy as np
import time


# In[8]:


# Define realistic price ranges for each product
# Define realistic price ranges for different types of products
price_ranges = {
    "electronics": (199, 1999),
    "beverages": (0.99, 3.49),
    "headphones": (99, 399),
    "smartphones": (499, 1299)
}


# In[18]:


# Function to randomly select a product type and generate its price range
def get_product_price_range():
    product_type = np.random.choice(list(price_ranges.keys()))
    return product_type, price_ranges[product_type]


# In[20]:


# Function to generate simulated sales quantity based on actual price
def simulate_sales(actual_price):
    # Example logic: Simulate sales based on price and other factors
    simulated_sales = np.round(np.random.normal(1000, 100), 0)
    simulated_sales = np.maximum(simulated_sales, 0)  # Ensure non-negative sales
    return int(simulated_sales)


# In[52]:


# Define possible number of competitors for each product
possible_competitor_counts = [2, 5, 10]


# In[48]:


# # Function to generate data for 1000 different products
# def generate_product_data(num_products):
#     data = []
#     current_time = time.time()
    
#     for product_id in range(1, num_products + 1):
#         product_type, price_range = get_product_price_range()
#         num_competitors = np.random.choice(possible_competitor_counts)
#         actual_price = np.round(np.random.uniform(price_range[0], price_range[1]), 2)
#         sales = np.random.randint(100, 1000)  # Simulate sales
        
#         # Append product entry with actual price and sales
#         product_entry = {
#             'product_id': f'product{product_id}',
#             'product_type': product_type,
#             'timestamp': current_time,
#             'actual_price': actual_price,
#             'sales': sales
#         }
#         data.append(product_entry)
        
#         # Generate competitors' prices
#         for competitor_id in range(1, num_competitors + 1):
#             competitor_price = np.round(np.random.uniform(price_range[0], price_range[1]), 2)
            
#             competitor_entry = {
#                 'product_id': f'product{product_id}',
#                 'product_type': product_type,
#                 'timestamp': current_time,
#                 'competitor_id': f'competitor{competitor_id}',
#                 'competitor_price': competitor_price,
#                 'actual_price': actual_price,  # Repeat actual_price for each competitor
#                 'sales': sales  # Repeat sales for each competitor
#             }
#             data.append(competitor_entry)
        
#         current_time -= np.random.uniform(3600, 86400)  # Decrease time by random amount (1 hour to 1 day)

#     return data


# In[110]:


# Function to generate data for different products with all competitors as columns
def generate_product_data(num_products):
    data = []
    current_time = time.time()
    
    for product_id in range(1, num_products + 1):
        product_type, price_range = get_product_price_range()
        num_competitors = np.random.choice(possible_competitor_counts)
        
        # Generate actual price and prime price
        actual_price = np.round(np.random.uniform(price_range[0], price_range[1]), 2)
        
        competitor_prices = []
        for i in range(num_competitors):
            min_allowed_price = actual_price * 0.85
            competitor_price = np.round(np.random.uniform(min_allowed_price, actual_price), 2)
            competitor_prices.append(competitor_price)
        
        # Set promotional price as the lowest competitor price
        promotional_price = min(competitor_prices)
        
        # Initialize entry with basic product information
        entry = {
            'product_id': f'product{product_id}',
            'product_type': product_type,
            'timestamp': current_time,
            'actual_price': actual_price,
            'promotional_price': promotional_price
        }
        
        # Generate competitors' prices and add them as columns
        for i in range(num_competitors):
            competitor_name = f'competitor{i+1}'
            competitor_price = np.round(np.random.uniform(min_allowed_price, actual_price), 2)
            entry[competitor_name] = competitor_price
        
        data.append(entry)
        current_time -= np.random.uniform(3600, 86400)  # Decrease time by random amount (1 hour to 1 day)

    return data


# In[116]:


# Generate data for 1000 different products
num_products = 10000000
product_data = generate_product_data(num_products)

# Create DataFrame
df = pd.DataFrame(product_data)

# Save to CSV
file_path = 'product_data.csv'
df.to_csv(file_path, index=False)

print(f"Data saved to {file_path}")
df.head()


# In[ ]:




