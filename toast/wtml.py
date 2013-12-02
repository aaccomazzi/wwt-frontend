from jinja2 import Template
from glob import glob
import os

template = Template( """

<Folder Name="ADS All Sky Survey">

{% for facet in facets %}

<ImageSet Generic="False" DataSetType="Sky" BandPass="Visible" Name="{{facet}}" Url="{{facet}}/{1}/{3}/{3}_{2}.png" BaseTileLevel="0" TileLevels="3" BaseDegreesPerTile="180" FileType=".png" BottomsUp="False" Projection="Toast" QuadTreeMap="" CenterX="0" CenterY="0" OffsetX="0" OffsetY="0" Rotation="0" Sparse="False" ElevationModel="False">
<Credits> ADS All Sky Survey </Credits>
<CreditsUrl> adsass.org </CreditsUrl>
<ThumbnailUrl>{{facet}}.jpg</ThumbnailUrl>
<Description/>
</ImageSet>
{% endfor %}

<ImageSet Generic="False" DataSetType="Sky" BandPass="Visible" Name="Harvard v All" Url="/harvard_v_all/{1}/{3}/{3}_{2}.png" BaseTileLevel="0" TileLevels="3" BaseDegreesPerTile="180" FileType=".png" BottomsUp="False" Projection="Toast" QuadTreeMap="" CenterX="0" CenterY="0" OffsetX="0" OffsetY="0" Rotation="0" Sparse="False" ElevationModel="False">
<Credits />
<CreditsUrl />
<ThumbnailUrl></ThumbnailUrl>
<Description />
</ImageSet>

<ImageSet Generic="False" DataSetType="Sky" BandPass="IR" Name="WISE All Sky (Infrared)" Url="http://www.worldwidetelescope.org/wwtweb/tiles.aspx?q={L},{X},{Y},wise" BaseTileLevel="0" TileLevels="7" BaseDegreesPerTile="180" FileType=".png" BottomsUp="False" Projection="Toast" QuadTreeMap="" CenterX="0" CenterY="0" OffsetX="0" OffsetY="0" Rotation="0" Sparse="False" ElevationModel="False">
<Credits>NASA/JPL-Caltech/UCLA</Credits>
<CreditsUrl>http://wise.ssl.berkeley.edu/</CreditsUrl>
<ThumbnailUrl>http://www.worldwidetelescope.org/wwtweb/thumbnail.aspx?name=wise</ThumbnailUrl>
</ImageSet>

<ImageSet Generic="False" DataSetType="Sky" BandPass="IR" Name="GLIMPSE/MIPSGAL" Url="http://www.worldwidetelescope.org/wwtweb/glimpse.aspx?q={1},{2},{3}" BaseTileLevel="0" TileLevels="11" BaseDegreesPerTile="180" FileType=".png" BottomsUp="False" Projection="Toast" QuadTreeMap="" CenterX="0" CenterY="0" OffsetX="0" OffsetY="0" Rotation="0" Sparse="False" ElevationModel="False" StockSet="False">
<ThumbnailUrl>http://www.worldwidetelescope.org/wwtweb/thumbnail.aspx?name=glimpsetn</ThumbnailUrl>
<Credits>NASA/JPL-Caltech/Univ. of Wisconsin. The GLIMPSE survey was performed using the Spitzer Space Telescope.</Credits>
<CreditsUrl>http://www.astro.wisc.edu/sirtf/</CreditsUrl>
</ImageSet>


</Folder>
"""
)


facets = [os.path.splitext(x)[0] for x in glob('*png')]
with open('adsass.wtml', 'w') as outfile:
    outfile.write(template.render(facets=facets))
