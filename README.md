
# Project: Fil Rouge Extraction API
This repository represents my final project for the 2023 SIO Python class.

**Goal:** Write a crawler that extracts metadata from ArXiv.org and stores them in a Flask application through an API. 



## Installation

Here are the steps to install the project:

Check if you have all the needed libraries:

```bash
pip install -r requirements.txt
  
```
    
## Documentation

### Running the API

```bash
  cd extraction_api-gravier
  python src/app.py
```
### Populating the database

Get the last 3 months of articles:
```bash

```

Using a keyword:
```bash
  curl -X POST -H "Content-Type: application/json" -d '{"query": "physics", "max_results": 5}' http://127.0.0.1:5000/populate_articles
```
Using an article id:
```bash
  curl -X POST -H "Content-Type: application/json" -d '{"article_id": "123456"}' http://127.0.0.1:5000/populate_articles
```

### Displaying the articles in the database
Get all the articles:
```bash
  http://127.0.0.1:5000/articles
```
Get an article by id (adds it to the database if not already in it):
```bash
  http://127.0.0.1:5000/articles/2401.10216v1
```
Sort by date:
```bash
/articles?start_date=2024-01-18&end_date=2024-01-18
```

### Get an article summary
```bash
  http://127.0.0.1:5000/text/2401.10216v1
```

## Running Tests

To run tests, run the following command:

```bash
  
```



## Authors

- [@maxine.gravier](https://gitlab-student.centralesupelec.fr/maxine.gravier)

