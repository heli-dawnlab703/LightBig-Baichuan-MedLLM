from modelscope.hub.api import HubApi
from modelscope.hub.repository import Repository

YOUR_ACCESS_TOKEN = '1fd70599-1f66-486e-9673-28c50660d3db'
# 请注意ModelScope平台针对SDK访问和git访问两种模式，提供两种不同的访问令牌(token)。此处请使用SDK访问令牌。
api = HubApi()
api.login(YOUR_ACCESS_TOKEN)
repo = Repository("./output/baichuan-13b/merge", clone_from='hello123hedong/LightBig-Baichuan-MedLLM')
repo.tag_and_push('v1.0.0', 'Test revision')

if __name__ == '__main__':
    pass