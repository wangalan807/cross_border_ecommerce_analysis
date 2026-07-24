
#  Cross_border E-commerce Advertising Analysis

一个基于 Python + MySQL +Pandas + Matplotlib 的跨境电商广告数据分析项目

---


#  项目简介
本项目模拟跨境电商平台的订单数据和广告投放数据，通过数据分析与可视化，完成：

- 国家销售额分析

- 广告 ROI 分析

- 广告转化率分析

- Dashboard 可视化展示

项目目标是构建一个完整的数据分析流程，包括：
数据库读取→ 数据处理→ 数据分析→ 数据可视化→ Dashboard 展示

---

#  技术栈

##  Python
      -Pandas
      -Matplotlib
      -PyMySQL
##  Database
      -MySQL
##  IDE
      -PyCharm

---

# 项目结构

```text
ecommerce_analysis/
│
├──data/                          # 原始数据
├──outputs/                       # 图表输出
│
├──src/
│    ├──analyzer.py               # 数据分析
│    ├──database.py               # 数据库连接
│    ├──loader.py                 # 数据读取
│    └──visualizer.py             # 数据可视化
│
├──main.py                        # 主程序入口
│
├──notebooks/
│  └──01_data_analysis.ipynb
│
└──README.md
```

---

###  数据完整性检查
本项目对清洗后的订单数据，广告数据和国家指标数据进行了完整性检查，包括：
- 表格是否为空
- 字段是否完整
- 缺失值检查
- 重复行检查

检查结果显示，三张核心数据表均无缺失值，无重复行，可以进行后续分析和可视化阶段。

# 项目功能

## 1.国家销售额分析

分析不同国家的销售额表现：

  - Australia 销售额最高
  - Canada 销售额最低

**输出图表：**

  - `sales_by_country.png`

---
## 2.广告ROI分析
计算广告投资回报率（ ROI ）：
ROI = 销售额 / 广告成本

分析结果：
  - UK ROI 最高
  - Germany / USA / Canada ROI 较低

**输出图表：**
  - `roi_by_country.png`

---

## 3.广告转化分析
计算广告点击转化率：
 Conversion Rate = (conversions / clicks ) * 100%
分析结果：

  - USA 转化率最高
  - Australia 转化率最低

**输出图表：**
  - `conversion_rate_by_country.png`

---

##  4. Dashboard 可视化
项目生成完整广告分析 Dashboard :
包含：

- Sales by Country

- ROI by Country

- Conversion Rate by Country

**输出图表：**
- `advertising_dashboard.png`

## 5. Dashboard 高级优化
本项目在基础数据分析和可视化的基础上，进一步对 Dashboard 进行了商业化优化，使其更接近真实企业 BI 报表。

### 1. KPI Cards

Dashboard 顶部展示核心业务指标，包括：
  - Total Sales: 总销售额
  - Top Sales Country: 销售额最高国家
  - Average ROI: 平均广告投资回报率
  - Best Conversion Rate Country: 转化率最高国家

这些 KPI 可以帮助业务方快速了解整体经营表现。

### 2. Top3 Highlight

在 Sales by Country 图表中，对销售额排名前三的国家进行高亮显示，其余国家用灰色显示。
这样可以让用户快速识别市场。

### 3. ROI Ranking
ROI by Country 图标按照 ROI 从高到低排序。

通过排序，可以快速发现广告投放效率最高的国家。


### 4. Conversion Rate Formatting
Conversion Rate by Country 图表使用百分比格式展示转化率。

这样更符合广告分析和业务汇报规范。


### 5. Daily Sales Trend
Dashboard 底部加入 Daily Sales Trend 折线图，用于观察每日销售额变化趋势。

同时加入 2—Day Moving Average 移动平均线，用于平滑短期波动，辅助观察整体趋势。

### 6. Anomaly Detection
在每日销售趋势图中，自动标记最低销售日。

本项目中， 03-04 的销售额最低，因此用红色标注为 Lowest Sales 。

这可以帮助业务方快速发现异常波动。


### 7. Key Insights
Dashboard 底部加入商业洞察分析：
- Australia leads sales
- UK delivers the best ROI
- USA achieves top conversion
- 03-04 sales dropped sharply

这些洞察可以帮助业务方快速理解数据背后的业务含义。


---

#  如何运行项目

## 1.安装依赖
```bash
  pip install pandas matplotlib pymysql
```

---
# 2.启动 MySQL
确保 MySQL 服务已启动。

---

# 3.运行主程序

```bash
  python main.py
```
运行后将在 outputs/ 文件夹生成分析图表。

---

# 项目收获

通过本项目，我完成了：
- MySQL 数据读取
- Pandas 数据分析
- 商业指标计算
- 数据可视化
- Dashboard 开发
- Python 工程化模块拆分

---

# 后续优化方向
未来计划加入：

- 用户消费分析
- 产品利润分析
- Power BI Dashboard
- Streamlit Web Dashboard
- 大规模数据集

---

# 作者

## 王少华

## 河南工业大学/土木工程专业

## 数据分析项目

