import requests

yuafeng_api ="https://api.yuafeng.cn/API/"


def search_stickers(query, page=1, num=10):
    """
    搜索QQ表情包。

    参数:
    query (str): 要搜索的表情包关键词。
    page (int): 页数，默认为1。
    num (int): 每页显示的数量，默认为10。

    返回:
    dict: API返回的数据或错误信息。
    """
    BASE_URL = f"{yuafeng_api}/ly/stickersSearch.php"
    params = {
        "msg": query,
        "page": page,
        "num": num
    }
    try:
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            result = response.json()
            if result["Code"] == 0:
                return {"success": True, "data": result["data"], "hasMorePage": result["hasMorePage"]}
            else:
                return {"success": False, "error": result["msg"]}
        else:
            return {"success": False, "error": f"HTTP Error {response.status_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}
