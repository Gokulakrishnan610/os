from flask import Flask

app = Flask(__name__)

@app.route('/bestfit')
def bestfit():
    return """#include <stdio.h>

int main() {
    int memory_blocks[] = {100, 500, 200, 300, 600};
    int processes[] = {212, 417, 112, 426};
    int n_blocks = sizeof(memory_blocks) / sizeof(memory_blocks[0]);
    int n_processes = sizeof(processes) / sizeof(processes[0]);
    int allocation[n_processes];

    // Initially, all processes are not allocated
    for (int i = 0; i < n_processes; i++) {
        allocation[i] = -1;
    }

    // Best Fit Allocation
    for (int i = 0; i < n_processes; i++) {
        int best_idx = -1;

        for (int j = 0; j < n_blocks; j++) {
            if (memory_blocks[j] >= processes[i]) {
                if (best_idx == -1 || memory_blocks[j] < memory_blocks[best_idx]) {
                    best_idx = j;
                }
            }
        }

        // If a block was found
        if (best_idx != -1) {
            allocation[i] = best_idx + 1; // Store block number (1-based index)
            memory_blocks[best_idx] -= processes[i]; // Reduce memory block size
        }
    }

    // Output
    printf("Process No.\tProcess Size\tBlock no.\n");
    for (int i = 0; i < n_processes; i++) {
        printf("%d\t\t%d\t\t", i + 1, processes[i]);
        if (allocation[i] != -1)
            printf("%d\n", allocation[i]);
        else
            printf("Not Allocated\n");
    }

    return 0;
}
"""
@app.route('/fcfs')
def fcfs():
    return """#include<stdio.h>

struct Process {
    int id;
    int burst_time;
    int waiting_time;
    int turnaround_time;
};

int main() {
    int n, total_waiting = 0, total_turnaround = 0;

    // Step 1: Input number of processes
    printf("Enter the number of processes: ");
    scanf("%d", &n);
    
    struct Process p[20];

    
    printf("Enter burst time for process ");
    // Step 2: Input burst time for each process
    for(int i = 0; i < n; i++) {
        p[i].id = i+1;
        scanf("%d", &p[i].burst_time);
    }   

    p[0].waiting_time = 0; // First process has 0 waiting time
    p[0].turnaround_time = p[0].burst_time; // Turnaround time for first process is its burst time
    for(int i = 1; i < n; i++) {
        p[i].waiting_time = p[i-1].waiting_time + p[i-1].burst_time;
        p[i].turnaround_time = p[i].waiting_time + p[i].burst_time;
    }

    for(int i = 0; i < n; i++) {
        total_waiting += p[i].waiting_time;
        total_turnaround += p[i].turnaround_time;
    }
    
    // Step 5: Display process details
    printf("\nProcess\tBurst Time\tWaiting Time\tTurn Around Time\n");
    for(int i = 0; i < n; i++) {
        printf("%d\t%d\t\t%d\t\t%d\n", p[i].id, p[i].burst_time, 
               p[i].waiting_time, p[i].turnaround_time);
    }
    
    // Step 6: Display average times
    float avg_waiting = (float) total_waiting / n;
    float avg_turnaround = (float) total_turnaround / n;
    printf("\nAverage waiting time is: %.1f\n", avg_waiting);
    printf("Average Turn around Time is: %.1f\n", avg_turnaround);
    
    return 0;
}"""

@app.route('/sjf')
def sjf():
    return """
#include<stdio.h>
#include<stdbool.h>

struct Process {
    int id;
    int burst_time;
    int waiting_time;
    int turnaround_time;
};

int main() {
    int n, total_waiting = 0, total_turnaround = 0;

    printf("Enter the number of processes: ");
    scanf("%d", &n);
    
    struct Process p[20];
    printf("Enter burst time for process ");

    for(int i = 0; i < n; i++) {
        p[i].id = i+1;
        scanf("%d", &p[i].burst_time);
    }

    for(int i = 0; i < n-1; i++) {
        for(int j = i+1; j < n; j++) {
            if(p[i].burst_time > p[j].burst_time) {
                struct Process temp = p[i];
                p[i] = p[j];
                p[j] = temp;
            }
        }
    }

    p[0].waiting_time = 0;
    p[0].turnaround_time = p[0].burst_time;

    for(int i = 1; i < n; i++) {
        p[i].waiting_time = p[i-1].waiting_time + p[i-1].burst_time;
        p[i].turnaround_time = p[i].waiting_time + p[i].burst_time;
    }

    for(int i = 0; i < n; i++) {
        total_waiting += p[i].waiting_time;
        total_turnaround += p[i].turnaround_time;
    }

    float avg_waiting = (float) total_waiting / n;
    float avg_turnaround = (float) total_turnaround / n;

    printf("Average waiting time: %.1f\\n", avg_waiting);
    printf("Average Turnaround time: %.1f\\n", avg_turnaround);

    return 0;
}
"""

