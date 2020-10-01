# Prerequisites:

You need to install kubernetes and setup a cluster for this deployment to work. Follow instuctions from 
Install Kubeadm: https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/

Cluster setup: https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/

Download python3.6 and install it on your local directory.

Follow the instructions below to install brigade. you need to customize brigade installation using custom containers built from this source. The modified makefile is already available. The instructions are given below. 

https://docs.brigade.sh/topics/developers/
Note: change the docker access repository to your needs. 

## Brigade: Event-based Scripting for Kubernetes

### Quickstart

Check out the quickstart on the docs [here](https://docs.brigade.sh/intro/quickstart/).

### Brigade :heart: Developers

To get started head to the [developer's guide](https://docs.brigade.sh/topics/developers/)

Brigade is well-tested on Minikube and [Azure Kubernetes Service](https://docs.microsoft.com/en-us/azure/aks/).


If you use our setup, please cite our Fifer work, Jashwant Raj Gunasekaran, Prashanth Thinakaran, Nachiappan C.Nachiappan, Mahmut Taylan Kandemir, and Chita R. Das. 2020.Fifer: Tackling Resource Underutilization in the Serverless Era. In21st International Middleware Conference (Middleware ’20), December7–11, 2020, Delft, Netherlands.ACM, New York, NY, USA.
