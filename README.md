# Covid Chat Bot
An A.I. that will answer questions related to covid 19 data and information. Visit the working demo below.

![Main][Main_Page]

[Covid Chat Bot - Running Demo](https://daduyafbhack.herokuapp.com/)

## Table of contents
* [General info](#general-info)
* [Setup](#setup)
* [How to use](#how-to-use)

## General info
This project is built using jquery and flask for the frontend and backend. Docker was used for containerizing and deployed to Heroku. 

## Setup
To run this project using a virtual environment, install it locally using pip:

```
$ git clone github.com/HansGabriel/daduya-valencia-hackathon
$ cd daduya-valencia-hackathon
$ pip install -r requirements.txt
$ export FLASK_APP=app.py
$ export FLASK_ENV=development
$ flask run
```
To run this project using docker-compose, run:

```
$ docker-compose up --build
```
Both can be accessed at **http://localhost:5000**


## How to use 
My A.I. isn't really as sophisticated as it seems since it was trained on a small sample of sentences. Anyways here are some the examples 

1.) **Number of deaths, infected, and recoveries per country**

![Message][Message]

Examples of getting these sentences:

- How many new infected in the united states of america
- How many total recoveries in the japan
- How many new deaths due to covid in malaysia

2.) **Getting graphs of deaths, infected, and recoveries per country**

![GraphData][GraphData]

Examples of getting these sentences:

- Can you give me a time graph of infected cases in philippines
- Can you give me a time graph of deaths in japan
- Can you give me a graph of recoveries in singapore

3.) **Using Audio**

![AudioData][AudioData]

You can press the recorder icon to start recording and press again to end. The same answers will be the A.I.'s response depending on your sentence.

4.) **Other Examples to try**


- Hi
- Hello, how are you
- Good bye
- Who are you?
- What to do if you are sick
- What are the symptoms of covid
- How to prevent the spread of covid

***DISCLAIMER!!!:*** The data may not be accurate and an API was used to fetch the data from this link [https://covid19api.com/](https://covid19api.com/).



 
[Main_Page]:
https://raw.githubusercontent.com/HansGabriel/daduya-valencia-hackathon/master/images/main.png
[Message]:
https://raw.githubusercontent.com/HansGabriel/daduya-valencia-hackathon/master/images/message.png
[GraphData]:
https://raw.githubusercontent.com/HansGabriel/daduya-valencia-hackathon/master/images/graph.png
[AudioData]:
https://raw.githubusercontent.com/HansGabriel/daduya-valencia-hackathon/master/images/audio.png