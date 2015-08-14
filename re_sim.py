# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 10:23:45 2015

@author: James
"""

import matplotlib.pyplot as plt
import random

class Job:
    def __init__(self, numOfWorkers, cost, skill):
        self.workers_needed = numOfWorkers
        self.cost = cost
        self.skill = skill
        
    def get_skill(self):
        return self.skill
    

class Worker:
    def __init__(self):
        self.ability = random.randint(1,100)
        self.reputation = 0.0
        self.like_list = []
        self.block_list = []
        self.ratings = []
        self.tasks_finished = 0
        self.mid_threshold = random.randint(21,50)
        self.low_threshold = random.randint(10,20)
        self.quality = random.randint(1,100)
        
    def get_reputation(self):
        return self.reputation
        
    def get_quality(self):
        return self.quality
        
    def get_ability(self):
        return self.ability
        
    def rate_Requestor(self, requestor):
        rep_requstor = requestor.getBehavior()
        if rep_requstor > self.mid_threshold:
            requestor.rate(1.0)
        elif rep_requstor > self.low_threshold:
            requestor.rate(0.0)
        else:
            requestor.rate(-1.0)

    def getAvgRating(self):
        return sum(self.ratings)/len(self.ratings) 
   
    def rate(self, value):
        self.ratings.append(value)
        self.reputation = self.getAvgRating()     
        
    def complete_task(self):
        self.tasks_finished += 1
        
class Requestor:    
    
    def __init__(self):
        self.behavior = random.randint(1,100)
        self.ratings = []
        self.reputation = 0.0
        self.like_list = []
        self.block_list = []
        self.mid_threshold = random.randint(21,50)
        self.low_threshold = random.randint(10,20)
        self.job = Job(random.randint(1,100),random.randint(50,1000), random.randint(1,100))
     
    def get_reputation(self):
        return self.reputation
        
    def new_job(self):
        self.job = Job(random.randint(1,100),random.randint(50,1000), random.randint(1,100))
        
    def rate_Worker(self, worker):
        rep_worker = worker.get_quality()
        if rep_worker > self.mid_threshold:
            worker.rate(1.0)
        elif rep_worker > self.low_threshold:
            worker.rate(0.0)
        else:
            worker.rate(-1.0) 
    def getBehavior(self):
        return self.behavior
        
    def getAvgRating(self):
        return sum(self.ratings)/len(self.ratings)      
    
    def rate(self, value):
        self.ratings.append(value)
        self.reputation = self.getAvgRating()
        
    def start_job(self, workers):
        #Gather priority_list of workers sorted in peference and reputation
        priority_list = [(worker,worker.reputation) for worker in workers]
        for elem in priority_list:
            worker = elem[0]
            rep = elem[1]
            preference = 0
            if worker in self.like_list:
                preference = 1
            elif worker in self.block_list:
                preference = -1
            priority_list[priority_list.index(elem)] = (preference,rep,worker)
        priority_list = sorted(priority_list)
        priority_list.reverse()
        
        worker_list = [worker for pref,rep,worker in priority_list if worker.get_ability() >= self.job.get_skill()]
        
        for worker in worker_list:
            worker.complete_task()
            self.rate_Worker(worker)
            worker.rate_Requestor(self)
        
        self.new_job()
        
def getAverageRep(array):
    reputations = []
    for elem in array:
        reputations.append(elem.get_reputation())
    return (sum(reputations)/len(reputations))

if __name__ == "__main__":
    workers = []
    for x in xrange(100):
        workers.append(Worker())
    requestors = []
    for x in xrange(100):
        requestors.append(Requestor())
    print("Requestors made")
    print("Running Jobs")
    
    worker_rep = []
    requestor_rep = []
    time = []
    fig = plt.figure()
    plt.ion()
    ax = fig.add_subplot(111)
    fig.canvas.set_window_title("Reputation Simulation")
    work_line, = ax.plot([],[],'-k',label='black')
    req_line, = ax.plot([],[],'-r',label='red')
    
    for x in xrange(100):
        print("Job " + str(x))
        worker_avg = getAverageRep(workers)
        requestor_avg = getAverageRep(requestors)
        print("Average worker reputation: " + str(worker_avg))
        print("Average requestor reputation: " + str(requestor_avg))
        for requestor in requestors:
            requestor.start_job(workers)
        worker_rep.append(worker_avg)
        requestor_rep.append(requestor_avg)
        time.append(x+1)
        work_line.set_xdata(time)
        work_line.set_ydata(worker_rep)
        req_line.set_ydata(requestor_rep)
        req_line.set_xdata(time)
        
        ax.relim()
        ax.autoscale_view()
        plt.draw()
        plt.show()