from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

html_filepath = "D:\Programming Projects\!Data\Leverless controller - Etsy.html"

def extract_items_from_html(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')
    cut_off_point = soup.find(string="There's so much more for you to discover")
    above_cut_off_divs = cut_off_point.find_all_previous("div", recursive=False)

    items_data = []
    for div in above_cut_off_divs:
        item_name_element = div.find("h3")
        price_element = div.find("span", class_="currency-value")
        if item_name_element and price_element:
            item_name = item_name_element.text.strip()
            item_price = float(price_element.text.replace("$", "").strip())
            items_data.append((item_name, item_price))

    unique_items_data = list(set(items_data))
    df = pd.DataFrame(unique_items_data, columns=["Item Name", "Price (in USD)"])
    
    return df

def perform_price_analytics(df):
    # Initial analytics on the original data
    avg_price = df["Price (in USD)"].mean()
    max_price = df["Price (in USD)"].max()
    min_price = df["Price (in USD)"].min()
    median_price = df["Price (in USD)"].median()
    std_dev_price = df["Price (in USD)"].std()
    
    # Price distribution for histogram
    plt.figure(figsize=(10,6))
    plt.hist(df["Price (in USD)"], bins=20, color='skyblue', edgecolor='black')
    plt.title("Distribution of Prices")
    plt.xlabel("Price")
    plt.ylabel("Number of Items")
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.savefig("price_distribution_histogram.png")
    plt.show()
    
    # Price range distribution for pie chart
    price_bins = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 1000, 2000]
    price_labels = ["$0-$50", "$50-$100", "$100-$150", "$150-$200", "$200-$250", 
                    "$250-$300", "$300-$350", "$350-$400", "$400-$450", "$450-$500", 
                    "$500-$1000", "$1000-$2000"]
    df["Price Range"] = pd.cut(df["Price (in USD)"], bins=price_bins, labels=price_labels, right=False)
    price_distribution = df["Price Range"].value_counts().sort_index()
    
    plt.figure(figsize=(10,6))
    plt.pie(price_distribution, labels=price_distribution.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.title("Distribution of Items Across Price Ranges")
    plt.savefig("price_range_distribution_pie.png")
    plt.show()
    
    # Adding analytics data to DataFrame using pandas.concat
    analytics_data = {
        "Average Price": avg_price,
        "Max Price": max_price,
        "Min Price": min_price,
        "Median Price": median_price,
        "Standard Deviation of Prices": std_dev_price
    }
    analytics_df = pd.DataFrame(list(analytics_data.items()), columns=["Item Name", "Price (in USD)"])
    df = pd.concat([df, analytics_df], ignore_index=True)
    
    return df

# Call the functions and save the result
df_items = extract_items_from_html(html_filepath)
df_with_analytics = perform_price_analytics(df_items)
df_with_analytics.to_excel("items_with_analytics.xlsx", index=False)
