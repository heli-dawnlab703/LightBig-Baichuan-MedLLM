import json
import re

from tqdm import tqdm

file_path = "../data/YIER医疗大模型评测-测试公开集（无答案）.json"
test_path = "../data/YIER-test.json"
result_path = "../data/result/ft_pt_answer_1.json"
out_path = '../data/submit_test.json'

nrow = sum(1 for _ in open(file_path, 'r'))
# 打开JSON文件并解析数据
with open(file_path, "r", encoding='utf-8') as ori_file, open(test_path, "r", encoding='utf-8') as test_file, \
        open(result_path, "r", encoding='utf-8') as result_file, open(out_path, "w", encoding="utf-8") as out_file:
    for ori_line, test_line, result_line in tqdm(zip(ori_file, test_file, result_file), total=nrow):
        ori_dict = json.loads(ori_line)
        test_dict = json.loads(test_line)
        reuslt_dict = json.loads(result_line)
        temp_list = []

        select_str = test_dict.get("conversation")[0]["content"]
        options_match = re.search(r'选项:{(.*?)}', select_str)
        if options_match:
            # 获取选项部分的内容
            options_text = options_match.group(1)
            # 去除转义字符 \
            options_text = options_text.replace('\\"', '"')
            # 将选项文本转换为字典
            options_dict = eval("{" + options_text + "}")
            answer_list = reuslt_dict.get("result")
            for i, value in enumerate(answer_list):
                if value != "" and len(value) > 0:
                    answer = options_dict.get(value)
                    temp_list.append(answer)

            ori_dict.update({"predict_answers": temp_list})
            out_file.write(json.dumps(ori_dict, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    pass
