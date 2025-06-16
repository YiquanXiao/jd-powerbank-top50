import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  # for change chrome setting 
from selenium.webdriver.chrome.service import Service  # for manage chromedriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
import re
import time
import random
import json
import os
from typing import List
from pprint import pprint


def get_chromedriver(
    webdriver_path: str = "chromedriver.exe",
    disable_logging: bool = True,
    headless: bool = False,
    user_agent: str | None = None,
    disable_automation_features: bool = True,
    patch_webdriver_property: bool = True,
    implicit_wait: int = 10
) -> WebDriver:
    """
    Launch the Chrome browser's WebDriver.
    启动 Chrome 浏览器的 WebDriver。

    Args:
        webdriver_path (str): Path to chromedriver.exe. Defaults to current directory.
                              chromedriver.exe 的路径，默认当前目录。
        disable_logging (bool): Whether to suppress Chrome logs. Defaults to True.
                                是否禁用控制台日志输出，默认 True。
        headless (bool): Whether to run Chrome in headless mode (no GUI). Defaults to False.
                         是否以无头模式运行浏览器，默认 False。
        user_agent (str or None): Custom User-Agent string. If None, no override.
                                  Can use https://www.whatismybrowser.com/detect/what-is-my-user-agent/ to find your current User-Agent.
                                  自定义 User-Agent 字符串，默认 None 表示不更改。
                                  可以使用 https://www.whatismybrowser.com/detect/what-is-my-user-agent/ 来查看当前 User-Agent。
        disable_automation_features (bool): Disable automation flags to bypass detection. Defaults to True.
                                            是否关闭 Chrome 的自动化特征（例如自动扩展），默认 True。
        patch_webdriver_property (bool): Patch navigator.webdriver to avoid detection. Defaults to True.
                                         是否将 navigator.webdriver 设置为 undefined，默认 True。
        implicit_wait (int): Global implicit wait time in seconds. Defaults to 10.
                             全局隐式等待时间（秒），默认 10 秒。

    Returns:
        webdriver.Chrome: Initialized Chrome WebDriver instance.
                          已初始化的 Chrome WebDriver 实例。
    """
    options = Options()

    # Suppress Chrome logs
    # 禁用 Chrome 日志输出
    if disable_logging:
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # Enable headless mode (no browser UI)
    # 启用无头模式（不显示浏览器界面）
    if headless:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920x1080")

    # Set custom User-Agent if provided
    # 设置自定义 User-Agent（如果传入）
    if user_agent is not None:
        options.add_argument(f"user-agent={user_agent}")

    # Disable automation detection features
    # 关闭自动化检测相关特征
    if disable_automation_features:
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # Initialize WebDriver
    # 初始化 WebDriver
    wd = webdriver.Chrome(service=Service(webdriver_path), options=options)

    # Apply implicit wait
    # 设置全局隐式等待时间
    wd.implicitly_wait(implicit_wait)

    # Patch navigator.webdriver = undefined to evade detection
    # 修改 navigator.webdriver 为 undefined 以规避检测
    if patch_webdriver_property:
        wd.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """
        })

    return wd


def random_sleep(
    min_sec: float = 9.0,
    max_sec: float = 12.0
) -> None:
    """
    Sleep for a random duration between min_sec and max_sec.
    Used to simulate human behavior and avoid detection as an automated script.
    
    在 min_sec 到 max_sec 之间随机 sleep 一段时间。
    用于模拟人类行为，避免被检测为自动脚本。

    Args:
        min_sec (float): Minimum sleep duration in seconds.
                         最小睡眠时间（秒），默认 9.0 秒。
        max_sec (float): Maximum sleep duration in seconds.
                         最大睡眠时间（秒），默认 12.0 秒。
    """
    delay = random.uniform(min_sec, max_sec)
    time.sleep(delay)


def clean_and_add_cookies(
    wd: WebDriver,
    cookie_path: str
) -> None:
    """
    Load cookies from a JSON file and add them to the WebDriver instance.
    从 JSON 文件加载 Cookie 并添加到 WebDriver 实例中。

    Args:
        wd (webdriver.Chrome): 
            The initialized Chrome WebDriver instance. 
            已初始化的 Chrome WebDriver 实例。
        cookie_path (str): 
            Path to the cookie file in JSON format.
            Cookie 文件的路径，格式为 JSON。
    """
    # Open the cookie file and load cookies
    # 打开 Cookie 文件并加载 Cookie
    with open(cookie_path, "r", encoding="utf-8") as f:
            cookies = json.load(f)
        
    # Clean the cookie data: Cookies may have None or "no_restriction" values that need to be converted to valid values
    # 清洗 Cookie 数据: Cookie 中有些值为 None 或 "no_restriction"，需要转换为合法值
    for c in cookies:
        # Convert "no_restriction" or None to valid values
        # 将 "no_restriction" 或 None 转换为合法值
        if c.get("sameSite") not in ["Strict", "Lax", "None"]:
            c["sameSite"] = "None"
        # # Selenium does not accept null values, so we need to remove these keys
        # # Selenium 不接受 null，需要删除这些键
        # for key in list(c.keys()):
        #     if c[key] is None:
        #         del c[key]
    
    # Add cookies to the WebDriver
    # 将 Cookie 添加到 WebDriver
    for ck in cookies:
        wd.add_cookie(ck)


def parse_count(text: str) -> int:
    """
    Parse a Chinese count string like '2万+', '200+' or '27' into an integer.
    解析中文计数字符串，如 '2万+'、'200+' 或 '27'，返回整数。
    
    Args:
        text (str): The count string to parse.
                    要解析的计数字符串。
    
    Returns:
        int: The parsed integer value.
             解析后的整数值。
    """
    text = text.rstrip('+')
    if text.endswith('万'):
        # convert "x万" to integer
        num = float(text[:-1])
        return int(num * 10000)
    return int(text)


def scrape_jd_top50_skus(
    webdriver_path: str,
    cookie_path: str,
    category_url: str,
    output_csv_path: str,
    user_agent: str,
    disable_logging: bool = True,
    headless: bool = False,
    disable_automation_features: bool = True,
    patch_webdriver_property: bool = True,
    implicit_wait: int = 30,
    top_n: int = 50
) -> list[str]:
    """
    抓取京东指定分类页前 top_n 件商品的 SKU 以及店铺名，并保存到 CSV。
    Scrape the top N product SKUs and Store names from a specified JD category page and save them to a CSV file.

    Args:
        webdriver_path (str): 
            ChromeDriver executable path.
        cookie_path (str): 
            Path to the JSON file containing cookies.
        category_url (str): 
            URL of the JD category page to scrape.
        output_csv_path (str): 
            Path where the output CSV will be saved.
        user_agent (str): 
            Browser User-Agent string.
        disable_logging (bool): 
            Whether to disable browser logging (default True).
        headless (bool): 
            Whether to run the browser in headless mode (default False).
        disable_automation_features (bool): 
            Whether to disable automation features (default True).
        patch_webdriver_property (bool): 
            Whether to patch the webdriver property (default True).
        implicit_wait (int): 
            Implicit wait time in seconds (default 30).
        top_n (int): 
            Number of SKUs to scrape (default 50).

    Returns:
        list[dict[str, str]]: A list of dictionaries. Each dictionary contains:
            - 'SKU' (str): The SKU number of the product.
            - 'Store' (str): The store name
    """
    # Initialize the Chrome WebDriver with the specified options
    driver = get_chromedriver(
        webdriver_path=webdriver_path,
        disable_logging=disable_logging,
        headless=headless,
        user_agent=user_agent,
        disable_automation_features=disable_automation_features,
        patch_webdriver_property=patch_webdriver_property,
        implicit_wait=implicit_wait
    )

    try:
        # Open JD homepage to load initial cookies
        driver.get("https://www.jd.com/?country=USA")
        random_sleep()

        # Load cookies from file and add them to the browser session
        clean_and_add_cookies(driver, cookie_path)
        driver.refresh()
        random_sleep()

        # Navigate to the target category page
        print("Navigating to JD category page...")
        driver.get(category_url)
        random_sleep()

        # Scroll to the bottom to trigger lazy-loading of products
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        random_sleep()
        
        # Get the full list of items after scrolling
        items = driver.find_elements(By.CSS_SELECTOR, "#J_goodsList .gl-item")
        print(f"Total items found: {len(items)}")

        # Extract SKU and store information from the items
        sku_store_list = []
        for i, item in enumerate(items):
            if i >= top_n:
                break
            
            sku = item.get_attribute("data-sku")
            try:
                store = item.find_element(By.CSS_SELECTOR, ".p-shop").text.strip()
            except: 
                store = ""

            if sku:
                sku_store_list.append({
                    "SKU": sku,
                    "Store": store
                })

    finally:
        # Ensure the browser is closed even if an error occurs
        driver.quit()

    # Save the list of SKUs and their corresponding stores to a CSV file
    df = pd.DataFrame(sku_store_list)
    df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")
    print(f"Saved top {len(sku_store_list)} SKUs (and Stores) to {output_csv_path}")

    return sku_store_list


def scrape_jd_reviews(
    webdriver_path: str,
    cookie_path: str,
    skus_csv_path: str,
    output_csv_path: str,
    user_agent: str,
    start_idx: int = 0,
    end_idx: int = 50,
    disable_logging: bool = True,
    headless: bool = False,
    disable_automation_features: bool = True,
    patch_webdriver_property: bool = True,
    implicit_wait: int = 30
) -> list[dict]:
    """
    抓取京东商品评论信息（包含好评率、评价数及前5条差评），并保存到 CSV。
    Scrape JD product reviews information (including positive rate, counts, and up to 5 negative reviews) and save to a CSV file.

    Args:
        webdriver_path (str): 
            Path to the ChromeDriver executable.
        cookie_path (str): 
            Path to the JSON cookie file.
        skus_csv_path (str): 
            Path to the CSV file containing the list of SKUs.
        output_csv_path (str): 
            Path where the output reviews CSV will be saved.
        user_agent (str): 
            Browser User-Agent string.
        start_idx (int): 
            Starting index of SKUs to process (inclusive).
        end_idx (int): 
            Ending index of SKUs to process (exclusive).
        disable_logging (bool): 
            Whether to disable browser logging (default True).
        headless (bool): 
            Whether to run in headless mode (default False).
        disable_automation_features (bool): 
            Whether to disable automation features (default True).
        patch_webdriver_property (bool): 
            Whether to patch the webdriver property (default True).
        implicit_wait (int): 
            Implicit wait time in seconds (default 30).

    Returns:
        list[dict]: A list of dictionaries, each containing review data for a SKU.
    """
    # Initialize the WebDriver
    driver = get_chromedriver(
        webdriver_path=webdriver_path,
        disable_logging=disable_logging,
        headless=headless,
        user_agent=user_agent,
        disable_automation_features=disable_automation_features,
        patch_webdriver_property=patch_webdriver_property,
        implicit_wait=implicit_wait
    )

    try:
        # Open JD homepage and apply cookies
        driver.get("https://www.jd.com/?country=USA")
        random_sleep()
        clean_and_add_cookies(driver, cookie_path)
        driver.refresh()
        random_sleep()

        # Load SKU list from CSV
        sku_df = pd.read_csv(skus_csv_path, encoding="utf-8-sig")

        reviews_info: list[dict] = []

        for idx, row in sku_df.iterrows():
            if idx < start_idx or idx >= end_idx:
                continue
            
            # Extract SKU and Store from the DataFrame row
            sku = row["SKU"]
            store = row["Store"]
            print(f"Processing item {idx + 1}/{len(sku_df)}: SKU = {sku}")
            
            review = {
                "SKU": sku, 
                "product_name": "",
                "store": store,
                "positive_rate": "0%",
                "positive_count": 0,
                "neutral_count": 0,
                "negative_count": 0,
                "negative_review_1": "",
                "negative_review_2": "",
                "negative_review_3": "",
                "negative_review_4": "",
                "negative_review_5": ""
            }

            # Navigate to product page
            product_url = f"https://item.jd.com/{sku}.html"
            driver.get(product_url)
            random_sleep()

            # Extract product name
            review["product_name"] = driver.find_element(
                By.XPATH, '/html/body/div[4]/div/div[2]/div/div[5]/div[1]/span[1]'
            ).text.strip()

            # Click "All Reviews" to open the reviews section
            all_reviews_btn = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@id="comment-root"]/div[@class="all-btn"]'))
                # EC.element_to_be_clickable((By.XPATH, '//*[@id="comment-root"]/div[3]/div'))
            )
            all_reviews_btn.click()
            random_sleep()

            # Wait for review tags overlay and collect tag elements
            rate_list = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.ID, "rateList"))
            )
            tag_divs = driver.find_elements(By.XPATH, '//*[@id="rateList"]/div/div[2]/div/div')
            random_sleep()

            # Parse each review tag for counts and rates
            for tag in tag_divs:
                label = tag.find_element(By.XPATH, './span[1]').text.strip()
                value = tag.find_element(By.XPATH, './span[2]').text.strip()
                if label == "全部":
                    m = re.match(r'(\d+\.?\d*)%', value)
                    review["positive_rate"] = f"{m.group(1)}%" if m else "0%"
                elif label == "好评":
                    review["positive_count"] = parse_count(value)
                elif label == "中评":
                    review["neutral_count"] = parse_count(value)
                elif label == "差评":
                    review["negative_count"] = parse_count(value)
                    tag.click()
                    random_sleep()

            # If there are negative reviews, scroll and extract up to 5
            if review["negative_count"] > 0:
                scrollable_div = driver.find_element(By.XPATH, '//*[@id="rateList"]/div/div[3]')
                for _ in range(5):
                    driver.execute_script("arguments[0].scrollTop += 300", scrollable_div)
                    random_sleep(2, 3)
                for n in range(1, 6):
                    try:
                        review_xpath = f'//*[@id="rateList"]/div/div[3]/div[@class="_list_1ygkr_67"]/div/div/div/div/div[{n}]/div/div/div[2]/div[2]/span'
                        review_elem = driver.find_element(By.XPATH, review_xpath)
                        review[f"negative_review_{n}"] = review_elem.text.strip()
                    except:
                        review[f"negative_review_{n}"] = ""

            reviews_info.append(review)

    finally:
        # Ensure the browser is closed
        driver.quit()

    # Save all reviews to CSV
    reviews_df = pd.DataFrame(reviews_info)
    reviews_df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")
    print(f"Saved reviews for SKUs {start_idx+1} to {end_idx} into {output_csv_path}")

    return reviews_info


def combine_jd_reviews_csv(
    data_dir: str = "../data/", 
    output_filename: str = "jd_reviews_all.csv"
) -> None:
    """
    合并指定目录下所有包含 'jd_reviews' 的 CSV 文件到一个总文件中，并保存为 jd_reviews_all.csv。
    Combine all CSV files with 'jd_reviews' in their filename from the given directory
    into a single CSV file named 'jd_reviews_all.csv'.

    Args:
        data_dir (str): 存放 CSV 文件的目录路径。Directory containing the review CSV files.
        output_filename (str): 合并后输出文件名。Name of the combined output CSV file.
    """
    # List all files in the data directory
    files: List[str] = os.listdir(data_dir)
    # Filter for CSV files that contain 'jd_reviews' in the filename
    review_files = [f for f in files if f.endswith(".csv") and "jd_reviews" in f]

    if not review_files:
        print(f"No 'jd_reviews' CSV files found in {data_dir}")
        return

    # Read each CSV into a DataFrame
    df_list: List[pd.DataFrame] = []
    for filename in review_files:
        path = os.path.join(data_dir, filename)
        print(f"Reading {path}...")
        df = pd.read_csv(path, encoding="utf-8-sig")
        df_list.append(df)

    # Concatenate all DataFrames
    combined_df = pd.concat(df_list, ignore_index=True)
    output_path = os.path.join(data_dir, output_filename)

    # Save the combined DataFrame to CSV
    combined_df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"Saved combined reviews to {output_path}")



if __name__ == "__main__":
    webdriver_path = "../../chromedriver.exe"
    cookie_path = "../data/jd_cache.json"
    category_url = "https://list.jd.com/list.html?cat=9987%2C830%2C13658&psort=3&psort=3&0.7649336460749802#J_main"
    jd_skus_path = "../data/jd_top50_skus.csv"
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
    
    # # Scrape the top 50 SKUs from the specified JD category page
    # # 从指定的京东分类页面抓取前 50 件商品的 SKU
    # skus = scrape_jd_top50_skus(
    #     webdriver_path=webdriver_path,
    #     cookie_path=cookie_path,
    #     category_url=category_url,
    #     output_csv_path=jd_skus_path,
    #     user_agent=ua,
    #     headless=False
    # )
    
    # Scrape reviews for the SKUs in batches of 10 (e.g., 0-10, 10-20, 20-30, etc.)
    # Every time after running, re-login and save cookies
    # 推荐10个10个地抓取评论 (e.g., 0-10, 10-20, 20-30, etc.)
    # 每运行完一次之后，重新登录并保存cookie
    
    start_idx = 0
    end_idx = 10
    jd_reviews_path = f"../data/jd_reviews_{start_idx:02d}_{end_idx:02d}.csv"
    
    scrape_jd_reviews(
        webdriver_path=webdriver_path,
        cookie_path=cookie_path,
        skus_csv_path=jd_skus_path,
        output_csv_path=jd_reviews_path,
        user_agent=ua,
        start_idx=start_idx,
        end_idx=end_idx,
        headless=False
    )
    
    
    













