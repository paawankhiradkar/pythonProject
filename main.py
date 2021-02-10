import re
import glob
import pandas as pd

#This is to check initial commit in git
print('#' * 100)
print('#' * 100)
print("Hi.. This is PK.")
print("Hold on your horses. The script execution has started.")
print('#' * 100)
print('#' * 100)

files = glob.glob('*.txt') #read and store all the .txt files in current directory
list2 = list()
df_list1 = list()  #final list which will be passed to dataframe for creating an excel file
dict_month = {'01':'Jan', '02':'Feb', '03':'Mar', '04':'Apr', '05':'May', '06':'Jun', '07':'Jul', '08':'Aug', '09':'Sep', '10':'Oct', '11':'Nov', '12':'Dec'}
month = None  #used to create sheet name with month
pattern = '^2\d\d\d\d\d\d\d_'
invalid_files_set = set()
valid_files = list()
print("[LOG]: Processing all the valid license files.")

#This will read the file names and separate valid and invalid files based on the date in the filename.
for file in files:
    if re.match(pattern, file):
        if (file[4:6] in dict_month):
            month = dict_month[file[4:6]] + "-" + file[0:4]
            valid_files.append(file)
        else:
            invalid_files_set.add(file)
    else:
        invalid_files_set.add(file)

#This will read the files one by one and create a data in disctionary format.
for file in valid_files:
    dict1 = dict()
    list1 = list()
    myfile = open(file)
    next_line = myfile.readline().strip()
    while next_line != "":
        if ':' in next_line:
            key, description = next_line.strip().split(':')
            dict1[key.strip()] = description.strip()
        else:
            if 'Model' not in next_line:
                dict2 = {}
                dict2['Model'] = next_line.strip().split('\t',2)[0]
                dict2['Serial Number'] = next_line.strip().split('\t',2)[1]
                dict2['Capacity (TB)'] = next_line.strip().split('\t',2)[2]
                list1.append(dict2)
        next_line = myfile.readline().strip()
    dict1['Storage System Details'] = list1
    list2.append(dict1)

print("[LOG]: Writing data into an excel file.")
#This will take neccesary colummns from the dictionary and create a new list to pass it as arg to datafram for creating excel.
for i in range(len(list2)):
    for j in range(len(list2[i]['Storage System Details'])):
        dict_1 = dict()
        dict_1 = {'Requester':list2[i]['Requester Email'], 'Customer Name':list2[i]['Customer Name'], 'Package Type':list2[i]['Package Type'], 'Setup':list2[i]['Setup Details'], 'License Type':list2[i]['License Type'], 'Order IDs':list2[i]['Order Ids'], 'License Start Date':list2[i]['License Start Date'], 'Model':list2[i]['Storage System Details'][j]['Model'], 'Serial Number':list2[i]['Storage System Details'][j]['Serial Number'], 'Capacaity (TB)':list2[i]['Storage System Details'][j]['Capacity (TB)'], 'Nodes':list2[i]['Nodes'], 'Additional Units': None if list2[i]['Additional Units'] == '(25 nodes/unit)' else list2[i]['Additional Units'][0:2]  }
        df_list1.append(dict_1)

#This will create a excel file.
df = pd.DataFrame(df_list1)
#df.to_excel('license_inv.xlsx', sheet_name=month, index=False)
df.to_excel('license_inv.xlsx', sheet_name=month, index=False)
print("[LOG]: Done with writing data into an excel file.")
if invalid_files_set:
    print("[LOG]: Found files with invalid dates. These files are not processed.", invalid_files_set)
print("[LOG]: Execution completed. Thank you!!")