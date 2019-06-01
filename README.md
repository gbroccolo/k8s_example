# k8s_example
From a Jupyter notebook to a scalable service in cloud

![alt text](img/image.pdf)

Run the single pod of containers
--------------------------------

An example of request:
```
curl -X POST \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "(18:27:26.345,2.345) (18:27:26.355,2.352) ..." \
http://localhost/get_anomalous_data
```

To run the service as a single local pod of containers:

* Run the containers:
  * `docker-compose up -d`
* Test the responsiveness of the service:
  * `telnet localhost 80`
* Remove the allocated docker resources (containers & network):
  * `docker-compose down`

Run the k8s cluster
-------------------

An example of request:
```
curl -X POST \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "(18:27:26.345,2.345) (18:27:26.355,2.352) ..." \
http://<cluster IP>:30000/get_anomalous_data
```

The prototype can be deployed using `minikube` to create a Kubernetes
cluster running on VMs.
See https://kubernetes.io/docs/setup/minikube/ for further details about
how to install/configure it.

Follow the below steps in order to create an autoscalable service
(**NOTE** the service listen to port 30000):

* Create the Kubernetes cluster:
  * `minikube start --memory=1024 --extra-config=controller-manager.horizontal-pod-autoscaler-upscale-delay=1m --extra-config=controller-manager.horizontal-pod-autoscaler-downscale-delay=2m --extra-config=controller-manager.horizontal-pod-autoscaler-sync-period=10s`
* Build the image locally and configure Minikube in order to pull it:
  * `eval $(minikube docker-env)`
  * `docker build -t anomaly_app:latest .`
* Deploy the autoscaled (basing on CPU usage) service:
  * `kubectl create -f k8s/deploys.yml,k8s/services.yml,k8s/hpas.yml`
* Test the responsiveness of the service:
  * `telnet $(minikube ip) 30000`
* Clean the environment, destroy the kubernetes cluster:
  * `kubectl delete hpa app && kubectl delete svc app redis && kubectl delete deployment app redis`
  * `minikube stop && minikube delete`

Wait few minutes (1-2) in order to have the autoscaler working.

In order to submit requests, consider the url `http://$(minikube ip):30000`.

A sample for requests
---------------------

Consider to use the sample in `data/` for requests, e.g.:
```
$ curl -X POST \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "@./data/sample.body" \
http://localhost/get_anomalous_data
submitted
$ curl -X GET http://localhost/get_anomalous_data
[["18:27:26.352", 2.449], ["18:27:26.411", 2.554]]
```
