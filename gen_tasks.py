import numpy as np
import sys
NUM_TASKS = 10

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

    def __init__(self, task_id, execution_time):
        self.task_id = task_id
        self.execution_time = execution_time
        self.dependencies = []
        self.num_dependencies = 0
        self.deadline = -1
    
    def print_task(self, verbose=False):
        if verbose:
            print(f"task_id: {str(self.task_id)} \t execution_time: {str(self.execution_time)} \t"
                f"dependencies: {str(self.dependencies)} \t num_dependencies = {str(self.num_dependencies)} \t"
             
                f"deadline = {str(self.deadline)}")
        else:
            print(f"{str(self.task_id)}, {str(self.execution_time)}, {str(self.dependencies)}, "
            f"{str(self.num_dependencies)}, {str(self.deadline)}")


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
    Returns a random execution time for a task.
    This is simply a wrapper for numpy randint and is here
    to make it easier to scale the values as needed.
'''
def gen_execution_time():
    return np.random.randint(low=100, high=None)

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
    Returns a numpy array of length n where each element is in the form:
    struct task { int task_id, int dependencies[], int num_dependecies, int execution_time
    int deadline} 
'''
def gen_task_set(M):
    # TODO: Add check for if DAG is zero matrix (extremely unlikely)
    n = M.shape[0]
    tasks = []

    # Assign a random execution time to each task
    for i in range(n):
        tasks.append(task(task_id=i, execution_time=gen_execution_time()))
    
    # Add dependencies for tasks
    # Start at 1 since task 0 cannot have any dependencies
    for i in range(1, n):
        for j in range(i):
            if M[i,j] == 1:
                tasks[i].dependencies.append(j)
                tasks[i].num_dependencies += 1

    # Calculate deadlines for tasks
    for i in range(n):
        past_execution_times = 0
        for j in tasks[i].dependencies:
            past_execution_times += tasks[j].execution_time
        tasks[i].deadline = gen_deadline(execution_time=tasks[i].execution_time, past_execution_times=past_execution_times)

    return tasks

def main():
    # A janky way to redirect print statements to a file in Python
    # without having to use > in the terminal
    with open('tasks.txt','w') as sys.stdout:
        M = erdos_renyi(NUM_TASKS)
        task_set = gen_task_set(M)
        for task in task_set:
            task.print_task(verbose=False)

if __name__ == "__main__":
    main()