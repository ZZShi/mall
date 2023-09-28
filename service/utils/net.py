import random

import requests
from loguru import logger


def get_hero() -> dict:
    """获取英雄信息"""
    hero_list = requests.get("https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js").json()["hero"]
    hero = random.choice(hero_list)
    logger.debug(f"英雄信息: {hero}")
    return hero


def get_ip_addr(ip: str) -> str:
    addr = "未知"
    url = f"http://ip-api.com/json/{ip}"
    try:
        data = requests.get(url).json()
        if data['status'] == 'success':
            region = data['regionName']
            city = data['city']
            addr = f"{region}, {city}"
    finally:
        logger.debug(f"{ip = } 的归属地为 {addr}")
        return addr


if __name__ == '__main__':
    get_ip_addr("125.119.235.142")
