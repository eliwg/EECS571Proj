import numpy as np
import sys

MAX_SUB_TASKS = 10 # Maximum number of sub-tasks per task
MAX_NUM_SPEEDS = 5 # Maximum number of different speeds a task can run at
NUM_DAGS = 100

# Global variable to ensure task ID's are not repeated
g_id = 0
g_release_time = 0

# A task is a DAG -> it has parts that can run sequentially and parts that can run in serial
# Use nomenclature from paper: DAG = task, a decomposed (serialized) task is made up of many subtasks
# Find a new way of representing these tasks
# Add random release time for tasks -> they are sporadic

# Add: scheduling window -> release time, execution time and deadline (follow constraint (2) in paper [1]) 
# (this needs to be done by task decomposition -> a task is only "released" when its dependencies are met)

# Need to use this because of speed profile definition
'''
    Struct for DAG tasks: {int task_id, int release_time, int deadline, int speeds[], float prob_speeds[], int num_speeds,
    int execution_times[], int num_subtasks, char[] dependencies, int len_dependencies}

    Struct for subtasks: {int subtask_id, int dependencies[], int num_dependecies, int execution_time, int deadline}
'''


'''
    Class to represent tasks (since Python doesn't do simple structs)
    Stores: struct task { int task_id, int dependencies[], int num_dependecies, int execution_time
    int deadline}

    Example verbose output:
    task_id: 11      execution_time: 54     dependencies: [1, 2, 6, 8]       num_dependencies = 4   deadline = 241

    Example non-verbose output (use this for scheduling):
    11, 54, [1, 2, 6, 8], 4, 241
'''
class task:

    def __init__(self, task_id, release_time):
        self.task_id = task_id
        self.release_time = release_time
        self.deadline = -1
        self.speeds = []
        self.prob_speeds = []
        self.num_speeds = -1
        self.execution_times = []
        self.num_subtasks = -1
        self.dependencies = ''
        self.len_dependencies = 0
    
    def print_task(self, verbose=False):
        pass
  

'''
    Generates a directed, acyclic graph with n nodes in the form of a
    lower triangular matrix of size n x n.
    Adapted from 3.1.1 in [2] ("The G(n,p) method")
    
    Direction of dependencies is always j->i
    e.g. if M[5][3] = 1, 3 is the parent of 5, 5 depends on 3.

    Default p=0.25 from paper
'''
def erdos_renyi(n, p=0.25):

    M = np.zeros((n,n))

    for i in range(n):
        for j in range(i):
            if np.random.rand() < p:
                M[i,j] = 1
            else:
                M[i,j] = 0

    return M.astype(int)

'''
    Returns a random release time for a task.
    This ensures that we can assume that tasks with lower
    task_id's are released sooner.
'''
def gen_release_time(release_time):
    return release_time + np.random.randint(low=0, high=10)


'''
    Returns a random deadline for a task.
    This is also a wrapper for numpy randint.
    Ensures feasibility by ensuring that a task's deadline
    is greater than the sum of its own execution time and
    the execution times of all dependecies.
'''
def gen_deadline(execution_time, past_execution_times):
    return execution_time + past_execution_times + np.random.randint(low=5, high=50)

'''
    Returns a random execution time for a task.
    This is simply a wrapper for numpy randint and is here
    to make it easier to scale the values as needed.
'''
def gen_execution_time():
    return np.random.randint(low=100, high=None)


'''
    Returns a numpy array of length n where each element is in the form:
    struct task { int task_id, int dependencies[], int num_dependecies, int execution_time
    int deadline} 
'''
def gen_task(M, id, release_time):
    
    n = M.shape[0]
    t = task(task_id=id, release_time=release_time)
    


    # # Assign a random execution time to each task
    # for i in range(n):
    #     subtasks.append(task(task_id=i, execution_time=gen_execution_time()))
    
    # # Add dependencies for tasks
    # # Start at 1 since task 0 cannot have any dependencies
    # for i in range(1, n):
    #     for j in range(i):
    #         if M[i,j] == 1:
    #             subtasks[i].dependencies.append(j)
    #             subtasks[i].num_dependencies += 1

    # # Calculate deadlines for tasks
    # for i in range(n):
    #     past_execution_times = 0
    #     for j in tasks[i].dependencies:
    #         past_execution_times += tasks[j].execution_time
    #     tasks[i].deadline = gen_deadline(execution_time=tasks[i].execution_time, past_execution_times=past_execution_times)

    # return tasks

def main():
    # A janky way to redirect print statements to a file in Python
    # without having to use > in the terminal
    with open('tasks.txt','w') as sys.stdout:
        M = erdos_renyi(NUM_DAGS)
        task_set = gen_task(M)
        for task in task_set:
            task.print_task(verbose=False)

if __name__ == "__main__":
    main()