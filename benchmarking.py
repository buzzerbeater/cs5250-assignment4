from simulator import RR_scheduling, SJF_scheduling, write_output, read_input
import math

def benchmark():
	process_list = read_input()
	# RR
	min_waiting_time = math.inf
	min_quantum = 1

	for quantum in range(1, 11):
		print ("----RR with quantum = %d----" %quantum)
		schedule, average_waiting_time =  RR_scheduling(process_list,time_quantum = quantum)
		print('With quantum %d, the average waiting time is %.2f' %(quantum, average_waiting_time))
		#print("\n")
		write_output('output-RR-%d.txt' %(quantum), schedule, average_waiting_time)
		# update min_waiting_time and min_quantum
		if average_waiting_time < min_waiting_time:
		  min_waiting_time = average_waiting_time
		  min_quantum = quantum
	print('In RR, the minimum average waiting time is %.2f with quantum = %d' %(min_waiting_time, min_quantum))

	# SJF
	min_waiting_time = math.inf
	min_alpha = 0.1

	for i in range(1, 11):
		alpha = (float (i))/10
		print ("----SJF with alpha = %.2f----" %alpha)
		schedule, average_waiting_time =  SJF_scheduling(process_list, alpha = alpha)
		print('With alpha: %.2f, the average waiting time: %0.2f' %(alpha, average_waiting_time))
		#print("\n")
		write_output('output-SJF-%.2f.txt' %alpha, schedule, average_waiting_time)
		# update min_waiting_time and min_quantum
		if average_waiting_time < min_waiting_time:
		  min_waiting_time = average_waiting_time
		  min_alpha = alpha
	print('In SJF, the minimum average waiting time is %.2f with alpha = %.2f' %(min_waiting_time, min_alpha))
	
if __name__ == "__main__":
	benchmark()