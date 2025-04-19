import random
import matplotlib.pyplot as plt
#================================================================================
class system:
    def __init__(self, machine, duration):
        self.machine = machine
        self.duration = duration
#================================================================================

class Job:
    def __init__(self, nameOfJob, operations):
        self.nameOfJob = nameOfJob
        self.operations = operations

#================================================================================

def get_input_info():
    print("                        {Welcome to Job Shop Scheduling!}\n")
    machine_number = int(input("Please enter the number of machines: "))
    jobs = []
    jobs_number = int(input("Please enter the number of jobs: "))
    for i in range(jobs_number):
        job_name = input(f"Please enter the name of Job {i + 1}: ")

        job_operations = []
        operations_numbers = int(input(f"Enter the number of Job_Operations for Job {job_name}: "))

        if operations_numbers == 0:
            print(f"Job {job_name} has no operations.")
            jobs.append(Job(job_name, job_operations))
            continue

        for j in range(operations_numbers):
            while True:
                machine, duration = input(
                    f"Please enter machine, and duration(time) for the operation {j + 1} (in this format:M1 10): ").split()
                machine_idx = int(machine[1:]) - 1
                if 0 <= machine_idx < machine_number:
                    break
                print(
                    f"Invalid machine index: {machine}. Please enter a machine index between M1 and M{machine_number}.")
            job_operations.append(system(machine, int(duration)))
        jobs.append(Job(job_name, job_operations))
    return machine_number, jobs


#================================================================================

def create_initial_population(jobs, size):
    population = []
    for _ in range(size):#generate random sequence for each job in the job list
        individual = []
        for job in jobs:
            sequence = random.sample(range(len(job.operations)), len(job.operations))#generate random sequence for each job in the job list from 0 to the length of the operation list
            individual.append(sequence)
        population.append(individual)
    return population

#================================================================================

def decode_individual(individual, jobs): #individual is a list of job sequences
    decoded = []
    for job_index, job_sequence in enumerate(individual):#enumerate() method adds a counter to an iterable and returns it in a form of enumerate object
        decoded_job = []
        for operation_index in job_sequence:
            decoded_job.append(jobs[job_index].operations[operation_index])
        decoded.append(decoded_job)
    return decoded

#================================================================================
def calculate_time(individual, jobs, num_machines):
    machine_end_times = [0] * num_machines
    job_end_times = [0] * len(jobs)
    decoded = decode_individual(individual, jobs)

    for job_idx, job in enumerate(decoded):
        start_time = 0
        for operation in job:
            machine_idx = int(operation.machine[1:]) - 1
            if machine_idx >= num_machines:
                raise ValueError(f"Operation references invalid machine index {machine_idx + 1}, which exceeds the number of machines ({num_machines}).")
            start_time = max(start_time, machine_end_times[machine_idx])
            machine_end_times[machine_idx] = start_time + operation.duration
            start_time += operation.duration
        job_end_times[job_idx] = start_time

    return max(job_end_times)

#================================================================================

def select_parents(population, jobs, machine_number):
    parent_size = 3
    selected = []
    for _ in range(2):
        parent = random.sample(population, parent_size)#generate random sequence for each job in the job list from 0 to the length of the operation list
        parent.sort(key=lambda ind: calculate_time(ind, jobs, machine_number))#sort the parent list based on the calculate_time function
        selected.append(parent[0])#add the first element of the sorted parent list to the selected list,then add the second element of the sorted parent list to the selected list
    return selected

#================================================================================

def crossover_function(parent_one, parent_two):
    if len(parent_one) > 1:
        crossover_point = random.randint(1, len(parent_one) - 1) #If the length of parent_one is greater than 1, this line generates a random integer crossover_point between 1 and len(parent_one) - 1. This point determines where the crossover will occur between the two parents.
        child_one = parent_one[:crossover_point] + parent_two[crossover_point:]#This line creates the first child by concatenating the first part of parent_one up to the crossover_point and the second part of parent_two from the crossover_point onwards.
        child_two = parent_two[:crossover_point] + parent_one[crossover_point:]#This line creates the second child by concatenating the first part of parent_two up to the crossover_point and the second part of parent_one from the crossover_point onwards.
    else:
        child_one = parent_one[:]#If the length of parent_one is 1, this line creates the first child as a copy of parent_one.
        child_two = parent_two[:]#This line creates the second child as a copy of parent_two.
    return child_one, child_two

#================================================================================
def mutation_function(individual):
    for job in individual:
        if len(job) > 1 and random.random() < 0.1:#If the length of job is greater than 1 and the random number is less than 0.1, this line is executed.
            i, j = random.sample(range(len(job)), 2)#This line generates two random integers i and j between 0 and len(job) - 1.
            job[i], job[j] = job[j], job[i]#This line swaps the values of job[i] and job[j].

#================================================================================
def genetic_algorithm_function(jobs, num_machines, size=50, generations=100):
    population = create_initial_population(jobs, size)
    for _ in range(generations):
        new_population = []
        for _ in range(size // 2):
            parent_one, parent_two = select_parents(population, jobs, num_machines)
            child_one, child_two = crossover_function(parent_one, parent_two)
            mutation_function(child_one)
            mutation_function(child_two)
            new_population.extend([child_one, child_two])
        population = new_population

    population.sort(key=lambda ind: calculate_time(ind, jobs, num_machines))
    return population[0]
#================================================================================

def System_schedule(best_individual, jobs, num_machines):
    decoded = decode_individual(best_individual, jobs)
    machine_schedules = [[] for _ in range(num_machines)]#This line creates a list of empty lists called machine_schedules, which will store the start and end times of each machine for each job.
    machine_end_times = [0] * num_machines

    for job_index, job in enumerate(decoded):
        start_time = 0
        for operation in job:
            machine_index = int(operation.machine[1:]) - 1#This line extracts the machine number from the machine string and subtracts 1 to get the index of the machine in the list.
            start_time = max(start_time, machine_end_times[machine_index])
            machine_schedules[machine_index].append((start_time, start_time + operation.duration, job_index))
            machine_end_times[machine_index] = start_time + operation.duration
            start_time += operation.duration

    figure, axis = plt.subplots()
    colors = plt.get_cmap('plasma')

    for machine_index, schedule in enumerate(machine_schedules):
        for start, end, job_index in schedule:
            axis.broken_barh([(start, end - start)], (machine_index - 0.4, 0.8), facecolors=colors(job_index / len(jobs)))#This line creates a horizontal bar in the Gantt chart for each job. The color of the bar is based on the job index divided by the total number of jobs.
            axis.text(start + (end - start) / 2, machine_index, f'Job {job_index + 1}', ha='center', va='center', color='lightblue')#This line adds the job index to the center of the bar.

    axis.set_ylim(-1, num_machines)#This line sets the y-axis limits to (-1, num_machines) to match the number of machines.
    axis.set_xlim(0, max(max(end for start, end, _ in machine) for machine in machine_schedules))#This line sets the x-axis limits to the maximum end time of any job in the Gantt chart.
    axis.set_yticks(range(num_machines))#This line sets the y-axis ticks to the range of num_machines.
    axis.set_yticklabels([f'Machine {i + 1}' for i in range(num_machines)])#This line sets the y-axis tick labels to the machine numbers.
    axis.set_xlabel('JobTime')
    axis.set_title('Job Shop Scheduling System!')
    plt.show()

def main():
    machine_number, jobs = get_input_info()

    size = 50
    generations = 100

    best_individual = genetic_algorithm_function(jobs, machine_number, size, generations)

    System_schedule(best_individual, jobs, machine_number)

if __name__ == "__main__":
    main()
