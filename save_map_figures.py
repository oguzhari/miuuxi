import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import contextily as ctx


def create_image(pickup_lat, pickup_lon, dropoff_lat, dropoff_lon):
    # Konumları oluştur
    geometry = [Point(pickup_lon, pickup_lat), Point(dropoff_lon, dropoff_lat)]
    geo_df = gpd.GeoDataFrame(geometry=geometry, crs="EPSG:4326")

    # Koordinat sistemini Web Mercator'a çevir (EPSG:3857)
    geo_df = geo_df.to_crs(epsg=3857)

    # Plot oluştur
    fig, ax = plt.subplots(figsize=(10, 10))

    # Konumları çiz
    geo_df.plot(ax=ax, marker="o", color="red", markersize=100, zorder=2)

    # Harita sınırlarını ayarla
    ax.set_xlim([-8268266, -8203572])
    ax.set_ylim([4961321, 5000465])

    # Gerçek dünya haritasını arka plana ekle
    ctx.add_basemap(ax, zoom=12, source=ctx.providers.CartoDB.Positron)

    labels = ["Nereden", "Nereye"]
    for x, y, label in zip(geo_df.geometry.x, geo_df.geometry.y, labels):
        ax.annotate(
            label,
            xy=(x, y),
            xytext=(7.5, 7.5),
            textcoords="offset points",
            fontsize=9,
        )

    # Görseli kaydet
    extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    plt.savefig("images/model.png", bbox_inches=extent, pad_inches=0)
