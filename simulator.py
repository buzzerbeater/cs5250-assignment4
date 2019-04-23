'''
CS5250 Assignment 4, Scheduling policies simulator
Sample skeleton program
Input file:
    input.txt
Output files:
    FCFS.txt
    RR.txt
    SRTF.txt
    SJF.txt
'''
import sys
import queue as Q

input_file = 'input.txt'

class Process:
    last_scheduled_time = 0
    def __init__(self, id, arrive_time, burst_time):
        self.id = id
        self.arrive_time = arrive_time
        self.burst_time = burst_time
    #for printing purpose
    def __repr__(self):
        return ('[id %d : arrival_time %d,  burst_time %d]'%(self.id, self.arrive_time, self.burst_time))
    def __lt__(self, other):
        return (self.burst_time < other.burst_time)

def FCFS_scheduling(process_list):
    #store the (switching time, proccess_id) pair
    schedule = []
    current_time = 0
    waiting_time = 0
    for process in process_list:
        if(current_time < process.arrive_time):
            current_time = process.arrive_time
        schedule.append((current_time,process.id))
        waiting_time = waiting_time + (current_time - process.arrive_time)
        current_time = current_time + process.burst_time
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

#Input: process_list, time_quantum (Positive Integer)
#Output_1 : Schedule list contains pairs of (time_stamp, proccess_id) indicating the time switching to that proccess_id
#Output_2 : Average Waiting Time
def RR_scheduling(process_list, time_quantum):
    my_process_list = [Process(p.id, p.arrive_time, p.burst_time) for p in process_list]
    length = len(my_process_list)
    schedule = []
    process_queue = []
    current_time = 0
    waiting_time = 0
    process_queue = []
    process_queue.append(my_process_list.pop(0))
    
    while (len(process_queue) > 0 or len(my_process_list) >0 ):
        process = process_queue.pop(0)
        schedule.append((current_time,process.id))
        waiting_time = waiting_time + (current_time - process.arrive_time)
        if (process.burst_time <= time_quantum):
            current_time = current_time + process.burst_time
            while(len(my_process_list) >0 and my_process_list[0].arrive_time <= current_time):
                process_queue.append(my_process_list.pop(0))         
        else:
            process.burst_time = process.burst_time - time_quantum
            current_time = current_time + time_quantum
            process.arrive_time = current_time
            while(len(my_process_list) >0 and my_process_list[0].arrive_time <= current_time):
                process_queue.append(my_process_list.pop(0))
            process_queue.append(process)

        if(len(my_process_list) >0 and len(process_queue) == 0):
            process_queue.append(my_process_list.pop(0))
            current_time = process_queue[0].arrive_time

    average_waiting_time = waiting_time/float(length)
    return schedule, average_waiting_time

def SRTF_scheduling(process_list):
    my_process_list = [Process(p.id, p.arrive_time, p.burst_time) for p in process_list]
    length = len(my_process_list)
    process_queue = Q.PriorityQueue()
    schedule = []
    current_time = 0
    waiting_time = 0
    process_queue.put(my_process_list.pop(0))

    while (len(my_process_list) >0 or (not process_queue.empty())):
        process = process_queue.get()
        if(len(schedule) == 0):
            schedule.append((current_time,process.id))
        if(len(schedule)>0):
            if(not schedule[len(schedule)-1][1] == process.id):
                schedule.append((current_time,process.id))
        #schedule.append((current_time,process.id))
        waiting_time = waiting_time + (current_time - process.arrive_time)
        if (len(my_process_list) ==0 ):
            current_time = current_time + process.burst_time
        elif (process.burst_time + current_time <= my_process_list[0].arrive_time):
            current_time = current_time + process.burst_time
        else:
            process.burst_time = process.burst_time - (my_process_list[0].arrive_time - current_time)
            current_time = my_process_list[0].arrive_time
            process.arrive_time = current_time
            process_queue.put(process)
        while(len(my_process_list) >0 and my_process_list[0].arrive_time <= current_time):
                process_queue.put(my_process_list.pop(0))

        if(len(my_process_list) >0 and process_queue.empty()):
            temp = my_process_list.pop(0)
            process_queue.put(temp)
            current_time = temp.arrive_time

    average_waiting_time = waiting_time/float(length)
    return schedule, average_waiting_time

