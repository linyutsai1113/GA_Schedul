import pandas as pd
import random

# 讀取Excel文件
data = pd.read_excel('GA-Input data-job attributes 092021.xlsx')

# 初始化種群
def initialize_population(data, population_size=10, machine_capacity=50):
    population = []
    num_jobs = len(data)
    job_ids = list(data.index)
    
    for _ in range(population_size):
        # 隨機分配機器ID給每個作業
        chromosome = {'Machine ID': [random.randint(1, 3) for _ in range(num_jobs)]}
        df_chromosome = pd.DataFrame(chromosome, index=job_ids)
        
        # 將作業根據批次容量和配方進行分組
        batches = []
        for recipe in data['recipe_id'].unique():
            recipe_jobs = df_chromosome[df_chromosome['Machine ID'] == recipe]
            batch = []
            batch_size = 0
            for job in recipe_jobs.index:
                if batch_size + data.loc[job, 'job_size'] <= machine_capacity:
                    batch.append(job)
                    batch_size += data.loc[job, 'job_size']
                else:
                    batches.append(batch)
                    batch = [job]
                    batch_size = data.loc[job, 'job_size']
            if batch:
                batches.append(batch)
        
        population.append({'chromosome': df_chromosome, 'batches': batches})
    
    return population

# 初始化種群
population = initialize_population(data)

def calculate_fitness(individual, data):
    makespan = 0
    
    for batch in individual['batches']:
        batch_release_time = max(data.loc[job, 'release_time'] for job in batch)
        batch_processing_time = data.loc[batch[0], 'processing_time']
        batch_completion_time = batch_release_time + batch_processing_time
        makespan = max(makespan, batch_completion_time)
    
    return makespan

# 計算種群中每個個體的適應度
for individual in population:
    individual['fitness'] = calculate_fitness(individual, data)