@app.route('/rr')
def rr():
    return """#include <stdio.h>
#include <string.h>
#include <stdbool.h>

struct Process {
    char name[5];
    int arrival_time;
    int burst_time;
    int remaining_time;
    int waiting_time;
    int turnaround_time;
};

int main() {
    int n, time_quantum, time = 0, completed = 0;

    printf("Enter number of processes: ");
    scanf("%d", &n);

    struct Process p[20];

    printf("Enter time quantum: ");
    scanf("%d", &time_quantum);

    for (int i = 0; i < n; i++) {
        printf("Enter Process Name, Arrival Time and Burst Time: ");
        scanf("%s %d %d", p[i].name, &p[i].arrival_time, &p[i].burst_time);
        p[i].remaining_time = p[i].burst_time;
        p[i].waiting_time = 0;
        p[i].turnaround_time = 0;
    }

    // Round Robin Execution
    while (completed < n) {
        bool executed = false;
        for (int i = 0; i < n; i++) {
            if (p[i].arrival_time <= time && p[i].remaining_time > 0) {
                executed = true;
                if (p[i].remaining_time > time_quantum) {
                    time += time_quantum;
                    p[i].remaining_time -= time_quantum;
                } else {
                    time += p[i].remaining_time;
                    p[i].waiting_time = time - p[i].arrival_time - p[i].burst_time;
                    p[i].turnaround_time = time - p[i].arrival_time;
                    p[i].remaining_time = 0;
                    completed++;
                }
            }
        }
        if (!executed) time++;
    }
    
    // Output
    int total_wt = 0, total_tat = 0;
    printf("\nProcess\tAT\tBT\tWT\tTAT\n");
    for (int i = 0; i < n; i++) {
        printf("%s\t%d\t%d\t%d\t%d\n", p[i].name, p[i].arrival_time, p[i].burst_time,
               p[i].waiting_time, p[i].turnaround_time);
        total_wt += p[i].waiting_time;
        total_tat += p[i].turnaround_time;
    }

    printf("\nAverage Waiting Time: %.2f\n", (float) total_wt / n);
    printf("Average Turnaround Time: %.2f\n", (float) total_tat / n);

    return 0;
}
"""
@app.route('/pri')
def pri():
    return """#include <stdio.h>

// Define a structure for each process
struct Process {
    int id;
    int burst_time;
    int priority;
    int waiting_time;
    int turnaround_time;
};

int main() {
    int n, i, j;
    struct Process p[20], temp;
    int total_waiting_time = 0;
    int total_turnaround_time = 0;

    // Step 1: Get number of processes
    printf("Enter the number of processes: ");
    scanf("%d", &n);

    // Step 2: Read burst time and priority
    printf("Enter the burst time and priority (lower number = higher priority) for each process:\n");
    for(i = 0; i < n; i++) {
        p[i].id = i + 1;
        printf("Process %d Burst Time: ", i + 1);
        scanf("%d", &p[i].burst_time);
        printf("Process %d Priority: ", i + 1);
        scanf("%d", &p[i].priority);
    }

    // Step 3: Sort by priority (ascending order)
    for(i = 0; i < n - 1; i++) {
        for(j = i + 1; j < n; j++) {
            if(p[i].priority > p[j].priority) {
                temp = p[i];
                p[i] = p[j];
                p[j] = temp;
            }
        }
    }

    // Step 4: Calculate waiting and turnaround time
    p[0].waiting_time = 0;
    p[0].turnaround_time = p[0].burst_time;

    for(i = 1; i < n; i++) {
        p[i].waiting_time = p[i - 1].waiting_time + p[i - 1].burst_time;
        p[i].turnaround_time = p[i].waiting_time + p[i].burst_time;
    }

    // Step 5: Calculate totals
    for(i = 0; i < n; i++) {
        total_waiting_time += p[i].waiting_time;
        total_turnaround_time += p[i].turnaround_time;
    }

    // Step 6: Display results
    printf("\nProcess\tBurst Time\tPriority\tWaiting Time\tTurn Around Time\n");
    for(i = 0; i < n; i++) {
        printf("%d\t%d\t\t%d\t\t%d\t\t%d\n", p[i].id, p[i].burst_time, p[i].priority, p[i].waiting_time, p[i].turnaround_time);
    }

    printf("\nAverage Waiting Time: %.1f\n", (float)total_waiting_time / n);
    printf("Average Turn Around Time: %.1f\n", (float)total_turnaround_time / n);

    return 0;
}
"""
@app.route('/firstfit')
def firstfit():
    return """#include <stdio.h>

int main() {
    int memory_blocks[] = {100, 500, 200, 300, 600};
    int processes[] = {212, 417, 112, 426};
    int n_blocks = sizeof(memory_blocks) / sizeof(memory_blocks[0]);
    int n_processes = sizeof(processes) / sizeof(processes[0]);
    int allocation[n_processes];

    // Initialize all allocations to -1 (not allocated)
    for (int i = 0; i < n_processes; i++) {
        allocation[i] = -1;
    }

    // First Fit Allocation
    for (int i = 0; i < n_processes; i++) {
        for (int j = 0; j < n_blocks; j++) {
            if (memory_blocks[j] >= processes[i]) {
                allocation[i] = j + 1; // Block number (1-based index)
                memory_blocks[j] -= processes[i];
                break; // Move to next process
            }
        }
    }

    // Output
    printf("Process No.\tProcess Size\tBlock no.\n");
    for (int i = 0; i < n_processes; i++) {
        printf("%d\t\t%d\t\t", i + 1, processes[i]);
        if (allocation[i] != -1)
            printf("%d\n", allocation[i]);
        else
            printf("Not Allocated\n");
    }

    return 0;
}
"""
@app.route('/lru')
def lru():
    return """#include <stdio.h>

int findLRU(int time[], int n) {
    int i, minimum = time[0], pos = 0;
    for (i = 1; i < n; i++) {
        if (time[i] < minimum) {
            minimum = time[i];
            pos = i;
        }
    }
    return pos;
}

int main() {
    int frames[10], pages[30], time[10], n, f, i, j, page_faults = 0, counter = 0;

    printf("Enter number of pages: ");
    scanf("%d", &n);

    printf("Enter the page reference string:\n");
    for (i = 0; i < n; i++)
        scanf("%d", &pages[i]);

    printf("Enter number of frames: ");
    scanf("%d", &f);

    for (i = 0; i < f; i++) {
        frames[i] = -1;
        time[i] = 0;
    }

    for (i = 0; i < n; i++) {
        int found = 0;

        for (j = 0; j < f; j++) {
            if (frames[j] == pages[i]) {
                found = 1;
                counter++;
                time[j] = counter;
                break;
            }
        }

        if (!found) {
            int pos = -1;
            for (j = 0; j < f; j++) {
                if (frames[j] == -1) {
                    pos = j;
                    break;
                }
            }

            if (pos == -1)
                pos = findLRU(time, f);

            frames[pos] = pages[i];
            counter++;
            time[pos] = counter;
            page_faults++;
        }

        // Print current frame state
        printf("Frames: ");
        for (j = 0; j < f; j++) {
            if (frames[j] != -1)
                printf("%d ", frames[j]);
            else
                printf("- ");
        }
        printf("\n");
    }

    printf("Total Page Faults = %d\n", page_faults);
    return 0;
}
"""

