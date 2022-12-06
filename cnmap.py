import cartopy.crs as ccrs
import cartopy.feature as cf
from cartopy.feature import ShapelyFeature
from matplotlib import pyplot as plt

# 等距投影
proj = ccrs.AzimuthalEquidistant(central_longitude=105, central_latitude=35)


ax = plt.axes(projection=proj)

ax.set_extent([80, 126, 0, 53])

# Make figure larger
plt.gcf().set_size_inches(10,10)


import cartopy.io.shapereader as shpreader
# Read shape file
pr = shpreader.Reader("shp_files/省.shp")
ct = shpreader.Reader("shp_files/市.shp")
co = shpreader.Reader("shp_files/县.shp")
ba = shpreader.Reader('shp_files/港澳台.shp')

# Filter for a specific country
provinces = [p for p in pr.records()]
cities = [c for c in ct.records()]
counties = [c for c in co.records()]
bases = [b for b in ba.records()]


import json
codes = json.load(open('latest_code.json'))
ct_codes = [c[:4] + '00' for c in codes]

co_shapes = [c.geometry for c in counties if c.attributes['qu_dm'] in codes or not c.attributes['qu_dm']]
ct_shapes = [c.geometry for c in cities if c.attributes['shi_dm'] in ct_codes]
pr_shapes = [p.geometry for p in provinces if p.attributes['sheng_dm']]
ba_shapes = [b.geometry for b in bases]


ax.add_feature(ShapelyFeature(ct_shapes,ccrs.PlateCarree(),facecolor='#e6e6e6',edgecolor='#777777',lw=0.5))
ax.add_feature(ShapelyFeature(co_shapes,ccrs.PlateCarree(),facecolor='#f86b1d',edgecolor='#dddddd',lw=0.25))
ax.add_feature(ShapelyFeature(pr_shapes,ccrs.PlateCarree(),facecolor='none',edgecolor='#222222',lw=0.75))
ax.add_feature(ShapelyFeature(ba_shapes,ccrs.PlateCarree(),facecolor='none',edgecolor='#222222',lw=0.75))
ax.add_feature(ShapelyFeature([l.geometry for l in shpreader.Reader('shp_files/线.shp').records()],ccrs.PlateCarree(),
                              facecolor='none',edgecolor='#222222',lw=0.75))

# for c in counties:
#     if c.attributes['qu_dm'] in codes:
#         # print(c.attributes['qu_mc'])
#         sf = ShapelyFeature([c.geometry],ccrs.PlateCarree(),facecolor='#ff8000',edgecolor='#cbcbcb',lw=0.25)
#         ax.add_feature(sf)
#
# for c in cities:
#     if c.attributes['shi_dm'] in ct_codes:
#         print(c.attributes['shi_mc'])
#         sf = ShapelyFeature([c.geometry],ccrs.PlateCarree(),facecolor='none',edgecolor='#909090',lw=0.5)
#         ax.add_feature(sf)
#
# for p in provinces:
#     if p.attributes['sheng_dm']:
#         sf = ShapelyFeature([p.geometry],ccrs.PlateCarree(),facecolor='none',edgecolor='#000000',lw=0.75)
#         ax.add_feature(sf)


# for c in cities:
#     shape_feature = ShapelyFeature([c.geometry], ccrs.PlateCarree(), facecolor="coral", edgecolor='#F0F8FF', lw=0.25)
#     ax.add_feature(shape_feature)

# Save figure as SVG
plt.axis('off')
plt.savefig('map.svg',bbox_inches='tight', pad_inches=0.0)

