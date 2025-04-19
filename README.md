#  Job Shop Scheduling with Genetic Algorithm

This project solves the **Job Shop Scheduling Problem (JSSP)** using a **Genetic Algorithm (GA)** and visualizes the optimal schedule using a **Gantt chart**. It was developed as part of the **Artificial Intelligence **.

---

##  Authors

- **Hala Jebreel** 
- **Diana Naseer** 


---

##  Problem Description

The Job Shop Scheduling Problem (JSSP) consists of a set of jobs, each made up of ordered operations. Each operation must run on a specific machine for a given duration. The main objective is to **minimize the makespan**, i.e., the total time required to complete all jobs.

We applied a genetic algorithm that:
- Encodes each job as a sequence of operation indices.
- Evaluates fitness based on makespan.
- Uses crossover and mutation to explore the search space.
- Produces an optimal schedule visualized with a Gantt chart.

---

## 🚀 How It Works

### ✨ Features
- Chromosome-based encoding of job sequences.
- Fitness function based on makespan.
- Parent selection via tournament.
- Single-point crossover.
- Mutation by swapping operations.
- Gantt chart output using `matplotlib`.

---

## Files

| File Name         | Description                                       |
|------------------|---------------------------------------------------|
| `Diana_Hala.py`  | Python implementation of the JSSP with GA         |
| `AI_Report_Hala_Diana.pdf` | PDF report detailing the algorithm, implementation, and results |

---

##  Sample Output

The algorithm displays a **Gantt chart** representing the optimized schedule across machines.

---

##  How to Run

Make sure you have **Python 3** and **matplotlib** installed.

```bash
pip install matplotlib
python Diana_Hala.py
