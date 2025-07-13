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
#set score to 100 for anyone whose name is david using .loc[]

df = pd.DataFrame({
    'Sales': [200, 500, 120, 300]
})


sales_over = df['Sales'] >= 300 
matching_sales = df[sales_over].index
df['High Sales'] = False 
df.loc[matching_sales, 'High Sales'] = True
print(df['High Sales'])
#create a new column high sales that is true whne sales >=10 else false



df = pd.DataFrame({
    'City': ['NYC', 'LA', 'NYC', 'Chicago'],
    'Pollution Level': [90, 40, 120, 30]
})
#replace pollution level with for 0 for all row where city is nyc and pollution level > 100 


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
#select all rows where temperature is less than 20 


#loc does not prevent iteration, but enables you to use vectorized operations, which are much faster than looping through rows manually

#its not looping thorugh each row...its using numpy's vector operations 


# for i, row in df.iterrows():
#     if row['Score'] > 80:
#         df.at[i, 'Passed'] = True

#this is slow 

#loc filters rows based on a condtion 
#select rows where age > 30
#df.loc[CONDITION] 

#filter rows with multiple conditoins

#df.loc[CONDITION & CONDITION]

#modify values conditoinally

#df.loc[CONDITOIN, COLMUN] = 1000 
#all rows where condition is true, set column to 1000 
#we can also do matching indices 


