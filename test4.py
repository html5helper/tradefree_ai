from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  # model="gpt-4o",
  model="gpt-4-0125-preview",
  # model="gpt-4-turbo-preview",
  #model="gpt-4-plugins",
  # response_format={ "type": "json_object" },
  messages=[
    {"role": "system", "content": "You are a helpful assistant designed to give keywords from youtube video descript."},
    #{"role": "user", "content": "the keywords for the youtube video?"},
    #clear{"role": "assistant", "content": "The 15 keywords."},
    {"role": "user", "content": "give me the keywords array in chinese from title:特斯拉自动驾驶里程碑：版本12.3免费试用全面开放！特斯拉ChatGPT时刻来临！Tesla FSD12.3 free trial to all users!"}
  ]
)

#print(completion.choices[0].message)
print(completion.choices)
