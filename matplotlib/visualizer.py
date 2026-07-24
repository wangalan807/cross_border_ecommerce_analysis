

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter



#=========定义主题颜色
BACKGROUND_COLOR = "#111111"
AXIS_BACKGROUND_COLOR = "#1a1a1a"
SALES_COLOR = "#4cc9f0"
ROI_COLOR = "#f4a261"
CONVERSION_COLOR = "#2ec4b6"
NORMAL_COLOR = "#666666"
TEXT_COLOR = "white"
GRID_COLOR = "gray"


# 1:画国家销售额图
def plot_country_sales(country_sales):
    fig,ax =plt.subplots(
        figsize=(8,5)
    )

    colors = [
        "#4cc9f0" if i < 3 else "#666666"
        for i in range(len(country_sales))
    ]

    country_sales.plot(
        kind="bar",
        ax=ax,
        color=colors
    )


    ax.set_title("Sales by Country")
    ax.set_xlabel("Country")
    ax.set_ylabel("Sales")
    ax.tick_params(axis="x",rotation=0)

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.5
    )

    for i,v in enumerate(country_sales):
        ax.text(i,v+1,f"{v:.0f}",ha="center")

    plt.savefig("outputs/sales_by_country.png")
    plt.show()

# 2：画广告投资回报率图
def plot_roi_chart(roi_df):
    fig,ax = plt.subplots(
        figsize=(8,5)
    )
    ax.bar(
        roi_df["country"],
        roi_df["ROI"],
        color="orange"
    )
    ax.set_title("ROI by Country")
    ax.set_xlabel("Country")
    ax.set_ylabel("ROI")
    ax.tick_params(axis="x",rotation=0)

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.5
    )
    for i,v in enumerate(roi_df["ROI"]):
        ax.text(i,v+0.01,f"{v:.2f}",ha="center")
    plt.savefig("../outputs/roi_by_country.png")
    plt.show()

# 3:画点击转换率柱状图
def plot_conversion_rate(conversion_df):
    fig,ax = plt.subplots(
        figsize=(8,5)
    )
    ax.bar(
        conversion_df["country"],
        conversion_df["conversion_rate"],
        color="green"
    )

    ax.set_title("Conversion Rate by Country")
    ax.set_xlabel("Country")
    ax.set_ylabel("Conversion Rate")
    ax.tick_params(axis="x",rotation=0)

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.5
    )

    for i,v in enumerate(conversion_df["conversion_rate"]):
        ax.text(i,v+0.01,f"{v:.2f}%",ha="center")

    plt.savefig("outputs/conversion_rate_by_country.png")
    plt.show()


