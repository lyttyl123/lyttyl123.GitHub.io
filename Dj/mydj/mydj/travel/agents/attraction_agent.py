from langchain_deepseek import ChatDeepSeek
from langchain.schema import HumanMessage, SystemMessage
import json
from dotenv import load_dotenv

load_dotenv()


class AttractionAgent:
    def __init__(self):
        self.llm = ChatDeepSeek(temperature=0.7, model='deepseek-chat')

    async def recommend_attractions(self, destination: str, weather_info: dict, preferences: dict) -> list:
        system_prompt = """
        你是一个旅游专家，根据目的地，天气情况，用户偏好，推荐适合的景点。
        请严格按照以下JSON格式返回结果：
        [
            {
            "name":"景点名称",
            "description":"景点描述",
            "best_time":"最佳游览时间",
            "duration":"建议游览时长",
            "tips":"建议游览方式",
            }
        ]
        注意：必须返回合法的JSON格式，不要添加任何其他的文字，也不要添加```json等分隔符
        """
        context = {
            "destination": destination,
            "weather": weather_info,
            "preferences": preferences
        }
        response = await self.llm.agenerate(
            [[
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"推荐景点：{json.dumps(context, ensure_ascii=False)}")
            ]]
        )
        #print(response)
        try:
            return json.loads(response.generations[0][0].text)
        except json.JSONDecodeError:
            return [
                {
                    "name": "故宫",
                    "description": "故宫是中国明清两代的皇家宫殿，位于北京中轴线的中心，是中国古代宫廷建筑之精华。",
                    "best_time": "上午9点至下午4点",
                    "duration": "3-4小时",
                    "tips": "建议提前在线购票以避免排队，携带防晒用品和充足的水。"
                }
            ]

#
# async def main():
#     agent = AttractionAgent()
#     await agent.recommend_attractions("北京", {"temperature":"20-25℃","condition":"晴","recommendation": "天气晴朗，适合外出活动，建议携带防晒用品"},{"price":"5000"})
#
#
# if __name__ == '__main__':
#     asyncio.run(main())
