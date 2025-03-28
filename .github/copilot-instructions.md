## Guidelines

- **Project Structure**: Follow the outlined directory structure for organizing data ingestion, ETL processes, automation, and vectorization tasks.

- **Docker**: Use Docker Compose to manage multi-container applications. Ensure that each service has a corresponding Dockerfile.

- **Environment Variables**: Store sensitive data in a `.env` file and reference them in your scripts to maintain security.

- **Languages and Tools**: Python is the primary language. Use libraries and frameworks relevant to data engineering, such as pandas for ETL processes and libraries compatible with your chosen vector store like Qdrant.

- **Workflow**: The project involves fetching raw data, ETL processes between MongoDB and PostgreSQL, automating with Prefect, and integrating a vector store for enhanced data querying.

- **Error Handling**: Use `try` and `except` blocks to catch and handle errors gracefully in your Python scripts. Ensure that meaningful error messages are logged for debugging purposes using the `logging` module.

- **Modular Programming**: Follow the principles of modular programming by breaking down the code into separate, interchangeable modules. Each module should contain everything necessary to execute only one aspect of the desired functionality. This promotes code reuse, maintainability, and ease of debugging. Avoid copying code across files; instead, create reusable modules and import them as needed.

Follow these guidelines to maintain a consistent and organized codebase throughout the project.
