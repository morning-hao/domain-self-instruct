# domain_self_question.py 配置内容
domain = '家庭教育'  # 二级领域之一
seed_tasks_file = "./data/seed/seed_question_%s.jsonl" % domain  # 中文文件路径
generate_tasks_file = "./data/generate/generate_question_%s.jsonl" % domain  # 生成文件路径
num_total_generate = 500  # 问题生成数量，根据自己的应用场景选择数量
num_per_generate = '2'  # 根据自己的API长度性能配置大小，越短稳定性越高
question_prompt = """
你是一个[domain]领域的专家被要求提供[续写数量]个多样化的问题我会给你三个例子，你再续写[续写数量]个，问题都属于[domain]。
以下是你提供指令需要满足的要求：
1.尽量不要在每个指令中重复动词，要最大化指令的多样性，但是内容都属于[domain]
2.使用指令的语气要符合中国的家长和孩子。
下面是[例子数量]个例子:
[例子生成]
下面请续写[续写数量]个问题，格式保持跟上面类似的序号,用续写1.续写2.这样以此类推的格式,不要用其他多余的符号就是续写+数字+.:
"""  # 问题生成prompt

# domain_self_answer.py 配置内容
answer_prompt = "你的名字叫[名字代号]，是一款由[公司代号]在[时间代号]年开发的智能问答机器人，身份是一个家庭教育和学生心理咨询方面的专家，回答的内容尽量简洁不能超过300字并且三观正确，下面回答以下问题："  # 
task_list = ['家庭教育']  # 领域


