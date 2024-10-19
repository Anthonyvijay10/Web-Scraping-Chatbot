from pymilvus import Collection, connections, utility
from pymilvus import DataType, FieldSchema, CollectionSchema
import os

class MilvusHandler:

    def __init__(self):

        self.host = os.getenv("MILVUS_HOST", "localhost")

        self.port = os.getenv("MILVUS_PORT", 19530)

        self.collection_name = "wikipedia_content"

        self.collection = None

        self.connect()

        self.create_collection()


    def connect(self):

        connections.connect(host=self.host, port=self.port)

    def create_collection(self):

        if utility.has_collection(self.collection_name):
            self.collection = Collection(self.collection_name)

            return


        fields = [

            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),

            FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=65535),

            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384)

        ]

        schema = CollectionSchema(fields, description="Wikipedia content")

        self.collection = Collection(self.collection_name, schema)

        self.collection.create_index(field_name="embedding", index_params={"index_type": "IVF_FLAT", "metric_type": "L2", "params": {"nlist": 1024}})

        # Load the collection into memory
        self.collection.load()


    def insert_data(self, data):

        if self.collection is None:

            raise ValueError("Collection not initialized. Call create_collection() first.")
        

        contents, embeddings = zip(*data)

        entities = [

            {"content": content, "embedding": embedding}

            for content, embedding in zip(contents, embeddings)

        ]

        self.collection.insert(entities)
        self.collection.flush()


    def search(self, query_vector, top_k=5):

        if self.collection is None:

            raise ValueError("Collection not initialized. Call create_collection() first.")
        

        # Load the collection if not already loaded
        self.collection.load()

        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}

        results = self.collection.search(

            data=[query_vector],
            anns_field="embedding",

            param=search_params,

            limit=top_k,

            output_fields=["content"]

        )

        return [(hit.entity.get('content'), hit.distance) for hit in results[0]]


    def __del__(self):

        if connections.has_connection():

            connections.disconnect(alias="default")
