# WathchGuard_mission
Solution: get the HTML page through the requests library, parse the contents of the HTML through beautiful soup and etree, and then store the extracted content in a CSV file.



Comparing module design: in the product page to get to the specified under the series of all the product name, then select the same product is used in the comparison, the comparison results page can get the performance index of the product data.The Firewall throughput value as the key, all the performance data as the value, to create a dictionary, by will be ordered by the dictionary's keys can be realized by "Firewall throughput" the function of the smallest, according to the order of the keys, will, in turn, the corresponding performance index data to a CSV file.

Also: 
	1. The Firewall of throughput value if Mbps, divided by 1024 
	2. If the Firewall throughput values are equal, the corresponding value is the key in the dictionary list, the elements in the list for all Firewall throughput performance data values are equal.Determine the type of key corresponding value when writing to a CSV file.
