from langchain_deepseek import ChatDeepSeek
from langchain.schema import HumanMessage, SystemMessage
import json
from dotenv import load_dotenv
import asyncio
load_dotenv()

class ItineraryAgent:
    def __init__(self):
        self.llm = ChatDeepSeek(temperature=0.5, model='deepseek-chat')

    async def plan_itinerary(self,travel_info:dict)->dict:
        system_prompt = """
        你是一个行程规划专家，根据旅行信息（包括目的地，天气，景点等），制定合理的行程安排。
        请严格按照以下JSON格式返回结果：
        {
            "daily_plan":{
                "day1":["上午行程","下午行程","晚上行程"],
                "day2":["上午行程","下午行程","晚上行程"],
            },
            "transportation":"交通建议",
            "meal_suggestions":"餐饮建议",
            "tips":"注意事项"
        }
        注意：必须返回合法的JSON格式，不要添加任何其他的文字，也不要添加```json等分隔符
        """
        response = await self.llm.agenerate(
            [[
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"指定行程{json.dumps(travel_info,ensure_ascii=False)}")
            ]]
        )
        #print(response)
        try:
            return json.loads(response.generations[0][0].text)
        except json.JSONDecodeError:
            return {
                "daily_plan":{
                    "day1":["上午9点参观故宫", "下午继续游览故宫", "晚上自由活动或休息","下午行程","晚上行程"],
                    "day2":["上午自由活动或参观周边景点", "下午自由活动或购物", "晚上返回或继续其他行程"],
                },
                "transportation":"建议乘坐地铁1号线到天安门东站下车，步行即可到达故宫。",
                "meal_suggestions":"故宫附近有多个餐饮选择，建议尝试北京特色小吃如炸酱面、北京烤鸭等。",
                "tips":"提前在线购票以避免排队，携带防晒用品和充足的水。穿着舒适的鞋子，因为需要步行较多。注意故宫的开放时间，避免错过入场时间。",
            }




# async def main():
#     agent = ItineraryAgent()
#     await agent.plan_itinerary(travel_info={
#                                    "name": "故宫",
#                                    "description": "故宫是中国明清两代的皇家宫殿，位于北京中轴线的中心，是中国古代宫廷建筑之精华。",
#                                    "best_time": "上午9点至下午4点",
#                                    "duration": "3-4小时",
#                                    "tips": "建议提前在线购票以避免排队，携带防晒用品和充足的水。",
#                                },)
#
#
# if __name__ == '__main__':
#     asyncio.run(main())

