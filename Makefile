CURRENT_DATE=$(shell date +"%Y-%m-%d")


crawl_landing_pisos:
	cd homematch/inmo_scraper/ && \
	poetry run scrapy crawl pisosdotcom --logfile ../../logs/$(CURRENT_DATE).json -L INFO \
	-o ../../data/crawler_data/fotocasa_flats.json