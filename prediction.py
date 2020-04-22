import math
import time
import logging
import math
import random
from multiprocessing import Queue
import Queue
import copy
import collections
import sys
import os
#import numpypy
import numpy as np
from numpy import mean
from collections import defaultdict
import pandas as pd
from sklearn.linear_model import LinearRegression
import microservices as usobj
import csv
from load_predictor import Predictor

tightSLA=float(1000)
looseSLA=float(2000)
sla_violations=0
SLA_TYPE=1
INITIAL_WORKERS = 10
VM_PREDICTION = 0
load_tracking = 0
MONITOR_INTERVAL = int(10000)
start_up_delay = int(1500)
type1_violations = 0
type2_violations = 0
last_task = 0
inception = 1000
resnet18 = 500
resnet50 = 800
resnet200 = 2500
caffenet = 700
squeezenet = 400
MODEL_SHARING = 0
def get_percentile(N, percent, key=lambda x:x):
    if not N:
        return 0
    k = (len(N) - 1) * percent
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return key(N[int(k)])
    d0 = key(N[int(f)]) * (c-k)
    d1 = key(N[int(c)]) * (k-f)
    return d0 + d1

def plot_cdf(values, filename):
    values.sort()
    f = open('filename', "w")
    for percent in range(100):
        fraction = percent / 100.
        f.write("%s\t%s\n" % (fraction, get_percentile(values, fraction)))
    f.close()

def lambda_cost(num, mem, time):
    return float(num*0.0000002 + (num*mem*time*0.00001667))

class JobStage(object):
    def __init__(self, ID, name):
        #self.simulation = simulation;
        #self.current_time = current_time
        #self.workers = []
	self.name = name
	self.id = ID
	#self.simulation = simulation
        #self.num_workers= num_workers
	#self.free_slots= num_workers
        #self.queued_tasks = Queue.PriorityQueue()
	self.sla=0
	self.completed = False



class Stage(object):
    def __init__(self, num_workers,ID,simulation):
        #self.simulation = simulation;
        #self.current_time = current_time
        self.workers = []
	self.id = ID
	self.simulation = simulation
        self.num_workers= num_workers
	self.free_slots= num_workers
        self.queued_tasks = Queue.PriorityQueue()
	self.queuing_delay = []
	self.jobs = []
        self.slack_tasks = Queue.PriorityQueue()
	self.sla=0
	self.slack = 0
    def execute_task(self, current_time):
    	global sla_violations,type1_violations, type2_violations
        new_event = []
	stage_id = self.id
        #if not self.queued_tasks.empty():
	if len(self.jobs) > 0:
            (queue_time,job_id) = self.queued_tasks.get()
	    print ("before sorting joblength freeslots", len(self.jobs),self.free_slots)
	    #print ("before sorting", self.queued_tasks.qsize())
	    #self.jobs.sort(key=lambda Job:Job.start_time,reverse=False)
	    if slack_aware == 0:
		self.jobs.sort(key=lambda Job:Job.start_time,reverse=False)
	    elif slack_aware == 1:
		self.jobs.sort(key=lambda Job:Job.slack,reverse=False)
	    job_id = self.jobs[0]
	    #print ("executing for job stageid job id arrivaltime",self.id,job_id.id, job_id.start_time, len(self.jobs))
	    del self.jobs[0]
            for i in range(len(job_id.stages)):
	        if stage_id == job_id.stages[i].id:
    		    #print("stageid, loop, stageidinjob jobstagelength, jobtasklength",stage_id,i,job_id.stages[i].id, len(job_id.stages),len(job_id.tasks))
		    task = job_id.tasks[i]
                    task.exec_time = float(usobj.microservices[job_id.stages[i].name].get_service_time())
		    #self.sla = task.exec_time
		    current_stage = i

            if self.free_slots > 0:
		#if (stage_id != 0) and (self.simulation.tasks[task.jobid].stage_finished[stage_id-1]=='False'):
		#    print("previous stage not completed for job", task.jobid,stage_id, self.simulation.tasks[task.jobid].stage_finished)
		#    return [(current_time + 5, ExecuteStage(self.simulation, task, stage_id))]
	        for Worker in self.workers:
		    if (not Worker.spin_up) and Worker.isIdle:
			Worker.isIdle = False
			task.worker = Worker
		task_id = task.id
        	self.isIdle = False
		self.free_slots -=1
		print("**********after deleting length",len(self.jobs))
                #print("executing task in lambda", task.jobid,task.stage_id, task.exec_time, current_time)
		task.start_time = current_time
                task_duration = task.exec_time
                probe_response_time = 5 + current_time
		self.queuing_delay.append(float(task.start_time - task.arrival_time))
        	if task_duration > 0:
            	        task_end_time = task_duration + probe_response_time
			task.end_time = task_end_time
			job_id.slack -= float(task_end_time - job_id.start_time)
			event = (StageTaskEndEvent(self,task.stage_id,Worker))
			new_event.append((task_end_time,event))
			#self.free_slots(task_end_time, task.stage_id)
            		if current_stage < (len(job_id.stages)-1):
			    job_id.stages[current_stage].completed=True
			    #print("stages not yet complete at time",task.stage_id,task_end_time, current_stage, job_id.stages[current_stage+1])
                	    new_event.append((task_end_time, ExecuteStage(self.simulation, job_id, job_id.stages, job_id.stages[current_stage+1].id)))


                	    print >> tasks_file,"task_id ,", task.jobid,job_id.id,stage_id, ",", "task_type," ,task.task_type,  ",",  "lambda task" , ",task_end_time ,", task_end_time, ",", "task_start_time,",task.start_time, ",", "task_arrival_time,",task.arrival_time, ",", " each_task_running_time,",(task_end_time - task.start_time),",", " task_queuing_time:,", (task.start_time - task.arrival_time)
            		else:
