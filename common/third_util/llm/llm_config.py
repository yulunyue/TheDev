from common.tool.export import StrModel, NumberModel, BoolModel, FileConfig


class LlmConfig(FileConfig):
    base_url = StrModel(default_value="http://127.0.0.1:4096")
    model = StrModel()
    api_key = StrModel()
    timeout = NumberModel(default_value=1800)
    no_proxy = BoolModel(default_value=True)
    provider_id = StrModel()
    model_id = StrModel()
    cwd = StrModel()


LlmConfig.set_resource("config/setting/llm.json")
