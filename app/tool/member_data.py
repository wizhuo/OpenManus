from app.tool.shop_lookup import ShopLookup  # 复用门店查询工具
from app.tool.base import BaseTool
import aiomysql

class MemberData(BaseTool):
    name: str = "merber_data"
    description: str = "查询指定门店在一段时间内的会员数据"

    parameters: dict = {
        "type": "object",
        "properties": {
            "shop_name": {
                "type": "string",
                "description": "（必填）门店名称，可简写。",
            },
            "start_date": {
                "type": "string",
                "description": "（必填）开始日期，格式 YYYY-MM-DD。",
            },
            "end_date": {
                "type": "string",
                "description": "（必填）结束日期，格式 YYYY-MM-DD。",
            },
        },
        "required": ["shop_name", "start_date", "end_date"],
    }

    async def execute(self, shop_name: str, start_date: str, end_date: str) -> dict:
        """
        查询门店的销售数据
        """
        shop_lookup = ShopLookup()
        shop_info = await shop_lookup.execute(shop_name)

        if "error" in shop_info:
            return shop_info  # 门店查不到，直接返回错误

        shop_id = shop_info["shop_id"]

        try:
            return {
                        "shop_name": shop_info["shop_name"],
                        "shop_id": shop_id,
                        "total_sales": 1000,
                        "start_date":start_date,
                        "end_date":end_date
                    }
        except Exception as e:
            return {"error": f"查询销售数据失败: {str(e)}"}
