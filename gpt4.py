from openai import OpenAI
import os

def get_keywords_by_content(request):
    try:
        client = OpenAI()
        completion = client.chat.completions.create(
            model="gpt-4-0125-preview",
            # response_format={ "type": "json_cobject" },
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to give keywords from youtube video descript."},
                # {"role": "user", "content": "the keywords for the youtube video in chinese"},
                {"role": "assistant", "content": "The 30 keywords."},
                {"role": "user", "content": "give me the keywords with json array format(no preview '```json') in chinese from the following comments:"+request}
                # {"role": "user", "content": "give me the keywords array in chinese from the following comments:"+request}
            ]
        )
        # return completion.choices[0].message
        return completion.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
