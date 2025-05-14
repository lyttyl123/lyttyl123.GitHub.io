from typing import List, Dict
from pydantic import BaseModel  # 数据校验


class TravelInfo(BaseModel):
    """
    旅行信息模型的类，继承自pydantic的BaseModel
    用于存储和验证旅行规划过程中的所有相关信息
    包含用户输入的基本信息和系统生成的规划信息
    利用pydantic提供的数据验证功能确保数据的正确性
    """
    destination: str  # 旅行目的地
    start_data: str  # 开始日期
    duration: int  # 行程天数

    preferences: Dict = {}  # 用户偏好，如兴趣，预算等
    weather_info: Dict = {}  # 天气分析结果，由agent生成
    attractions: list[Dict] = []  # 推荐的经景点列表，由景点agent生成
    itinerary: Dict = {}  #最终生成旅行列表由agent生成
    user_feel:str = "" # 用户的生成结果的反应
