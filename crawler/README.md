# JD Powerbank Top 50 - Crawler

This folder contains Python scripts to crawl product info and reviews from JD.com.

---

## Purpose

The crawler can:
- Automatically collect top N product SKUs and store names from any JD category page.
- Extract each product’s review stats: positive, neutral, and negative counts.
- Scrape up to 5 negative review texts for each product.
- Save data to CSV for further analysis.

> **Note:**  
> Although originally designed for power banks, you can use it for other JD product categories — just replace the power bank category URL with your desired category search URL.

---

## Requirements

- Python 3.8+
- Selenium
- ChromeDriver
- pandas

---

## How to Use

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

## Output

* SKU list CSV:
  `../data/jd_top50_skus.csv`

* Reviews CSV for each batch:
  `../data/jd_reviews_[start]_[end].csv`

* Merged CSV:
  `../data/jd_reviews_all.csv`

---

## Notes

* JD.com has anti-bot protections:

  * Use random sleep (`random_sleep`) to mimic human actions.
  * Split crawling into batches.
  * Always update cookies if blocked.