# 4:画dashboard图
def plot_ad_dashboard(country_sales,roi_df,conversion_df,daily_sales,kpi_metrics):

    roi_df = roi_df.sort_values(
        by="ROI",
        ascending=False
    )

    fig = plt.figure(figsize=(16,10))

    gs = fig.add_gridspec(2,3)

    ax1 = fig.add_subplot(gs[0,0])
    ax2 = fig.add_subplot(gs[0,1])
    ax3 = fig.add_subplot(gs[0,2])
    ax4 = fig.add_subplot(gs[1,:])




    fig.patch.set_facecolor(BACKGROUND_COLOR)
    fig.suptitle(
        "Cross-border E-commerce Advertising Dashboard",
        fontsize=18,
        fontweight="bold",
        color=TEXT_COLOR
    )

    fig.text(
        0.18,
        0.86,
        f"Total Sales\n{kpi_metrics['total_sales']:.2f}",
        color=TEXT_COLOR,
        fontsize=18,
        fontweight="bold",
        ha="center",
        va="center",
        bbox=dict(
            facecolor=AXIS_BACKGROUND_COLOR,
            edgecolor=SALES_COLOR,
            boxstyle="round,pad=0.7",
            linewidth=1.5
        )
    )
    fig.text(
        0.42,
        0.86,
        f"Top Sales Country\n{kpi_metrics['top_sales_country']}",
        color=TEXT_COLOR,
        fontsize=13,
        fontweight="bold",
        ha="center",
        va="center",
        bbox=dict(
            facecolor=AXIS_BACKGROUND_COLOR,
            edgecolor=ROI_COLOR,
            boxstyle="round,pad=0.6"
        )
    )

    fig.text(
        0.60,
        0.86,
        f"Average ROI\n{kpi_metrics['avg_roi']:.2f}",
        color=TEXT_COLOR,
        fontsize=13,
        fontweight="bold",
        ha="center",
        va="center",
        bbox=dict(
            facecolor=AXIS_BACKGROUND_COLOR,
            edgecolor=ROI_COLOR,
            boxstyle="round,pad=0.6"
        )
    )

    fig.text(
        0.82,
        0.86,
        f"Best Conversion Rate Country\n{kpi_metrics['best_conversion_rate_country']}",
        color=TEXT_COLOR,
        fontsize=13,
        fontweight="bold",
        ha="center",
        va="center",
        bbox=dict(
            facecolor=AXIS_BACKGROUND_COLOR,
            edgecolor=CONVERSION_COLOR,
            boxstyle="round,pad=0.6"
        )


    )


    for ax in [ax1,ax2,ax3,ax4]:
        ax.set_facecolor(AXIS_BACKGROUND_COLOR)
        ax.title.set_color(TEXT_COLOR)
        ax.xaxis.label.set_color(TEXT_COLOR)
        ax.yaxis.label.set_color(TEXT_COLOR)
        ax.tick_params(colors=TEXT_COLOR)

        for spine in ax.spines.values():
            spine.set_color(TEXT_COLOR)


    sales_color = [
        SALES_COLOR if i<3 else NORMAL_COLOR
        for i in range(len(country_sales))
    ]

    ax1.bar(
        country_sales.index,
        country_sales.values,
        color=sales_color
    )
    ax1.set_title("Sales by Country")
    ax1.set_xlabel("Country")
    ax1.set_ylabel("Sales")
    ax1.grid(
        axis="y",
        linestyle="--",
        alpha=0.5
    )
    for i,v in enumerate(country_sales.values):
        ax1.text(i,v+1,f"{v:.0f}",ha="center",color=TEXT_COLOR)


    ax2.bar(
        roi_df["country"],
        roi_df["ROI"],
        color=ROI_COLOR

    )

    ax2.set_title("ROI by Country")
    ax2.set_xlabel("Country")
    ax2.set_ylabel("ROI")
    ax2.grid(
        axis="y",
        linestyle="--",
        alpha=0.5
    )
    for i,v in enumerate(roi_df["ROI"]):
        ax2.text(i,v+0.01,f"{v:.2f}",ha="center",color=TEXT_COLOR)

    ax3.bar(
        conversion_df["country"],
        conversion_df["conversion_rate"],
        color=CONVERSION_COLOR
    )
    ax3.set_title("Conversion Rate by Country")
    ax3.set_xlabel("Country")
    ax3.set_ylabel("Conversion Rate")
    ax3.yaxis.set_major_formatter(
        FuncFormatter(lambda y,_:f"{y:.1f}%")
    )
    ax3.grid(
        axis="y",
        linestyle="--",
        alpha=0.5
    )
    for i,v in enumerate(conversion_df["conversion_rate"]):
        ax3.text(i,v+0.01,f"{v:.2f}%",ha="center",color=TEXT_COLOR)


    ax4.plot(
        daily_sales.index,
        daily_sales.values,
        marker="o",
        linewidth=3,
        color=SALES_COLOR
    )

    rolling_mean = daily_sales.rolling(window=2).mean()
    ax4.plot(
        rolling_mean.index,
        rolling_mean.values,
        linestyle="--",
        linewidth=2,
        color=ROI_COLOR,
        label="2-Day Moving Average"
    )


    legend = ax4.legend()
    legend.get_frame().set_facecolor(AXIS_BACKGROUND_COLOR)
    legend.get_frame().set_edgecolor(TEXT_COLOR)

    for text in legend.get_texts():
        text.set_color(TEXT_COLOR)


    lowest_date = daily_sales.idxmin()
    lowest_sales = daily_sales.min()
    top_sales_country = kpi_metrics["top_sales_country"]
    best_conversion_country = kpi_metrics["best_conversion_rate_country"]
    best_roi_country = roi_df.loc[
        roi_df["ROI"].idxmax(),
        "country"
    ]

    for x,y in zip(daily_sales.index,daily_sales.values):
        if x == lowest_date:
            continue

        ax4.text(
            x,y+2,
            f"{y:.0f}",
            ha="center",
            color=TEXT_COLOR
        )


    ax4.scatter(
        lowest_date,
        lowest_sales,
        color="red",
        s=80,
        zorder=5
    )

    ax4.text(
        lowest_date,
        lowest_sales + 5,
        f"Lowest Sales\n{lowest_sales:.0f}",
        color="red",
        ha="center",
        fontweight="bold"
    )

    ax4.set_title("Daily Sales Trend")
    ax4.set_xlabel("Date")
    ax4.set_ylabel("Sales")
    ax4.grid(
        linestyle="--",
        alpha=0.5
    )

    ax4.xaxis.set_major_locator(mdates.DayLocator())
    ax4.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))





    fig.text(
        0.05,
        0.04,
        "Key Insights:",
        color=TEXT_COLOR,
        fontsize=13,
        fontweight="bold"
    )

    fig.text(
        0.15,
        0.04,
        f"{top_sales_country} leads sales;",
        color=SALES_COLOR,
        fontsize=13,
        fontweight="bold"
    )

    fig.text(
        0.32,
        0.04,
        f"{best_roi_country} delivers the best ROI;",
        color=ROI_COLOR,
        fontsize=13,
        fontweight="bold"
    )

    fig.text(
        0.50,
        0.04,
        f"{best_conversion_country} achieves top conversion;",
        color=CONVERSION_COLOR,
        fontsize=13,
        fontweight="bold"
    )

    fig.text(
        0.78,
        0.04,
        f"{lowest_date.strftime('%m-%d')} sales dropped sharply.",
        color="red",
        fontsize=13,
        fontweight="bold"
    )




    plt.tight_layout(rect=[0,0.06,1,0.82])
    plt.savefig("outputs/advertising_dashboard.png")
    plt.show()


