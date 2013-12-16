all: tiles adsass.wtml export

FACETS := Galaxy_512 HII-region_512 Infrared_512 Nebula_512 Other_512 Radio_512 Star_512 UV_512 X_512 allSources_512 date-1800_1850_512 date-1850_1900_512 date-1900_1910_512 date-1910_1920_512 date-1920_1930_512 date-1930_1940_512 date-1940_1945_512 date-1945_1950_512 date-1950_1955_512 date-1955_1960_512 date-1960_1965_512 date-1965_1970_512 date-1970_1975_512 date-1975_1980_512 date-1980_1985_512 date-1985_1990_512 date-1990_512 date-1991_512 date-1992_512 date-1993_512 date-1994_512 date-1995_512 date-1996_512 date-1997_512 date-1998_512 date-1999_512 date-2000_512 date-2001_512 date-2002_512 date-2003_512 date-2004_512 date-2005_512 date-2006_512 date-2007_512 date-2008_512 date-2009_512 date-2010_512 date-2011_512 date-2012_512 date-2013_512 date-pre1800_512 harvard_v_all

TILES := $(addprefix ., ${FACETS})

tiles: ${TILES}

.% : toast.py
	python toast.py $*
	touch $@

adsass.wtml: wtml.py
	python wtml.py

export:
	cp -r ${FACETS} ../web/
	cp adsass.wtml ../web/
