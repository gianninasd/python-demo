Python-demo
================
A Python program that reads a CSV file and for each record, calls a REST API that performs a card payment using pool threading for parallel processing.

## Pre-requisites
* Install Python 3.7.1
* Install Python requests package by running `pip install requests` 
* Install Python mysql client by running `pip install mysql-connector-python`
* Install Python Cryptography client by running `pip install cryptography`

All downloaded 3rd party libraries can be found in `<python install dir>\Lib\site-packages`

## Getting started
Open a console and run the following commands to get going:
* `git clone https://github.com/gianninasd/python-demo`
* `cd python-demo`
* `python fileProc.py sample.csv`

You will see processing output on your console and in a file called "fileProc.log"

To execute all unit tests from the root folder, from the console run: `python -m unittest discover -v -s test`

## References
* Docs: https://www.python.org/doc/
* Tutorials: 
  * https://realpython.com/
  * https://www.w3schools.com/python/default.asp
  * https://pyformat.info/
* Requests: http://docs.python-requests.org/en/master/
* Futures: http://masnun.com/2016/03/29/python-a-quick-introduction-to-the-concurrent-futures-module.html
* MySQL Connector: https://dev.mysql.com/doc/connector-python/en/
* Cryptography: https://cryptography.io/en/latest/
