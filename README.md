# To build all the container dependencies

``` docker compose build ```

# After the build finished running launch everything and run the app

``` docker compose up ```


# Commands to simplying a few things

### Creating the user

``` docker compose run app python3 manage.py createsuperuser ```


# Destroy the environment after use

``` docker compose down ```


# Once the env is up and running the app can be accessed on

``` http:\\localhost:8000 ``` 

### Root view provides access to open swagger ui

### api schema file is available at 

``` http:\\localhost:8000\schema ```

