import json
from tqdm import tqdm



file_path = "./YIER医疗大模型评测-训练集.json"
out_path = './YIER-train.json'

context_prompt = '''
示例1：
user: 
{
   "question": "关于补体调控叙述正确的是",
   "selection": ["补体激活过程中生成的中间产物不稳定", "只有结合在细胞表面的抗原抗体复合物才能触发经典途径", "补体系统活化失控可造成自身损伤", "产生病理效应", "细胞表面结合有多种补体调节因子", "补体调节蛋白有十余种"],
   "source": "临床考研真题"
}
assistant: 
{ 
    "predict_answers": ["补体激活过程中生成的中间产物不稳定", "只有结合在细胞表面的抗原抗体复合物才能触发经典途径", "补体系统活化失控可造成自身损伤", "细胞表面结合有多种补体调节因子"] 
}
user: 
'''


nrow = sum(1 for _ in open(file_path, 'r'))
# 打开JSON文件并解析数据
with open(file_path, "r", encoding='utf-8') as json_file, open(out_path, "w", encoding="utf-8") as out_file:
    for line in tqdm(json_file, total=nrow):
        json_dict = json.loads(line)
        output_dict = {"_id" :  "" , "conversation" : []}
        count = 0
        if_count = 0
        user_content_str = context_prompt
        assistant_content_str = ""
        for key, item in json_dict.items():
            if key == "answer_choices":
                assistant_content_str  += 'assistant: \n' + '{\n"  predict_answers" :' + json.dumps(json_dict.get(key), ensure_ascii=False, indent=2).replace('\n', '') + '\n }'
                count += 1
                continue
            if key == "sample_id":
                output_dict.update({"_id":json_dict.get(key)})
                count += 1
                continue
            if len(json_dict.get(key)) != 0:
                if if_count == 0:
                    user_content_str += "{\n  " + key + ":" +  json.dumps(json_dict.get(key), ensure_ascii=False, indent=2).replace('\n', '')  + ",\n"
                elif count == len(json_dict) - 1:
                    user_content_str += "  " + key + ":" + json.dumps(json_dict.get(key), ensure_ascii=False, indent=2).replace('\n', '') + "\n}"
                else:
                    user_content_str += "  "  + key + ":" + json.dumps(json_dict.get(key), ensure_ascii=False, indent=2).replace('\n', '') + ",\n"
                if_count += 1
            count += 1
        output_dict["conversation"].append({"role": "user", "content": user_content_str})
        output_dict["conversation"].append({"role": "assistant", "content": assistant_content_str})
        out_file.write(json.dumps(output_dict, ensure_ascii=False) + '\n')












if __name__ == '__main__':
    pass

