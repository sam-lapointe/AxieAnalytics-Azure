# AxieAnalytics
AxieAnalytics is a web application that **indexes** asset **sales** in the Axie Infinity ecosystem (Web3 Gaming). While the official marketplace displays current listings, it lacks a clear history of past sales. AxieAnalytics fills this gap by **tracking**, **storing**, and **visualizing asset sales** data on the Ronin blockchain using native Azure microservices and event driven architecture.

Website: https://axieanalytics.com/

## 🎯 Technical Goals
My main objectives for this project were to **learn** and **gain hands-on experience** with **microservices architecture**, **native Azure services** and **DevOps principles**. Because of these goals, the architecture and choice of Azure services are somewhat overkill for an application of this size. In the future, I plan to migrate the application to run on **Kubernetes** locally to reduce costs, as I already have the necessary hardware available.

## 🌐 Project Architecture Overview
AxieAnalytics is built with native Azure services and follows a microservices architecture. It is composed of five main components:

1. webhook_listener

    **Type**: Azure Function (Python)
    
    **Role**: Listens to a third-party webhook triggered by specific events on the Ronin blockchain.
    
    **Output**: Sends processed event data to an Azure Service Bus Topic for downstream processing.

2. store_sales

    **Type**: Azure Function (Python)

    **Role**:

    - Subscribed to the **Service Bus Topic**.

    - Queries a blockchain node for the transaction receipt.

    - Extracts asset sale information (e.g., asset type, sale price).

    - For **Axie sales**, stores the data in **Azure PostgreSQL**.

    **Output**: Sends enriched messages to another **Service Bus Topic** for Axie detail enrichment.

3. store_axies

    **Type**: Azure Function (Python)

    **Role**:

    - Subscribed to the downstream **Service Bus Topic**.

    - Fetches Axie metadata from third-party APIs.

    - Stores Axie attributes and enriched data in the **PostgreSQL** database.

4. backend

    **Type**: Azure Web App (Python with FastAPI)

    **Role**:

    - Serves as a REST API for the frontend.

    - Interacts with PostgreSQL and **Azure Redis Cache** for fast data access (e.g., graph data on homepage).

5. frontend

    **Type**: Azure Web App (JavaScript with React)

    **Role**: User interface that fetches and displays historical sales data through the backend API.

## 🛠️ Infrastructure & DevOps
- **Database**: Azure Database for PostgreSQL Flexible Server

- **Database Management**: Liquibase (YAML format) for schema migrations and versioning.

- **Secrets Management**: Azure Key Vault

- **Message Broker**: Azure Service Bus with Topics and Subscriptions

- **Cache**: Azure Redis Cache (private endpoint, accessible only from the backend inside the VNet)

- **Monitoring**: Azure Application Insights integrated into all Azure Functions

- **Security**:


    - Azure Managed Identities are used per service to enforce least privilege access.

    - Backend and Redis are secured inside an Azure Virtual Network (VNet).

- **CI/CD**: Azure DevOps Pipelines

- **Infrastucture as Code (IaC)**: Terraform

- **Version Control**: GitHub

Azure Database for PostgreSQL does not use a private endpoint like Azure Redis Cache because the Azure Functions interacting with the database run on the Consumption plan, which does not support VNet integration. Instead, the PostgreSQL database is configured to allow connections from any Azure service. This approach provides some isolation but is not significantly more secure than allowing public access.

## 📊 Roadmap (Planned Improvements)
- Migrate the application to Kubernetes locally.

- Set up Grafana and Prometheus for monitoring.

- Implement the ELK stack (Elasticsearch, Logstash, Kibana) for centralized logging.

- Add full local development environment support using Docker.

- Complete continuous integration (CI) with tests for both backend and frontend.

- Create end-to-end tests.