#        if(self.simulation.add_task_completion_time(task_id,
 #           task_end_time,1)):
		            sla = float(task_end_time) - float(self.simulation.tasks[task.jobid].start_time)
			    if SLA_TYPE == 1:
		    		required_sla = float(tightSLA)
		            else:
				required_sla = float(looseSLA)
			    #print("sla is ", sla,required_sla,tightSLA,looseSLA)
			    if sla > required_sla:
				sla_violations+=1
				if job_id.job_type == 0:
				    type1_violations+=1
				else:
				    type2_violations+=1
	    		    job_id.end_time = task_end_time
			    self.simulation.completed_tasks+=1
	                    print >> tasks_file,"task_id ,", task.jobid,job_id.id,stage_id, ",", "task_type," ,task.task_type,  ",",  "lambda task" , ",task_end_time ,", task_end_time, ",", "task_start_time,",task.start_time, ",", "task_arrival_time,",task.arrival_time, ",", "each_task_running_time,",(task_end_time - task.start_time),",", " task_queuing_time:,", (task.start_time - task.arrival_time)
            		    print >> finished_file,"job_id", task.jobid, "job_type", job_id.job_type ,"task_end_time, ", task_end_time,",", "task_start_time,",job_id.start_time,",", " job_running_time, ",(job_id.end_time -job_id.start_time)
	      		    event = (StageTaskEndEvent(self,task.stage_id, Worker))
			    new_event.append((task_end_time,event))

                	    new_event.append((task_end_time,TaskEndEvent(self)))
                	    return new_event
	    else:
		#print("stage workers are busy",task.jobid,task.stage_id)
		#self.simulation.tasks[task.jobid].stage_lastTime[current_stage]=current_time
		new_event.append((current_time+100, ExecuteStage(self.simulation, job_id, job_id.stages, self.id)))
        #print("returning", new_event)
        return new_event
    def update_free_slots(self, current_time):
	#self.stage_id = stage_id
	#print("updating free slots for stage", self.id, self.free_slots,self.num_workers)

	if self.free_slots < self.num_workers:
            self.free_slots += 1
	    #print("updated free slots for stage", self.id, self.free_slots,self.num_workers)
	return []
    def free_slot(self, current_time):
        #self.free_slots += 1
        #get_task_events = self.get_task(current_time)
        return []




class TaskEndEvent:

    def __init__(self, worker):
        self.worker = worker

    def run(self, current_time):
        #print "task end event"
        return self.worker.free_slot(current_time)
class StageTaskEndEvent:

    def __init__(self, worker,stage_id, Worker):
        self.worker = worker
	self.stage_id = stage_id
	self.Worker = Worker
    def run(self, current_time):
        #print "task end event"

	self.Worker.lastIdleTime = current_time
	self.Worker.isIdle = True
        return self.worker.update_free_slots(current_time)

class Lambda(object):
    def __init__(
            self,
            simulation,
            current_time,
            up_time,
	    spin_up,
            task_type,
            exec_time
            ):
        self.simulation = simulation
        self.start_time = current_time
	self.lastIdleTime = current_time
        self.spin_up = spin_up
        self.isIdle = True
        self.up_time = up_time
        if task_type == 0:
            self.exec_time = float(400)
            self.mem = float(2024)
        if task_type == 1:
            self.exec_time = float(400)
            self.mem = float(3024)
        if task_type == 2:
            self.exec_time = float(950)
            self.mem = float(3048)
        self.exec_time = exec_time
    def lambda_status(self, current_time):
        if (not self.isIdle):
            #self.isIdle = True
            #self.lastIdleTime = current_time
            return False
        return True

    def execute_task(self,task, current_time, stage_id):
	global sla_violations
        task_id = task.id
        #print("executing task in lambda", task_id, task.exec_time)
        self.isIdle = False
        task_duration = task.exec_time
        probe_response_time = 5 + current_time
        new_event = []
        if task_duration > 0:
            task_end_time = task_duration + probe_response_time + self.up_time
            if stage_id < (len(self.simulation.stages)-1):
		#print("stages not yet complete")
                new_event.append((task_end_time, ExecuteStage(self.simulation, task, stage_id+1)))


                #print >> tasks_file,"task_id ,", task.jobid,stage_id, ",", "task_type," ,task.task_type,  ",",  "lambda task" , ",task_end_time ,", task_end_time, ",", "task_start_time,",task.start_time, ",", " each_task_running_time,",(task_end_time - task.start_time),",", " task_queuing_time:,", (task_end_time - task.start_time) - task.exec_time
            else:
#        if(self.simulation.add_task_completion_time(task_id,
 #           task_end_time,1)):
		self.simulation.tasks[task.jobid].end_time = task_end_time
                print >> tasks_file,"task_id ,", task.jobid,stage_id, ",", "task_type," ,task.task_type,  ",",  "lambda task" , ",task_end_time ,", task_end_time, ",", "task_start_time,",task.start_time, ",", " each_task_running_time,",(task_end_time - task.start_time),",", " task_queuing_time:,", (task_end_time - task.start_time) - task.exec_time
                print >> finished_file,"job_id", task.jobid, "task_end_time, ", task_end_time,",", "task_start_time,",self.simulation.tasks[task.jobid].start_time,",", " each_task_running_time, ",(self.simulation.tasks[task.jobid].end_time - self.simulation.tasks[task.jobid].start_time)
		sla = float(self.simulation.tasks[task.jobid].end_time - self.simulation.tasks[task.jobid].start_time)
		if SLA_TYPE == 1:
			required_sla = float(tightSLA)
		else:
			required_sla = float(looseSLA)
		if sla > required_sla:
			sla_violations+=1
                new_event = TaskEndEvent(self)
                return [(task_end_time, new_event)]
        #print("returning", new_event)
        return new_event

    def execute_queue_task(self,Task, current_time, stage_id):
        #print("running task on worker",self.id,self.task_type)
 	global sla_violations
        new_event = []
        if not self.simulation.stages[stage_id].queued_tasks.empty():
            (queue_time,task) = self.simulation.stages[stage_id].queued_tasks.get()
            if self.simulation.stages[stage_id].free_slots > 0:
		if (stage_id != 0) and (self.simulation.tasks[task.jobid].stage_finished[stage_id-1]=='False'):
		    #print("previous stage not completed for job", task.jobid,stage_id)#self.simulation.tasks[task.jobid].stage_finished)
		    return [(current_time + 5, ExecuteStage(self.simulation, task, stage_id))]
	        task_id = task.id

		self.isIdle = False
		self.simulation.stages[stage_id].free_slots -=1
                #print("executing task in lambda", task.jobid,task.stage_id, task.exec_time,current_time)
		task.start_time = current_time
                task_duration = task.exec_time
                probe_response_time = 5 + current_time
        	if task_duration > 0:
            	        task_end_time = task_duration + probe_response_time
			task.end_time = task_end_time
			event = (StageTaskEndEvent(self,task.stage_id, self))
			new_event.append((task_end_time,event))
			#self.free_slots(task_end_time, task.stage_id)
            		if stage_id < (len(self.simulation.stages)-1):
			    self.simulation.tasks[task.jobid].stage_finished[stage_id]='True'
			    #print("stages not yet complete at time",task.stage_id,task_end_time, self.simulation.tasks[task.jobid].stage_finished)
                	    #new_event.append((task_end_time, ExecuteStage(self.simulation, task, stage_id+1)))


                	    print >> tasks_file,"task_id ,", task.jobid,stage_id, ",", "task_type," ,task.task_type,  ",",  "lambda task" , ",task_end_time ,", task_end_time, ",", "task_start_time,",task.start_time, ",", "task_arrival_time,",task.arrival_time, ",", " each_task_running_time,",(task_end_time - task.start_time),",", " task_queuing_time:,", (task.start_time - task.arrival_time)
            		else:
