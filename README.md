# Data Engineering Workflow

This project is a modular and scalable data engineering workflow designed to handle data ingestion, transformation, and storage efficiently. It leverages modern tools and frameworks to automate processes, ensure data quality, and enable advanced querying capabilities.

## Key Features

- **Data Ingestion**: Fetch raw data from external sources (e.g., web scraping, APIs) and store it in MongoDB for initial processing.
- **ETL Pipelines**: Extract, transform, and load data between MongoDB and PostgreSQL using Python-based pipelines.
- **Automation**: Orchestrate workflows and automate tasks using Prefect for seamless execution and monitoring.
- **Containerization**: Use Docker and Docker Compose to manage multi-container applications, ensuring portability and consistency across environments.

## Tools and Technologies

- **Python**: The primary programming language for implementing ETL pipelines and automation.
- **MongoDB**: A NoSQL database for storing raw and semi-structured data.
- **PostgreSQL**: A relational database for structured data storage and querying.
- **Prefect**: A workflow orchestration tool for automating and monitoring data pipelines.
- **Docker**: For containerizing the application and managing dependencies.
- **SQLAlchemy**: For interacting with PostgreSQL in a Pythonic way.
- **BeautifulSoup**: For web scraping and parsing HTML content.
- **pandas**: For data manipulation and transformation.

## Project Structure

The project follows a modular structure to ensure maintainability and scalability:

- **`src/`**: Contains the source code for ETL pipelines, shared utilities, and vectorization tasks.
- **`tests/`**: Includes unit and integration tests for validating the functionality of the pipelines and utilities.
- **`docker/`**: Dockerfiles and scripts for containerizing the application.
- **`prefect/`**: Prefect flows for orchestrating and automating workflows.

## Getting Started

1. Clone the repository and navigate to the project directory.
2. Set up the environment variables by creating a `.env` file (refer to `.env.example` for guidance).
3. Use Docker Compose to spin up the required services (MongoDB, PostgreSQL, Prefect, etc.).
4. Run the Prefect flows or individual scripts to execute the data pipelines.

## Future Enhancements

- Add support for additional data sources and pipelines.
- Enhance monitoring and logging for better observability.
- Optimize performance for large-scale data processing.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the project.

## License

This project is licensed under the [MIT License](LICENSE). See the [LICENSE](LICENSE) file for details.
