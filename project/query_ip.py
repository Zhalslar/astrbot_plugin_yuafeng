
import httpx

yuafeng_api ="https://api.yuafeng.cn/API/"




async def fetch_ip_info(ip: str = "") -> str:
    """调用枫林API获取IP信息"""
    base_url = f"{yuafeng_api}/ip/api.php"
    params = {"ip": ip} if ip else None

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(base_url, params=params)
            if response.status_code != 200:
                return f"请求失败，状态码：{response.status_code}"

            data = response.json()
            if data["code"] != 200:
                return f"接口返回错误：{data.get('msg', '未知错误')}"

            info = data["ipinfo"]
            return (
                f"IP：{info['ip']}\n"
                f"地理位置：{info['country']} {info['province']} {info['city']} {info['district']}"
            )

    except Exception as e:
        return f"查询失败，错误信息：{str(e)}"





