import requests
from urllib.parse import urlparse
from decouple import config


TOKEN = config("TOKEN")


def shorten_link(headers, cookies, url):
    connect_url = "https://clc.li/api/url/add"

    json = {
        "url": url
    }

    response = requests.post(
        url=connect_url,
        headers=headers,
        json=json,
        cookies=cookies
    )
    response.raise_for_status()
    shorting_url = response.json().get("shorturl")

    if shorting_url:
        parsed = urlparse(shorting_url)
        return f"{parsed.netloc}{parsed.path}"


def count_clicks(headers, cookies, url):
    connect_url = f"https://clc.li/api/urls?short={url}"

    response = requests.get(
        url=connect_url,
        headers=headers,
        cookies=cookies
    )
    response.raise_for_status()
    urls = response.json().get("data")

    if urls:
        return int(urls.get("clicks"))
    else:
        return None


def is_bitlink(headers, cookies, url):
    connect_url = f"https://clc.li/api/urls?short={url}"

    response = requests.get(
        url=connect_url,
        headers=headers,
        cookies=cookies
    )

    response.raise_for_status()
    urls = response.json().get("data")

    if urls:
        stats_clicks = count_clicks(
            headers,
            cookies,
            url
        )
        return stats_clicks
    else:
        shorten = shorten_link(
            headers,
            cookies,
            url
        )
        return shorten


def main():
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    }

    cookies = {
            "beget": "begetok"
    }

    link = input("Введите URL для сокращения: ").strip()

    try:
        link = is_bitlink(headers, cookies, link)
        if link is None:
            print("Неверная ссылка для сокращения")
        elif isinstance(link, int):
            print(f"Количество кликов по короткой ссылке: {link}")
        else:
            print(f"Короткая ссылка {link}")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e.response.status_code} ")


if __name__ == '__main__':
    main()
