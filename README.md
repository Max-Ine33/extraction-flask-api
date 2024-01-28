
# Project: Fil Rouge Extraction API
This repository represents my final project for the 2023 SIO Python class.

**Goal:** Write a crawler that extracts metadata from ArXiv.org and stores them in a Flask application through an API. 



## Installation
To get started with the Fil Rouge Extraction API, follow these steps to clone the project and set up a virtual environment:


### Cloning the project

    ```bash
    git clone https://gitlab-student.centralesupelec.fr/maxine.gravier/extraction_api-gravier.git
    ```

### Checking Python Version

Before running the Fil Rouge Extraction API, ensure that you have Python 3.10 installed on your system. You can check your Python version by opening a terminal or command prompt and executing the following command:
  
```bash
python --version
```  
  
### Setting up a Virtual Environment and Installing Dependencies

To ensure a clean and isolated environment for running the Fil Rouge Extraction API, it's recommended to use a virtual environment. Follow these steps to set up a virtual environment and install the required dependencies:

1. Navigate to the project's root directory:

    ```bash
    cd extraction_api-gravier
    ```

2. Create a virtual environment. Run the following command:

    ```bash
    python -m venv venv
    ```


3. Activate the virtual environment:

    > On Windows:

    ```bash
    .\venv\Scripts\activate
    ```

    > On Unix or MacOS:

    ```bash
    source venv/bin/activate
    ```

4. With the virtual environment activated, install the project dependencies:

    ```bash
    pip install -r requirements.txt
    ```
  
## Running the API

```bash
  gunicorn src.app:app -c gunicorn_config.py
```

    
## Documentation

### Populating the database

Populate with the most recent 1000 articles:
```bash
  curl -X GET http://localhost:8080/auto_populate
```
  
Using a keyword:
```bash
  curl -X POST -H "Content-Type: application/json" -d '{"query": "physics", "max_results": 5}' http://localhost:8080/populate_articles
```  
  
Using an article id:
```bash
  curl -X POST -H "Content-Type: application/json" -d '{"article_id": "123456"}' http://localhost:8080/populate_articles
```

### Displaying the articles in the database
Get all the articles:  
```bash
  curl -X GET http://localhost:8080/articles
```  
  
Get an article by id (adds it to the database if not already in it):  
```bash
  curl -X GET http://localhost:8080/articles/2401.10216
```  
  
Sort by date:  
```bash
curl -X GET http://localhost:8080/articles?start_date=2024-01-18&end_date=2024-01-18
```

### Get an article summary
```bash
  curl -X GET http://localhost:8080/text/2401.10216
```
### Delete all entries in the database
```bash
curl -X POST http://localhost:8080/empty_database -H "Content-Type: application/json" -d '{}'
```

## Running Tests

To run tests, run the following command:

```bash
  python -m unittest discover -s test -p 'test_*.py'

```


## Authors

- [@maxine.gravier](https://gitlab-student.centralesupelec.fr/maxine.gravier)

