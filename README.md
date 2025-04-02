# Data Engineering Workflow

This project is a modular and scalable data engineering workflow designed to handle data ingestion, transformation, and storage efficiently. It leverages modern tools and frameworks to automate processes, ensure data quality, and enable advanced querying capabilities.

## Key Features

- **Data Ingestion**: Fetch raw data from external sources (e.g., web scraping, APIs) and store it in MongoDB or Azure Blob Storage for initial processing.
- **ETL Pipelines**: Extract, transform, and load data between MongoDB/Azure Blob Storage and PostgreSQL/Azure PostgreSQL using Python-based pipelines.
- **Automation**: Orchestrate workflows and automate tasks using Prefect for seamless execution and monitoring.
- **Vectorization and Qdrant Integration**: Use Qdrant as a vector store to enable advanced vector-based querying and retrieval.
- **RAG (Retrieval-Augmented Generation)**: Integrate OpenAI's API with Qdrant to enable retrieval-augmented question answering.
- **Containerization**: Use Docker and Docker Compose to manage multi-container applications, ensuring portability and consistency across environments.
- **Azure Integration**: Optionally use Azure services for cloud-based data storage and processing.

## Tools and Technologies

- **Python**: The primary programming language for implementing ETL pipelines and automation.
- **MongoDB**: A NoSQL database for storing raw and semi-structured data.
- **PostgreSQL**: A relational database for structured data storage and querying.
- **Azure Blob Storage**: A scalable cloud storage solution for raw data ingestion.
- **Azure PostgreSQL**: A managed PostgreSQL service for structured data storage.
- **Prefect**: A workflow orchestration tool for automating and monitoring data pipelines.
- **Qdrant**: A vector database for storing and querying high-dimensional vectors.
- **OpenAI API**: For generating embeddings and enabling RAG-based question answering.
- **Docker**: For containerizing the application and managing dependencies.
- **SQLAlchemy**: For interacting with PostgreSQL in a Pythonic way.
- **BeautifulSoup**: For web scraping and parsing HTML content.
- **pandas**: For data manipulation and transformation.

## Project Structure

The project follows a modular structure to ensure maintainability and scalability:

- **`src/`**: Contains the source code for ETL pipelines, shared utilities, vectorization tasks, and RAG integration.
- **`tests/`**: Includes unit and integration tests for validating the functionality of the pipelines and utilities.
- **`docker/`**: Dockerfiles and scripts for containerizing the application.
- **`prefect/`**: Prefect flows for orchestrating and automating workflows.

## Azure Integration

This project supports Azure services for cloud-based data storage and processing. You can enable Azure integration by setting the appropriate environment variables in your `.env` file. Refer to the `env.example` file for the full list of variables.

### How to Enable Azure Integration:
1. Set `USE_AZURE=True` in your `.env` file to enable Azure Blob Storage for raw data ingestion.
2. Set `USE_AZURE_PG=True` in your `.env` file to enable Azure PostgreSQL for structured data storage.

When these options are enabled:
- Raw data will be fetched from Azure Blob Storage (with support for dynamic or manual blob selection).
- Transformed data will be loaded into Azure PostgreSQL.

If these options are set to `False`, the pipeline will default to using local MongoDB and PostgreSQL.

## Qdrant and RAG Integration

This project integrates Qdrant as a vector store and OpenAI's API for retrieval-augmented generation (RAG). The workflow includes:

1. **Vectorization**: Text data is vectorized using Sentence Transformers and stored in Qdrant.
2. **Qdrant Collection Management**: Collections are created and managed dynamically based on vector dimensions.
3. **RAG Workflow**: OpenAI's API is used to generate embeddings and answer questions by retrieving relevant vectors from Qdrant.

### How to Use RAG:
1. Ensure Qdrant is running and accessible.
2. Set the `OPENAI_API_KEY` in your `.env` file.
3. Use the `src/rag/rag_qa.py` script to ask questions and retrieve answers.

Example:
```bash
python src/rag/rag_qa.py "What are cognitive biases?"
```

## Getting Started

1. Clone the repository and navigate to the project directory.
2. Set up the environment variables by creating a `.env` file (refer to `env.example` for guidance).
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
