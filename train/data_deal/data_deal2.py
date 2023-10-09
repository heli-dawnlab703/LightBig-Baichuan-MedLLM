import json
from tqdm import tqdm

file_path = "../data/YIER医疗大模型评测-测试公开集（无答案）.json"
out_path = '../data/YIER-test.json'

context_prompt = "你现在是一个医疗问答模型，根据下面的选择题题目，从提供的选项中选出该问题对应的正确答案。\n### 问题: {instruction} ### 回答:\n"
zimu_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
nrow = sum(1 for _ in open(file_path, 'r'))
# 打开JSON文件并解析数据
with open(file_path, "r", encoding='utf-8') as json_file, open(out_path, "w", encoding="utf-8") as out_file:
    for line in tqdm(json_file, total=nrow):
        json_dict = json.loads(line)
        output_dict = {"_id": "", "conversation": []}
        user_content_str = ""
        assistant_content_str = ""
        temp_dict = {}
        temp_dict_reverse = {}
        for key, item in json_dict.items():
            if len(json_dict.get(key)) != 0:
                if key == "sample_id":
                    output_dict.update({"_id": json_dict.get(key)})
                if key == "answer_choices":
                    answer_choices = json_dict.get(key)
                    if len(answer_choices) > 0:
                        for t, k in enumerate(answer_choices):
                            v = temp_dict_reverse.get(k)
                            assistant_content_str = assistant_content_str.join(' ').join(v)

                if key == "question":
                    user_content_str += json_dict.get(key)

                if key == "selection":
                   select_list = json_dict.get(key)
                   for i, value in enumerate(select_list):
                        temp_dict[zimu_list[i]] = value
                        temp_dict_reverse[value] = zimu_list[i]
                   user_content_str += ' ### 选项:' + json.dumps(temp_dict, ensure_ascii=False, indent=2).replace('\n', '')
                   user_content_str = context_prompt.format(instruction=user_content_str)
        output_dict["conversation"].append({"role": "user", "content": user_content_str})
        output_dict["conversation"].append({"role": "assistant", "content": assistant_content_str})
        out_file.write(json.dumps(output_dict, ensure_ascii=False) + '\n')












if __name__ == '__main__':
    pass

