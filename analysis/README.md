# JD Powerbank Top 50 - Analysis

**This README includes both English and 中文 versions.**  
**Click to jump to: [English Version](#english-version) | [中文说明](#中文说明)**

---

## English Version

This folder contains a Jupyter notebook for analyzing the crawled JD.com power bank data.

---

### Purpose

The analysis notebook helps you:
- Visualize and compare positive rates across stores and products.
- Identify products with the lowest positive rates.
- Explore common pain points using negative review keywords.
- Prepare plots and summary tables for reporting.

---

### Requirements

- Python 3.8+
- Jupyter Notebook
- pandas
- matplotlib
- HanLP (optional, for Chinese keyword extraction)

---

### How to Use

1️. **Prepare Data**

* Ensure the merged reviews file `jd_reviews_all.csv` is in the `../data/` folder.

2️. **Open Notebook**

```bash
jupyter notebook jd_pb_50analysis.ipynb
````

3️. **Run Cells**

* Follow the notebook steps:

  * Load and clean data.
  * Visualize store and product positive rates.
  * Highlight products with low ratings.
  * Analyze negative reviews (optional: run HanLP for keyword extraction).

---

### Output

* Plots and tables showing:

  * Store-level ranking.
  * Product-level ranking.
  * Top negative review keywords.

* Results can be saved as images or embedded directly in reports.

---

### Notes

* For more accurate keyword results, you may combine HanLP with manual curation.

---

## 中文说明

本文件夹包含用于分析京东充电宝 Top 50 评论数据的 Jupyter Notebook。

---

### 功能简介

此分析笔记本用于：

* 可视化并对比不同店铺和商品的好评率。
* 找出好评率最低的商品。
* 从差评中提取常见痛点关键词。
* 生成可用于报告的图表和汇总表。

---

### 运行环境

* Python 3.8+
* Jupyter Notebook
* pandas
* matplotlib
* HanLP（可选，用于中文关键词提取）

---

### 使用方法

1️. **准备数据**

* 确保已将合并好的评论文件 `jd_reviews_all.csv` 放在 `../data/` 文件夹内。

2️. **打开笔记本**

```bash
jupyter notebook jd_pb_50analysis.ipynb
```

3️. **逐步执行**

* 按照 Notebook 中的步骤依次执行：

  * 加载并清洗数据
  * 可视化店铺和商品好评率
  * 找出低评分商品
  * 分析差评（可选：使用 HanLP 提取关键词）

---

### 输出结果

* 包含：

  * 店铺层级排名
  * 商品层级排名
  * 差评关键词汇总

* 结果可保存为图片或直接用于报告中。

---

### 注意事项

* 若想获得更准确的关键词结果，可结合 HanLP 分词与人工筛选。

