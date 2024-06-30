import pandas as pd
import numpy as np


# 讀取Excel文件
data = pd.read_excel('GA-Input data-job attributes 092021.xlsx')

# 建立兩個欄位machine_id和batch_id
data['machine_id'] = np.nan
data['batch_id'] = np.nan

# 每一個job隨機分配machine_id(1-5)
data['machine_id'] = np.random.randint(1, 6, size=len(data))

# 按照machine_id排序由小到大
data = data.sort_values(by='machine_id')

# 當recipe_id與machine_id相同時將batch_id設為相同值
for i in range(len(data)):
    if data['recipe_id'][i] == data['machine_id'][i]:
        data['batch_id'][i] = data['recipe_id'][i]

# 由小到大：batch_id主排序、job_size次排序，none值排在最後
data = data.sort_values(by=['batch_id','job_size'], na_position='last')


# 初始化batch_id和batch_size
batch_id = 1
batch_size = 0

# 遍歷每一行
for index, row in data.iterrows():
    if batch_size + row['job_size'] > 50:
        batch_id += 1
        batch_size = row['job_size']
    else:
        batch_size += row['job_size']
    data.at[index, 'batch_id'] = batch_id
                

#輸出excel
print(data)
data.to_excel('GA_hw1.xlsx', index=False)
