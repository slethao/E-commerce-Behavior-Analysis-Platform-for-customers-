## E-commerce Behavior Analysis based on Customer's Commentary and Reviews

This project does analysis on amazon customer reivews on
various products from 2013 through 2014 using batch ingestions to create a Directed Acyclic Graph (DAG) that
will format and securly store data that will be readily avaibale to use for the natural language model (NLM) that will be used to do sentimental analysi on the 5-star reivew and reviewer text comments.

## Feauture

- Batch Ingestion
- Automated DAG
- Medallion Architect
- NLM
- Front-End Dashboard

## Installation

```
source .venv/bin/activate
pip -r install
```

## Usage

Command Line Instruction

```
perfect start server
docker compose up -d
sudo lsof  -i: 5423
kill -9 <PID> (all of them)
suod lsof -i: 4200
kill -9 <PID> (all of them)
```

<br>
After you have done all these commands you should be able to execute:

```bash
python Python\ Scripts/Analysis_Made.py
```

or

```bash
python3 Python\ Scripts/Analysis_Made.py
```

## Technologies Use

Frameworks: Prefect and TextBlob
<br>
Database: postgresSQL
<br>
Technologies: Docker and Python
