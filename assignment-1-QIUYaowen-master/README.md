# CSIT6000O Assignment-1: EC2 Measurement (2 questions, 4 marks)

### Deadline: 23:59, Feb 25, Friday

---

### Name: QIU Yaowen
### Student Id: 20784389

---

## Question 1: Measure the EC2 CPU and Memory performance

1. (1 mark) Report the name of measurement tool used in your measurements (you are free to choose any open source measurement software as long as it can measure CPU and memory performance). Please describe your configuration of the measurement tool, and explain why you set such a value for each parameter. Explain what the values obtained from measurement results represent (e.g., the value of your measurement result can be the execution time for a scientific computing task, a score given by the measurement tools or something else).

    Tool used: sysbench
    
    Configuration: Use default parameters
    
    #### For CPU performance test:
    
    Number of threads = 4;  Max Prime Number = 10000;    Running Time = 10s
    
    This setting can test the performance of CPU in fair. And the time cost is acceptable
    
    Value: Event per second (CPU Speed), means how many times of calculation of Max Prime Number is executed in one second
    
    #### For Memory Performance test:
    
    Number of threads = 4;  Memory Total Size = 10GB;  Operation = Write
    
    Value: Total time, means the time of 10GB writing operation cost.

2. (1 mark) Run your measurement tool on general purpose `t3.medium`, `m5.large`, and `c5d.large` Linux instances, respectively, and find the performance differences among these instances. Launch all the instances in the **US East (N. Virginia)** region. Does the performance of EC2 instances increase commensurate with the increase of the number of vCPUs and memory resource?

    In order to answer this question, you need to complete the following table by filling out blanks with the measurement results corresponding to each instance type.

    | Size      | CPU performance | Memory performance |
    |-----------|-----------------|--------------------|
    | `t3.medium` |          1676.21       |        1.5738s            |
    | `m5.large`  |            1658.75     |            1.5337s        |
    | `c5d.large` |             1815.81    |              1.4020s      |

    > Region: US East (N. Virginia). Use `Ubuntu Server 18.04 LTS (HVM)` as AMI.

    ### Answer:
    In general, Both the CPU performance and Memory performace of EC2 instances increase commensurate with the increase of the number of vCPUs and memory.
    
    For example, the rank of memomry performance is t3.medium < m5.large < c5d.large. Although the CPU performance of m5.large is slightly worse than t3.medium, there is a big gap between m5.large and c5d.large.
    
    
## Question 2: Measure the EC2 Network performance

1. (1 mark) The metrics of network performance include **TCP bandwidth** and **round-trip time (RTT)**. Within the same region, what network performance is experienced between instances of the same type and different types? In order to answer this question, you need to complete the following table.
    
    
    ### ALL CONNECTIONS THROUNG PRIVATE IP ADDRESS

    | Type          | TCP b/w (Mbps) | RTT (ms) |
    |---------------|----------------|----------|
    | `t3.medium` - `t3.medium` |        36.6 Gbits/sec        |      0.020ms    |
    | `m5.large` - `m5.large`  |          44.2 Gbits/sec       |        0.018ms  |
    | `c5n.large` - `c5n.large` |           47.2 Gbits/sec      |     0.019ms     |
    | `t3.medium` - `c5n.large`   |   4.00 Gbits/sec             |   0.019ms       |
    | `m5.large` - `c5n.large`  |           3.92 Gbits/sec     |     0.702ms     |
    | `m5.large` - `t3.medium` |          4.70 Gbits/sec      |         0.644ms |

    > Region: US East (N. Virginia). Use `Ubuntu Server 18.04 LTS (HVM)` as AMI.

2. (1 mark) What about the network performance for instances deployed in different regions? In order to answer this question, you need to complete the following table.

    ### ALL CONNECTIONS THROUNG PUBLIC IP ADDRESS

    | Connection | TCP b/w (Mbps)  | RTT (ms) |
    |------------|-----------------|--------------------|
    | N. Virginia - Oregon |            24.9 Mbits/sec     |               66.626ms     |
    | N. Virginia - N. Virginia |              4.01 Gbits/sec   |             0.117 ms       |
    | Oregon - Oregon |            4.08 Gbits/sec     |      0.124ms              |
 
    > Region: US East (N. Virginia), US West (Oregon). Use `Ubuntu Server 18.04 LTS (HVM)` as AMI. All instances are `c5.large`.