class MyProcess(Process):
    last_scheduled_time = 0
    estimated_burst_time = 0
    def __init__(self, id, arrive_time, burst_time):
        super().__init__(id, arrive_time, burst_time)
    #for printing purpose
    def __repr__(self):
        super().__repr__
    def __lt__(self, other):
        return (self.estimated_burst_time < other.estimated_burst_time)

def SJF_scheduling(process_list, alpha):
    my_process_list = [MyProcess(p.id, p.arrive_time, p.burst_time) for p in process_list]

    process_history = {}
    length = len(process_list)
    process_queue = Q.PriorityQueue()
    schedule = []
    current_time = 0
    waiting_time = 0

    process = my_process_list.pop(0)
    process_queue.put(process)
    process_history[process.id] = (process.burst_time, 5)

    while(len(my_process_list) > 0 or (not process_queue.empty())):
        process = process_queue.get()
        schedule.append((current_time,process.id))
        waiting_time = waiting_time + (current_time - process.arrive_time)
        current_time = current_time + process.burst_time
        while(len(my_process_list) >0 and my_process_list[0].arrive_time <= current_time):
            next_process = my_process_list.pop(0)
            if(process_history.get(next_process.id) == None):
                guess = 5
            else:
                last_burst, last_guess = process_history.get(next_process.id)
                guess = alpha * last_burst + (1 - alpha) * last_guess
                next_process.estimated_burst_time = guess
            process_history[next_process.id] = (next_process.burst_time, guess)
            process_queue.put(next_process)
        if(len(my_process_list) >0 and process_queue.empty()):
            next_process = my_process_list.pop(0)
            if(process_history.get(next_process.id) == None):
                guess = 5
            else:
                last_burst, last_guess = process_history.get(next_process.id)
                guess = alpha * last_burst + (1 - alpha) * last_guess
                next_process.estimated_burst_time = guess
            process_history[next_process.id] = (next_process.burst_time, guess)
            process_queue.put(next_process)
            current_time = next_process.arrive_time

    average_waiting_time = waiting_time/float(length)
    return schedule, average_waiting_time

def read_input():
    result = []
    with open(input_file) as f:
        for line in f:
            array = line.split()
            if (len(array)!= 3):
                print ("wrong input format")
                exit()
            result.append(Process(int(array[0]),int(array[1]),int(array[2])))
    return result

def write_output(file_name, schedule, avg_waiting_time):
    with open(file_name,'w') as f:
        for item in schedule:
            f.write(str(item) + '\n')
        f.write('average waiting time %.2f \n'%(avg_waiting_time))

def main(argv):
    process_list = read_input()
    print ("printing input ----")
    for process in process_list:
        print (process)
    print ("simulating FCFS ----")
    FCFS_schedule, FCFS_avg_waiting_time =  FCFS_scheduling(process_list)
    write_output('FCFS.txt', FCFS_schedule, FCFS_avg_waiting_time )
    print ("simulating RR ----")
    RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum = 2)
    write_output('RR.txt', RR_schedule, RR_avg_waiting_time )
    #process_list = read_input()
    print ("simulating SRTF ----")
    SRTF_schedule, SRTF_avg_waiting_time =  SRTF_scheduling(process_list)
    write_output('SRTF.txt', SRTF_schedule, SRTF_avg_waiting_time )
    #process_list = read_input()
    print ("simulating SJF ----")
    SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha = 0.5)
    write_output('SJF.txt', SJF_schedule, SJF_avg_waiting_time )

if __name__ == '__main__':
    main(sys.argv[1:])
