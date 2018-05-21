# WathchGuard_mission
Solution: get the HTML page through the requests library, parse the contents of the HTML through beautiful soup and etree, and then store the extracted content in a CSV file.



Module design: in the product compare page to get all the product name of the specified series, then select the same product to comparison.We can get the performance data from the comparison results page .The Firewall throughput value as the key, all the performance data as the value, to create a dictionary.By sort with the dictionary'keys, we can implementation the function:sorted from small to large by "Firewall Throughput". In turn, write performance index data to a CSV file.

Also: 
	1. The Firewall of throughput value if Mbps, divided by 1024 
	2. If the value of Firewall is equal, the "value" corresponding to the "key" in the dictionary will be 'list', and the element in the list is the performance index data with equal value for all Firewall values.Determine the type of key corresponding value when writing to a CSV file.
	
	
In addition, the getAllSeriesInfo.py file in the main trunk gets the performance metrics data for all series.
Other modules can only obtain the specified series performance index data.
