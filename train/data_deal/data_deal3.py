import json
from tqdm import tqdm

# YIER医疗大模型评测-测试公开集（无答案）.json  YIER医疗大模型评测-训练集.json
file_path = "../data/YIER医疗大模型评测-测试公开集（无答案）.json"
out_path = '../data/YIER-test-1.json'
flag = "test"


context_prompt = "你现在是一个医疗问答模型，根据下面的判断题题目，从提供的问题以及回答中判断该回答是否正确。\n### 问题: {instruction} ### 回答: {answer}\n"
zimu_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
nrow = sum(1 for _ in open(file_path, 'r', encoding='utf-8'))
# 打开JSON文件并解析数据
with open(file_path, "r", encoding='utf-8') as json_file, open(out_path, "w", encoding="utf-8") as out_file:
    for line in tqdm(json_file, total=nrow):
        json_dict = json.loads(line)
        user_content_str = ""
        assistant_content_str = ""
        temp_dict = {}
        temp_dict_reverse = {}
        question = ""
        id  = ""
        answer = ""
        for key, item in json_dict.items():
            if len(json_dict.get(key)) != 0:
                if key == "sample_id":
                    id = json_dict.get(key)
                if key == "answer_choices":
                    answer_choices = json_dict.get(key)
                    if len(answer_choices) > 0:
                        for t, k in enumerate(answer_choices):
                            answer = k

                if key == "question":
                    question = json_dict.get(key)

                if key == "selection":
                   select_list = json_dict.get(key)
                   for i, value in enumerate(select_list):
                        temp_dict[zimu_list[i]] = value
                        temp_dict_reverse[value] = zimu_list[i]

        for key1, value1 in temp_dict_reverse.items():
            output_dict = {"_id": "", "conversation": []}
            user_content_str = context_prompt.format(instruction=question, answer=key1)
            output_dict["_id"]=str(id) + value1
            output_dict["conversation"].append({"role": "user", "content": user_content_str})
            if flag == "test":
                output_dict["conversation"].append({"role": "assistant", "content": ""})
            else:
                if key1 == answer:
                    output_dict["conversation"].append({"role": "assistant", "content": "回答正确"})
                else:
                    output_dict["conversation"].append({"role": "assistant", "content": "回答错误"})

            out_file.write(json.dumps(output_dict, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    pass




