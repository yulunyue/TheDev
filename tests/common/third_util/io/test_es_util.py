import time
from common.util.export import TestBase, EsError
from common.third_util.io.es_util import EsUtil, EsConfig


class TestEsConfig(TestBase):
    def test_default_config(self):
        EsConfig.set_resource("config/setting/es.json")
        config = EsConfig.get("default")
        hosts = config.hosts.get_value()
        self.expect(hosts is not None, True)

    def test_config_values(self):
        EsConfig.set_resource("config/setting/es.json")
        config = EsConfig.get("default")
        self.expect(isinstance(config.hosts.get_value(), list), True)
        self.expect(isinstance(config.timeout.get_value(), (int, float)), True)


class TestEsConnection(TestBase):
    def setup_method(self):
        self.es = EsUtil("default")

    def teardown_method(self):
        if hasattr(self, "es") and self.es:
            self.es.close()

    def test_connect(self):
        client = self.es.get_client()
        self.expect(client is not None, True)

    def test_close(self):
        self.es.get_client()
        self.es.close()
        self.expect(self.es._client is None, True)


class TestEsIndex(TestBase):
    @classmethod
    def setup_class(cls):
        cls.es = EsUtil("default")
        cls.index_name = f"test_index_{int(time.time() * 1000)}"

    @classmethod
    def teardown_class(cls):
        if hasattr(cls, "es") and cls.es:
            try:
                if cls.es.index_exists(cls.index_name):
                    cls.es.delete_index(cls.index_name)
            except Exception:
                pass
            cls.es.close()

    def test_create_index(self):
        result = self.es.create_index(self.index_name)
        self.expect(result is not None, True)

    def test_index_exists(self):
        if not self.es.index_exists(self.index_name):
            self.es.create_index(self.index_name)
        exists = self.es.index_exists(self.index_name)
        self.expect(exists in [True, True.body], True)

    def test_get_mapping(self):
        if not self.es.index_exists(self.index_name):
            self.es.create_index(self.index_name)
        mapping = self.es.get_mapping(self.index_name)
        self.expect(mapping is not None, True)

    def test_delete_index(self):
        if not self.es.index_exists(self.index_name):
            self.es.create_index(self.index_name)
        result = self.es.delete_index(self.index_name)
        self.expect(result is not None, True)


class TestEsDoc(TestBase):
    @classmethod
    def setup_class(cls):
        cls.es = EsUtil("default")
        cls.index_name = f"test_doc_{int(time.time() * 1000)}"
        cls.es.create_index(cls.index_name)

    @classmethod
    def teardown_class(cls):
        if hasattr(cls, "es") and cls.es:
            try:
                if cls.es.index_exists(cls.index_name):
                    cls.es.delete_index(cls.index_name)
            except Exception:
                pass
            cls.es.close()

    def test_index_doc(self):
        doc = {"name": "test", "value": 123}
        result = self.es.index_doc(self.index_name, doc, id="1", refresh=True)
        self.expect(result is not None, True)

    def test_get_doc(self):
        doc = {"name": "get_test", "value": 456}
        self.es.index_doc(self.index_name, doc, id="2", refresh=True)
        result = self.es.get_doc(self.index_name, "2")
        self.expect(result is not None, True)
        self.expect(result["id"] == "2", True)
        self.expect(result["source"]["name"] == "get_test", True)

    def test_get_doc_not_found(self):
        result = self.es.get_doc(self.index_name, "not_exist_id")
        self.expect(result is None, True)

    def test_update_doc(self):
        self.es.index_doc(self.index_name, {"name": "old"}, id="3", refresh=True)
        self.es.update_doc(self.index_name, "3", {"doc": {"name": "new"}}, refresh=True)
        result = self.es.get_doc(self.index_name, "3")
        self.expect(result["source"]["name"] == "new", True)

    def test_delete_doc(self):
        self.es.index_doc(self.index_name, {"name": "to_delete"}, id="4", refresh=True)
        self.es.delete_doc(self.index_name, "4", refresh=True)
        result = self.es.get_doc(self.index_name, "4")
        self.expect(result is None, True)

    def test_mget_docs(self):
        self.es.index_doc(self.index_name, {"name": "mget1"}, id="m1", refresh=True)
        self.es.index_doc(self.index_name, {"name": "mget2"}, id="m2", refresh=True)
        results = self.es.mget_docs(self.index_name, ["m1", "m2"])
        self.expect(len(results) == 2, True)


