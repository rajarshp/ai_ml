#!/usr/bin/env python
# coding: utf-8

# In[49]:


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import lightgbm as lgb
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.inspection import PartialDependenceDisplay, permutation_importance
import shap
from sklearn.model_selection import learning_curve, cross_val_score
import warnings


# In[50]:


warnings.filterwarnings(action='ignore', category=UserWarning, module='LightGBM')
df = pd.read_csv('product_data.csv')


# In[51]:


df


# In[52]:


## Label Encoding


# Example: Label encoding for product_id and competitor_id
# label_encoder = LabelEncoder()

# df['product_id'] = label_encoder.fit_transform(df['product_id'])

# # Optionally, you can also encode product_type if it's categorical
# df['product_type'] = label_encoder.fit_transform(df['product_type'])

# # Check the encoded columns
# print(df[['product_id',  'product_type']].head())


# In[53]:


# ##  One-Hot Encoding

# one_hot_encoder = OneHotEncoder(sparse=False)

# # Fit-transform the data and add new columns to the DataFrame
# product_type_encoded = one_hot_encoder.fit_transform(df[['product_type']])
# product_type_encoded_df = pd.DataFrame(product_type_encoded, columns=one_hot_encoder.get_feature_names(['product_type']))

# # Concatenate with original DataFrame
# df = pd.concat([df, product_type_encoded_df], axis=1)

# # Drop original categorical column (if needed)
# df.drop(columns=['product_type'], inplace=True)

# # Check the encoded DataFrame
# print(df.head())


# In[54]:


# Fill missing values with a placeholder (e.g., -1) for competitor columns
# for col in features.columns:
#     if 'competitor' in col:
#         features[col].fillna(-1, inplace=True)  # Fill missing competitor prices with -1 or any other appropriate placeholder

# features = features.fillna(features.mean())

competitor_columns = [col for col in df.columns if col.startswith('competitor')][:5]

# Fill NaN values in competitor columns with the mean of that row
# df['competitor_mean'] = df[competitor_columns].mean(axis=1)

# print(df.head())
# for col in competitor_columns:
#     df[col].fillna(df['competitor_mean'], inplace=True)

# df.drop(columns=['competitor_mean'], inplace=True)

df[competitor_columns] = df[competitor_columns].apply(lambda x: x.fillna(x.mean()), axis=1)
df['max_discount'] = np.round(df['actual_price'] - df[competitor_columns].min(axis=1), 2)

df['min_price'] = df[competitor_columns].min(axis=1)

# keep only 5 competitors
other_columns = [col for col in df.columns if not col.startswith('competitor')]
keep_columns = other_columns + competitor_columns

df_final = df[keep_columns]
# Feature engineering: Extract relevant features and target
features = df_final.drop(columns=['product_id', 'product_type', 'timestamp', 'promotional_price'])
target = df_final['promotional_price']  # Target variable: actual price

print(features)


# In[55]:


# Train-test split
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

base_model = lgb.LGBMRegressor(verbosity=-1)

print(X_test)

# Fit the model
base_model.fit(X_train, y_train)

# Make predictions
y_pred = base_model.predict(X_test)

# Train the quantile regression models for lower and upper bounds
min_price_model = lgb.LGBMRegressor(objective='quantile', alpha=0.1)
max_price_model = lgb.LGBMRegressor(objective='quantile', alpha=0.9)

min_price_model.fit(X_train, y_train)
max_price_model.fit(X_train, y_train)

# Predict the quantiles
lower_bound_pred = min_price_model.predict(X_test)
upper_bound_pred = max_price_model.predict(X_test)


# In[56]:


feature_importances = base_model.feature_importances_
feature_names = features.columns

importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': feature_importances
}).sort_values(by='Importance', ascending=False)

# Plot feature importance
plt.figure(figsize=(10, 6))
plt.barh(importance_df['Feature'], importance_df['Importance'])
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.title('Feature Importance')
plt.gca().invert_yaxis()  # Invert y-axis to have the most important feature on top
plt.show()


