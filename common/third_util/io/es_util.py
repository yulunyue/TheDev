from common.util.export import logger, File, List, Dict, EsError
from common.tool.export import FileConfig, ListModel, StrModel, NumberModel, BoolModel
from typing import Optional, Iterator, Any


class EsConfig(FileConfig):
    hosts = ListModel(default_value=["http://localhost:9200"])
    username = StrModel()
    password = StrModel()
    api_key = StrModel()
    timeout = NumberModel(default_value=30)
    max_retries = NumberModel(default_value=3)
    verify_certs = BoolModel(default_value=False)
    verify_version = BoolModel(default_value=False)


class EsUtil:
    def __init__(self, name: str = "default"):
        self.name = name
        EsConfig.set_resource("config/setting/es.json")
        self.config: EsConfig = EsConfig.get(name)
        self._client = None

    def get_client(self):
        if self._client is None:
            self._client = self._create_client()
        return self._client

    def _create_client(self):
        try:
            from elasticsearch import Elasticsearch
            import elasticsearch
            version_info = elasticsearch.__version__
            if isinstance(version_info, tuple):
                es_version = version_info[0]
            else:
                es_version = int(str(version_info).split(".")[0])
        except ImportError:
            raise EsError("elasticsearch library not installed. Run: pip install elasticsearch")

        hosts = self.config.hosts.get_value()
        if not hosts:
            hosts = ["http://localhost:9200"]

        kwargs = {
            "hosts": hosts,
        }

        timeout = self.config.timeout.get_value()
        max_retries = self.config.max_retries.get_value()

        if es_version >= 8:
            kwargs["request_timeout"] = timeout
            kwargs["max_retries"] = max_retries
        else:
            kwargs["timeout"] = timeout
            kwargs["max_retries"] = max_retries

        api_key = self.config.api_key.get_value()
        if api_key:
            if es_version >= 8:
                kwargs["api_key"] = api_key
            else:
                kwargs["api_key"] = api_key
        else:
            username = self.config.username.get_value()
            password = self.config.password.get_value()
            if username and password:
                if es_version >= 8:
                    kwargs["basic_auth"] = (username, password)
                else:
                    kwargs["http_auth"] = (username, password)

        verify_certs = self.config.verify_certs.get_value()
        if not verify_certs:
            kwargs["verify_certs"] = False

        verify_version = self.config.verify_version.get_value()
        if not verify_version and es_version >= 7:
            kwargs["verify_elasticsearch"] = False
            kwargs["verify_server_version"] = False

        try:
            client = Elasticsearch(**kwargs)
            return client
        except Exception as e:
            raise EsError(f"Failed to create ES client: {e}", context=str(e))

    def close(self):
        if self._client is not None:
            try:
                self._client.close()
            except Exception as e:
                logger.error(f"Error closing ES client: {e}")
            finally:
                self._client = None

    def create_index(self, index: str, mapping: dict = None, settings: dict = None):
        body = {}
        if settings:
            body["settings"] = settings
        if mapping:
            body["mappings"] = mapping

        client = self.get_client()
        try:
            if body:
                return client.indices.create(index=index, body=body)
            return client.indices.create(index=index)
        except Exception as e:
            raise EsError(f"Failed to create index '{index}': {e}", context=str(e))

    def delete_index(self, index: str):
        client = self.get_client()
        try:
            return client.indices.delete(index=index)
        except Exception as e:
            raise EsError(f"Failed to delete index '{index}': {e}", context=str(e))

    def index_exists(self, index: str) -> bool:
        client = self.get_client()
        try:
            return client.indices.exists(index=index)
        except Exception as e:
            raise EsError(f"Failed to check index '{index}': {e}", context=str(e))

    def get_mapping(self, index: str) -> dict:
        client = self.get_client()
        try:
            result = client.indices.get_mapping(index=index)
            return result.body if hasattr(result, "body") else result
        except Exception as e:
            raise EsError(f"Failed to get mapping for '{index}': {e}", context=str(e))

    def put_mapping(self, index: str, mapping: dict):
        client = self.get_client()
        try:
            return client.indices.put_mapping(index=index, body=mapping)
        except Exception as e:
            raise EsError(f"Failed to put mapping for '{index}': {e}", context=str(e))

    def get_settings(self, index: str) -> dict:
        client = self.get_client()
        try:
            result = client.indices.get_settings(index=index)
            return result.body if hasattr(result, "body") else result
        except Exception as e:
            raise EsError(f"Failed to get settings for '{index}': {e}", context=str(e))

    def put_settings(self, index: str, settings: dict):
        client = self.get_client()
        try:
            return client.indices.put_settings(index=index, body=settings)
        except Exception as e:
            raise EsError(f"Failed to put settings for '{index}': {e}", context=str(e))

    def index_doc(self, index: str, body: dict, id: str = None, refresh: bool = False):
        client = self.get_client()
        try:
            kwargs = {"index": index, "document": body}
            if id:
                kwargs["id"] = id
            if refresh:
                kwargs["refresh"] = refresh
            return client.index(**kwargs)
        except Exception as e:
            raise EsError(f"Failed to index document in '{index}': {e}", context=str(e))

    def get_doc(self, index: str, id: str, source_includes: list = None) -> Optional[dict]:
        client = self.get_client()
        try:
            kwargs = {"index": index, "id": id}
            if source_includes:
                kwargs["_source_includes"] = source_includes
            result = client.get(**kwargs)
            if result.get("found", False):
                doc = {"id": result["_id"], "source": result.get("_source", {})}
                return doc
            return None
        except Exception as e:
            if "NotFoundError" in str(type(e).__name__):
                return None
            raise EsError(f"Failed to get document '{id}' from '{index}': {e}", context=str(e))

    def update_doc(self, index: str, id: str, body: dict, refresh: bool = False):
        client = self.get_client()
        try:
            kwargs = {"index": index, "id": id, "body": body}
            if refresh:
                kwargs["refresh"] = refresh
            return client.update(**kwargs)
        except Exception as e:
            raise EsError(f"Failed to update document '{id}' in '{index}': {e}", context=str(e))

    def delete_doc(self, index: str, id: str, refresh: bool = False):
        client = self.get_client()
        try:
            kwargs = {"index": index, "id": id}
            if refresh:
                kwargs["refresh"] = refresh
            return client.delete(**kwargs)
        except Exception as e:
            raise EsError(f"Failed to delete document '{id}' from '{index}': {e}", context=str(e))

    def mget_docs(self, index: str, ids: list, source_includes: list = None) -> list:
        client = self.get_client()
        try:
            kwargs = {"index": index, "ids": ids}
            if source_includes:
                kwargs["_source_includes"] = source_includes
            result = client.mget(**kwargs)
            docs = []
            for doc in result.get("docs", []):
                if doc.get("found", False):
                    docs.append({"id": doc["_id"], "source": doc.get("_source", {})})
            return docs
        except Exception as e:
            raise EsError(f"Failed to mget documents from '{index}': {e}", context=str(e))

    def bulk(self, actions: list):
        if not actions:
            return None

        client = self.get_client()
        try:
            from elasticsearch.helpers import bulk as es_bulk

            return es_bulk(client, actions)
        except Exception as e:
            raise EsError(f"Bulk operation failed: {e}", context=str(e))

    def bulk_index(self, index: str, docs: list, id_field: str = "id"):
        actions = []
        for doc in docs:
            doc_id = doc.get(id_field)
            action = {"_index": index, "_source": doc}
            if doc_id:
                action["_id"] = doc_id
            actions.append(action)
        return self.bulk(actions)

    def bulk_update(self, index: str, docs: list, id_field: str = "id"):
        actions = []
        for doc in docs:
            doc_id = doc.get(id_field)
            if not doc_id:
                continue
            actions.append(
                {
                    "_op_type": "update",
                    "_index": index,
                    "_id": doc_id,
                    "doc": doc,
                }
            )
        return self.bulk(actions)

    def bulk_delete(self, index: str, ids: list):
        actions = [{"_op_type": "delete", "_index": index, "_id": doc_id} for doc_id in ids]
        return self.bulk(actions)

    def search(
        self,
        index: str,
        query: dict,
        source: list = None,
        sort: list = None,
        size: int = 10,
        from_: int = 0,
    ) -> dict:
        client = self.get_client()
        try:
            kwargs = {"index": index, "query": query, "size": size, "from_": from_}
            if source:
                kwargs["_source"] = source
            if sort:
                kwargs["sort"] = sort
            result = client.search(**kwargs)
            return result.body if hasattr(result, "body") else result
        except Exception as e:
            raise EsError(f"Search failed on '{index}': {e}", context=str(e))

    def count(self, index: str, query: dict = None) -> int:
        client = self.get_client()
        try:
            kwargs = {"index": index}
            if query:
                kwargs["query"] = query
            result = client.count(**kwargs)
            return result.get("count", 0)
        except Exception as e:
            raise EsError(f"Count failed on '{index}': {e}", context=str(e))

    def scroll_iter(
        self,
        index: str,
        query: dict = None,
        scroll: str = "2m",
        size: int = 1000,
    ) -> Iterator[dict]:
        client = self.get_client()
        try:
            kwargs = {"index": index, "scroll": scroll, "size": size}
            if query:
                kwargs["query"] = query

            result = client.search(**kwargs)
            scroll_id = result.get("_scroll_id")
            hits = result.get("hits", {}).get("hits", [])

            for hit in hits:
                yield {"id": hit["_id"], "source": hit.get("_source", {}), "score": hit.get("_score")}

            while hits:
                result = client.scroll(scroll_id=scroll_id, scroll=scroll)
                scroll_id = result.get("_scroll_id")
                hits = result.get("hits", {}).get("hits", [])

                for hit in hits:
                    yield {"id": hit["_id"], "source": hit.get("_source", {}), "score": hit.get("_score")}

            self.clear_scroll(scroll_id)
        except Exception as e:
            raise EsError(f"Scroll failed on '{index}': {e}", context=str(e))

    def scroll_all(
        self,
        index: str,
        query: dict = None,
        scroll: str = "2m",
        size: int = 1000,
    ) -> list:
        return list(self.scroll_iter(index, query, scroll, size))

    def clear_scroll(self, scroll_id: str):
        client = self.get_client()
        try:
            return client.clear_scroll(scroll_id=scroll_id)
        except Exception as e:
            logger.error(f"Failed to clear scroll {scroll_id}: {e}")

    def aggregate(self, index: str, aggs: dict, query: dict = None, size: int = 0) -> dict:
        client = self.get_client()
        try:
            kwargs = {"index": index, "aggs": aggs, "size": size}
            if query:
                kwargs["query"] = query
            result = client.search(**kwargs)
            return result.get("aggregations", {})
        except Exception as e:
            raise EsError(f"Aggregation failed on '{index}': {e}", context=str(e))

    def refresh(self, index: str):
        client = self.get_client()
        try:
            return client.indices.refresh(index=index)
        except Exception as e:
            raise EsError(f"Failed to refresh index '{index}': {e}", context=str(e))

    def aliases(self, index: str) -> dict:
        client = self.get_client()
        try:
            result = client.indices.get_alias(index=index)
            return result.body if hasattr(result, "body") else result
        except Exception as e:
            raise EsError(f"Failed to get aliases for '{index}': {e}", context=str(e))

    def put_alias(self, index: str, alias: str):
        client = self.get_client()
        try:
            return client.indices.put_alias(index=index, name=alias)
        except Exception as e:
            raise EsError(f"Failed to put alias '{alias}' for '{index}': {e}", context=str(e))

    def delete_alias(self, index: str, alias: str):
        client = self.get_client()
        try:
            return client.indices.delete_alias(index=index, name=alias)
        except Exception as e:
            raise EsError(f"Failed to delete alias '{alias}' from '{index}': {e}", context=str(e))

    def reindex(self, source: str, dest: str) -> dict:
        client = self.get_client()
        try:
            body = {"source": {"index": source}, "dest": {"index": dest}}
            result = client.reindex(body=body)
            return result.body if hasattr(result, "body") else result
        except Exception as e:
            raise EsError(f"Reindex failed from '{source}' to '{dest}': {e}", context=str(e))

    def cat_indices(self, format: str = "json") -> list:
        client = self.get_client()
        try:
            result = client.cat.indices(format=format)
            if isinstance(result, str):
                import json

                return json.loads(result)
            return result
        except Exception as e:
            raise EsError(f"Failed to list indices: {e}", context=str(e))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False