#        if(self.simulation.add_task_completion_time(task_id,
 #           task_end_time,1)):
		            sla = float(task_end_time) - float(self.simulation.tasks[task.jobid].start_time)
			    if SLA_TYPE == 1:
		    		required_sla = float(tightSLA)
		            else:
				required_sla = float(looseSLA)
			    #print("sla is ", sla,required_sla,tightSLA,looseSLA)
			    if sla > required_sla:
				sla_violations+=1
	    		    self.simulation.tasks[task.jobid].end_time = task_end_time
			    self.simulation.completed_tasks+=1
	                    print >> tasks_file,"task_id ,", task.jobid,stage_id, ",", "task_type," ,task.task_type,  ",",  "lambda task" , ",task_end_time ,", task_end_time, ",", "task_start_time,",task.start_time, ",", "task_arrival_time,",task.arrival_time, ",", "each_task_running_time,",(task_end_time - task.start_time),",", " task_queuing_time:,", (task.start_time - task.arrival_time)
            		    print >> finished_file,"job_id", task.jobid, "task_end_time, ", task_end_time,",", "task_start_time,",self.simulation.tasks[task.jobid].start_time,",", " each_task_running_time, ",(self.simulation.tasks[task.jobid].end_time - self.simulation.tasks[task.jobid].start_time)

                	    new_event.append((task_end_time,TaskEndEvent(self)))
                	    return new_event
	    else:
		#print("stage workers are busy",task.jobid,task.stage_id)
		self.simulation.tasks[task.jobid].stage_lastTime[stage_id]=current_time
		new_event.append((current_time+5, ExecuteStage(self.simulation, task, stage_id)))
        #print("returning", new_event)
        return new_event

    def free_slots(self, current_time, stage_id):
	self.stage_id = stage_id
	#print("updating free slots for stage", stage_id, self.simulation.stages[self.stage_id].free_slots,self.simulation.stages[self.stage_id].num_workers)
	if self.simulation.stages[self.stage_id].free_slots < self.simulation.stages[self.stage_id].num_workers:
            self.simulation.stages[self.stage_id].free_slots += 1
	    #print("updated free slots for stage", stage_id, self.simulation.stages[self.stage_id].free_slots,self.simulation.stages[self.stage_id].num_workers)
	return []
        #get_task_events = self.get_task(current_time)

    def free_slot(self, current_time):
        #self.free_slots += 1
        #get_task_events = self.get_task(current_time)
        return []



class VM(object):

    vm_count = 1

    def __init__(
            self,
            simulation,
            current_time,
            up_time,
            task_type,
            vcpu,
            vmem,
            price,
            spin_up,
            id):
        self.simulation = simulation
        self.start_time = current_time
        self.up_time = up_time
        self.end_time = current_time
        self.vcpu = vcpu
        self.vmem = vmem
        self.queued_tasks = Queue.PriorityQueue()
        self.id = id
        self.isIdle = True
        self.lastIdleTime = current_time
        self.price = price
        self.task_type = task_type
        self.spin_up = spin_up
        #print("adding worker id and type",self.id,self.task_type)
        if task_type == 0:
            self.free_slots = 6
            self.max_slots = 6
        if task_type == 1:
            self.free_slots = 5
            self.max_slots = 5
        if task_type == 2:
            self.free_slots = 2
            self.max_slots = 2
        self.num_queued_tasks = 0

    def add_task(self, task_id, current_time):
        #print("adding new task to VM", task_id,self.id)
        self.queued_tasks.put((current_time,task_id))
        self.isIdle = False
        new_events = self.get_task(current_time)
        self.spin_up = False
        # self.probes_repliid_to_immediately += len(new_events)
        # logging.getLogger("sim").debug("Worker %s: %s" %(self.id, self.probes_replied_to_immediately))

        return new_events

    def VM_status(self, current_time):
        if (not self.isIdle and (self.num_queued_tasks == 0)):
            self.isIdle = True
            self.lastIdleTime = current_time
            return True
        return False
    def get_task(self, current_time):
        new_events = []
        #print("running task on worker",self.id,self.task_type)
        if not self.queued_tasks.empty():
            #print "task queued", self.num_queued_tasks, self.queued_tasks.qsize()
            #print("worker not empty at time",self.id,self.task_type,current_time)
            if(self.free_slots == 0):

                #print self.id," task queued delay", self.num_queued_tasks
                (queue_time,task_id) = self.queued_tasks.get()
                #print current_time + self.simulation.tasks[task_id].exec_time + 10, self.simulation.tasks[task_id].start_time
                new_events.append((current_time + self.simulation.tasks[task_id].exec_time + 10,ScheduleVMEvent(self,task_id)))
                return new_events

            #print self.id,self.num_queued_tasks,self.free_slots,"executing task"
            self.free_slots -= 1
            self.num_queued_tasks -= 1
            (queue_time,task_id) = self.queued_tasks.get()
            task_duration = self.simulation.tasks[task_id].exec_time
            probe_response_time = 5 + current_time
            if task_duration > 0:
                task_end_time = task_duration + probe_response_time
                #print("worker not empty at time",self.id,self.task_type,task_end_time)
                new_event = TaskEndEvent(self)
                task = self.simulation.tasks[task_id]
                #if task.id >=15548:
                 #   print ("task id ", task.id, "task type" , "VM id" , self.id, task.task_type, "task_end_time ", task_end_time, "task_start_time:",task.start_time, " each_task_running_time: ",(task_end_time - task.start_time))
                print >> tasks_file,"task_id ,", task.id,",",  "task_type," ,task.task_type, ",", "VM_id," , self.id ,",", "task_end_time ,", task_end_time, ",", "task_start_time,",task.start_time, ",", " each_task_running_time,",(task_end_time - task.start_time), ",", " task_queuing_time:,", (task_end_time - task.start_time) - task.exec_time
                if(self.simulation.add_task_completion_time(task_id,
                    task_end_time,0)):
                    #print "writing to file"
                    print >> finished_file,"num tasks ", task.num_tasks, "," ,"VM_tasks ,", task.vm_tasks,"lambda_tasks ,", task.lambda_tasks , "task_end_time, ", task_end_time, "task_start_time,",task.start_time, " each_task_running_time ,",(task.end_time - task.start_time)
                return [(task_end_time, new_event)]
        return []

    def free_slot(self, current_time):
        self.free_slots += 1
        #get_task_events = self.get_task(current_time)
        return []