# In[57]:


# HEAT MAP

# Compute the correlation matrix
corr = features.corr()

# Generate a heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()


# In[58]:


# Partial Dependence Plots (PDP)

fig, ax = plt.subplots(figsize=(12, 8))
PartialDependenceDisplay.from_estimator(base_model, X_train, features.columns, ax=ax)
plt.suptitle('Partial Dependence Plots')
plt.subplots_adjust(top=0.95)
plt.show()


# In[59]:


## SHAP Value

# Create a SHAP explainer
explainer = shap.TreeExplainer(base_model)
shap_values = explainer.shap_values(X_train)

# Summary plot
shap.summary_plot(shap_values, X_train, plot_type="bar")

# SHAP dependence plot for a single feature
shap.dependence_plot('competitor1', shap_values, X_train)


# In[60]:


# Feature Importance as a Bar Plot with Error Bars
perm_importance = permutation_importance(base_model, X_test, y_test, n_repeats=10, random_state=42)

# Create a DataFrame for visualization
perm_importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': perm_importance.importances_mean,
    'Importance STD': perm_importance.importances_std
}).sort_values(by='Importance', ascending=False)

# Plot permutation importance
plt.figure(figsize=(10, 6))
plt.barh(perm_importance_df['Feature'], perm_importance_df['Importance'], xerr=perm_importance_df['Importance STD'])
plt.xlabel('Permutation Importance')
plt.ylabel('Feature')
plt.title('Permutation Feature Importance')
plt.gca().invert_yaxis()
plt.show()


# In[61]:


# Make predictions for the entire dataset
df_predicted = df_final.copy()
df_predicted['max_predicted_price_range'] = np.round(max_price_model.predict(features),2)
df_predicted['min_predicted_price_range'] = np.round(min_price_model.predict(features),2)
df_predicted['base_predicted_price'] = np.round(base_model.predict(features),2)

# Export DataFrame to CSV with predicted promotional price
file_path_with_predictions = 'products_with_predicted_prime.csv'
df_predicted.to_csv(file_path_with_predictions, index=False)

print(f"Data with predicted prime saved to {file_path_with_predictions}")


# In[62]:


# Evaluate model performance
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"MAE: {mae}")
print(f"MSE: {mse}")
print(f"RMSE: {rmse}")
print(f"R^2: {r2}")


# In[63]:


## Actual vs. Predicted Plot

plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred)
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--')
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Actual vs Predicted')
plt.show()


# In[65]:


## Learning Curves

train_sizes, train_scores, test_scores = learning_curve(base_model, X_train, y_train, cv=5, scoring='neg_mean_squared_error', train_sizes=np.linspace(0.1, 1.0, 10))

train_scores_mean = -np.mean(train_scores, axis=1)
test_scores_mean = -np.mean(test_scores, axis=1)

plt.figure(figsize=(10, 6))
plt.plot(train_sizes, train_scores_mean, label='Training error')
plt.plot(train_sizes, test_scores_mean, label='Validation error')
plt.ylabel('MSE')
plt.xlabel('Training size')
plt.title('Learning Curves')
plt.legend()
plt.show()


# In[66]:


## Cross-Validation Scores


cv_scores = cross_val_score(base_model, features, target, cv=5, scoring='neg_mean_squared_error')
cv_rmse = np.sqrt(-cv_scores)

print(f"Cross-Validation RMSE: {cv_rmse.mean()} ± {cv_rmse.std()}")


# In[67]:


# Create the modelabs
import pickle

with open('base_model.pkl', 'wb') as f:
    pickle.dump(base_model, f)

with open('min_price_model.pkl', 'wb') as f:
    pickle.dump(min_price_model, f)

with open('max_price_model.pkl', 'wb') as f:
    pickle.dump(max_price_model, f)


# In[ ]:




