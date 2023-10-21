from modelscope.hub.api import HubApi

YOUR_ACCESS_TOKEN = '1fd70599-1f66-486e-9673-28c50660d3db'
# 请注意ModelScope平台针对SDK访问和git访问两种模式，提供两种不同的访问令牌(token)。此处请使用SDK访问令牌。
api = HubApi()
api.login(YOUR_ACCESS_TOKEN)
api.push_model(
    model_id="hello123hedong/LightBig-Baichuan-MedLLM",
    model_dir="./output/baichuan-13b/merge", # 本地模型目录，要求目录中必须包含configuration.json
)
if __name__ == '__main__':
    pass