class JobArrival:
    task_count=0
    def __init__(
            self,
            start_time,
	    num_tasks,
	    job_type
            ):
        self.id = int(JobArrival.task_count)
        JobArrival.task_count += 1
        self.start_time = start_time
        self.num_tasks = num_tasks
	self.job_type = job_type
	#print("jobtype",self.job_type)
	self.jobs = []

class Job(object):

    task_count = 0

    def __init__(
            self,
            start_time,
            task_type,
	    num_tasks,
	    job_type,
	    stages,
	    stageids,
	    simulation
            ):
        self.id = int(Job.task_count)
	self.job_type = task_type
        Job.task_count += 1
        self.start_time = start_time
        self.num_tasks = num_tasks
	self.tasks=[]
        self.task_type = task_type
 	self.stage_finished =['False','False','False']
	self.stage_lastTime = [0,0,0]
        self.end_time = start_time
        self.completed_tasks = 0
	self.chains = stages
	self.total_time = 0
	self.stages = []
	self.simulation = simulation
	self.slack = 0
	for i in range(len(self.chains)):
	    self.stages.append(JobStage(stageids[i], self.chains[i]))
        self.lambda_tasks = 0
        self.exec_time = 0
	stages = []

	#if self.job_type == 0:
	#    stages.append()
	#else self.job_type == 1:
	#    stages = []
	for i in range(self.num_tasks):
            self.tasks.append(Task(start_time, self.task_type,self.id, stages))
	    self.total_time += float(usobj.microservices[self.stages[i].name].get_service_time())
	    self.simulation.stages[stageids[i]].sla = float(usobj.microservices[self.stages[i].name].get_service_time())
	self.slack = float(tightSLA - self.total_time)
	for i in range(self.num_tasks):
	    self.simulation.stages[stageids[i]].slack = float(self.simulation.stages[stageids[i]].sla/self.total_time * float(tightSLA))
	    #print("stage_slack is", self.simulation.stages[stageids[i]].slack, float(self.simulation.stages[stageids[i]].sla/self.total_time),float(tightSLA))
        #print("slack for job is",self.start_time,self.id, self.slack)
    def task_completed(self, completion_time):
        self.completed_tasks += 1
        self.end_time = max(completion_time, self.end_time)
        assert self.completed_tasks <= self.num_tasks
        return self.num_tasks == self.completed_tasks


class Task(object):

    task_count = 0

    def __init__(
            self,
            start_time,
            task_type,
            jobid,
	    stages
            ):
        self.id = int(Task.task_count)
        Task.task_count += 1
        self.start_time = start_time
	self.arrival_time = start_time
        self.jobid = jobid
	self.stage_id = 0
        self.stages = stages
        self.task_type = task_type
        self.end_time = start_time
        self.completed_tasks = 0
        self.lambda_tasks = 0
        self.vm_tasks = 0
	self.worker = None
        if task_type == 0:
            self.exec_time = 400
            self.mem = 1024
        if task_type == 1:
            self.exec_time = 400
            self.mem = 2024
        if task_type == 2:
            self.exec_time = 950
            self.mem = 3048
        self.exec_time = 0
  #  def task_completed(self, completion_time):
  #      self.completed_tasks += 1
  #      self.end_time = max(completion_time, self.end_time)
  #      assert self.completed_tasks <= self.num_tasks
  #      return self.num_tasks == self.completed_tasks


class Event(object):

    """ Abstract class representing events. """

    def __init__(self):
        raise NotImplementedError('Event is an abstract class and cannot be instantiated directly'
                )

    def run(self, current_time):
        """ Returns any events that should be added to the queue. """

        raise NotImplementedError('The run() method must be implemented by each class subclassing Event'
                )

class ExecuteStage(Event):
    def __init__ (self, simulation, job_id,stage_id, stage):
        self.job_id = job_id
        self.simulation=simulation
        self.stage_id = stage_id
	self.stage = stage
        #self.job_id.exec_time = float(usobj.microservices[chains[stage_id]].get_service_time())
        #self.job_id.stage_id = self.stage_id
    def run(self, current_time):
        #self.job_id.start_time = float(current_time)
	if schedule_type == 1:
            #print("executing stage for",self.job_id, self.job_id.jobid,"AT stage",self.stage_id)
	    if (len(self.simulation.stages[self.stage_id].workers)%20) == 0:
		print("cold start")
                self.simulation.stages[self.stage_id].workers.append(Lambda(self.simulation,current_time, 1850, True, 0, self.job_id.exec_time))
                self.simulation.stages[self.stage_id].workers.append(Lambda(self.simulation,current_time, 1850, True, 0, self.job_id.exec_time))

	    else:
                self.simulation.stages[self.stage_id].workers.append(Lambda(self.simulation,current_time, 1500, True, 0, self.job_id.exec_time))
            return self.simulation.stages[self.stage_id].workers[-1].execute_task(self.job_id,current_time, self.stage_id)
        elif schedule_type == 2:
	    #print(len(self.simulation.stages),self.stage, self.job_id.stages[0].id,self.job_id.stages[1].id)
            #print("executing stage for",self.job_id, self.job_id.id,"AT stage",self.stage_id, self.simulation.stages[self.stage], self.stage, self.simulation.stages)
	    self.simulation.stages[self.stage].queued_tasks.put((current_time,self.job_id))
	    self.simulation.stages[self.stage].jobs.append(self.job_id)
	    #print len(self.simulation.stages[self.stage].jobs),"adding jobs"
	    self.simulation.stages[self.stage].slack_tasks.put((self.job_id.slack,self.job_id))
	    #print(self.simulation.stages[self.stage].queued_tasks.qsize())
#            return self.simulation.stages[self.stage_id].workers[0].execute_queue_task(self.job_id,current_time, self.stage_id)
            return self.simulation.stages[self.stage].execute_task(current_time)

class ScheduleStagesEvent(Event):

    def __init__(self, simulation, job_id):
        self.simulation = simulation
        self.job_id = job_id
        self.num_stages = len(self.simulation.stages)
        self.stages= self.simulation.stages

    def run(self, current_time):
        logging.getLogger('sim'
                ).debug('Probe for job %s arrived at %s'
                        % (self.job_id,
                            current_time))
	self.job_id.arrival_time = current_time
        return self.execute_stage(self.job_id, current_time)
    def execute_stage(self,job_id, current_time):
	#print("executine stages\n",job_id)
        self.job_id = job_id
        new_events = []
	self.sched_time = current_time
	new_events.append((current_time, ExecuteStage(self.simulation,self.job_id,self.job_id.stages, self.job_id.stages[0].id)))
	#for i in range(self.num_stages):
        """self.job_id.tasks[i].exec_time = float(usobj.microservices[chains[self.job_id.job_type][i]].get_service_time())
	self.stages[i].sla = self.job_id.tasks[i].exec_time
        self.job_id.tasks[i].stage_id = i
	self.job_id.tasks[i].arrival_time = current_time
	print("calling stage",i,self.sched_time, self.job_id.tasks[i].exec_time, self.sched_time+self.job_id.tasks[i-1].exec_time)
	if i!=0:
        new_events.append((self.sched_time, ExecuteStage(self.simulation,self.job_id.tasks[i], i)))
	else:
		new_events.append((current_time, ExecuteStage(self.simulation,self.job_id.tasks[i], i)))
	    self.sched_time += self.job_id.tasks[i].exec_time
        #new_events.append((current_time + self.simulation.tasks[task_id].exec_time + 10,ScheduleVMEvent(self,task_id)))
        print("Aft schedule stage",new_events)"""
        return new_events

class TaskArrival(Event):
    """ Event to signify a job arriving at a scheduler. """
    def __init__(
            self,
            simulation,
            interarrival_delay,
            task_type,
            num_tasks
            ):
        self.simulation = simulation
        self.interarrival_delay = float(interarrival_delay)
        self.num_tasks = int(num_tasks)
        self.task_type = int(task_type)

        # self.task_distribution= task_distribution

    def run(self, current_time):
        global last_task
        #task = Task(current_time, self.task_type,self.num_tasks)
	if self.task_type == 0:
	    chainids = [0,1,2,3]
            task = Job(current_time, self.task_type,self.num_tasks,0, chains[0], chainids, self.simulation)
            logging.getLogger('sim').debug('Job %s arrived at %s'
                % (task.id, current_time))
        if self.task_type == 1:
	    chainids = [4,5,3]
            task = Job(current_time, self.task_type,self.num_tasks,0, chains[1], chainids, self.simulation)
            logging.getLogger('sim').debug('Job %s arrived at %s'
                % (task.id, current_time))


        # Schedu1le job.

        new_events = self.simulation.send_tasks(task, current_time)

        # Add new Job Arrival event, for the next job to arrive after this one.

        arrival_delay = random.expovariate(1.0
                / self.interarrival_delay)

        # new_events.append((current_time + arrival_delay, self))
        #print("adding self task arriva",new_events)

        logging.getLogger('sim').debug('Retuning %s events'
                % len(new_events))
        line = self.simulation.tasks_file.readline()
        #print line
        if line == '':
            print('task empty')
            last_task = 1
            return new_events
        #task_type = float(line.split(',')[2])
        #end_time = float(line.split(',')[3])/1000
        #start_time = line.split(',')[5]
        arrival_time = float(line.split(',')[0])
	num_tasks = float(line.split(',')[3])
	num_tasks2 = float(line.split(',')[4])
        #waiting_time = line.split(',')[9]
        #print(arrival_time,start_time,end_time,waiting_time,task_type)
        self.simulation.task_arrival.append([int(arrival_time), num_tasks])
        while num_tasks > 0:
 	    new_events.append((arrival_time * 1000, TaskArrival(self.simulation, arrival_time,0,len(chains[0]))))
	    num_tasks-=1
        while num_tasks2 > 0:
 	    new_events.append((arrival_time * 1000, TaskArrival(self.simulation, arrival_time,1,len(chains[1]))))
	    num_tasks2-=1
        #print("Aft task arrival",new_events)
        return new_events



       #start_time = float(line.split(',')[0])
        #num_tasks = line.split(',')[3]
        #task_type = line.split(',')[2]

        #print "adding new task",int(start_time*1000), num_tasks, task_type
        # new_task = Task(self, line, 1000, start_time, num_tasks, task_type)

        #new_events.append((start_time * 1000,
            #TaskArrival(self.simulation, arrival_time ,task_type)))
        #print ("task arrival new events", new_events)
        return new_events

class lambdaCreateEvent(Event):
    def __init__(self,simulation, VM,stage):
        self.simulation = simulation
        self.worker = VM
	self.stage = stage
        #self.task_type = task_type
    def run(self, current_time):
        #self.VMs[self.task_type].append(VM(self.simulation,current_time,60000,self.task_type,4,8192,0.10,True,len(self.VMs[self.task_type])))
        print current_time, " spin up compeleted for VM", self.worker,len(self.simulation.stages[self.stage].workers),self.simulation.stages[self.stage].num_workers
        self.worker.spin_up = False
	self.simulation.stages[self.stage].num_workers+=1
	self.simulation.stages[self.stage].free_slots+=1
        #for i in range(len(self.simulation.stages)):
            #print >> f, i,len(self.simulation.stages[i].workers), ",",self.worker.start_time

        new_events = []
        return new_events

class lambda_Monitor_Event(Event):
    def __init__(self, simulation):
        self.simulation = simulation
    def run(self, current_time):
        new_events = []
        global last_task
        print(current_time, "lambda_monito_EVENT",)
        for index in range(len(self.simulation.stages)):
            width = self.simulation.stages[index].num_workers
            k=0
            #print( len(self.simulation.VMs[index]), len(self.simulation.completed_VMs[index]))
            while k < width:
                if (not self.simulation.stages[index].workers[k].spin_up):
                    if(self.simulation.stages[index].workers[k].isIdle):
                        if ((current_time - self.simulation.stages[index].workers[k].lastIdleTime) > 1200000):
                        #if(current_time - self.simulation.VMs[index][k].start_time >=3600000):
                            self.simulation.completed_lambdas.setdefault(index,[]).append(self.simulation.stages[index].workers[k])
                            self.simulation.stages[index].workers[k].end_time = current_time
                            #print >> f, self.simulation.VMs[index][k].id, ",",self.simulation.VMs[index][k].end_time,",", self.simulation.VMs[index][k].start_time,",", self.simulation.VMs[index][k].lastIdleTime
                            del self.simulation.stages[index].workers[k]
			    self.simulation.stages[index].free_slots-=1
			    self.simulation.stages[index].num_workers-=1
                            print index, len(self.simulation.stages[index].workers),"width changing"
                        width-=1
                k+=1
        if(self.simulation.event_queue.qsize() > 1):
            new_events.append((current_time+180000,lambda_Monitor_Event(self.simulation)))
        return new_events

class PeriodicTimerEvent(Event):
    def __init__(self,simulation):
        self.simulation= simulation
        self.f = open(VM_stats_path,'w')

    def run(self, current_time):
        new_events = []
	print ("+++++++++++++++++periodic timer event","+++++++++++++++")
        global last_task
	global sla_violations, SLA_TYPE, queue_aware
	Max = float(0)
	if SLA_TYPE == 1:
	    sla = tightSLA
	bottleneck = -1
	average = 0

	if(PREDICTION == 1):
                print("PREDICTION",len(self.simulation.task_arrival))
                             #load= random.randint(200,400)
                #print(load,len(forecasts))
                #print("*****", forecasts)
		df = pd.DataFrame((self.simulation.task_arrival),columns=['time','req'])
		wtr = csv.writer(open ('predictions.csv', 'w'), delimiter=',', lineterminator='\n')
		Times = 1.5
                train = df[-60:]
		#print train
                X = train.time.tolist()
                y = train.req.tolist()
		load = max(y)
                forecasts = predictor.predict(load * Times)
		print("forecasts", load, max(forecasts))
		for i in range(len(self.simulation.stages)):
	            stage_limit = int(1000/self.simulation.stages[i].sla)
		    average = float(sum(self.simulation.stages[i].queuing_delay[-100:]) / len(self.simulation.stages[i].queuing_delay[-100:]))
		    #average = max(self.simulation.stages[i].queuing_delay[-100:])
	            print("stage queuing delays", average)
	            lambdas_needed = float(max(forecasts)) - (stage_limit * len(self.simulation.stages[i].workers))
                    lambdas_needed = int(lambdas_needed/stage_limit)
	            print (current_time,"+++++++++++++++++periodic timer event",current_time, stage_limit,"lambdas_needed",lambdas_needed,("added tasks,",len(self.simulation.tasks),"stage sla,",self.simulation.stages[i].sla, "numtasks run,",stage_limit),"self.simulation.stages[i].num_workers",len(self.simulation.stages[i].workers),i,"+++++++++++++++")

	            if lambdas_needed > 0:
	                print ("adding workers ***********periodic timer event","lambdas_needed",lambdas_needed,"self.simulation.stages[i].num_workers",self.simulation.stages[i].num_workers,i,"+++++++++++++++")
	                for j in range(int(math.ceil(lambdas_needed))):
	                    self.simulation.stages[i].workers.append(Lambda(self.simulation, 0, 1000, True, 0, 0))
		            if MODEL_SHARING == 1:
	                        new_events.append((float(current_time + 500), lambdaCreateEvent(self.simulation, self.simulation.stages[i].workers[-1], i)))
	                    new_events.append((float(current_time + 1850), lambdaCreateEvent(self.simulation, self.simulation.stages[i].workers[-1], i)))
		    if average > float(sla):
			print("adding for queue_delay",i,len(self.simulation.stages[i].workers),average, lambdas_needed,float(self.simulation.stages[i].slack))
			if lambdas_needed <=0:
	 		    for j in range(2):
	                        self.simulation.stages[i].workers.append(Lambda(self.simulation, 0, 1000, True, 0, 0))
		                if MODEL_SHARING == 1:
	                            new_events.append((float(current_time + 500), lambdaCreateEvent(self.simulation, self.simulation.stages[i].workers[-1], i)))
	                        new_events.append((float(current_time + 1850), lambdaCreateEvent(self.simulation, self.simulation.stages[i].workers[-1], i)))

		    print >> self.f, "current_time,", current_time, ",",len(self.simulation.stages[i].workers), ",", i

	if queue_aware == 1:
	    for i in range(len(self.simulation.stages)):
	        if len(self.simulation.stages[i].queuing_delay) > 0:
	           average = float(sum(self.simulation.stages[i].queuing_delay) / len(self.simulation.stages[i].queuing_delay))
	        print("current_queue_size",self.simulation.stages[i].queued_tasks.qsize(),average)
	        if Max < (float(self.simulation.stages[i].sla)):
		    Max = float(self.simulation.stages[i].sla)
	        if average > float(self.simulation.stages[i].sla):
		    bottleneck = i

	            print(sla,self.simulation.stages[i].sla, Max, bottleneck)
	            stage_limit = int(1000/self.simulation.stages[bottleneck].sla)
	            lambdas_needed = (len(self.simulation.stages[i].queuing_delay) - len(self.simulation.stages[bottleneck].workers) )
                    lambdas_needed = int(lambdas_needed/stage_limit)
	            print (current_time,"+++++++++++++++++periodic timer event",current_time, stage_limit, "bottleneck",bottleneck, "lambdas_needed",lambdas_needed,(len(self.simulation.tasks),self.simulation.completed_tasks),"self.simulation.stages[i].num_workers",len(self.simulation.stages[bottleneck].workers),"+++++++++++++++")
	            if lambdas_needed > 0:
	                print ("adding workers ***********periodic timer event","bottlenck",bottleneck, "lambdas_needed",lambdas_needed,"self.simulation.stages[i].num_workers",self.simulation.stages[bottleneck].num_workers,"+++++++++++++++")
	                for j in range(int(math.ceil(lambdas_needed*1.5))):
	                    self.simulation.stages[bottleneck].workers.append(Lambda(self.simulation, 0, 1000, True, 0, 0))
		            if MODEL_SHARING == 1:
	                        new_events.append((float(current_time + 500), lambdaCreateEvent(self.simulation, self.simulation.stages[bottleneck].workers[-1], bottleneck)))
	                    new_events.append((float(current_time + 1850), lambdaCreateEvent(self.simulation, self.simulation.stages[bottleneck].workers[-1], bottleneck)))
	    #self.simulation.stages[bottleneck].num_workers += lambdas_needed
	    #self.simulation.stages[bottleneck].free_slots += lambdas_needed



        #print("periodic timer event",current_time,"VM1 VM2 VM3",len(self.simulation.VMs[0]),len(self.simulation.VMs[1]),len(self.simulation.VMs[2]))
      #  total_load       = str(int(10000*(1-self.simulation.total_free_slots*1.0/(TOTAL_WORKERS*SLOTS_PER_WORKER)))/100.0)
      #  small_load       = str(int(10000*(1-self.simulation.free_slots_small_partition*1.0/len(self.simulation.small_partition_workers)))/100.0)
      #  big_load         = str(int(10000*(1-self.simulation.free_slots_big_partition*1.0/len(self.simulation.big_partition_workers)))/100.0)
       # small_not_big_load ="N/A"
       # if(len(self.simulation.small_not_big_partition_workers)!=0):
            #Load        = str(int(10000*(1-self.simulation.free_slots_small_not_big_partition*1.0/len(self.simulation.small_not_big_partition_workers)))/100.0)

	"""if (load_tracking == 1):
            for i in range(3):
                low_load = 0
                for j in range (len(self.simulation.VMs[i])):
                    if((float(self.simulation.VMs[i][j].num_queued_tasks)/float(self.simulation.VMs[i][j].max_slots)) <=0.4):
                        low_load+=1
                print >> load_file,"VM type," + str(i) + "low_load: "+ str(low_load) + ",num_vms," + str(len(self.simulation.VMs[i])) + ",current_time: " + str(current_time)
                print "load written", i, low_load, len(self.simulation.VMs[i]), float(self.simulation.VMs[i][0].free_slots),self.simulation.VMs[i][0].num_queued_tasks
                     X = np.array(X).reshape(-1,1)
                print X
                y = np.array(y).reshape(-1,1)
                print "*****",y
                for i in range(len(X)): wtr.writerow(X[i])
                for i in range(len(y)): wtr.writerow(y[i])
	        model = LinearRegression()
                model.fit(X, y)
                #print model
                X_predict = np.array([current_time+start_up_delay]).reshape(-1,1)
                y_predict = model.predict([X_predict[0]])
                print "predicted requests",X_predict,y_predict
                if(int(y_predict) > len(self.simulation.VMs[i])*self.simulation.VMs[i][0].max_slots):
                    print ("rolling mean more",y_predict, "existing VM size", len(self.simulation.VMs[i])*self.simulation.VMs[i][0].max_slots)
                    num_vms = int(math.ceil(int(int(y_predict)- len(self.simulation.VMs[i])*self.simulation.VMs[i][0].max_slots)/int(self.simulation.VMs[i][0].max_slots)))
                    if(num_vms !=0):
                        print ("num_vms spawning",burst_threshold*num_vms)
                        for j in range(num_vms):
                        #print "adding new VMs", num_vms
                            self.simulation.VMs[i].append(VM(self.simulation,current_time,start_up_delay,i,4,8192,0.10,True,len(self.simulation.VMs[i])))
                            new_events.append((current_time+start_up_delay,VMCreateEvent(self.simulation,self.simulation.VMs[i][-1],i)))
 #rolling_mean = df.rolling(window=60).mean()
                #rolling_mean = mean([self.simulation.task_arrival[i] for i in range(len(self.simulation.task_arrival[i])-10, len(self.simulation.task_arrival[i]))])
                rolling_mean = np.mean(np.array(self.simulation.task_arrival[i][-10:]))
                if(rolling_mean > len(self.simulation.VMs[i])*self.simulation.VMs[i][0].max_slots):
                    print "rolling mean more",rolling_mean, "existing VM size", len(self.simulation.VMs[i])*self.simulation.VMs[i][0].max_slots
                    num_vms = int(math.ceil(int(rolling_mean - len(self.simulation.VMs[i])*self.simulation.VMs[i][0].max_slots)/int(self.simulation.VMs[i][0].max_slots)))
                    for j in range(num_vms*2):
                        #print "adding new VMs", num_vms
                        new_events.append((current_time,VMCreateEvent(self.simulation,i)))
                if(rolling_mean < len(self.simulation.VMs[i])*self.simulation.VMs[i][0].max_slots):
                    num_vms = int(math.ceil(int(len(self.simulation.VMs[i])*self.simulation.VMs[i][0].max_slots - rolling_mean)/int(self.simulation.VMs[i][0].max_slots)))
                    print "rolling mean lesser ",rolling_mean, "existing VM size", len(self.simulation.VMs[i])*self.simulation.VMs[i][0].max_slots, "size to be reduced ", num_vms
                    if(num_vms!=0):
                        for j in range(1,num_vms+1):
                            self.simulation.VMs[i][-j].end_time = current_time
                            print self.simulation.VMs[i][-j].start_time, current_time
                        self.simulation.completed_VMs.setdefault(i, []).extend(self.simulation.VMs[i][-num_vms:])
                        self.simulation.VMs[i] = self.simulation.VMs[i][:-num_vms]
                    #    print j,len(self.simulation.VMs[i])
                    #    print j,len(self.simulation.completed_VMs[i])"""

        if(self.simulation.event_queue.qsize() > 1):
            #print "events left ",self.simulation.event_queue.qsize()," tasks arrived", len(self.simulation.task_arrival)
            new_events.append((float(current_time) + MONITOR_INTERVAL,PeriodicTimerEvent(self.simulation)))
        return new_events
class ScheduleVMEvent(Event):

    def __init__(self, worker, job_id):
        self.worker = worker
        self.job_id = job_id
        self.worker.num_queued_tasks += 1
    def run(self, current_time):
        logging.getLogger('sim'
                ).debug('Probe for job %s arrived at worker %s at %s'
                        % (self.job_id, self.worker.id,
                            current_time))
        return self.worker.add_task(self.job_id, current_time)

class ScheduleLambdaEvent(Event):

    def __init__(self, worker, job_id):
        self.worker = worker
        self.job_id = job_id
    def run(self, current_time):
        logging.getLogger('sim'
                ).debug('Probe for job %s arrived at %s'
                        % (self.job_id,
                            current_time))
        return self.worker.execute_task(self.job_id, current_time)


class Simulation(object):

    def __init__(self, workload_file):
        self.workload_file = workload_file

        # avg_used_slots = load * SLOTS_PER_WORKER * TOTAL_WORKERS
        # self.interarrival_delay = (1.0 * MEDIAN_TASK_DURATION * TASKS_PER_JOB / avg_used_slots)
        # print ("Interarrival delay: %s (avg slots in use: %s)" %
         #      (self.interarrival_delay, avg_used_slots))
        self.stages=[]
	print("chains",len(chains[0]), len(chains[1]))
        for i in range(len(servers[0])):
            self.stages.append(Stage(servers[0][i],i,self))
	    if schedule_type == 2:
		for j in range(int(servers[0][i])):
		    print(i,j)
		    self.stages[i].workers.append(Lambda(self,0, 1000, False,0, 0))
        self.tasks = defaultdict()
        self.task_arrival = []
        # self. num_jobs
	self.completed_tasks = 0
        self.event_queue = Queue.PriorityQueue()
        self.VMs = defaultdict(lambda: np.ndarray(0))
        self.completed_lambdas = defaultdict(list)
        self.lambdas = defaultdict()
        # self.file_prefix = file_prefix

        j = 0
        while j < INITIAL_WORKERS:
            i = 0
            while i < 3:
                self.VMs.setdefault(i, []).append(VM(self,0,start_up_delay,i,4,8192, 0.10,False,len(self.VMs[i])))
                i += 1
            j += 1
        #print self.VMs
        # self.worker_indices = range(TOTAL_WORKERS)
        # self.task_distribution = task_distribution

    def add_task_completion_time(self, task_id, completion_time, isLambda):
        task_complete = \
                self.tasks[task_id].task_completed(completion_time)
        if(isLambda == 1):
            self.tasks[task_id].lambda_tasks+=1
        else:
            self.tasks[task_id].vm_tasks+=1
        return task_complete

    def send_tasks(self, task, current_time):
        scheduled_tasks = 0
        global VM_PREDICTION
        new_VM = False
        self.tasks[task.id] = task
        print(task.task_type, current_time)
        is_scheduled = False
        schedule_events = []
        #if schedule_type == 1: ########### FaaS Chains #####
        schedule_events.append((current_time,ScheduleStagesEvent(self, self.tasks[task.id])))

        return schedule_events
    def calculate_cost(self, end_time):
        total_cost = 0
       #/ f = open(VM_stats_path,'w')
        for i in range(3):
            for j in range(len(self.VMs[i])):
                print >> f,i,",", end_time ,",",self.VMs[i][j].start_time,",", self.VMs[i][j].lastIdleTime
                total_cost+=self.VMs[i][j].price * ((end_time - self.VMs[i][j].start_time)/3600000)
        for i in range(3):
            for j in range(len(self.completed_VMs[i])):
                total_cost+=self.completed_VMs[i][j].price * ((self.completed_VMs[i][j].end_time - self.completed_VMs[i][j].start_time)/3600000)

        return total_cost
    def run(self):
        self.tasks_file = open(self.workload_file, 'r')
        line = self.tasks_file.readline()
        #task_type = float(line.split(',')[1])
        #end_time = float(line.split(',')[3])/1000
        #start_time = line.split(',')[5]
        #arrival_time = float(line.split(',')[7])
        #waiting_time = line.split(',')[9]
        #print(arrival_time,start_time,end_time,waiting_time,task_type)
        #print line

        arrival_time = float(line.split(',')[0])
        num_tasks = float(line.split(',')[3])
        task_type = float(line.split(',')[2])
        #print start_time, num_tasks, task_type
	num_tasks2 = float(line.split(',')[4])

        self.task_arrival.append([int(arrival_time), num_tasks])
        # new_task = Task(self, line, 1000, start_time, num_tasks, task_type)
	while num_tasks > 0:
            self.event_queue.put((arrival_time*1000 , TaskArrival(self,
            arrival_time,0,len(chains[0]))))
	    num_tasks-=1
        while num_tasks2 > 0:
            self.event_queue.put((arrival_time*1000 , TaskArrival(self,
            arrival_time,1,len(chains[1]))))
	    num_tasks2-=1
	last_time = 0
        if load_tracking == 1:
	    self.event_queue.put(((arrival_time*1000)+1000, PeriodicTimerEvent(self)))
            self.event_queue.put(((arrival_time*1000)+1000, lambda_Monitor_Event(self)))
        while not self.event_queue.empty():
            (current_time, event) = self.event_queue.get()
            #print current_time, event, self.event_queue.qsize()
            assert current_time >= last_time
            #print ("first sim events are",event)
            last_time = current_time
            new_events = event.run(current_time)
            #print ("second sim events are",new_events)
            #print ("event_queue",self.event_queue.list())
            for new_event in new_events:
                self.event_queue.put(new_event)
        self.tasks_file.close()
        """
        total_VM_cost = self.calculate_cost(current_time)
        cost_file = open(cost_path,'w')
        print ("total VM cost is",total_VM_cost)
        print >> cost_file,"total VM cost is",total_VM_cost
        self.file_prefix = "pdf"
        complete_jobs = [j for j in self.tasks.values()
                if j.completed_tasks == j.num_tasks]
        print ('%s complete jobs' % len(complete_jobs))
        print >> cost_file,'%s complete jobs' % len(complete_jobs)
        response_times = [job.end_time - job.start_time for job in
                complete_jobs if job.start_time > 500]

        print ("Included %s jobs" % len(response_times))
        plot_cdf(response_times, "%s_response_times.data" % self.file_prefix)

        print ('Average response time: ', np.mean(response_times))
        print >> cost_file ,'Average response time: ', np.mean(response_times)

        total_lambda_cost = 0
        for i in range(3):
            print ("type ",i,"lambda tasks", len(self.lambdas[i]))
            print >> cost_file, "type ",i,"lambda tasks", len(self.lambdas[i])
            print ("type ",i,"lamda cost: ",lambda_cost(len(self.lambdas[i]), self.lambdas[i][0].mem/1024, self.lambdas[i][0].exec_time/1000))
            print >> cost_file , "type ",i,"lamda cost: ",lambda_cost(len(self.lambdas[i]), self.lambdas[i][0].mem/1024, self.lambdas[i][0].exec_time/1000)
            total_lambda_cost+=lambda_cost(len(self.lambdas[i]), self.lambdas[i][0].mem/1024, self.lambdas[i][0].exec_time/1000)
        # longest_tasks = [job.longest_task for job in complete_jobs]
        print ("total lambda cost ", total_lambda_cost)
        print >> cost_file, "total lambda cost ", total_lambda_cost
        print ("total cost of deployment ", total_lambda_cost + total_VM_cost)
        print >> cost_file, "total cost of deployment ", total_lambda_cost + total_VM_cost"""
	print("number of SLA violation", sla_violations,len(self.tasks), "percentage", float(float(sla_violations)/len(self.tasks)*100), type1_violations, type2_violations);
        # plot_cdf(longest_tasks, "%s_ideal_response_time.data" % self.file_prefix)

