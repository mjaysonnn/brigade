# Prerequisites:

## Real System
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

## Simulator
The trace driven simulator is avaialble in slack_aware.py file. Instructions for execution are

python slack_aware.py trace_file schedule_type load_tracking predictive Func-chain1 Func-chain2 startup_containers results_dir slack_aware

trace_file: inout csv file. eg. traces/wits_load.csv
schedule_type: 0-baseline 1-stageaware
load_tracking - default 0. 1- gives additional logs
predictive- 1 - enables load prediction 
Func-chain1- eg. HS AP FACED FACER
Func-chain2- eg. ASR NLP QA
startup_containers- initializing the setup. eg. 5
results_dir- output folder
slack_aware- 1 for LSF scheduling. 
