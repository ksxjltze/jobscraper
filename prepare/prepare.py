import pandas as pd

df = pd.read_csv("./jobs.csv")
job_types = df["Type"]

job_data = job_types.str.split(' - ')
job_data = job_data.fillna("None")

job_data_list = job_data.to_list()
columns = ['Type', 'Maximum', 'Minimum']

def isSalaryYearly(x):
    index = x.lower().find("a year")
    return index != -1

def convertSalary(x):
    startIndex = x.lower().find("$")
    endIndex = x.lower().find("a month")
    
    if endIndex == -1:
        endIndex = x.lower().find("a year")
        
        if endIndex == -1:
            endIndex = len(x)
    
    salary = x[startIndex + 1:endIndex].strip().replace(',', '')
    if len(salary) == 0:
        return -1
    
    salary = int(salary)
    return salary

length = len(columns)
for i in range(0, len(job_data_list)):
    job = job_data_list[i]
    
    if type(job) == str:
        job_data_list[i] = [job]
        job = job_data_list[i]
        
    job.reverse()
    for i in range(len(job), length):
        job.append("")
    

indexed_data = pd.DataFrame(job_data_list, columns=columns)
indexed_data["isYearly"] = indexed_data['Maximum'].apply(isSalaryYearly)
indexed_data['Minimum'] = indexed_data['Minimum'].apply(convertSalary)
indexed_data['Maximum'] = indexed_data['Maximum'].apply(convertSalary)
# indexed_data['Minimum'] = indexed_data['Minimum'].apply(convertYearly)

df = df.drop(columns=["Type", "Pay"])
result = df.join(indexed_data).sort_values("Maximum", ascending=False)
print(result)

result.to_csv("./jobs_processed.csv")