class TestEsBulk(TestBase):
    @classmethod
    def setup_class(cls):
        cls.es = EsUtil("default")
        cls.index_name = f"test_bulk_{int(time.time() * 1000)}"
        cls.es.create_index(cls.index_name)

    @classmethod
    def teardown_class(cls):
        if hasattr(cls, "es") and cls.es:
            try:
                if cls.es.index_exists(cls.index_name):
                    cls.es.delete_index(cls.index_name)
            except Exception:
                pass
            cls.es.close()

    def test_bulk_index(self):
        docs = [{"id": f"bulk_{i}", "name": f"doc_{i}"} for i in range(10)]
        success, failed = self.es.bulk_index(self.index_name, docs, id_field="id")
        self.es.refresh(self.index_name)
        self.expect(failed == 0, True)

    def test_bulk_update(self):
        docs = [{"id": f"update_{i}", "name": f"updated_{i}"} for i in range(5)]
        self.es.bulk_index(self.index_name, docs, id_field="id")
        updates = [{"id": f"update_{i}", "name": f"new_{i}"} for i in range(5)]
        self.es.bulk_update(self.index_name, updates, id_field="id")
        self.es.refresh(self.index_name)
        doc = self.es.get_doc(self.index_name, "update_0")
        self.expect(doc["source"]["name"] == "new_0", True)

    def test_bulk_delete(self):
        docs = [{"id": f"del_{i}", "name": f"to_delete_{i}"} for i in range(3)]
        self.es.bulk_index(self.index_name, docs, id_field="id")
        self.es.refresh(self.index_name)
        self.es.bulk_delete(self.index_name, ["del_0", "del_1", "del_2"])
        self.es.refresh(self.index_name)
        for i in range(3):
            doc = self.es.get_doc(self.index_name, f"del_{i}")
            self.expect(doc is None, True)


class TestEsSearch(TestBase):
    @classmethod
    def setup_class(cls):
        cls.es = EsUtil("default")
        cls.index_name = f"test_search_{int(time.time() * 1000)}"
        cls.es.create_index(cls.index_name)
        docs = [{"id": f"search_{i}", "name": f"doc_{i}", "value": i} for i in range(20)]
        cls.es.bulk_index(cls.index_name, docs, id_field="id")
        cls.es.refresh(cls.index_name)

    @classmethod
    def teardown_class(cls):
        if hasattr(cls, "es") and cls.es:
            try:
                if cls.es.index_exists(cls.index_name):
                    cls.es.delete_index(cls.index_name)
            except Exception:
                pass
            cls.es.close()

    def test_search(self):
        query = {"match_all": {}}
        result = self.es.search(self.index_name, query, size=5)
        hits = result.get("hits", {}).get("hits", [])
        self.expect(len(hits) == 5, True)

    def test_search_with_query(self):
        query = {"match": {"name": "doc_1"}}
        result = self.es.search(self.index_name, query)
        hits = result.get("hits", {}).get("hits", [])
        self.expect(len(hits) > 0, True)

    def test_count(self):
        count = self.es.count(self.index_name)
        self.expect(count == 20, True)

    def test_scroll_iter(self):
        query = {"match_all": {}}
        docs = list(self.es.scroll_iter(self.index_name, query, size=5))
        self.expect(len(docs) == 20, True)

    def test_scroll_all(self):
        query = {"match_all": {}}
        docs = self.es.scroll_all(self.index_name, query, size=5)
        self.expect(len(docs) == 20, True)


class TestEsAggs(TestBase):
    @classmethod
    def setup_class(cls):
        cls.es = EsUtil("default")
        cls.index_name = f"test_aggs_{int(time.time() * 1000)}"
        cls.es.create_index(cls.index_name)
        docs = [{"id": f"aggs_{i}", "category": f"cat_{i % 3}", "value": i} for i in range(10)]
        cls.es.bulk_index(cls.index_name, docs, id_field="id")
        cls.es.refresh(cls.index_name)

    @classmethod
    def teardown_class(cls):
        if hasattr(cls, "es") and cls.es:
            try:
                if cls.es.index_exists(cls.index_name):
                    cls.es.delete_index(cls.index_name)
            except Exception:
                pass
            cls.es.close()

    def test_aggregate(self):
        aggs = {"avg_value": {"avg": {"field": "value"}}}
        result = self.es.aggregate(self.index_name, aggs)
        self.expect("avg_value" in result, True)


class TestEsUtils(TestBase):
    @classmethod
    def setup_class(cls):
        cls.es = EsUtil("default")
        cls.index_name = f"test_utils_{int(time.time() * 1000)}"
        cls.alias_name = f"test_alias_{int(time.time() * 1000)}"
        cls.es.create_index(cls.index_name)

    @classmethod
    def teardown_class(cls):
        if hasattr(cls, "es") and cls.es:
            try:
                if self.es.index_exists(cls.alias_name):
                    cls.es.delete_index(cls.alias_name)
                if self.es.index_exists(cls.index_name):
                    cls.es.delete_index(cls.index_name)
            except Exception:
                pass
            cls.es.close()

    def test_refresh(self):
        result = self.es.refresh(self.index_name)
        self.expect(result is not None, True)

    def test_put_and_delete_alias(self):
        self.es.put_alias(self.index_name, self.alias_name)
        aliases = self.es.aliases(self.index_name)
        self.expect(self.alias_name in str(aliases), True)
        self.es.delete_alias(self.index_name, self.alias_name)

    def test_cat_indices(self):
        indices = self.es.cat_indices()
        self.expect(isinstance(indices, list), True)