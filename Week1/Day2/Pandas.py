import pandas as pd
# Create a sample DataFrame
data ={
    "Name" : ["A","B"],
    "Mark" : [90, 80]
}
df = pd.DataFrame(data)
print(df)
# print(type(df))#check type of df


##DataFrame operations
data1 ={
    "Names" : ["Amit","Bharat","Chirag","Deepak","Priya","Riya"],
    "Marks" : [90, 80, 85, 75, None, 88],
    "Subject" : ["Math","Science","English","Math","Science","English"]
}
df = pd.DataFrame(data1)
print(df)

print(df.head())#first 5 rows
print(df.tail())#last 5 rows
print(df.info())
print(df.describe())#statistical summary of numerical columns

##df["Marks"]#access Marks column
df["Marks"].fillna(0)#fill missing values with 0

high_scores = df[df["Marks"] > 85]#filter rows where Marks > 85
print(high_scores)

grouped = df.groupby("Subject")["Marks"].mean()#group by Subject and calculate mean of Marks
print(grouped)

df["Results"] = df["Marks"].apply(lambda x: "Pass" if x >= 80 else "Fail")#add new column Results based on Marks
print(df)

df_sorted = df.sort_values(by="Marks", ascending=False)#sort DataFrame by Marks in descending order
print(df_sorted)

df.to_csv("students.csv", index=False)#save DataFrame to CSV file without index