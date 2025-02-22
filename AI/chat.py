from langchain_openai import ChatOpenAI 

content = """
شرکت ما دانش بنیان هست و درآمدش معاف مالیاتی هست
ولی توی اظهارنامه به اشتباه جزو درآمد مشمول اعلام شد و چون درآمد خوداظهاری مشمول درنظر گرفته شده، برگه مطالبه مالیاتی به میزان کل صادر شده. روش و راه استفاده از این معافیت و دفاع اون چیه!
با توجه به قوانین موجود در ایران و بند های این قوانین یک لایحه بنویس
. به هر بندی که از آن استفاده میشود، اشاره کن.
"""

messages = [
    {"role": "system", "content": "You are a helpful lawyer."},
    {"role": "user", "content": content},
]

model_name = "gpt-4o-mini"


llm = ChatOpenAI(
    model=model_name, base_url="https://api.avalai.ir/v1", api_key="aa-uGWiJcHMkhdW8s1qw4949XWbvXa6Ak04QYwRkKDk9pG8YAVh"
)

try:
    response = llm.invoke(messages)
    print("Response:", response.content)
except Exception as e:
    print("Error occurred:", str(e))

