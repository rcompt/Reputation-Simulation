# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 10:23:45 2015

@author: James
"""

import matplotlib.pyplot as plt
import random
import pylab as P

#Job class primarily used within the Requestor class
class Job:
    def __init__(self, numOfWorkers, cost, skill):
        self.workers_needed = numOfWorkers
        self.cost = cost
        self.skill = skill
        
    #Returns the skill needed in order to finish the task
    def get_skill(self):
        return self.skill
    
#Worker class to represent a worker in the system
class Worker:
    def __init__(self):
        #Skill of the worker
        self.ability = random.randint(1,100)
        #Worker's reputation
        self.reputation = 0.0
        #List of requestors the worker has rated 1
        self.like_list = []
        #list of workers the worker has rated -1
        self.block_list = []
        #List of all ratings the worker has received
        self.ratings = []
        #Number of tasks finsihed
        self.tasks_finished = 0
        #Threshold for worker to rate the requestor a 0
        self.mid_threshold = random.randint(21,50)
        #Threshold for worker to rate the requestor a -1
        self.low_threshold = random.randint(10,20)
        #Quality of the worker's work
        self.quality = random.randint(1,100)
        
    def get_reputation(self):
        return self.reputation
        
    def get_quality(self):
        return self.quality
        
    def get_ability(self):
        return self.ability
        
    #rate a requestor
    #Rating is dependent on the mid and lower thresholds
    #If a requestor's behvaior level is greater than the mid threshold then they are given a 1
    #If a requestos's behavior level is inbetween the mid and low threshold then they are given a 0
    #If a requestor's behavior level is below the low threshold then they are given a 0
    def rate_Requestor(self, requestor):
        rep_requstor = requestor.getBehavior()
        if rep_requstor > self.mid_threshold:
            requestor.rate(1.0)
            if requestor not in self.like_list:
                self.like_list.append(requestor)
        elif rep_requstor > self.low_threshold:
            requestor.rate(0.0)
        else:
            requestor.rate(-1.0)
            if requestor not in self.block_list:
                self.block_list.append(requestor)
    #Helper function for "rate" function
    def getAvgRating(self):
        return sum(self.ratings)/len(self.ratings) 
   #rates the worker and updates their reputation
    def rate(self, value):
        self.ratings.append(value)
        self.reputation = self.getAvgRating()     
    #Function that does the task
    def complete_task(self):
        self.tasks_finished += 1
    
#Class representing the requestors in a system
class Requestor:    
    
    #Same traits as a worker except for they also have a Job object representing their need for a Job to be completed
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
    
    #Creates a new job
    def new_job(self):
        self.job = Job(random.randint(1,100),random.randint(50,1000), random.randint(1,100))
    
    #Rate a worker, works the same as the worker rating a requestor
    def rate_Worker(self, worker):
        rep_worker = worker.get_quality()
        if rep_worker > self.mid_threshold:
            worker.rate(1.0)
            if worker not in self.like_list:
                self.like_list.append(worker)
        elif rep_worker > self.low_threshold:
            worker.rate(0.0)
        else:
            worker.rate(-1.0) 
            if worker not in self.block_list:
                self.block_list.append(worker)
                
    def getBehavior(self):
        return self.behavior
        
    def getAvgRating(self):
        return sum(self.ratings)/len(self.ratings)      
    
    def rate(self, value):
        self.ratings.append(value)
        self.reputation = self.getAvgRating()
    
    #function acts as posting a job
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
        #Gather workers that have the ability to complete the task
        worker_list = [worker for pref,rep,worker in priority_list if worker.get_ability() >= self.job.get_skill()]
        #Have workers complete the task
        for worker in worker_list:
            worker.complete_task()
            self.rate_Worker(worker)
            worker.rate_Requestor(self)
        
        self.new_job()

#Return average reputation of the list of objects
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
        workers.append(Worker())
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
    
    #Plot histogram of all worker reputations
    all_reputations = [x.getReputation() for x in workers]
    sigma = P.std(all_reputations)
    mu = P.average(all_reputations)
    n, bins, patches = P.hist(all_reputations, 20, normed=1, histtype='step',cumulative=True)
    y = P.normpdf(bins, mu, sigma)
    P.plot(bins, y)
    P.figure()
    