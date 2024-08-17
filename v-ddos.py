import requests
from concurrent.futures import ThreadPoolExecutor
import argparse
import time

# 定义发送请求的函数
def send_request(url, retries):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers)
            print(f"Response Code: {response.status_code} for URL: {url}")
            return
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            time.sleep(1)  # 等待1秒后重试
    print(f"Failed to reach {url} after {retries} attempts.")

# 主函数
def main():
    parser = argparse.ArgumentParser(description="HTTP压力测试工具")
    parser.add_argument("url", help="测试目标URL")
    parser.add_argument("requests_per_second", type=int, help="每秒请求数量（最小为1）")
    parser.add_argument("--retries", type=int, default=3, help="最大重试次数（默认3）")
    
    args = parser.parse_args()

    if args.requests_per_second < 1:
        print("每秒请求数量必须大于或等于1")
        return

    url = args.url
    requests_per_second = args.requests_per_second
    delay = 1.0 / requests_per_second  # 计算每个请求之间的延迟

    with ThreadPoolExecutor(max_workers=requests_per_second) as executor:
        try:
            while True:  # 无限循环
                executor.submit(send_request, url, args.retries)
                time.sleep(delay)  # 控制请求速率
        except KeyboardInterrupt:
            print("压力测试已停止。")

if __name__ == "__main__":
    main()
