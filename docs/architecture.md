### Overview

This diagram shows how the project pieces are wired together:

![](architecture.jpg)

### Scrapers

In python, ideally you'd run these on a remote server:

- GDAX client 
- Reddit client 
- Twitter client 


All continuously collecting data and put into Kafka, managed by supervisord.

### Python/Flask Server

Serves APIs to interact with:

- Kafka
- Frontend 
- TensorFlow serving

Tensorflow serving is this really neat project by Google that lets you bundle up a 
pre-trained model, compile it into a large binary, and deploy it inside a Docker 
container. It also provides functionality to version your models and continuously 
deploy them.

### Frontend

Vue.js Application → So far only one feature is implemented: a chart of historical 
data fro GDAX. This data is fetched by calling the API from Flask, which connects to
Kafka and gathers it. Despite the 2 hops it needs to make 
(frontend → Flask → Kafka → Flask → Frontend), it is quite fast and mostly depends on 
internet connectivity (reads from kafka are blazing fast). 
 
Another feature recently implemented is the ability to display live incoming data through
websockets. 


### Why Kafka?

A simple question that may arise is why was this chosen. Why not using a simple SQL-based 
database such as Postgres, or storing stuff in S3 or just plain text? Here are some of the reasons behind it.

1. Extremely simple mental model      

Kafka topics can be seen as append-only logs of events 
that clearly reflects how market operates: an immutable, append-only log of events ordered by time. This
makes it easy to reason about possible transformations to be applied to the data such as labeling, time slicing, 
and ultimately time-series modeling. We don't need to deal with indexes or schemas, as those would only 
add overhead. 

2. Read performance    

TensorFlow is known to bottleneck when [not fed enough data](https://www.tensorflow.org/performance/datasets_performance), 
and as far as read performance goes, [Kafka's read performance is unmatched](https://engineering.linkedin.com/kafka/benchmarking-apache-kafka-2-million-writes-second-three-cheap-machines).
The ability to read 50 million messages per second means that there is no need to prefetch your data, and
your programs can view Kafka simply as an iterator from which data can be fed into a tensorflow model.
   
3. Scaling

Although not yet supported, scaling Kafka is easy, and it is just a matter of configuration. Working with
multiple nodes/clusters enables horizontal scaling and fault tolerance, which clearly are qualities we want.

Another consideration: working with an immutable log allows us to model the incoming data as infinite stream, 
which lets us work with interesting tools such as [ReactiveX](http://reactivex.io) and perform functional-style
type of operations. This is not only great fun, but it also helps making the system easier to reason about and
write code for.

