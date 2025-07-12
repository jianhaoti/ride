import pandas as pd 
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Score': [85, 60, 95, 70]
})

bool_mask = (df['Score'] > 80)
matching_indices = df[bool_mask].index
print(df.loc[matching_indices])
#use a boolean mask along with loc to select rows where score is above 80

bool_mask2 = (df['Name'] == 'David')
matching_indices = df[bool_mask2].index
df.loc[matching_indices, 'Score'] = 100 
print(df)
#question 2, update values with .loc[]

df = pd.DataFrame({
    'Sales': [200, 500, 120, 300]
})


sales_over = df['Sales'] >= 300 
matching_sales = df[sales_over].index
df['High Sales'] = False 
df.loc[matching_sales, 'High Sales'] = True
print(df['High Sales'])


df = pd.DataFrame({
    'City': ['NYC', 'LA', 'NYC', 'Chicago'],
    'Pollution Level': [90, 40, 120, 30]
})


replace_these = (df['City'] == 'NYC') & (df['Pollution Level'] > 100)
matching_indices = df[replace_these].index
df.loc[matching_indices, 'Pollution Level'] = 0 
print(df)


df = pd.DataFrame({
    'Temperature': [25, 15, 30, 10]
})

bit_mask = df['Temperature'] < 20
matching_indices = df[bit_mask].index
print(df.loc[matching_indices])







#question 4, create an new boolean column...


