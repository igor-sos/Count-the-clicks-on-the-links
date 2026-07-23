import requests
from urllib.parse import urlparse
from decouple import config


def shorten_link(headers, cookies, url):
    connect_url = "https://clc.li/api/url/add"

    long_url = {
        "url": url
    }

    response = requests.post(
        url=connect_url,
        headers=headers,
        json=long_url,
        cookies=cookies
    )
    response.raise_for_status()
    short_url = response.json().get("shorturl")

    if short_url:
        parsed = urlparse(short_url)
        return f"{parsed.netloc}{parsed.path}"


def count_clicks(headers, cookies, url):
    payload = {'short': url}
    connect_url = "https://clc.li/api/urls"

    response = requests.get(
        url=connect_url,
        headers=headers,
        cookies=cookies,
        params=payload
    )
    response.raise_for_status()
    return response.json().get("data").get("clicks")


def is_bitlink(headers, cookies, url):
    payload = {'short': url}
    connect_url = "https://clc.li/api/urls"

    response = requests.get(
        url=connect_url,
        headers=headers,
        cookies=cookies,
        params=payload
    )
    response.raise_for_status()
    return response.json().get("data") is not None


def main():
    token = config("CLCLI_TOKEN")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    cookies = {
            "beget": "begetok"
    }

    link = input("Введите URL для сокращения: ").strip()

    try:
        if is_bitlink(headers, cookies, link):
            print("Количество кликов по короткой ссылке:", end=" ")
            print(count_clicks(headers, cookies, link))
        else:
            print("Короткая ссылка", end=" ")
            print(shorten_link(headers, cookies, link))

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e.response.status_code} ")


if __name__ == '__main__':
    main()
