yes = {
  "destination": "云南",
  "start_data": "2025-05-31",
  "duration": 3,
  "preferences": {
    "interests": [
      "美食",
      "文化"
    ],
    "budget": 10000,
    "pace": "中等"
  },
  "weather_info": {
    "temperature": "18-28℃",
    "condition": "多云转晴",
    "recommendation": "建议携带轻薄外套，白天注意防晒，早晚温差较大需适当增减衣物"
  },
  "attractions": [
    {
      "name": "丽江古城",
      "description": "丽江古城是世界文化遗产，以其独特的纳西族文化和古建筑风格闻名。游客可品尝当地美食，如丽江粑粑和纳西烤鱼，同时感受浓厚的文化氛围。",
      "best_time": "全天",
      "duration": "4-6小时",
      "tips": "建议傍晚时分游览，可以欣赏古城夜景。"
    },
    {
      "name": "大理古城",
      "description": "大理古城是白族文化的代表，拥有丰富的历史遗迹和美食。游客可以品尝大理扇和酸辣鱼，同时参观三塔寺等文化景点。",
      "best_time": "上午或傍晚",
      "duration": "3-5小时",
      "tips": "建议租一辆自行车游览古城，更加轻松自在。"
    },
    {
      "name": "昆明石林",
      "description": "石林是云南著名的自然与文化双重遗产，独特的喀斯特地貌令人叹为观止。游可以在景区内品尝彝族风味美食。",
      "best_time": "上午",
      "duration": "3-4小时",
      "tips": "建议穿着舒适的鞋子，因为景区内步行较多。"
    },
    {
      "name": "香格里拉松赞林寺",
      "description": "松赞林寺是云南最大的藏传佛教寺庙，被誉为“小布达拉宫”。游客可以体验藏文化和美食，如酥油茶和牦牛肉。",
      "best_time": "上午",
      "duration": "2-3小时",
      "tips": "建议尊重当地宗教习俗，进入寺庙时需脱帽。"
    }
  ],
  "itinerary": {
    "daily_plan": {
      "day1": [
        "上午游览丽江古城，品尝当地美食如丽江粑粑和纳西烤鱼",
        "下午继续探索丽江古城，感受纳西族文化",
        "晚上欣赏丽江古城夜景"
      ],
      "day2": [
        "上午前往大理古城，参观三塔寺等文化景点",
        "下午租自行车游览大理古城，品尝大理乳扇和酸辣鱼",
        "晚上在大理古城体验白族夜生活"
      ],
      "day3": [
        "上午游览昆明石林，欣赏喀斯特地貌，品尝彝族风味美食",
      ]
    },
    "transportation": "建议租车或包车，方便在景点间移动；也可选择高铁和长途巴士，但需提前预订。",
    "meal_suggestions": "尝试当地特色美食如丽江粑粑、纳西烤鱼、大理乳扇、酸辣鱼、彝族风味美食和藏族酥油茶、牦牛肉。",
    "tips": "1. 携带轻薄外套，注意防晒和早晚温差；2. 穿着舒适的鞋子，尤其是游览石林时；3. 尊重当地宗教习俗，如进入寺庙时需脱帽；4. 建议傍晚游览丽江古城和大理古城，以欣赏夜景。"
  },
  "user_feel": ""
}
# print(yes["itinerary"]["transportation"])
# print(yes["weather_info"])
# 去的地点
# k = ""
# for a in yes["attractions"]:
#     k += f"{a['name']}：{a['description']}\n最佳出行时间：{a['best_time']}\n可游玩时间：{a['duration']}\n注意事项：{a['tips']}\n\n"
# print(k)
# 第0天:
# 上午游览丽江古城，品尝当地美食如丽江粑粑和纳西烤鱼
# 下午继续探索丽江古城，感受纳西族文化
# 晚上欣赏丽江古城夜景
# num = 1
# st = ""
# for b in yes["itinerary"]["daily_plan"]:
#     # print(yes["itinerary"]["daily_plan"][b])
#     st += f"第{num}天:\n"
#     for c in yes["itinerary"]["daily_plan"][b]:
#         st += f"{c}\n"
#     num += 1
# print(st)
# print(yes["itinerary"]["daily_plan"])




# "weather_info": {
#     "temperature": "18-28℃",
#     "condition": "多云转晴",
#     "recommendation": "建议携带轻薄外套，白天注意防晒，早晚温差较大需适当增减衣物"
#   },
# 天气
# print(f"当天温度为{yes['weather_info']['temperature']}{yes['weather_info']['condition']}\n{yes['weather_info']['recommendation']}")