from common.tool.export import StrModel, NumberModel, BoolModel, FileConfig


class LlmConfig(FileConfig):
    base_url = StrModel(default_value="http://127.0.0.1:4096")
    model = StrModel(default_value="codeagent/maas-glm-5-aliyun-codeagent")
    timeout = NumberModel(default_value=1800)
    no_proxy = BoolModel(default_value=True)
    provider_id = StrModel(default_value="codeagent_lzh")
    model_id = StrModel(default_value="codeagent/maas-glm-5-aliyun-codeagent")


LlmConfig.set_resource("config/setting/llm.json")