random.seed(1)
os.system("rm -rf %s"%(sys.argv[8]))
os.mkdir(sys.argv[8])
slack_aware = int(sys.argv[9])
queue_aware = slack_aware
finished_file_path = os.path.join(sys.argv[8], 'finished_file.csv')
all_tasks_path = os.path.join(sys.argv[8], 'all_tasks.csv')
VM_stats_path = os.path.join(sys.argv[8], 'VM_stats.csv')
load_file_path =  os.path.join(sys.argv[8], 'load')
cost_path = os.path.join(sys.argv[8], 'cost')
f = open(VM_stats_path,'w')
logging.basicConfig(level=logging.INFO)
schedule_type = int(sys.argv[2])
load_tracking = int(sys.argv[3])
PREDICTION = float(sys.argv[4])
burst_threshold = float(sys.argv[4])
finished_file = open(finished_file_path,'w')
tasks_file = open(all_tasks_path,'w')
load_file = open(load_file_path,'w')
chains = []
chains.append(sys.argv[5].split())
chains.append(sys.argv[6].split())
print " input dag chains is ", len(chains)
#chains.append(sys.argv[5])
#chains.append(sys.argv[6])
#chains.append(sys.argv[7])
#server1=float(sys.argv[9])
#server2=float(sys.argv[10])
#server3=float(sys.argv[11])
servers = []
servers.append(sys.argv[7].split())
print servers
for i in range(len(servers[0])):
    servers[0][i] = float(servers[0][i])
#servers.append(sys.argv[8].split())
print servers[0]
print(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
sim = Simulation(sys.argv[1])
predictor = Predictor(init_load=50,    model_path='wiki_model_32.h5',
                scaler_path='wiki_scaler.save')

sim.run()
f.close()
load_file.close()
