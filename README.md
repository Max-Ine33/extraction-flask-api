
# Project: Fil Rouge Extraction API :thread:
This repository represents my final project for the 2023 SIO Python class :dizzy:

**Goal:** Write a crawler that extracts metadata from ArXiv.org and stores them in a Flask application through an API. 



## Installation  :arrow_down:
To get started with the Fil Rouge Extraction API, follow these steps to clone the project and set up a virtual environment:


### Cloning the project :link:
```bash
  git clone https://gitlab-student.centralesupelec.fr/maxine.gravier/extraction_api-gravier.git
```
  
  
### Checking Python :snake: Version

Before running the Fil Rouge Extraction API, ensure that you have Python 3.10 installed on your system. You can check your Python version by opening a terminal or command prompt and executing the following command:
  
```bash
python --version
```  
  

### Setting up a Virtual Environment and Installing Dependencies :hammer_and_wrench:

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
  


## Running the API :runner:

```bash
  gunicorn src.app:app -c gunicorn_config.py
```

    

## Documentation :books:

### Populating the database

| Description                              | Command |
|------------------------------------------|---------|
| Populate with the most recent 1000 articles | `curl -X GET http://localhost:8080/auto_populate` |
| Using a keyword                           | `curl -X POST -H "Content-Type: application/json" -d '{"query": "physics", "max_results": 5}' http://localhost:8080/populate_articles` |
| Using an article id                        | `curl -X POST -H "Content-Type: application/json" -d '{"article_id": "2401.10216"}' http://localhost:8080/populate_articles` |

### Displaying the articles in the database

| Description                          | Command |
|--------------------------------------|---------|
| Get all the articles                  | `curl -X GET http://localhost:8080/articles` |
| Display more pages                    | `curl -X GET http://localhost:8080/articles?page=6` |
| Get an article by id                  | `curl -X GET http://localhost:8080/articles/2401.10216` |
| Sort by date                          |   |
| Display articles published after 2024-01-18 | `curl -X GET http://localhost:8080/articles?start_date=2024-01-18` |
| Display articles published before 2024-01-18 | `curl -X GET http://localhost:8080/articles?end_date=2024-01-18` |
| Display articles published between 2024-01-17 and 2024-01-18 | `curl -X GET http://localhost:8080/articles?start_date=2024-01-17&end_date=2024-01-18` |

### Get an article summary

| Command                                |
|----------------------------------------|
| `curl -X GET http://localhost:8080/text/2401.10216` |

### Delete an article from the database

| Command                                |
|----------------------------------------|
| `curl -X POST http://localhost:8080/remove/2401.13999` |

### Delete all entries in the database

| Command                                |
|----------------------------------------|
| `curl -X POST http://localhost:8080/empty_database -H "Content-Type: application/json" -d '{}'` |

  


## Running Tests :white_check_mark:

To run tests, run the following command:

```bash
  python -m unittest discover -s test -p 'test_*.py'
```
  


## Additional Info :nerd_face:
### Changing the port
To change the port where the API is running (8080 by default), you can update this line in the gunicorn_config.py file:  
```bash
bind = "0.0.0.0:8080"
```
  

### Using the UI
A basic UI was created:   
![Screenshot of the UI](doc/home.png? "Screenshot of the UI")  
It can be used to try the API with some simple requests.  
  


## Authors :rainbow:

- [@maxine.gravier](https://gitlab-student.centralesupelec.fr/maxine.gravier) 
