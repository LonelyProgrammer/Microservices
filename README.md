# Microservices
Investigating the lifecycle of Microservices

# History
I started this project after seeing all the fuss about microservices, especially the spring boot microservice framework. A part of me always wanted to prove that simple things do work better than complex airy things.This prompted me to use python and REST to build a scalable, robust microservice.This is a work in progress and this is the first time I am creating a microservice of my own. The purpose of this project is to learn from scratch.

# Development Platform

1. IDE - Visual Studio Code Version 1.28.2 

2. MAC OS 10.14

# Technical Stuff
The project has the following dependencies:
1.Python 2.7,

2.Cassandra 3.10,

3.Django Framework 1.11.16,

4.Django REST Framework 3.8.2,

5.django-cassandra-engine 1.5.4,

6.boto3 1.9.65

7.PyJWT 1.6.1

8.AWS Chalice 1.6.1

# Important Links
1. https://scotch.io/tutorials/build-a-rest-api-with-django-a-test-driven-approach-part-1

2. https://www.slothparadise.com/how-to-install-and-use-cassandra-on-django/

# Roadblocks encountered and solution:
So after writing the project in Django the issue was deploying the service to AWS.
However I was not very keen on managing the operations part viz. spinning up clusters and EC2 instances etc. 
so I decided to go serverless i.e.
(https://aws.amazon.com/lambda/serverless-architectures-learn-more/) 
with AWS api gateway and AWS lambda(https://docs.aws.amazon.com/lambda/latest/dg/welcome.html).
I was lucky to have found AWS Chalice which just did the job for me (https://chalice.readthedocs.io/en/latest/)

# Using AWS chalice for the serverless experience:
I had to scrap out the Django project tat I had created, and I started with the following tutorial:
https://medium.com/richcontext-engineering/creating-a-serverless-blog-with-chalice-bdc39b835f75
I am however keeping the Django project for reference in this site.

# To directly jump to the serverless part clone/fork the AWSChaliceDemo folder and start with the following steps:
1. Navigate to the "todoListBlog" folder

2.Create a user using the command  -- python users.py -c

3. Verify if the user is created -- python users.py -l

4.Hit the POST endpoint https://55w26nfmg5.execute-api.eu-west-1.amazonaws.com/api/login using POSTMAN or the command line(I like the "httpie" tool ) , e.g. echo '{"username": "Rishi", "password": "Password"}'| http POST https://55w26nfmg5.execute-api.eu-west-1.amazonaws.com/api/login

5. This will give you a JWT token

6.Use the JWT token in command line or POSTMAN to hit the GET/POST/PUT/DELETE apis e.g. http https://55w26nfmg5.execute-api.eu-west-1.amazonaws.com/api/todos Authorization:""""Replace your JWT token here""""

# Taking this further:
1.Create a CI/CD pipleine for this project preferably using Jenkins (Also try to use AWS CodePipeline)

2.Create a front end web application to consume these microservices pereferably in Angular JS

3.Log all the logs from these microservices into elastic search perferably using Kibana

4.Configure alerts from elastic search to deliver alert messages to Slack

# Pledge
I shall comment all the vital sections of my code so that all the newbies (like me) can understand it without the aid of any tutorial.

I shall continue enhancing this project,so that everyone can use it independent of platform.

I shall make this project scalable and robust.

**Controversial** "I shall continue to hate JAVA and promote PYTHON."

