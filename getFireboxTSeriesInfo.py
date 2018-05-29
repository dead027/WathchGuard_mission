# coding=utf-8

import requests
import re
from bs4 import BeautifulSoup
from lxml import etree

requests.packages.urllib3.disable_warnings()


class GetPerformanceData(object):

    def __init__(self):
        self.URL = "https://www.watchguard.com"
        self.session = requests.session()
        self.attribute_name_list = ["Firewall Throughput", "VPN Throughput", "AV Throughput",
                                    "IPS Throughput", "UTM Throughput", "Concurrent Sessions*"]
        self.series = ["WatchGuard® Firebox M Series",
                       "WatchGuard Firebox T Series",
                       "WatchGuard XTM Firewalls",
                       "WatchGuard® XTM 800 Series",
                       "LEGACYPRODUCTS_WatchGuard® Firebox M Series",
                       "LEGACYPRODUCTS_WatchGuard Firebox T Series",
                       "LEGACYPRODUCTS_WatchGuard XTM Firewalls",
                       "WatchGuard® XTM 8 Series",
                       "WatchGuard® XTM 5 Series",
                       "WatchGuard® XTM 3 Series",
                       "WatchGuard® XTM 2 Series"]

    def get_product_list_by_module(self, series):
        """
        Get all products of specified series from page.
        :param series: The series of names to be processed.
        :return: List of products
        """
        assert series in self.series, "Series type incorrect."
        get_url = self.URL + "/wgrd-products/appliances-compare"
        # get page
        get_rtn = self.session.get(get_url, verify=False)
        # use bs4 to parse
        soup = BeautifulSoup(get_rtn.content, "html.parser")
        # deal with LEGACY PRODUCTS
        if series not in [self.series[4], self.series[5], self.series[6]]:
            elements = soup.select("select#p1 optgroup[label='%s']" % series.encode("utf-8"))
            elements = elements[0].find_all("option")
        else:
            elements = soup.select("select#p1 optgroup[label='%s']" % series[15:].encode("utf-8"))
            elements = elements[1].find_all("option")
        # get all options
        product_list = []
        for item in elements:
            product_name = item.get_text()
            product_id = item["value"]
            product_list.append({"name": product_name, "id": product_id})
        return product_list

    def get_product_performance_info(self, product):
        """
        get product performance info, and put it into a dictionary
        :param product:
        :return:performance info dictionary
        """
        product_id = product["id"]
        get_url = self.URL + "/wgrd-products/appliances-compare/" + product_id + "/" + product_id
        # get page
        get_rtn = self.session.get(get_url, verify=False)
        selector = etree.HTML(get_rtn.content)
        product_data = {}

        for attr in self.attribute_name_list:
            # Create product data structure. the key is the attribute name, and the value is the attribute value.
            product_data[attr] = attr + ": " + selector.xpath("//td[contains(text(),'%s')]/../td[2]" %
                                                              attr)[0].text + "\n"
            product_data["product"] = product
        return product_data

    def store_series_product_performance_data(self, series):
        """
        Write series product performance data to csv file
        :param series:
        :return:
        """
        pro_list = self.get_product_list_by_module(series)
        pro_data_dic = {}
        # create dic by product and throughput value
        for pro in pro_list:
            product_data = self.get_product_performance_info(pro)
            throughput = product_data[self.attribute_name_list[0]]
            result = re.search("Firewall Throughput: (.+?) (.+?)", throughput)
            performance_value = float(result.group(1))
            performance_type = result.group(2)
            # deal with "Mbps" and "Gbps"
            if performance_type == "M":
                performance_value /= 1024
            key = str(performance_value)
            if key in pro_data_dic:
                # deal with duplication data
                pro_data_dic[str(performance_value)] = [pro_data_dic[str(performance_value)], product_data]
            else:
                pro_data_dic[str(performance_value)] = product_data
        # sort by performance value
        t_value_list = []
        [t_value_list.append(float(value)) for value in pro_data_dic.keys()]
        t_value_list.sort()

        # write to csv
        with open(series.decode("utf-8") + ".csv", "a+") as f:
            for item in t_value_list:
                p_data = pro_data_dic[str(item)]
                if isinstance(p_data, list):
                    for data in p_data:
                        f.write("【" + data["product"]["name"] + "】\n")
                        for attr in self.attribute_name_list:
                            f.write(data[attr])
                        f.write("\n\n\n")
                else:
                    f.write("【" + p_data["product"]["name"] + "】\n")
                    for attr in self.attribute_name_list:
                        f.write(p_data[attr])
                    f.write("\n\n\n")


if __name__ == "__main__":
    gpd = GetPerformanceData()
    gpd.store_series_product_performance_data(gpd.series[1])