# 5.画每日销售额趋势图（折线图）

def plot_daily_sales_trend(daily_sales):
    plt.figure(figsize=(10,5))

    plt.plot(
        daily_sales.index,
        daily_sales.values,
        marker="o",
        linewidth=3
    )

    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))


    plt.title("Daily Sales Trend")
    plt.xlabel("Date")
    plt.ylabel("Sales")

    plt.grid(
        linestyle="--",
        alpha=0.5
    )

    for x,y in zip(daily_sales.index,daily_sales.values):
        plt.text(x,y+1,f"{y:.0f}",ha="center")

    plt.tight_layout()
    plt.savefig("outputs/daily_sales_trend.png")

    plt.show()

# 画一个用户消费柱状图，分析高价值用户

def plot_top_users(user_sales):
    plt.figure(figsize=(10,5))

    plt.bar(
        user_sales.index.astype(str),
        user_sales.values
    )

    plt.title("Top Users by Sales")
    plt.xlabel("User ID")
    plt.ylabel("Sales")

    plt.grid(
        axis="y",
        linestyle="--",
        alpha=0.5
    )

    for i,v in enumerate(user_sales.values):
        plt.text(i,v+2,f"{v:.0f}",ha="center")

    plt.tight_layout()
    plt.savefig("outputs/top_users_by_sales.png")
    plt.show()
