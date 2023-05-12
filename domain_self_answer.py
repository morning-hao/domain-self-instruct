import os
import json
import jsonlines
from tqdm import tqdm
from chatgpt import q2r
from config import answer_prompt, task_list


def read_question_list(file_path):
    question_list = []
    with jsonlines.open(file_path) as reader:
        for obj in reader:
            question_list.append(obj['question'])
    return question_list


def write_output(output_filename, output_dict):
    with open(output_filename, 'a', encoding='utf-8') as f:
        f.write(json.dumps(output_dict, ensure_ascii=False) + '\n')


def main():
    for task_name in task_list:
        print('本次任务类别:', task_name)
        question_list = read_question_list('./data/generate/generate_question_%s.jsonl' % task_name)
        print('本次任务问题数量：', len(question_list))
        output_filename = './data/train/train_data_%s.jsonl' % task_name

        # 检查文件是否存在，如果不存在则创建一个空文件
        if not os.path.exists(output_filename):
            with open(output_filename, 'w', encoding='utf-8'):
                pass

        # 读取文件并将已有问题存储到一个集合中
        existing_questions = set()
        with open(output_filename, 'r', encoding='utf-8') as f:
            for line in f:
                entry = json.loads(line)
                existing_questions.add(entry['question'])

        # 遍历问题列表并检查问题是否已存在
        for i, question in tqdm(enumerate(question_list)):
            print('第%s个' % i)
            if question in existing_questions:
                print('问题已存在')
                continue  # 如果问题已存在，跳过
            print('问题:', question)
            question_input = answer_prompt + question
            try:
                result = q2r(question_input)
                print('回答:', result)
            except Exception as e:
                print('异常:', e)
                continue  # 如果有异常，跳过
            output = {'index': i, 'question': question, 'answer': result}

            # 将新结果追加到文件中
            write_output(output_filename, output)
            print("已保存")
            print("len(问题):", len(question))
            print("len(回答):", len(result))


if __name__ == '__main__':
    main()
