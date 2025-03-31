from app.tool.shop_lookup import ShopLookup  # 复用门店查询工具
from app.tool.base import BaseTool
import pymysql
import pandas as pd

class SalesData(BaseTool):
    name: str = "sales_data"
    description: str = "查询指定门店在一段时间内的销售数据"

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
            return get_data(shop_id,start_date,end_date)
        except Exception as e:
            return {"error": f"查询销售数据失败: {str(e)}"}



# 数据库连接配置
db_config = {
    "host": "10.111.105.43",  # 你的 MySQL 服务器地址
    "port": 3306,               # MySQL 端口
    "user": "u_dev",     # 你的用户名
    "password": "Pff6Ynxs7pLrv9fL", # 你的密码
    "database": "sc_db", # 数据库名
    "charset": "utf8mb4"
}

# 查询语句
sql_query = """
SELECT
    id AS 'ID',
    settlement_monitor_id AS '日志监控表ID',
    settle_date AS '日结日期',
    tenant_id AS '租户编码',
    shop_id AS '门店编号',
    shop_name AS '门店名称',
    store_type AS '门店类型(10-自营 20-加盟)钱大妈专用',
    region_type AS '区域类型(0-华南,1-华东)',
    total_amount AS '销售收入-营业额',
    product_amount AS '货款',
    material_amount AS '物料款',
    clean_amount AS '店日常费用-清洁费',
    fix_amount AS '店日常费用-维修费',
    office_amount AS '店日常费用-办公室费用',
    brand_amount AS '品牌使用费用',
    brand_amount_offline AS '线下品牌使用费用',
    brand_amount_online AS '线上品牌使用费用',
    yfk_amount AS '销售收入-预付卡售卡金额',
    vip_deposit_amount AS '销售收入-会员充值金额',
    vip_money_bag_amount AS '会员零钱包充值',
    total_short_amount AS '销售收入-昨日短溢收',
    other_amount AS '其他支出',
    diff_fix_amount AS '差异调整',
    cash_pay_amount AS '公司代收-现金',
    wechat_pay_amount AS '公司代收-微信',
    alipay_pay_amount AS '公司代收-支付宝',
    unionpay_amount AS '公司代收-银联卡支付',
    cloudflash_pay_amount AS '公司代收-银联云支付(杉德)',
    fast_card_pay_amount AS '公司代收-便捷卡支付',
    vip_card_pay_amount AS '公司代收-会员卡储值金支付',
    vip_bouns_point_pay_amount AS '公司代收-会员积分支付',
    online_pay_amount AS '公司代收-线上销售',
    vip_coupon_qdm_amount AS '公司代收-会员券（公司）',
    vip_coupon_shop_amount AS '公司代收-会员券（门店）',
    coupon_pay_amount AS '公司代收-优惠券支付',
    thirdparty_coupon_pay_amount AS '第三方代金券金额',
    meal_cost_amount AS '门店日常费用-餐费',
    wechat_charges_amount AS '门店会员及手续费-微信手续费',
    alipay_charges_amount AS '门店会员及手续费-支付宝手续费',
    unionpay_charges_amount AS '门店会员及手续费-银联卡手续费',
    cloudflash_pay_charges_amount AS '门店会员及手续费-云闪付(杉德)手续费',
    vip_bp_charges_amount AS '门店会员及手续费-会员赠与积分',
    store_allowance_amount AS '公司支持-补贴款',
    discount_amount_before_seven AS '19点前总折扣额',
    discount_amount_after_seven AS '19点后总折扣额',
    customer_quantity_before_seven AS '19点前客流量',
    customer_quantity_after_seven AS '19点后客流量',
    pos_customer_qty_before_twelve AS '12点前线下客流量',
    pos_customer_qty_before_seven AS '19点前线下客流量',
    pos_customer_qty_after_seven AS '19点后线下客流量',
    pos_amount_before_twelve AS '12点前线下销售额',
    pos_amount_before_seven AS '19点前线下销售额',
    pos_amount_after_seven AS '19点后线下销售额',
    sales_amount_before_seven AS '19点前营业额',
    sales_amount_after_seven AS '19点后营业额',
    vip_discount_amount_before_seven AS '19点前会员折扣',
    vip_discount_amount_after_seven AS '19点后会员折扣',
    vip_customer_quantity_before_seven AS '19点前VIP客流量',
    vip_customer_quantity_after_seven AS '19点后VIP客流量',
    vip_sales_amount_before_seven AS '19点前VIP营业额',
    vip_sales_amount_after_seven AS '19点后VIP营业额',
    other_discount_amount_before_seven AS '19点前日常折扣额',
    other_discount_amount_after_seven AS '19点后日常折扣额',
    order_count AS '统计订单数量',
    total_change_amount AS '门店线下POS舍零去分总数',
    sync_status AS '同步到ERP状态',
    discount_amount_before_twelve AS '12点前总折扣额',
    customer_quantity_before_twelve AS '12点前总客流量',
    sales_amount_before_twelve AS '12点前总营业额',
    vip_discount_amount_before_twelve AS '12点前总会员折扣',
    vip_customer_quantity_before_twelve AS '12点前VIP数量',
    vip_sales_amount_before_twelve AS '12点前VIP营业额',
    other_discount_amount_before_twelve AS '12点前日常折扣额',
    total_platform_income AS '应汇公司款',
    shop_income AS '加盟店净毛利',
    should_be_cash AS '应有现金',
    created_at AS '创建时间',
    created_by AS '创建人',
    updated_at AS '更新时间',
    updated_by AS '更新人',
    last_updated_at AS '最后更新时间',
    octopus_amount AS '八达通支付金额',
    octopus_charges_amount AS '八达通手续费',
    category_version AS '新分类版本号(0旧版本,1新版本)',
    distribution_amt AS '分销员提成',
    platform_promo_amt AS '平台承担非券促销费用',
    valid_customer_quantity_before_seven AS '19点前有效客流量',
    platform_promo_amt_home AS '到家平台承担非券促销费用',
    platform_promo_amt_shop AS '到店平台承担非券促销费用',
    next_day_logistics_amount AS '次日达物流费',
    total_extra_income AS '额外收入总计'
FROM t_sc_settlement_daily_total WHERE shop_id = %s AND settle_date >= %s AND settle_date <= %s limit 1;
"""


def get_data(shop_id: str, start_date: str, end_date: str):
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            cursor.execute(sql_query, (shop_id, start_date, end_date))
            data = cursor.fetchall()  # 获取所有数据
            columns = [desc[0] for desc in cursor.description]  # 获取列名（别名）

        # 结果转换为 DataFrame
        df = pd.DataFrame(data, columns=columns)

        if df.empty:
            return []  # 返回空列表

        result = df.head().to_dict(orient="records")  # 转换为 JSON 格式
        return result

    except Exception as e:
        print(f"查询失败: {e}")
        return []  # 查询失败也返回空列表

    finally:
        if connection:
            connection.close()
