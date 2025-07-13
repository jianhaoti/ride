#practice apply with lambda functions 
#gpt generated these for me 

#practice any and all 
import pandas as pd


df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6]
})


df['Sum'] = df.apply(lambda row: row['A'] + row['B'], axis=1) #applies the function row by row 

#processes every row of df and applies lambda to each row 
print(df)


df = pd.DataFrame({
    'Timestamp': ['2025-07-11 14:23:00', '2025-07-11 07:45:00']
})

df['Hour'] = df.apply(lambda row: pd.to_datetime(row['Timestamp']).hour, axis = 1)
print(df)



df = pd.DataFrame({
    'Score': [92, 75, 64, 89, 58]
})


#df['Grade'] = df.apply(lambda row: if row['Score'] >= 90 then "A" elif row['Score'] >= 80 then "B" elif row['Score'] >= 70 then "C" else "F", axis = 1)
#print(df)

#python doesnt have if elif it has 

df['Grade'] = df.apply(lambda row: "A" if row['Score'] >= 90 else "B" if row['Score'] >= 80 else "C" if row['Score'] >= 70 else "F", axis = 1)
print(df)
