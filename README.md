
# Project: Fil Rouge Extraction API
This repository represents my final project for the 2023 SIO Python class.

**Goal:** Write a crawler that extracts metadata from ArXiv.org and stores them in a Flask application through an API. 



## Installation

Here are the steps to install the project:

```bash
  
```
    
## Documentation

Here is how to run the API:

```bash
  python app.py
```

```bash
  curl -X POST -H "Content-Type: application/json" -d '{"query": "physics", "max_results": 5}' http://127.0.0.1:5000/populate_articles
```

```bash
  curl -X POST -H "Content-Type: application/json" -d '{"article_id": "123456"}' http://127.0.0.1:5000/populate_articles
```

```bash
  http://127.0.0.1:5000/articles
```

```bash
  http://127.0.0.1:5000/articles/2401.10216v1
```

```bash
  http://127.0.0.1:5000/text/2401.10216v1
```


## Running Tests

To run tests, run the following command:

```bash
  
```

## Need to get fixed

-id doesnt exist when populating
-if article isnt in database when looking for summary, adds it



## Authors

- [@maxine.gravier](https://gitlab-student.centralesupelec.fr/maxine.gravier)

