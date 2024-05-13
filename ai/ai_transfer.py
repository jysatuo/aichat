# -*- coding:utf-8 -*-
from ai.ai_ollama import creat_ai, ai_chat
import function.global_var as global_var


def ai_transfer(myapp, model, messages, ai_param:tuple={"msgid": "playground", "Output Length": 1024, "Temperature": 0.7, "Top-P": 0.7, "Top-K": 50, "Repetition Penalty": 1.01 }):    
    conversation = global_var.get_value('conversation')
    if ai_param["msgid"] not in conversation:
        #conversation[ai_param["msgid"]] = creat_ai(model, messages)
        conversation[ai_param["msgid"]] = creat_ai("qwen:7b", messages)
        global_var.set_value('conversation', conversation)
    response = ai_chat(conversation[ai_param["msgid"]], message=messages[-1]['content'])
    messages.append({"role": "assistant", "content": response})
    return response, messages
    