# Welcome to Customer Lifetime Value Project!

Hi! This project consists of doing an ETL for a CSV file that contains the information of customers and his orders. It was done using Python 3.6.


### Files List
1. **readme.md** this file =)
2. **server.py** Server file for Flask REST API
3. **client_reader.py** The file that reads from the csv and save to another csv and database.
4. **test_reader.py** Testing with pytest
5. **Python developer test.pdf** The problem to solve.
6. **model.dill** Binary file that contains the prediction model
7. **orders.csv** CVS file with the raw information.
8. **requirements.txt** Python requirements for the project. 

### What you need

1. Python 3.5 or 3.6
2. PIP
3. Some browser or some REST client to test the API
4. Some text editor to view the csv file.

### How to run it.

1. You will need all the requirements installed, To do that you will need to run `pip install -r requirements.txt`
2. Its important that all files remains in the same folder.
3. **First** you need to run `python client_reader.py`Which will read from the raw database and then transform and do the prediction. Then it will save the predictions on `exit.csv` file and on the database `database.db`which is a sqlite3 database that Flask can read.
4. Last you would need to run `export FLASK_APP=server.py` and then `flask run`. With this two commands, you will have the Flask server running in the port 5000.
5. To retrieve the CLV prediction for any customer you will need their customer_id and with that enter to `localhost:5000/predictions/<customer_id>` <customer_id> should be replaced with the customer_id. If you enter a valid customer id, Flask will respond with a JSON containing the customer_id as user_id and the clv, otherwise, Flask will respond with a 404 HTTP error.
6. After you run step #3, it will be available the file exit.csv. This file contains  a dump of the database but in a CSV format.
7. To run the test you need to run `pytest`from the terminal.

## Questions

1. **How would you deploy the app?**
    This depends on what is available to work with, for instance: 
* This repo could live on a local server that runs the script and then serve it on the local network. 
* Another way is to upload it to an Amazon EC2 or Amazon Lambda (or any other server that runs Python). The script is easly configurable to allow the passing of the "raw_data file" as an argument and then with a modification of the SQLAlchemy connection you can point it to a remote database and store the information in another service like Amazon RDS or Sqlite3 running in the same server or some Postgresql or Mysql server.
* Another way may be to allow the Flask server to receive upload files and the configure it to do the task. Because the task of processing the file takes aprox 12 sec, it will we recommended to receive the file and then using celery or another queue system runs it asyncronously.
2. **How to schedule the ETL job?**
    Schedule the ETL job depends on how the "raw_data file" will be updated. For instance, we could have a independent process that runs every 24h (starts running at 9am every day) and update the "raw_data file" then, we could run `client_reader` every 24h at 11am. This way we we would have the data updated every day for noon. 
    If we like to see how each customer updates his clv we will need to do another database models, because we are only saving the predicted CLV, then we will need to store orders as well on the database and then obtain the results after each save. 
3. **How long it take you to finnish the assignment?**
    I take me around 4 hours to complete this task. Only the code part. I do spend more time writing this readme. 


### Problems and bug faced.
*  I do encounter a problem trying to run in just one script the reader and the server. But because the way of starting of Flask, this was very tricky so I opted for another approach which consists of running two scripts separately. This will ensure that both tasks run without problems
* Another problem was trying to understand how the `model.dill`works and what input it needs. Because at first I was confused between which data it needs. The csv and the input list has the same length and it confuses me. Then was the issue with the numpy.array. In the description, it shows that the predict function takes a numpy.array and the example has two elements, but I didn't understand that it was the data from every customer already "formatted". Well, I didn't understand at the beginning =)p.
