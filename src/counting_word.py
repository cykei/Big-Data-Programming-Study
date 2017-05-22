import os
from operator import add
import re
overview="Apache Spark provides programmers with an application programming interface centered on a data structure called the resilient distributed dataset (RDD), a read-only multiset of data items distributed over a cluster of machines, that is maintained in a fault-tolerant way.[2] It was developed in response to limitations in the MapReduce cluster computing paradigm, which forces a particular linear dataflow structure on distributed programs: MapReduce programs read input data from disk, map a function across the data, reduce the results of the map, and store reduction results on disk. Spark's RDDs function as a working set for distributed programs that offers a (deliberately) restricted form of distributed shared memory.[3]The availability of RDDs facilitates the implementation of both iterative algorithms, that visit their dataset multiple times in a loop, and interactive/exploratory data analysis, i.e., the repeated database-style querying of data. The latency of such applications (compared to a MapReduce implementation, as was common in Apache Hadoop stacks) may be reduced by several orders of magnitude.[2][4] Among the class of iterative algorithms are the training algorithms for machine learning systems, which formed the initial impetus for developing Apache Spark.[5] Apache Spark requires a cluster manager and a distributed storage system. For cluster management, Spark supports standalone (native Spark cluster), Hadoop YARN, or Apache Mesos.[6] For distributed storage, Spark can interface with a wide variety, including Hadoop Distributed File System (HDFS),[7] MapR File System (MapR-FS),[8] Cassandra,[9] OpenStack Swift, Amazon S3, Kudu, or a custom solution can be implemented. Spark also supports a pseudo-distributed local mode, usually used only for development or testing purposes, where distributed storage is not required and the local file system can be used instead; in such a scenario, Spark is run on a single machine with one executor per CPU core."
removed=re.sub('\[\d+\]','',overview)

f=open('data/wiki_apache_spark_overview.txt','w')
f.write(removed)
f.close()
lines=spark.sparkContext.textFile(os.path.join("data","wiki_apache_spark_overview.txt"))
word_count=lines.flatMap(lambda x: x.split(' ')).map(lambda x: (x.lower().rstrip().lstrip().rstrip(',').rstrip('.'),1)).reduceByKey(add)


arr=word_count.collect()
for i in arr:
    print i[0],':',i[1]