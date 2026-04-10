#AI LAB TASK 9 
import pandas as pd 
#file ka path copy kia hai 
data = pd.read_csv("C:/Users/Ahtsham-Riaz/Downloads/student_data.csv")
#first 5 rows ko print karna ka lia
print(data.head())
#last 5 ko print karna ka lia 
print(data.tail())
#ROWS AND C0LOUMS
print(data.shape)
#null value
print(data.isnull().sum())

# fill missing values
data = data.fillna(data.mode().iloc[0])

# data type
print(data.dtypes)