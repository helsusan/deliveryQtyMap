import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Load data
df = pd.read_excel("france_delv_data.xlsx")

# Pastikan department format 2 digit
df["Department"] = df["Department"].astype(str).str.zfill(2)

# Total quantity semua tahun & bulan per department
dept_qty = (
    df.groupby("Department", as_index=False)["Delv Qty"]
      .sum()
)

print(dept_qty.sort_values("Delv Qty", ascending=False).head())

# Load France GeoJSON
france = gpd.read_file("departements.geojson")

# Merge
map_data = france.merge(
    dept_qty,
    left_on="code",
    right_on="Department",
    how="left"
)

map_data["Delv Qty"] = map_data["Delv Qty"].fillna(0)

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
    "Marin France Dealers Delivery Quantity",
    fontsize=20,
    weight="bold"
)

ax.axis("off")

plt.tight_layout()

for idx, row in map_data.iterrows():
    point = row.geometry.representative_point()

    ax.annotate(
        text=row["code"],
        xy=(point.x, point.y),
        ha="center",
        fontsize=7
    )

plt.savefig(
    "France_Delivery_Map.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()