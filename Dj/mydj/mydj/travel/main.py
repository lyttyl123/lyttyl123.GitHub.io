from langgraph.graph import StateGraph, END
from typing import Dict, TypeVar
import json
import asyncio
from .states import TravelInfo
from .agents.itinerary_agent import ItineraryAgent
from .agents.attraction_agent import AttractionAgent
from .agents.weather_agent import WeatherAgent

StateType = TypeVar("StateType", bound=Dict)


def creat_travel_assistant():
    # 初始化各个代理
    weather_agent = WeatherAgent()
    attraction_agent = AttractionAgent()
    itinerary_agent = ItineraryAgent()
    workflow = StateGraph(StateType)

    async def check_weather(state: Dict) -> Dict:
        # 将状态转化为TravelInfo的对象
        travel_info = TravelInfo(**state)
        weather_info = await weather_agent.analyze_weather(
            travel_info.destination,
            travel_info.start_data,
        )
        travel_info.weather_info = weather_info
        return travel_info.model_dump()

    async def recommend_attraction(state: Dict) -> Dict:
        # 将状态转化为TravelInfo的对象
        travel_info = TravelInfo(**state)
        attraction = await attraction_agent.recommend_attractions(
            travel_info.destination,
            travel_info.weather_info,
            travel_info.preferences
        )
        travel_info.attractions = attraction
        return travel_info.model_dump()

    async def plan_itinerary(state: Dict) -> Dict:
        # 将状态转化为TravelInfo的对象
        travel_info = TravelInfo(**state)
        itinerary = await itinerary_agent.plan_itinerary(travel_info.model_dump())
        travel_info.itinerary = itinerary
        return travel_info.model_dump()

    workflow.add_node("check_weather", check_weather)
    workflow.add_node("recommend_attraction", recommend_attraction)
    workflow.add_node("plan_itinerary", plan_itinerary)

    workflow.set_entry_point("check_weather")
    workflow.add_edge("check_weather", "recommend_attraction")
    workflow.add_edge("recommend_attraction", "plan_itinerary")
    workflow.add_edge("plan_itinerary", END)
    return workflow.compile()


async def main(place,date,day,interests,budget,pace):
    assistant = creat_travel_assistant()

    initial = TravelInfo(
        destination=place,  # 旅行目的地
        start_data=date,  # 开始日期
        duration=day,  # 行程天数
        preferences = {
            "interests":interests,
            "budget":budget,
            "pace":pace
        }
    ).model_dump()

    final_state = await assistant.ainvoke(initial)
    return json.dumps(final_state,ensure_ascii=False,indent=2)

def run(place,date,day,interests,budget,pace):
    # a = asyncio.run(main("云南","2025-05-31",3,["美食","文化"],10000,"中等"))
    a = asyncio.run(main(place,date,day,interests,budget,pace))
    return a
