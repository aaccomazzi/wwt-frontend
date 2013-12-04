all: download merge export

FILES := $(addprefix Npix, $(addsuffix .tsv, $(shell seq 0 3071)))

download: ${FILES}
merge: merged.json

%.tsv:
	curl -O http://alasky.u-strasbg.fr/cats/SIMBAD/Norder4/Dir0/$@ > $@

merged.json: merge.py
	python merge.py

export:
	cp merged.json ../web/simbad.json
