import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Load data
df = pd.read_excel("germany_delv_data.xlsx")

# Total quantity semua tahun & bulan per district
district_qty = (
    df.groupby("District", as_index=False)["Delv Qty"]
      .sum()
)

print(
    district_qty.sort_values("Delv Qty", ascending=False)
    .head(10)
)

df["District"] = (
    df["District"]
      .astype(str)
      .str.strip()
)

district_qty = (
    df.groupby("District", as_index=False)["Delv Qty"]
      .sum()
)

# Load Germany GeoJSON
germany = gpd.read_file("geoBoundaries-DEU-ADM2.geojson")

# Merge
germany["shapeName"] = (
    germany["shapeName"]
      .astype(str)
      .str.strip()
)

map_data = germany.merge(
    district_qty,
    left_on="shapeName",
    right_on="District",
    how="left"
)

map_data["Delv Qty"] = map_data["Delv Qty"].fillna(0)

unmatched = district_qty[
    ~district_qty["District"].isin(germany["shapeName"])
]

print("\nDistrict not matched:")
print(unmatched)

# PLOT

fig, ax = plt.subplots(
    1,
    1,
    figsize=(12,12)
)

custom_cmap = LinearSegmentedColormap.from_list(
    "my_blue",
    ["#FFF8D6", "#FECF00", "#B8860B"]
)

map_data.plot(
    column="Delv Qty",
    cmap=custom_cmap,
    linewidth=0.6,
    edgecolor="black",
    legend=True,
    legend_kwds={
        "label": "Delivery Quantity",
        "shrink": 0.6
    },
    ax=ax
)

ax.set_title(
    "Marin Germany Dealers Delivery Quantity",
    fontsize=20,
    weight="bold"
)

ax.axis("off")

plt.tight_layout()

for idx, row in map_data.iterrows():

    if pd.notna(row["Delv Qty"]) and row["Delv Qty"] > 0:

        point = row.geometry.representative_point()

        ax.annotate(
            text=row["shapeName"],
            xy=(point.x, point.y),
            ha="center",
            fontsize=10
        )

plt.savefig(
    "Germany_Delivery_Map.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()