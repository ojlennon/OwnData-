from qdrant_client import QdrantClient

class QdrantManager:
    def __init__(self, host: str = "localhost", port: int = 6333):
        self.client = QdrantClient(host=host, port=port)

    def get_collection(self, collection_name: str):
        try:
            return self.client.get_collection(collection_name)
        except Exception as e:
            return {"error": str(e)}, 500

    def add_document(self, collection_name: str, document: dict):
        try:
            return self.client.upsert(collection_name, [document])
        except Exception as e:
            return {"error": str(e)}, 500
        
    def get_closest_field(self, collection_name: str, field_name: str):
        try:
            return self.client.search(collection_name, field_name)
        except Exception as e:
            return {"error": str(e)}, 500