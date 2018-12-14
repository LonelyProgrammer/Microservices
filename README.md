# Microservices
Investigating the lifecycle of Microservices

# History
I started this project after seeing all the fuss about microservices, especially the spring boot microservice framework. The place I work in have developers who have a Phd degree and now they code in Java Spring boot. A part of me always wanted to prove that simple things do work better than complex airy things.This prompted me to use python and REST to build a scalable, robust microservice to add,update and delete songs and artists.This is a work in progress and this is the first time I am creating a microservice of my own. The purpose of this project is to learn from scratch.

# Development Platform

IDE - Visual Studio Code Version 1.28.2 

MAC OS 10.14

Tested in Ubuntu 18.04 LTS Amazon EC2 instance

# Technical Stuff
The project has the following dependencies:
Python 2.7,
Cassandra 3.10,
Django Framework 1.11.16,
Django REST Framework 3.8.2,
django-cassandra-engine 1.5.4,
AWS Chalice 1.6.1

# Important Links
https://scotch.io/tutorials/build-a-rest-api-with-django-a-test-driven-approach-part-1

https://www.slothparadise.com/how-to-install-and-use-cassandra-on-django/

# Roadblocks encountered and solution:
So after writing the project in Django the issue was deploying the service to AWS.
However I was not very keen on managing the operations part viz. spinning up clusters and EC2 instances etc. 
so I decided to go serverless i.e.
(https://aws.amazon.com/lambda/serverless-architectures-learn-more/) 
with AWS api gateway and AWS lambda(https://docs.aws.amazon.com/lambda/latest/dg/welcome.html).
I was lucky to have found AWS Chalice which just did the job for me (https://chalice.readthedocs.io/en/latest/)

# Using AWS chalice to move to the AWS cloud:
I had to scrap out the Django project tat I had created, and I started with the following tutorial:
https://medium.com/richcontext-engineering/creating-a-serverless-blog-with-chalice-bdc39b835f75
I am however keeping the Django project for reference in this site.

# To directly jump to the serverless part clone/fork the AWSChaliceDemo folder

# Pledge
I shall comment all the vital sections of my code so that all the newbies (like me) can understand it without the aid of any tutorial.

I shall continue enhancing this project,so that everyone can use it independent of platform.

I shall make this project scalable and robust.

**Controversial** "I shall continue to hate JAVA and promote PYTHON."

