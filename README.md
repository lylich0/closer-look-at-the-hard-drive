<h1 align="center">How Does Hard Drive Work?</h1>

## Description
Let's take a closer look at how the hard drive manages requests. There are various disk scheduling algorithms, each with distinct features. The main purpose of a disk scheduling algorithm is to select a disk request 
from the queue of IO requests and decide the schedule for when this request will be processed. 

I decided to implement three different algorithms - `FCFS (First Come, First Served), SSTF (Shortest Seek Time First), and Circular LOOK` - to understand the advantages and disadvantages of each.

Implemented Concepts:
+ Process Creation
+ Queueing
+ Scheduling
