# Prerequisites:

You need to install kubernetes and setup a cluster for this deployment to work. Follow instuctions from 
Install Kubeadm: https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/

Cluster setup: https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/

Download python3.6 and install it on your local directory.

Follow the instructions below to install brigade. you need to customize brigade installation using custom containers built from this source. The modified makefile is already available. The instructions are given below. 

https://docs.brigade.sh/topics/developers/
Note: change the docker access repository to your needs. 

## Brigade: Event-based Scripting for Kubernetes

![Build Status](https://badges.deislabs.io/v1/github/build/brigadecore/brigade/badge.svg?branch=master)
[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/2688/badge)](https://bestpractices.coreinfrastructure.org/projects/2688)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fbrigadecore%2Fbrigade.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fbrigadecore%2Fbrigade?ref=badge_shield)

Script simple and complex workflows using JavaScript. Chain together containers,
running them in parallel or serially. Fire scripts based on times, GitHub events,
Docker pushes, or any other trigger. Brigade is the tool for creating pipelines
for Kubernetes.

- JavaScript scripting
- Project-based management
- Configurable event hooks
- Easy construction of pipelines
- Check out the [docs](https://docs.brigade.sh/) to get started.

 <!-- [![asciicast](https://asciinema.org/a/JBsjOpah4nTBvjqDT5dAWvefG.png)](https://asciinema.org/a/JBsjOpah4nTBvjqDT5dAWvefG) -->

### The Brigade Technology Stack

- Brigade :heart: JavaScript: Writing Brigade pipelines is as easy as writing a few lines of JavaScript.
- Brigade :heart: Kubernetes: Brigade is Kubernetes-native. Your builds are translated into
  pods, secrets, and services
- Brigade :heart: Docker: No need for special plugins or elaborate extensions. Brigade uses
  off-the-shelf Docker images to run your jobs. And Brigade also supports DockerHub
  webhooks.
- Brigade :heart: GitHub: Brigade comes with built-in support for GitHub, DockerHub, and
  other popular web services. And it can be easily extended to support your own
  services.

The [design introduction](https://docs.brigade.sh/topics/design/) introduces Brigade concepts and
architecture.

### Quickstart

Check out the quickstart on the docs [here](https://docs.brigade.sh/intro/quickstart/).

### Brigade :heart: Developers

To get started head to the [developer's guide](https://docs.brigade.sh/topics/developers/)

Brigade is well-tested on Minikube and [Azure Kubernetes Service](https://docs.microsoft.com/en-us/azure/aks/).


If you use our setup, please cite our Fifer work, Jashwant Raj Gunasekaran, Prashanth Thinakaran, Nachiappan C.Nachiappan, Mahmut Taylan Kandemir, and Chita R. Das. 2020.Fifer: Tackling Resource Underutilization in the Serverless Era. In21st International Middleware Conference (Middleware ’20), December7–11, 2020, Delft, Netherlands.ACM, New York, NY, USA.