@app.route('/fifo')
def ipc():
    return """#include <stdio.h>

int main() {
    int frames[10], pages[30], n, f, i, j, k, page_faults = 0;
    int index = 0;

    printf("Enter number of pages: ");
    scanf("%d", &n);

    printf("Enter the page reference string:\n");
    for (i = 0; i < n; i++)
        scanf("%d", &pages[i]);

    printf("Enter number of frames: ");
    scanf("%d", &f);

    for (i = 0; i < f; i++)
        frames[i] = -1;

    for (i = 0; i < n; i++) {
        int found = 0;

        // Check if page is already in frame
        for (j = 0; j < f; j++) {
            if (frames[j] == pages[i]) {
                found = 1;
                break;
            }
        }

        // Page fault
        if (!found) {
            frames[index] = pages[i];
            index = (index + 1) % f;
            page_faults++;
        }

        // Print current frame state
        printf("Frames: ");
        for (k = 0; k < f; k++) {
            if (frames[k] != -1)
                printf("%d ", frames[k]);
            else
                printf("- ");
        }
        printf("\n");
    }

    printf("Total Page Faults = %d\n", page_faults);
    return 0;
}
"""
@app.route('/optimal')
def sema():
    return """#include <stdio.h>

int predict(int pages[], int frames[], int n, int index, int f) {
    int i, j, farthest = index, res = -1;

    for (i = 0; i < f; i++) {
        for (j = index; j < n; j++) {
            if (frames[i] == pages[j]) {
                if (j > farthest) {
                    farthest = j;
                    res = i;
                }
                break;
            }
        }

        if (j == n)
            return i;
    }

    return (res == -1) ? 0 : res;
}

int main() {
    int frames[10], pages[30], n, f, i, j, page_faults = 0;

    printf("Enter number of pages: ");
    scanf("%d", &n);

    printf("Enter the page reference string:\n");
    for (i = 0; i < n; i++)
        scanf("%d", &pages[i]);

    printf("Enter number of frames: ");
    scanf("%d", &f);

    for (i = 0; i < f; i++)
        frames[i] = -1;

    for (i = 0; i < n; i++) {
        int found = 0;

        for (j = 0; j < f; j++) {
            if (frames[j] == pages[i]) {
                found = 1;
                break;
            }
        }

        if (!found) {
            int empty = -1;
            for (j = 0; j < f; j++) {
                if (frames[j] == -1) {
                    empty = j;
                    break;
                }
            }

            if (empty != -1)
                frames[empty] = pages[i];
            else
                frames[predict(pages, frames, n, i + 1, f)] = pages[i];

            page_faults++;
        }

        // Print current frame state
        printf("Frames: ");
        for (j = 0; j < f; j++) {
            if (frames[j] != -1)
                printf("%d ", frames[j]);
            else
                printf("- ");
        }
        printf("\n");
    }

    printf("Total Page Faults = %d\n", page_faults);
    return 0;
}
"""




if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Use PORT from environment or fallback to 10000
    app.run(host='0.0.0.0', port=port, debug=True)
