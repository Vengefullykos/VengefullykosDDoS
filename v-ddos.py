import requests
from concurrent.futures import ThreadPoolExecutor
import argparse
import time

# Define the function to send requests
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
            time.sleep(1)  # Wait for 1 second before retrying
    print(f"Failed to reach {url} after {retries} attempts.")

# Main function
def main():
    parser = argparse.ArgumentParser(description="HTTP Stress Testing Tool")
    parser.add_argument("url", help="Target URL for testing")
    parser.add_argument("requests_per_second", type=int, help="Number of requests per second (minimum is 1)")
    parser.add_argument("--retries", type=int, default=3, help="Maximum number of retries (default is 3)")
    
    args = parser.parse_args()

    if args.requests_per_second < 1:
        print("Requests per second must be greater than or equal to 1")
        return

    url = args.url
    requests_per_second = args.requests_per_second
    delay = 1.0 / requests_per_second  # Calculate the delay between each request

    with ThreadPoolExecutor(max_workers=requests_per_second) as executor:
        try:
            while True:  # Infinite loop
                executor.submit(send_request, url, args.retries)
                time.sleep(delay)  # Control the request rate
        except KeyboardInterrupt:
            print("Stress testing has been stopped.")

if __name__ == "__main__":
    main()
