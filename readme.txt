/landchina
	# Data downloaded by year, month and day.
	
	landchina_2013_2016.csv
		# All data from 2013 to 2016.
	landchina_2013_2016_small.csv
		# Fewer variables.
	error.csv
		# Records that are not successfully downloaded.

/match_book
	# Contains match book between Shapefile expression and the Chinese expression.
	match_book_auto.csv
		# Generete by merging CHN_adm raw data set, and transfer unicode to Chinese characters.

	match_book_20170407.xlsx
		# Match book adjusted by hand.

downloader.py
	# Class of a downloader.

main.py
	# File to download the data set.

merger.py
	# Merge data from all days together into a file.

merge_two.py
	# Merge the data set with the matchbook.

price.csv
	# numbers clustered by province. Used to draw choropleth maps.

	