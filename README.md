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

## Neo4j Graph Storage & Automated Bias Detection

This project now includes an automated pipeline for cognitive bias detection and graph storage using Neo4j.

### How It Works

- **Automated Script:**  
  The script at `src/graph/automate_bias_detection.py` sends articles to the RAG/LLM backend, receives structured bias analysis, parses the results, and writes them to Neo4j as a knowledge graph.
- **Graph Schema:**  
  - **Article** nodes represent ingested articles.
  - **Bias** nodes represent detected cognitive biases.
  - **HAS_BIAS** relationships connect articles to biases, with properties for explanation and justification.

### How to Use

1. **Set up your environment variables** in `.env`:
   ```
   NEXT_PUBLIC_FASTAPI_URL=http://localhost:8000      # or your FastAPI backend URL
   NEO4J_URI=bolt://localhost:7687                    # or bolt://neo4j:7687 if running in Docker
   NEO4J_AUTH=neo4j/your_secure_password              # your Neo4j credentials
   ```
2. **Ensure Neo4j and your FastAPI backend are running.**
3. **Run the automation script:**
   ```bash
   python src/graph/automate_bias_detection.py
   ```
4. **View results in Neo4j:**
   - Open [http://localhost:7474](http://localhost:7474) and log in.
   - Run:
     ```cypher
     MATCH (a:Article)-[r:HAS_BIAS]->(b:Bias)
     RETURN a, r, b
     ```
   - Explore the graph and relationship properties.

### Why Neo4j?

Neo4j enables advanced querying and visualization of relationships between articles and detected biases, supporting deeper analysis and insights.

## Chat UI

The project includes a modern web-based chat interface built with Next.js for interacting with the RAG system. The chat UI provides a user-friendly way to ask questions and receive answers from the RAG system.

### Features:
- Real-time chat interface
- Modern, responsive design
- Direct integration with the RAG backend
- Error handling and loading states

### How to Use the Chat UI:
1. Ensure all services are running (FastAPI, Qdrant, etc.)
2. Access the chat interface at `http://localhost:3000`
3. Type your question and press Enter or click the send button
4. View the AI's response in the chat interface

![Classify Bias Screenshot](screenshots/classify-bias.png)

The chat UI communicates with the FastAPI backend, which processes questions using the RAG system and returns answers in real-time.

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

This project is licensed under the [GNU Affero General Public License v3.0](LICENSE). See the [LICENSE](LICENSE) file for details.
