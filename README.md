# 🎮 Games Release Tracker
This project is a comprehensive tool for tracking game releases across multiple platforms, with functionalities such as web scraping, data storage in RDS, and visualizing trends in a dashboard. Below is an overview of how to set up and run the different components of the project.

## 🗺️ Architecture Diagram
![Architecture Diagram](architecture_diagram.png)

## ⚙️ Setup Instructions
Follow the steps below in order to set up the full project. Each section contains a link to a more detailed README.

1. [Terraform Setup](https://github.com/mehrdadhalali/Games-Release-Tracker/blob/main/terraform/README.md)
- Start by setting up your infrastructure using Terraform.
- This section covers the creation of necessary AWS resources like RDS and ECR.

2. [Database Schema](https://github.com/mehrdadhalali/Games-Release-Tracker/blob/main/schema/README.md)
- Once your infrastructure is set up, apply the database schema to your RDS.
- This section contains the SQL commands required for setting up the database structure.

3. [Web Scraping](https://github.com/mehrdadhalali/Games-Release-Tracker/blob/main/web_scraping/README.md)
- After setting up the database, scrape the game release data from various platforms.
- Follow the instructions here to run the web scraping scripts and load the data into your database.

4. [Load Data to RDS](https://github.com/mehrdadhalali/Games-Release-Tracker/blob/main/load_to_rds/README.md)
- This section describes how to load the scraped data into the RDS.
- Ensure all data is correctly inserted into the database for further analysis.

5. [Dashboard Setup](https://github.com/mehrdadhalali/Games-Release-Tracker/blob/main/dashboard/README.md)
- Set up the dashboard to visualize the data.
- This section includes instructions for deploying the Streamlit dashboard and configuring SNS for subscriptions.

6. [Reporting](https://github.com/mehrdadhalali/Games-Release-Tracker/blob/main/report/README.md)
- Generate reports based on game releases and trends.
- Instructions here explain how to run the report generation scripts.
