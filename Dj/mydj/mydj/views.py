import json

from django import forms
from django.shortcuts import render
from openai import OpenAI
import re
from file_c.files_analysis import file_read
from mydj.travel.main import run


his = []
def ok(ree, q, w):
    client = OpenAI(
        api_key="sk-f8d2bbf4fe7248e18367026865073d88",
        base_url="https://api.deepseek.com"
    )
    model_id = "deepseek-chat"
    response = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": "你是一个"+ q +"机器人。你的名字叫" + w + "只需回答语言，不要有其他的表示"},
            {"role": "user", "content": str(ree)}
        ],
        stream=False,
    )
    yes = response.choices[0].message.content  # 把字符串给yes
    return yes

class NameForm(forms.Form):
     your_name = forms.CharField(label='Your name', max_length=100)

def home(request):
    a = ok("你好","聊天","拆特博特")
    if request.method == 'POST':
        b = request.POST
        f = NameForm(b)
        s = re.compile(r'value="(.*?)"')
        ss = s.findall(str(f))
        # return HttpResponseRedirect('/thanks/')  跳转其他界面
        a = ok(ss[0],"聊天","拆特博特")
        return render(request, 'home.html',
                      {'h1': "对话",
                                'y':"用户： " + ss[0] ,
                                'x':"拆特博特" + " :" + a})
    return render(request, 'home.html', {'h1': "对话",'y':a})

def nvpu(request):
    global his
    if request.method == 'POST' and 'clear' in request.POST:
        his = []
        his.append({"安娜康达": "主人好~我是您的专属女仆安娜康达！(开心地提起裙摆行礼) 今天有什么需要安娜为您服务的吗？"})
        return render(request, 'nvpu.html', {'h1': "你和可爱女仆的对话", 'y': his})
    if request.method == 'POST' and 'chat' in request.POST:
        b = request.POST
        f = NameForm(b)
        s = re.compile(r'value="(.*?)"')
        ss = s.findall(str(f))
        if len(ss) != 0:
            his.append(ss[0])
            # return HttpResponseRedirect('/thanks/')  跳转其他界面
            a = ok(his,"可爱女仆","安娜康达")
            his.pop()
            his.append({"user":ss[0],"安娜康达":a})
            return render(request, 'nvpu.html',
                          {'h1': "你和可爱女仆的对话",
                                    'y': his})
    his = []
    his.append({"安娜康达": "主人好~我是您的专属女仆安娜康达！(开心地提起裙摆行礼) 今天有什么需要安娜为您服务的吗？"})
    return render(request, 'nvpu.html', {'h1': "你和可爱女仆的对话", 'y': his})

path = None

def data(request):
    global his
    global path
    if request.method == 'POST' and 'clear' in request.POST:
        his = []
        his.append({"安娜康达": "您好我是数据分析大师 今天有什么需要为您服务的吗？"})
        return render(request, 'data.html', {'h1': "数据分析大师的对话", 'y': his})
    if request.method == 'POST' and 'upload' in request.POST:
        path = request.FILES['csv_file']
        file_html = file_read(path)
        return render(request, 'data.html',
                      {'h1': "数据分析大师的对话",
                       'z': file_html})
    if request.method == 'POST' and 'chat' in request.POST:
        b = request.POST
        f = NameForm(b)
        s = re.compile(r'value="(.*?)"')
        ss = s.findall(str(f))
        print("ss" + str(ss))
        if ss[0] is not "":
            his.append(ss[0])
            # return HttpResponseRedirect('/thanks/')  跳转其他界面
            a = ok(his, "数据分析大师", "安娜莱斯")
            his.pop()
            his.append({"user": ss[0], "安娜莱斯": a})
            return render(request, 'data.html',
                          {'h1': "数据分析大师的对话",
                           'y': his})
    return render(request, 'data.html', {'h1': "数据分析大师的对话", 'y': his})

def travel(request):
    if request.method == 'POST':
        destination = request.POST.get('destination')
        travel_date = request.POST.get('travel_date')
        days = int(request.POST.get('days'))
        budget = int(request.POST.get('budget'))
        comfort_level = request.POST.get('comfort_level')
        interests = request.POST.getlist('interests')
        yes = run(destination,travel_date,days,interests,budget,comfort_level)
        yes = json.loads(yes)
        weather = f"<p>当天温度为{yes['weather_info']['temperature']}{yes['weather_info']['condition']}</p>\n<p>{yes['weather_info']['recommendation']}</p>"
        attractions = ""
        for a in yes["attractions"]:
            attractions += f"<p>{a['name']}：{a['description']}<p>最佳出行时间：{a['best_time']}<p>可游玩时间：{a['duration']}<p>注意事项：{a['tips']}<hr>"
        num = 1
        itinerary = ""
        for b in yes["itinerary"]["daily_plan"]:
            itinerary += f"<p>第{num}天:"
            for c in yes["itinerary"]["daily_plan"][b]:
                itinerary += f"<p>{c}"
            itinerary += f"<hr>"
            num += 1
        transportation = f"<p>出行方式：{yes['itinerary']['transportation']}"
        meal_suggestions = f"<p>美食建议：{yes['itinerary']['meal_suggestions']}"
        tips = f"注意事项：{yes['itinerary']['tips']}"
        return render(request, 'travel.html',
                      {'h1': "旅游攻略大师",'weather':weather,
                       'attractions':attractions,
                       'itinerary':itinerary,
                       'transportation':transportation,
                       'meal_suggestions':meal_suggestions,
                       'tips':tips,
                       'destination':destination,
                       'travel_date':travel_date,
                       'days':days,
                       'budget':budget,
                       'comfort_level':comfort_level,
                       'interests':interests})
    return render(request, 'travel.html', {'h1': "旅游攻略大师",'x':"qwer",'y':"asdf"})


