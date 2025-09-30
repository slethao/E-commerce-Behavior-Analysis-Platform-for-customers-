## <span style="color: #86a0ba">E-commerce Behavior Analysis based on Customer's Commentary and Reviews</span>

This project does analysis on amazon customer reivews on
various products from 2013 through 2014 using batch ingestions to create a Directed Acyclic Graph (DAG) that
will format and securly store data that will be readily avaibale to use for the natural language model (NLM) that will be used to do sentimental analysis on the 5-star reivew and reviewer text comments.

Groups in Dataset:
| <span style="color:#c3b6fd;">Groups</span> | Description |
| ------------- | ------------- |
| <span style="color:#c3b6fd;">reviewerID</span> | The commenter's unique identifer for the reviewer. |
| <span style="color:#c3b6fd;">asin</span> | Amazon Standard Identification Number for the product |
| <span style="color:#c3b6fd;">reviewerName</span> | Name of the reviewer. |
| <span style="color:#c3b6fd;">helpful</span> | Number of helpful votes the review recieved. |
| <span style="color:#c3b6fd;">reviewText</span> | The content of the review written by the customer. |
| <span style="color:#c3b6fd;">overall rating</span> | The overall rating given to the product (ranging from 1 to 5 stars). |
| <span style="color:#c3b6fd;">summary</span> | A breif summary of the review |
| <span style="color:#c3b6fd;">unixReviewTime</span> | The time the review was posted in Unix timestamp format. |
| <span style="color:#c3b6fd;">reviewTime</span> | The time the review was posted in a readable date format |
| <span style="color:#c3b6fd;">day_diff</span> | The number of days between the review date and the current date. |
| <span style="color:#c3b6fd;">helpful_yes</span> | Number of positive helpful votes. |
| <span style="color:#c3b6fd;">total_vote</span> | Total numbers of votes the review received. |

<a href="https://www.kaggle.com/datasets/mehmetisik/amazon-review">
Click here to See the Dataset being used
</a>

## <span style="color: #86a0ba">Feauture<span>

- Batch Ingestion
- Automated DAG
- Medallion Architect
- NLM
- Front-End Dashboard

## <span style="color: #86a0ba">Installation</span>

```
source .venv/bin/activate
pip -r install
```

## <span style="color: #86a0ba">Usage</span>

Command Line Instruction

```
sudo lsof  -i: 5423
kill -9 <PID> (all of them)
suod lsof -i: 4200
kill -9 <PID> (all of them)
perfect start server
docker compose up -d
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

## <span style="color: #86a0ba">Technologies Use</span>

<span style="color: #b39db7">Frameworks: </span>Prefect and TextBlob
<br>
<span style="color: #b39db7">Database: </span>postgresSQL
<br>
<span style="color: #b39db7">
Technologies:
</span> Docker and Python
