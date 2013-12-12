all: catalog tiles

catalog:
	cd cats && make

tiles:
	cd toast && make
