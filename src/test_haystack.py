#%%
import glob

from haystack import Pipeline
from haystack.components.converters import MarkdownToDocument
from haystack.components.embedders import SentenceTransformersDocumentEmbedder, SentenceTransformersTextEmbedder
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.writers import DocumentWriter
from haystack_integrations.components.retrievers.pgvector import PgvectorEmbeddingRetriever
from haystack_integrations.document_stores.pgvector import PgvectorDocumentStore

# Set an environment variable `PG_CONN_STR` with the connection string to your PostgreSQL database.
# e.g., "postgresql://USER:PASSWORD@HOST:PORT/DB_NAME"

# Initialize PgvectorDocumentStore
document_store = PgvectorDocumentStore(
    table_name="haystack_test",
    embedding_dimension=768,
    vector_function="cosine_similarity",
    recreate_table=True,
    search_strategy="hnsw",
)

# Create the indexing Pipeline and index some documents
file_paths = glob.glob("../neural-search-pills/pills/*.md")


indexing = Pipeline()
indexing.add_component("converter", MarkdownToDocument())
indexing.add_component("splitter", DocumentSplitter(split_by="sentence", split_length=2))
indexing.add_component("embedder", SentenceTransformersDocumentEmbedder())
indexing.add_component("writer", DocumentWriter(document_store))
indexing.connect("converter", "splitter")
indexing.connect("splitter", "embedder")
indexing.connect("embedder", "writer")

indexing.run({"converter": {"sources": file_paths}})

# Create the querying Pipeline and try a query
querying = Pipeline()
querying.add_component("embedder", SentenceTransformersTextEmbedder())
querying.add_component("retriever", PgvectorEmbeddingRetriever(document_store=document_store, top_k=3))
querying.connect("embedder", "retriever")

results = querying.run({"embedder": {"text": "What is a cross-encoder?"}})

for doc in results["retriever"]["documents"]:
    print(doc)
    print("-" * 10)
# %%
