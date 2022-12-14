# To build all the container dependencies

`docker compose build`

# After the build finished running launch everything and run the app

`docker compose up`

# Destroy the environment after use

`docker compose down`

# Commands to simplying a few things

# Once the env is up and running the app can be accessed on

## Creating the dummy users

`docker exec -it <app container_id> bash`

`./manage.py create_dummy_users`

dummy user credentials:

testuser1/testpass1
testuser2/testpass2

[UI](http://localhost:3000)
[BACKEND API](http://localhost:8000)
[BACKEND SCHEMA OPEN API](http://localhost:8000)
[BACKEND ADMIN](http://localhost:8000/admin)
[Celery flower](http://localhost:5555)

## Root view provides access to open swagger ui

## api schema file is available at

`http:\\localhost:8000\schema`

# Used blockchain.info api to access data No API key required

## Assumptions:

1. Multiple users can add the same address as we can't truly identify the owner of a wallet
2. Each time we try to sync the data we fetch all the transactions. We only store the transactions that doesn't exists in the database. Querying the transactions after a certain date or block number is ideal as it would reduce the number of requests we make and save bandwidth as well. Since the Blockchain api used doesn't have many options to filter transactions
3. Using 2 database model. Address and Transaction

Address has the following fields

address - wallet address transaction_count - transactions associated with a wallet address final_balance - final balance of the wallet after the most recent transaction.

address + user combined is considered unique in the Account model

Transaction table has the following fields Hash: Transaction hash which is a unique string of characters Inputs: transaction inputs // stored as json due to lack of time. Should be parsed and stored in a cleaner way Out: transaction outputs // stored as json due to lack of time. Should be parsed and stored in a cleaner way fee: fee paid for executing the transaction date: date and time at which the transaction is executed

1. Transactions are considered unique using a combination of address relation pk and hash since address is not considered unique to the user using wallet_address + hash will result in integrity issue if multiple users add the same wallet

Stack: Django Djangorestframework celery -> for running syncing in the background redis -> Celery message broker and result backend postgres -> to store the data

Usage of result backend gives us the ability to moniter the status of background sync task

# Django rest framework built in ui is used interact with the api.

# Swagger ui is also available to interact with the API

Inefficiencies:

Fetching all transactions during each sync. This should be optimized to avoid calls for txs that already exists.
Using a no-sql database to store tx is a much better option than using a RDBMS db as NO-SQL is cheaper and scales much better than RDBMS.
