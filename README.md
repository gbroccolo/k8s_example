# k8s_example
From a Python script to a scalable service in cloud

Run the single pod of containers
--------------------------------

An example of request:
```
curl -X POST \
-H “Content-Type: application/x-www-form-urlencoded” \
-d “(18:27:26.345, 2.345) (18:27:26.355, 2.352) ...” \
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
-H “Content-Type: application/x-www-form-urlencoded” \
-d “(18:27:26.345, 2.345) (18:27:26.355, 2.352) ...” \
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
* Deploy the autoscaled (basing on CPU usage) service:
  * `kubectl create -f k8s/deploy.yml,k8s/service.yml,k8s/hpa.yml`
* Test the responsiveness of the service:
  * `telnet $(minikube ip) 30000`
* Clean the environment, destroy the kubernetes cluster:
  * `kubectl delete hpa anomaly-hpa && kubectl delete svc anomaly-service && kubectl delete deployment anomaly-deployment`
  * `minikube stop && minikube delete`

In order to submit requests, consider the url `http://$(minikube ip):30000`.
