from common.tool.base_class.base_model import StrModel, NumberModel, BoolModel
from common.tool.base_class.storage.json_config import JsonConfig


class LlmConfig(JsonConfig):
    base_url = StrModel(default_value="http://10.159.226.57:31943/v1")
    model = StrModel(default_value="codeagent/maas-glm-5-aliyun-codeagent")
    timeout = NumberModel(default_value=1800)
    no_proxy = BoolModel(default_value=True)
    opencode_base_url = StrModel(default_value="http://localhost:54321")
    provider_id = StrModel(default_value="codeagent_lzh")
    model_id = StrModel(default_value="codeagent/maas-glm-5-aliyun-codeagent")