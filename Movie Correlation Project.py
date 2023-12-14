# %% 

# Import libraries
import pandas as pd
import seaborn as sns
import numpy as np

import matplotlib
import matplotlib.pyplot as plt

print("matplotlib: {}".format(matplotlib.__version__))

plt.style.use("ggplot")
from matplotlib.pyplot import figure

# %matplotlib widget
%matplotlib inline
matplotlib.rcParams["figure.figsize"] = (12, 8)  # adjusts the configuration of the plots we will create

# Read in the data
df = pd.read_csv(r'C:\Users\Shemeika\Downloads\movies.csv')

# TO CREATE A NEW CELL USE THE FOLLOWING COMMAND '# %%'
# %%

# Let's look at the data
df.head()

# %%

# Find missing data 

for col in df.columns:
    pct_missing = np.mean(df[col].isnull())
    print('{}-{}%'.format(col, pct_missing))

# %%

# Drop missing/NaN values and recheck dataframe

df.dropna(inplace = True)

for col in df.columns:
    pct_missing = np.mean(df[col].isnull())
    print('{}-{}%'.format(col, pct_missing))


# %%

# Data types for our columns
df.dtypes

# %%
# Reformat columns to remove the unnecessary decimal point
# df['budget'] = df['budget'].astype('int64')
# df['gross'] = df['gross'].astype('int64')

df = df.astype({"budget": 'int64', "gross": 'int64', "votes": 'int64',
                "score": 'int64', "runtime": 'int64'}) 
df.dtypes

# %%

# check for changes
df


# %%

# Transform "released" column to str from obj 

df['released'] = df['released'].astype('string')
df.dtypes

#%%

# Extract the release yr from "released" and call it "yearcorrect"
# could combine the above cell and the below regex into 1: 
# df['yearcorrect'] = df['released'].astype('string').str.extract(r'[^\d]*[\d]+[^\d]+([\d]+)', expand=False)
import re

df['yearcorrect'] = df['released'].str.extract(r'[^\d]*[\d]+[^\d]+([\d]+)', expand=False)
df


# %%
# used as a test cell to delete 'yearcorrect' column to test the above code

# df = df.drop('yearcorrect', axis=1)

# %%
# to shorten the below output
# "notebook.output.scrolling": true

# sort movies by gross column in descending order 
df.sort_values(by=['gross'], inplace=False, ascending=False)


# %%
# Look at all of the data

# pd.set_option('display.max_rows', None)

# %%
# drop duplicates

df['company'].drop_duplicates().sort_values(ascending=False)
# df.drop_duplicates() if you want to remove all duplicates 
# from the dataframe but we're not doing this this time

# %%
# Budget high correlation
# company high correlation

# Build a scatterplot with budget vs gross
plt.scatter(x = df['budget'], y = df['gross'])
plt.title('Budget vs Gross Earning')
plt.xlabel('Gross Earnings')
plt.ylabel('Budget for Film')
plt.show()

# %%
# Regression Plot - plot the budget vs gross using seaborn

sns.regplot(x='budget', y='gross', data=df, scatter_kws={"color": "green"}, line_kws={"color":"blue"})

# It shows a positive correlation

# %%
# Let's start looking at correlation
# There are different correlations Pearson (default), 
# Kendall, and Spearman
p_corr = df.corr(method='pearson', numeric_only=True)
k_corr = df.corr(method='kendall', numeric_only=True)  
s_corr = df.corr(method='spearman', numeric_only=True)

print("Pearson\n", p_corr)
print("\nKendall\n", k_corr) 
print("\nSpearman\n", s_corr)

# %%
correlation_matrix = df.corr(method='pearson', numeric_only=True)

sns.heatmap(correlation_matrix, annot=True)
plt.title('Correlation Matrix for Numeric Features')
plt.xlabel('Movie Features')
plt.ylabel('Movie Features')
plt.show()

# %%
# Look at Company, which is not numeric and numerize
df_numerized = df

# For loop
for col_name in df_numerized.columns:
    if (df_numerized[col_name].dtype == 'object'):
        df_numerized[col_name] = df_numerized[col_name].astype('category')
        df_numerized[col_name] = df_numerized[col_name].cat.codes
    
# df_numerized.head()
df

# %%
df.head().sort_values('gross', ascending=False)

# %%
correlation_matrix = df_numerized.corr(method='pearson', numeric_only=True)

sns.heatmap(correlation_matrix, annot=True)
plt.title('Correlation Matrix for Numeric Features')
plt.xlabel('Movie Features')
plt.ylabel('Movie Features')
plt.show()

# %%

df_numerized.corr(numeric_only=True)

# %%
correlation_mat = df_numerized.corr(numeric_only=True)
corr_pairs = correlation_mat.unstack()
corr_pairs

# %%
# another way to display the above:

sorted_pairs = corr_pairs.sort_values(ascending=False)
sorted_pairs

# %%
high_corr = sorted_pairs[(sorted_pairs)>0.5]
high_corr

# %%
