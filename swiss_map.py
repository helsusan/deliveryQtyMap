import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Load data
df = pd.read_excel("swiss_delv_data.xlsx")

# Total quantity semua tahun & bulan per boundary
boundary_qty = (
    df.groupby("Boundary", as_index=False)["Delv Qty"]
      .sum()
)

print(
    boundary_qty.sort_values("Delv Qty", ascending=False)
    .head(10)
)

df["Boundary"] = (
    df["Boundary"]
      .astype(str)
      .str.strip()
)

boundary_qty = (
    df.groupby("Boundary", as_index=False)["Delv Qty"]
      .sum()
)

# Load Switzerland GeoJSON
swiss = gpd.read_file("geoBoundaries-CHE-ADM1.geojson")

# Merge
swiss["shapeName"] = (
    swiss["shapeName"]
      .astype(str)
      .str.strip()
)

map_data = swiss.merge(
    boundary_qty,
    left_on="shapeName",
    right_on="Boundary",
    how="left"
)

map_data["Delv Qty"] = map_data["Delv Qty"].fillna(0)

unmatched = boundary_qty[
    ~boundary_qty["Boundary"].isin(swiss["shapeName"])
]

print("\nBoundary not matched:")
print(unmatched)

# PLOT

fig, ax = plt.subplots(
    1,
    1,
    figsize=(12,12)
)

custom_cmap = LinearSegmentedColormap.from_list(
    "my_blue",
    ["#F7FBFF", "#00A2E1", "#005A9E"]
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
    "Marin Switzerland Dealers Delivery Quantity",
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
    "Switzerland_Delivery_Map.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()