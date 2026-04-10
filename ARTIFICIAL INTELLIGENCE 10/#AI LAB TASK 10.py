#AI LAB TASK 10 
import pandas as pd
import numpy as np

# 1. Read CSV
data = pd.read_csv("C:/Users/Ahtsham-Riaz/Downloads/student_data.csv")

# 2. Shape
print("Rows:", data.shape[0])
print("Columns:", data.shape[1])

# 3. Null values
print(data.isnull().sum())

# 4. REAL COLUMN use karo (pehle check karo)
print(data.columns)

col = 'age'   

# 5. Unique values
print(data[col].unique())

# 6. Fill missing values (mode)
num = data[col].mode()[0]
data[col] = data[col].fillna(num)

# 7. Convert to int
data[col] = data[col].astype(np.int64)

# 8. Drop unnecessary column (agar exist karta ho)
if 'id' in data.columns:
    data.drop('id', axis=1, inplace=True)

# 9. Data types
print(data.dtypes)

# 10. Split X and Y
x = data.iloc[:, :-1]
y = data.iloc[:, -1]

print(x.shape)
print(y.shape)

# 11. Convert object columns to numbers
cat_columns = x.select_dtypes(include=['object']).columns
x[cat_columns] = x[cat_columns].apply(lambda col: pd.factorize(col)[0])