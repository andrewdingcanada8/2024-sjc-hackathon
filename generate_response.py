from openai import OpenAI
from prompts import UXGEN_SYSTEM_PROMPT, GENERAL_SYSTEM_PROMPT

def gen_resp(user_prompt: str, key: str):
    client = OpenAI(api_key=key)
    system_prompt = ""
    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        # model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )
    return response.choices[0].message.content


def gen_general_resp(user_prompt: str, key: str):
    client = OpenAI(api_key=key)
    system_prompt = GENERAL_SYSTEM_PROMPT
    response = client.chat.completions.create(
        # model="gpt-4-0125-preview",
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )
    return response.choices[0].message.content


def gen_ux_resp(user_prompt: str, key: str):
    client = OpenAI(api_key=key)
    system_prompt = UXGEN_SYSTEM_PROMPT
    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        # model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )
    return response.choices[0].message.content