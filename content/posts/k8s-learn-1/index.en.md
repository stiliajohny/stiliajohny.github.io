---
title: 'Kubernetes for Beginners: Deploying a Static Website Made Easy'
date: 2023-04-14
author: 'John Stilia'
categories: [DevOps]
tags: ['Docker', 'Containerization', 'Website Deployment', 'DevOps', 'Website Hosting']

resources:
  - name: featured-image
    src: featured-image.png
  - name: featured-image-preview
    src: featured-image.png

draft: false
lightgallery: true
fontawesome: true
linkToMarkdown: true
rssFullText: false

toc:
  auto: yes
comment:
  enable: true
---

<style>
img {
    box-shadow: inset 10px 10px 60px #fff;
    -moz-border-radius:25px;
    border-radius:10px;
}
</style>

Deploy your static website on Kubernetes and learn the basics of container orchestration with this easy guide.

<!--more-->

Great choice! Deploying a static website on Kubernetes is a simple yet powerful way to learn the basics of Kubernetes.

Together we can explore with simple steps how to deploy a static website on Kubernetes.
**Yes** its easy, and this is the purpose; taking some easy steps to understand and learn the basics of Kubernetes.

Lets dig into it!

# The docker image

## Prep the files

I use Hugo, you can either have a range of HTML, JS, CSS or a simple index.html file. In my case I have a Hugo website, so I need to build it first.

I will use hugo cli to build that localy and export the statif files to the `public` folder. Then I will copy the content of the `public` folder to the nginx container.

```bash
hugo -D --minify
```

## Create the Dockerfile

Create a Docker image of your website: To deploy your static website on Kubernetes, you first need to create a Docker image of your website. You can use a simple Dockerfile to create the image. For example, if you have a website in a directory called mywebsite, you can create a Dockerfile with the following contents:

```dockerfile
FROM nginx:alpine
COPY public /usr/share/nginx/html
```

> This Dockerfile uses the nginx base image and copies the contents of the public directory to the html directory of the image.

## Build the Docker image

Now that you have a Dockerfile, you can build the Docker image. You can use the docker build command to build the image. For example, if you have a Dockerfile in the current directory, you can build the image with the following command:

```bash
docker build -t stiliajohny/mywebsite:v1 .
```

> This command builds the Docker image and tags it as `mywebsite:v1`.

## Push the Docker image to a registry

No this is optional. If you want to push the image to a registry, you can use the docker push command. For example, if you want to push the image to the Docker Hub registry, you can use the following command:

```bash
docker push stiliajohny/mywebsite:v1
```

> If you upload the image to Docker Hub, you need to name the image with your Docker Hub username. For example, if your Docker Hub username is `myusername`, you need to name the image as `myusername/mywebsite:v1`.

# Deploy the website on Kubernetes

To deploy the website on Kubernetes, you need to create a deployment and a service. The deployment manages the pods that run the website, and the service exposes the website to the outside world.

> Deployment is a Kubernetes object that manages a set of pods. A deployment is responsible for creating and updating pods. A deployment is also responsible for managing the replica set that is associated with the pods. A replica set is responsible for managing the pods that are created by the deployment.

> Service is a Kubernetes object that exposes a set of pods to the outside world. A service is responsible for load balancing the traffic that is sent to the pods. A service is also responsible for exposing the pods to the outside world.

## Create the deployment

Create a file called `mywebsite-deployment.yaml` with the following contents:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mywebsite-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mywebsite
  template:
    metadata:
      labels:
        app: mywebsite
    spec:
      containers:
        - name: mywebsite-container
          image: mywebsite:v1
          ports:
            - containerPort: 80
```

This YAML file creates a deployment with three replicas of the mywebsite container. The container runs the mywebsite:v1 image and listens on port 80.

## Create the service

Create a file called `mywebsite-service.yaml` with the following contents:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mywebsite-service
spec:
  selector:
    app: mywebsite
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: LoadBalancer
```

This YAML file creates a service that exposes the website to the outside world. The service selects the pods with the app: mywebsite label and exposes port 80.

## Deploy the website

To deploy the website, run the following commands:

```bash
kubectl apply -f mywebsite-deployment.yaml
kubectl apply -f mywebsite-service.yaml
```

# Check if the deployment and the service were deployed correctly

To check if the deployment and the service were deployed correctly, run the following commands:

```bash
[johnstilia:...itHub/stiliajohny.github.io]$ kubectl get deployments

NAME                   READY   UP-TO-DATE   AVAILABLE   AGE
mywebsite-deployment   3/3     3            3           2m52s
```

To check if the pods were created correctly, run the following command:

```bash
[johnstilia:...itHub/stiliajohny.github.io]$ kubectl get pods

NAME                                    READY   STATUS    RESTARTS   AGE
mywebsite-deployment-55c8956b6d-7rgxt   1/1     Running   0          3m24s
mywebsite-deployment-55c8956b6d-mqmd5   1/1     Running   0          3m24s
mywebsite-deployment-55c8956b6d-48xbg   1/1     Running   0          3m24s

```

To check id the service was created correctly, run the following command:

```bash
[johnstilia:...itHub/stiliajohny.github.io]$ kubectl get service

NAME                TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)        AGE
kubernetes          ClusterIP      10.43.0.2       <none>          443/TCP        171m
mywebsite-service   LoadBalancer   10.43.232.123   123.123.123.123   80:30364/TCP   2m42s

```

> The EXTERNAL-IP field shows the IP address of the service. You can use this IP address to access the website on the port 80.

# Access the website

To access the website, open a browser and navigate to the EXTERNAL-IP address of the service. For example, if the EXTERNAL-IP address is `123.123.123.123`, you can access the website at `http://123.123.123.123.:80`.

> Congratulations! You have now deployed a static website on Kubernetes. This is just the beginning of your journey with Kubernetes, and there is a lot more to learn.
