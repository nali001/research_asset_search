import os
import json
import itertools

class PwcResource: 
    def __init__(self):
        ''' Handle the resources provided by paperwithcodes. 
        '''
        self.methods = None
        self.datasets = None
        self.tasks = None

    def get_methods(self, method_file):
        ''' Extract method names
        '''
        pwc_methods = []
        with open(method_file) as f: 
            methods = json.load(f) 

        for method in methods: 
            pwc_methods.append(method['name'])
            pwc_methods.append(method['full_name'])
        pwc_methods = list(set(pwc_methods))
        return pwc_methods

    def get_datasets(self, dataset_file):
        ''' Extract dataset names and task names'''
        pwc_datasets = []
        pwc_tasks = []
        with open(dataset_file) as f: 
            datasets = json.load(f) 

        for dataset in datasets: 
            pwc_datasets.append(dataset['name'])
            pwc_datasets.append(dataset['full_name'])
            if 'tasks' in dataset.keys(): 
                for task in dataset['tasks']:
                    pwc_tasks.append(task['task'])
            else: 
                continue
        
        pwc_datasets = list(set(pwc_datasets))
        pwc_tasks = list(set(pwc_tasks))
        return pwc_datasets, pwc_tasks
        
    def get_resources(self, file_path):
        method_file = os.path.join(file_path, 'methods.json')
        dataset_file = os.path.join(file_path, 'datasets.json')

        self.methods = self.get_methods(method_file)
        self.datasets, self.tasks = self.get_datasets(dataset_file)
        return self

# --------------------------------- Usage examples
def generate_pwc_queries(PWC_PATH): 
    ''' Generate queries for crawler using methods, datasets and tasks from PWC
    '''
    pwc = PwcResource()
    pwc.get_resources(PWC_PATH)
    methods = {'query': pwc.methods, 'type': ['method']*len(pwc.methods)}
    datasets = {'query': pwc.datasets, 'type': ['dataset']*len(pwc.datasets)}
    tasks = {'query': pwc.tasks, 'type': ['task']*len(pwc.tasks)}
    print(f'------------------ PWC resources -------------------')
    print(f'methods: {len(pwc.methods)}\ndatasets: {len(pwc.datasets)}\ntasks: {len(pwc.tasks)}\n')

    pwc_queries = {}
    for key in ['query', 'type']: 
        pwc_queries[key] = list(itertools.chain(methods[key], datasets[key], tasks[key]))
    df_pwc_queries = pd.DataFrame.from_dict(pwc_queries)
    
    # Save df_pwc_queries
    print(f'Save methods, dataset, tasks to `{PWC_PATH}/pwc_queries.csv`\n')
    df_pwc_queries.to_csv(os.path.join(PWC_PATH, 'pwc_queries.csv'), index=False)
    return df_pwc_queries