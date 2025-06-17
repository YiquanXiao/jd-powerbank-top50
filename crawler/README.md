# JD Powerbank Top 50 - Crawler

**This README includes both English and 中文 versions.**  
**Click to jump to: [English Version](#english-version) | [中文说明](#中文说明)**

---

## English Version

This folder contains Python scripts to crawl product info and reviews from JD.com.

---

### Purpose

The crawler can:
- Automatically collect top N product SKUs and store names from any JD category page.
- Extract each product’s review stats: positive, neutral, and negative counts.
- Scrape up to 5 negative review texts for each product.
- Save data to CSV for further analysis.

> **Note:**  
> Although originally designed for power banks, you can use it for other JD product categories — just replace the power bank category URL with your desired category search URL.

---

### Requirements

- Python 3.8+
- Selenium
- ChromeDriver
- pandas

---

### How to Use

1️. **Prepare Cookies**

* Log in to JD.com manually in Chrome.
* Export your cookies to JSON (e.g., using a browser extension).
* Save the cookie file, e.g., `jd_cache.json`.

2️. **Configure**

* Edit `jd_pb_50review.py` to set:
  * `webdriver_path`
  * `cookie_path`
  * `category_url` (change this to any JD category page)

3️. **Run**

* To scrape SKUs:

  ```python
  scrape_jd_top50_skus(
      webdriver_path=...,
      cookie_path=...,
      category_url=...,
      output_csv_path=...,
      user_agent=...,
      ...
  )
  ```

* To scrape reviews:

  ```python
  scrape_jd_reviews(
      webdriver_path=...,
      cookie_path=...,
      skus_csv_path=...,
      output_csv_path=...,
      user_agent=...,
      start_idx=0,
      end_idx=10,
      ...
  )
  ```

> It’s recommended to crawl reviews in small batches (e.g., 10 at a time) and re-login/re-save cookies between batches to avoid JD detection.

* To merge multiple crawl results:

  ```python
  combine_jd_reviews_csv(
      data_dir="../data/",
      output_filename="jd_reviews_all.csv"
  )
  ```

---

### Output

* SKU list CSV:
  `../data/jd_top50_skus.csv`

* Reviews CSV for each batch:
  `../data/jd_reviews_[start]_[end].csv`

* Merged CSV:
  `../data/jd_reviews_all.csv`

---

### Notes

* JD.com has anti-bot protections:

  * Use random sleep (`random_sleep`) to mimic human actions.
  * Split crawling into batches.
  * Always update cookies if blocked.

---

## 中文说明

本文件夹包含用于抓取京东商品信息和评论的 Python 脚本。

---

### 功能简介

此爬虫可以：

* 自动从任意京东商品品类页收集前 N 件商品的 SKU 和店铺名。
* 提取每个商品的评论数据（好评数、中评数、差评数）。
* 抓取每个商品最多 5 条差评文本。
* 将结果保存为 CSV 文件，供后续分析使用。

> **提示：**
> 虽然本项目最初用于抓取充电宝数据，但也可用于其他京东品类，只需将充电宝的搜索链接替换为你想要抓取的品类链接即可。

---

### 运行环境

* Python 3.8+
* Selenium
* ChromeDriver
* pandas

---

### 使用方法

1️. **准备 Cookies**

* 在 Chrome 浏览器中手动登录京东。
* 使用浏览器插件等工具导出登录后的 Cookies 为 JSON 文件。
* 将文件保存为 `jd_cache.json`（或其他任意名称）。

2️. **配置参数**

* 编辑 `jd_pb_50review.py`，设置：

  * `webdriver_path`（ChromeDriver 路径）
  * `cookie_path`（Cookie 文件路径）
  * `category_url`（京东品类链接）

3️. **运行**

* 抓取 SKU：

  ```python
  scrape_jd_top50_skus(
      webdriver_path=...,
      cookie_path=...,
      category_url=...,
      output_csv_path=...,
      user_agent=...,
      ...
  )
  ```

* 抓取评论：

  ```python
  scrape_jd_reviews(
      webdriver_path=...,
      cookie_path=...,
      skus_csv_path=...,
      output_csv_path=...,
      user_agent=...,
      start_idx=0,
      end_idx=10,
      ...
  )
  ```

> 建议将评论抓取分成小批次（如每次抓 10 个），每次抓取后重新登录并更新 Cookies，以降低被封禁风险。

* 合并多次抓取结果：

  ```python
  combine_jd_reviews_csv(
      data_dir="../data/",
      output_filename="jd_reviews_all.csv"
  )
  ```

---

### 输出结果

* SKU 列表 CSV：
  `../data/jd_top50_skus.csv`

* 各批次评论 CSV：
  `../data/jd_reviews_[start]_[end].csv`

* 合并后的评论 CSV：
  `../data/jd_reviews_all.csv`

---

### 注意事项

* 京东有防爬虫机制：

  * 使用 `random_sleep` 随机等待模拟人工行为。
  * 分批次抓取，避免一次性获取过多数据。
  * 若被封禁需重新登录并更新 Cookies。



