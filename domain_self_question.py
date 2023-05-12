import os
import re
import json
import random
from chatgpt import q2r  # 这个需要用自己的接口实现
from config import domain, generate_tasks_file, num_total_generate, num_per_generate, question_prompt

if os.path.exists(generate_tasks_file):
    # 从文件中读取原始问题
    with open(generate_tasks_file, "r") as f:
        for_count = [json.loads(line) for line in f]
    num_total_generate -= len(for_count)
print('所需的生成数量:', num_total_generate)

while num_total_generate > 0:
    # 从文件中读取数据
    with open("./data/seed/seed_question_%s.jsonl" % domain, "r", encoding="utf-8") as file:
        data = [json.loads(line) for line in file]

    # 随机抽取3个问题
    random_questions = random.sample(data, 2)
    if os.path.exists(generate_tasks_file):
        with open(generate_tasks_file, 'r', encoding='utf-8') as file:
            data = [json.loads(line) for line in file]
        random_questions.extend(random.sample(data, 1))
    num_example = str(len(random_questions))
    # 问题prompt
    question_prompt = question_prompt.replace('[domain]', domain).replace('[续写数量]', num_per_generate).replace('[例子数量]', num_example)
    example = '\n'.join(
        ['问题%s.' % (index + 1) + question_dict['question'] for index, question_dict in enumerate(random_questions)])
    prompt = question_prompt.replace('[例子生成]', example)
    print(prompt)

    print('剩余数量:', num_total_generate)
    res = q2r(prompt)  # 输入为prompt，类型为字符串，返回的结果也是一个字符串就是gpt响应后的内容
    print('生成的信息:', res)


    def decoda_res(res):
        generate_question = []
        pattern = r"续写\d+\.\s*(.+)"
        res = res.split('\n')
        for sub_res in res:
            if not sub_res or '续写' not in sub_res:
                continue
            result = re.search(pattern, sub_res).group(1)
            if result and isinstance(result, str):
                generate_question.append(result)
        return generate_question


    generate_questions_base = decoda_res(res)

    # 检查文件是否存在，如果不存在则创建一个空文件
    if not os.path.exists(generate_tasks_file):
        with open(generate_tasks_file, 'w', encoding='utf-8'):
            pass
    # 从文件中读取原始问题
    with open(generate_tasks_file, "r") as f:
        generate_questions_old = [json.loads(line) for line in f]

    # 获取当前最大 ID
    max_id = max([q["id"] for q in generate_questions_old]) if generate_questions_old else 0
    generate_questions_new = []
    # 为新问题分配 ID 并将它们添加到列表中
    for question in generate_questions_base:
        max_id += 1
        new_question = {"id": max_id, "question": question}
        generate_questions_new.append(new_question)

    # 将结果写入 generate_tasks_file 文件
    with open(generate_tasks_file, "a") as f:
        for question in generate_questions_new:
            print('生成问题:', question)
            f.write(json.dumps(question, ensure_ascii=False) + "\n")
    num_total_generate -= int(num_per_generate)
