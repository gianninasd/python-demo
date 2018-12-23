Python-demo
================
A Python program that reads a CSV file, stores each record in a database and then for each record, calls a REST API that performs a card payment using pool threading for parallel processing.

## Pre-requisites
* Install and run MySQL 5.5 or higher
* Install Python 3.7.1
* Install Python requests package by running `pip install requests` 
* Install Python mysql client by running `pip install mysql-connector-python`
* Install Python Cryptography client by running `pip install cryptography`

All downloaded 3rd party libraries can be found in `<python install dir>\Lib\site-packages`

## Setup database
Run `db/fileproc.sql` to create the database tables within MySQL

## Running applications
There two seperate applications you need to launch, the Loader and the Processor, first get the code:
* `git clone https://github.com/gianninasd/python-demo.git`
* `cd python-demo`

Now follow these steps to launch both applications:
* Open a console and run `python fileLoader.py` ... it will monitor for csv files in the `working` sub-folder
* Open a second console and run `python fileProc.py` ... it will monitor the database for records in INITIAL status

You will see processing output on your consoles and in a file called `fileProc.log`

To execute all unit tests from the root folder, from the console run: `python -m unittest discover -v -s test`

## References
* Docs: https://www.python.org/doc/
* Tutorials: 
  * https://realpython.com/
  * https://www.w3schools.com/python/default.asp
  * https://pyformat.info/
  * https://python-textbok.readthedocs.io/en/1.0/Introduction.html
* Requests: http://docs.python-requests.org/en/master/
* Futures: http://masnun.com/2016/03/29/python-a-quick-introduction-to-the-concurrent-futures-module.html
* MySQL Connector: https://dev.mysql.com/doc/connector-python/en/
* Cryptography: https://cryptography.io/en/latest/
