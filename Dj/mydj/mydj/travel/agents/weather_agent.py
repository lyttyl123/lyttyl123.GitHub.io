from langchain_deepseek import ChatDeepSeek
from langchain.schema import HumanMessage, SystemMessage
import json
from dotenv import load_dotenv

load_dotenv()


class WeatherAgent:
    def __init__(self):
        self.llm = ChatDeepSeek(temperature=0.3, model='deepseek-chat')

    async def analyze_weather(self, destination: str, date: str) -> dict:
        system_prompt = """
        你是一个天气分析的专家，根据目的地和日期预测天气的情况。
        请严格按照以下JSON格式返回结果：
        {
        "temperature":"温度范围如：20-25℃",
        "condition":"天气情况如：晴，多云",
        "recommendation":"基于天气的出行建议",
        }
        注意：必须返回合法的JSON格式，不要添加任何其他的文字，也不要添加```json等分隔符
        """
        response = await self.llm.agenerate(
            [[
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"分析{destination}在{date}的天气情况")
            ]]
        )
        #print(response)

        try:
            return json.loads(response.generations[0][0].text)
        except json.JSONDecodeError:
            return {
                "temperature": "20-25℃",
                "condition": "晴",
                "recommendation": "天气晴朗，适合外出活动，建议携带防晒用品",
            }

# async def main():
#     agent = WeatherAgent()
#     await agent.analyze_weather("北京", "2025-5-31")
#
#
# if __name__ == '__main__':
#     asyncio.run(main())
