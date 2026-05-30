import requests
from requests.auth import HTTPBasicAuth
from common.util.export import logger, EsError, json
from common.tool.export import FileConfig, ListModel, StrModel, NumberModel, BoolModel
from typing import Optional, Iterator, Any, Dict, List
import urllib3

urllib3.disable_warnings()


class EsConfig(FileConfig):
    hosts = ListModel(default_value=["http://localhost:9200"])
    username = StrModel()
    password = StrModel()
    api_key = StrModel()
    timeout = NumberModel(default_value=30)
    verify_certs = BoolModel(default_value=False)


class EsApi:
    def __init__(self, name: str = "default"):
        self.name = name
        EsConfig.set_resource("config/setting/es.json")
        self.config: EsConfig = EsConfig.get(name)
        self._base_url = None
        self._session = None

    def _get_base_url(self) -> str:
        if self._base_url is None:
            hosts = self.config.hosts.get_value()
            if hosts:
                self._base_url = hosts[0].rstrip("/")
            else:
                self._base_url = "http://localhost:9200"
        return self._base_url

    def _get_session(self) -> requests.Session:
        if self._session is None:
            self._session = requests.Session()
            username = self.config.username.get_value()
            password = self.config.password.get_value()
            api_key = self.config.api_key.get_value()
            if api_key:
                self._session.headers["Authorization"] = f"ApiKey {api_key}"
            elif username and password:
                self._session.auth = HTTPBasicAuth(username, password)
        return self._session

    def _request(
        self,
        method: str,
        path: str,
        params: dict = None,
        data: dict = None,
        raw_data: str = None,
    ) -> dict:
        url = f"{self._get_base_url()}/{path.lstrip('/')}"
        session = self._get_session()
        timeout = self.config.timeout.get_value()
        verify = self.config.verify_certs.get_value()

        kwargs = {"timeout": timeout, "verify": verify}
        if params:
            kwargs["params"] = params
        if data:
            kwargs["json"] = data
        if raw_data:
            kwargs["data"] = raw_data
            kwargs["headers"] = {"Content-Type": "application/json"}

        try:
            resp = session.request(method, url, **kwargs)
            if resp.status_code >= 400:
                try:
                    error_body = resp.json()
                except Exception:
                    error_body = resp.text
                raise EsError(
                    f"ES request failed: {resp.status_code}",
                    context={"url": url, "error": error_body},
                )
            if resp.status_code == 204:
                return {}
            return resp.json()
        except requests.exceptions.RequestException as e:
            raise EsError(f"ES request error: {e}", context=str(e))

    def close(self):
        if self._session is not None:
            self._session.close()
            self._session = None

    def ping(self) -> bool:
        try:
            result = self._request("GET", "/")
            return "version" in result
        except EsError:
            return False

    def info(self) -> dict:
        return self._request("GET", "/")

    def create_index(self, index: str, mapping: dict = None, settings: dict = None):
        body = {}
        if settings:
            body["settings"] = settings
        if mapping:
            body["mappings"] = mapping
        return self._request("PUT", index, data=body if body else None)

    def delete_index(self, index: str):
        return self._request("DELETE", index)

    def index_exists(self, index: str) -> bool:
        try:
            result = self._request("GET", f"{index}/_settings")
            return index in result or bool(result)
        except EsError as e:
            if "404" in str(e) or "index_not_found" in str(e):
                return False
            raise

    def get_mapping(self, index: str) -> dict:
        return self._request("GET", f"{index}/_mapping")

    def put_mapping(self, index: str, mapping: dict):
        return self._request("PUT", f"{index}/_mapping", data=mapping)

    def get_settings(self, index: str) -> dict:
        return self._request("GET", f"{index}/_settings")

    def put_settings(self, index: str, settings: dict):
        return self._request("PUT", f"{index}/_settings", data=settings)

    def index_doc(
        self, index: str, body: dict, id: str = None, refresh: bool = False
    ) -> dict:
        path = f"{index}/_doc"
        if id:
            path = f"{index}/_doc/{id}"
        params = {}
        if refresh:
            params["refresh"] = "true"
        return self._request("POST", path, params=params, data=body)

    def get_doc(self, index: str, id: str, source_includes: list = None) -> Optional[dict]:
        params = {}
        if source_includes:
            params["_source_includes"] = ",".join(source_includes)
        try:
            result = self._request("GET", f"{index}/_doc/{id}", params=params)
            if result.get("found", False):
                return {"id": result["_id"], "source": result.get("_source", {})}
            return None
        except EsError as e:
            if "404" in str(e):
                return None
            raise

    def update_doc(self, index: str, id: str, body: dict, refresh: bool = False):
        params = {}
        if refresh:
            params["refresh"] = "true"
        return self._request("POST", f"{index}/_update/{id}", params=params, data=body)

    def delete_doc(self, index: str, id: str, refresh: bool = False):
        params = {}
        if refresh:
            params["refresh"] = "true"
        return self._request("DELETE", f"{index}/_doc/{id}", params=params)

    def mget_docs(self, index: str, ids: list, source_includes: list = None) -> list:
        body = {"ids": ids}
        params = {}
        if source_includes:
            params["_source_includes"] = ",".join(source_includes)
        result = self._request("GET", f"{index}/_mget", params=params, data=body)
        docs = []
        for doc in result.get("docs", []):
            if doc.get("found", False):
                docs.append({"id": doc["_id"], "source": doc.get("_source", {})})
        return docs

    def bulk(self, actions: list) -> dict:
        if not actions:
            return {"errors": False, "items": []}
        lines = []
        for action in actions:
            op_type = action.get("_op_type", "index")
            meta = {"_index": action["_index"]}
            if "_id" in action:
                meta["_id"] = action["_id"]
            lines.append(json.dumps({op_type: meta}))
            if op_type in ("index", "create"):
                lines.append(json.dumps(action.get("_source", {})))
            elif op_type == "update":
                lines.append(json.dumps({"doc": action.get("doc", {})}))
        bulk_data = "\n".join(lines) + "\n"
        return self._request("POST", "_bulk", raw_data=bulk_data)

    def bulk_index(self, index: str, docs: list, id_field: str = "id") -> dict:
        actions = []
        for doc in docs:
            doc_id = doc.get(id_field)
            action = {"_index": index, "_source": doc}
            if doc_id:
                action["_id"] = doc_id
            actions.append(action)
        return self.bulk(actions)

    def bulk_update(self, index: str, docs: list, id_field: str = "id") -> dict:
        actions = []
        for doc in docs:
            doc_id = doc.get(id_field)
            if not doc_id:
                continue
            update_doc = {k: v for k, v in doc.items() if k != id_field}
            actions.append(
                {"_op_type": "update", "_index": index, "_id": doc_id, "doc": update_doc}
            )
        return self.bulk(actions)

    def bulk_delete(self, index: str, ids: list) -> dict:
        actions = [
            {"_op_type": "delete", "_index": index, "_id": doc_id} for doc_id in ids
        ]
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
        body = {"query": query, "size": size, "from": from_}
        if source:
            body["_source"] = source
        if sort:
            body["sort"] = sort
        return self._request("POST", f"{index}/_search", data=body)

    def count(self, index: str, query: dict = None) -> int:
        body = {}
        if query:
            body["query"] = query
        result = self._request("POST", f"{index}/_count", data=body)
        return result.get("count", 0)

    def scroll_iter(
        self, index: str, query: dict = None, scroll: str = "2m", size: int = 1000
    ) -> Iterator[dict]:
        body = {"size": size}
        if query:
            body["query"] = query
        result = self._request(
            "POST", f"{index}/_search", params={"scroll": scroll}, data=body
        )
        scroll_id = result.get("_scroll_id")
        hits = result.get("hits", {}).get("hits", [])

        for hit in hits:
            yield {"id": hit["_id"], "source": hit.get("_source", {}), "score": hit.get("_score")}

        while hits:
            result = self._request(
                "POST", "_search/scroll", params={"scroll": scroll}, data={"scroll_id": scroll_id}
            )
            scroll_id = result.get("_scroll_id")
            hits = result.get("hits", {}).get("hits", [])
            for hit in hits:
                yield {"id": hit["_id"], "source": hit.get("_source", {}), "score": hit.get("_score")}

        self.clear_scroll(scroll_id)

    def scroll_all(
        self, index: str, query: dict = None, scroll: str = "2m", size: int = 1000
    ) -> list:
        return list(self.scroll_iter(index, query, scroll, size))

    def clear_scroll(self, scroll_id: str):
        try:
            self._request("DELETE", "_search/scroll", data={"scroll_id": scroll_id})
        except EsError as e:
            logger.error(f"Failed to clear scroll: {e}")

    def aggregate(self, index: str, aggs: dict, query: dict = None, size: int = 0) -> dict:
        body = {"aggs": aggs, "size": size}
        if query:
            body["query"] = query
        result = self._request("POST", f"{index}/_search", data=body)
        return result.get("aggregations", {})

    def refresh(self, index: str):
        return self._request("POST", f"{index}/_refresh")

    def aliases(self, index: str) -> dict:
        return self._request("GET", f"{index}/_alias")

    def put_alias(self, index: str, alias: str):
        return self._request("PUT", f"{index}/_alias/{alias}")

    def delete_alias(self, index: str, alias: str):
        return self._request("DELETE", f"{index}/_alias/{alias}")

    def reindex(self, source: str, dest: str) -> dict:
        body = {"source": {"index": source}, "dest": {"index": dest}}
        return self._request("POST", "_reindex", data=body)

    def cat_indices(self, format: str = "json") -> list:
        result = self._request("GET", "_cat/indices", params={"format": format})
        return result if isinstance(result, list) else []

    def delete_by_query(self, index: str, query: dict) -> dict:
        return self._request("POST", f"{index}/_delete_by_query", data={"query": query})

    def cluster_health(self) -> dict:
        return self._request("GET", "_cluster/health")

    def cluster_state(self) -> dict:
        return self._request("GET", "_cluster/state")

    def node_stats(self) -> dict:
        return self._request("GET", "_nodes/stats")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False