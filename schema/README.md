# Schema

## Overview

This directory contains the schema SQL and two bash scripts to connect to and reset the database respectively.

## Folder Structure

- `schema.sql`: This has all the SQL to create the initial tables and seed all the static data on genres, platforms, and operating systems.
- `connect.sh`: This short shell script allows for easy connection to the database hosted on AWS RDS.
- `reset.sh`: This short shell script allow for the database hosted on AWS RDS to be reset according to the SQL in the `schema.sql` file.

## Set-up and Usage

1. Ensure you have an `.env` file inside the [schema directory](../schema).
2. Inside the `.env`, make sure you have the following:

```
DB_HOST=XXX
DB_PORT=XXX
DB_NAME=XXX
DB_USER=XXX
DB_PASSWORD=XXX
```

3. Open the terminal and enter:
    - ```bash reset.sh``` to set up and reset the database with the `schema.sql` file.

4. Then enter
    - ```bash connect.sh``` to start an interactive session with the AWS RDS and check the nessasary tables have been set up.

## ERD

This image shows the entity relationship diagram for the database created in `schema.sql`

![ERD](../ERD.png)