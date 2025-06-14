# StackOverflow Data Analysis and Topic Classification
![project description](https://github.com/abdullahfawazaltulahi/Stackoverflow_project/assets/63244923/d9fd05c7-7670-45c9-bef0-1d65ad20adb3)

# Introduction:

In the dynamic world of technology, staying informed about the latest trends and discussions is essential for IT professionals and enthusiasts. This project aims to harness the power of Azure cloud services to build a robust big-data engineering solution that not only analyzes data from StackOverflow but also provides continuous updates on the platform's user behavior, post trends, and topic popularity.

# Project Objectives:

The primary objective of this project is to develop an Azure-based big data engineering solution that continuously ingests, transforms, and visualizes data from StackOverflow, ensuring that the insights and visualizations are always up-to-date. The specific objectives of the project are as follows:

  - Ingest data from two sources: AWS RDS Postgres database and Azure Storage Blob container, with continuous updates for the "Posts" data.
  -  Perform data transformation using Databricks notebook to clean, transform, and apply machine learning techniques continuously.
  - Generate interactive visualizations using Azure Synapse to display the top 10 discussed topics on StackOverflow, updated continuously.

# Project Scope:
The project will focus on how to deal with different integration sources and how to build a pipeline to meet the business requirements:
  - Business requirements:
    *  Data Lake Requirements:
        * Create a Data Lake. It is nothing but the Azure Storage Blob but with the features of hierarchical namespace.
        * Create an Azure Data Factory to finish the data ingestion and processing.
        * Connect to an AWS RDS Postgres database and ingest PostTypes and Users tables from RDS to your Data Lake. But you need to ingest once every week.
        * Connect to a WeCloudData Azure blob container to copy the parquet files of Posts from StackOverflow into your data lake. You need to ingest it every day.
   
    * Machine Learning Process Requirements:
        * Develop a Databricks notebook to process data and feed the data into a Machine Learning Model, and output the running result from the Machine Learning Model. `we need a series of work to clean and transform the data.`
    * Chart Requirements:
        * Develop a chart on Synapse based on the output result data of the Machine Learning Model to display the top 10 topics of today.

# Data Ingestion:
  - Establish a connection to AWS RDS Postgres database and ingest "Users" and "PostTypes" tables into Azure Data Lake.
  - Connect to Azure Storage Blob container and ingest daily "Posts" data files in Parquet format, ensuring that the data is updated continuously.
<img width="576" alt="data ingestion" src="https://github.com/abdullahfawazaltulahi/Stackoverflow_project/assets/63244923/d4b05e8e-8dcb-458a-9de8-983055685107">

# Data Transformation:
Create a Databricks notebook to perform the following operations continuously:
  - Data cleaning and transformation to prepare the data for machine learning.
  - Develop a machine learning model to classify the topics of StackOverflow posts based on their text content, with continuous updates to the model.
<img width="573" alt="data transformation" src="https://github.com/abdullahfawazaltulahi/Stackoverflow_project/assets/63244923/0d2e09ed-9e66-4f23-990c-3544bdc4aab4">

# Data Visualization:
Utilize Azure Synapse to connect to the Data Lake and generate a chart that displays the top 10 topics of the day, updated continuously.

# Project Deliverables:
Upon completion of the project, the following deliverables will be produced:

  - A comprehensive Azure-based big data engineering solution for StackOverflow data analysis, with continuous updates.
  - A Databricks notebook containing the data transformation and machine learning code, updated continuously.
  - An interactive dashboard generated using Azure Synapse that visualizes the top 10 discussed topics on StackOverflow, updated continuously.
# What we add to the project:
- Archives Files: we archive files from the place where we will load the new data 
into the archive folder where we still keep the old ones by format and date of 
archiving it
- Alert notification: We must receive notice whenever something goes wrong with the pipeline, 
whether the execution pipeline succeeds or fails.
- Handling schema Changes: In certain circumstances, we must map the required columns 
and use the data flow's validate schema option to prevent the schema for our product from 
changing.
## Coming Feature:
- Our team is developing a Change Data Capture (CDC) technique which is a new feature in Azure Data Factory to track and capture modifications within datasets. This solution will efficiently deliver these changes to downstream pipelines promptly.
## Project Status:
Please note that this project is currently in progress and is undergoing continuous development. The data ingestion, transformation, and visualization processes are designed to run continuously, ensuring that the insights and visualizations provided are always up-to-date.
