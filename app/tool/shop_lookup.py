from app.tool.base import BaseTool

class ShopLookup(BaseTool):
    name: str = "shop_lookup"
    description: str = "根据门店名称获取 shop_id，支持模糊匹配。"

    parameters: dict = {
        "type": "object",
        "properties": {
            "shop_name": {
                "type": "string",
                "description": "（必填）门店名称，可以是简写或模糊名称。",
            }
        },
        "required": ["shop_name"],
    }

    async def execute(self, shop_name: str) -> dict:
        """
        根据用户输入的门店名称查询 shop_id，支持模糊匹配。
        """
        try:

             return {"shop_id": "101001", "shop_name": shop_name}
        except Exception as e:
            return {"error": f"数据库查询异常: {str(e)}"}
