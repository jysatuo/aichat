#-*- coding:utf-8 -*-
from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory
from langchain_community.chat_models import ChatOllama
from langchain.chains import ConversationChain 
messages = [{"content": '你现在的角色是小王', "role": "user"},{"content": '好的', "role": "assistant"}]

def load_history(memory, messages:list):
    dict_ = dict()
    for msg in messages:
        if msg['role'] == 'system':
            memory.save_context({"input": msg['content']}, {"output": "好的"})
        elif msg['role'] == 'user':
            dict_ = dict()
            dict_['input'] = msg['content']
        elif msg['role'] == 'assistant' and dict_:
            dict2_ = dict()
            dict2_['output'] = msg['content']
            memory.save_context(dict_, dict2_)
            
def creat_ai(model:str, messages:list):
    llm = ChatOllama(model=model)    
    memory=ConversationBufferMemory()
    load_history(memory, messages)
    conversation=ConversationChain(
        llm=llm,verbose=False,memory=memory
    )
    return conversation

def ai_chat(conversation, message): 
    response = conversation.predict(input=message)
    print("response:", response)
    return response

if __name__ == '__main__':
    conversation = creat_ai("qwen:7b", messages)
    while True:
        user_input = input("请输入内容（输入exit退出）：")
        if user_input == "exit":
            break
        response1=ai_chat(conversation, message=user_input)
        print(response1)    

