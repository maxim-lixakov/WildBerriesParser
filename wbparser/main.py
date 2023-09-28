import csv
import json
from dataclasses import dataclass
from typing import List, Union

from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor

from wbparser.wildberries.wildberries.spiders.goods import GoodsSpider


@dataclass
class WBparser:
    """A class used to parse data from Wildberries.
    Pass several identifiers/urls to one WBparser object to make sure that Scrapy will work asynchronously.

    Examples:

        .. code:: python

            parser = WBparser()
            parser.parse_data(ids=[<product_id_1>])
            parser.save_data()


        .. code:: python

            parser = WBparser()
            parser.parse_data(urls=[<url_1>, <url_2>, <url_3>,], ids=[<product_id_1>, <product_id_2>,])
            parser.save_data(file_format='json', file_name='rareProducts')
            print(parser.result)
            print(parser.name)
    """

    ids: Union[None, List[int], List[str]] = None
    urls: Union[None, List[str]] = None
    result: Union[None, List[dict]] = None

    def _crawl(self, runner):
        deferred = runner.crawl(GoodsSpider, wb_parser=self)
        deferred.addBoth(lambda _: reactor.stop())
        return deferred

    def parse_data(
            self,
            urls: Union[None, List[str]] = None,
            ids: Union[None, List[int], List[str]] = None
    ) -> List[dict]:
        """Parses the data for the products identifiers or/and products pages. The data goes to the result attribute.

        :param urls: Product pages to parse, defaults to None
        :type urls: str, optional
        :param ids: Products identifiers, defaults to None
        :type ids: str, optional
        :return: List of dicts, each of which contains info about parsed WB items
        :rtype: list[dict]
        """
        self.urls = urls
        self.ids = ids
        runner = CrawlerRunner()
        reactor.callLater(0, self._crawl, runner)
        reactor.run()
        return self.result

    def save_data(self, file_format='json', file_name='goods', encoding='utf-8') -> None:
        """Creates a file with the selected format and saves the parsing result to it.

        :param file_format: One of two possible formats (json or csv), defaults to json
        :type file_format: str, optional
        :param file_name: File name, defaults to goods
        :type file_name: str, optional
        :param encoding: Encoding type, defaults to utf-8
        :type encoding: str, optional
        :return: Nothing is returned
        :rtype: None
        """
        if not file_name.isalnum():
            raise ValueError('Only letters and numbers are allowed in the filename')

        if self.result:

            if file_format == 'json':
                with open(f'{file_name}.json', 'w', encoding=encoding) as f:
                    f.write(json.dumps(self.result, indent=0))

            elif file_format == 'csv':
                keys = self.result[0].keys()
                with open(f'{file_name}.csv', 'w', newline='', encoding=encoding) as f:
                    dict_writer = csv.DictWriter(f, keys)
                    dict_writer.writeheader()
                    dict_writer.writerows(self.result)

    @property
    def name(self) -> List[str]:
        """Accesses the product name property.

        :return: Product names of parsed items
        :rtype: List[str]
        """
        return [dct.get('name') for dct in self.result]

    @property
    def brand(self) -> List[str]:
        """Accesses the brand property.

        :return: Brands of parsed items
        :rtype: List[str]
        """
        return [dct.get('brand') for dct in self.result]

    @property
    def priceU(self) -> List[int]:
        """Accesses the product price property.

        :return: Prices of parsed items
        :rtype: List[int]
        """
        return [dct.get('priceU') for dct in self.result]

    @property
    def salePriceU(self) -> List[int]:
        """Accesses the sale price property.

        :return: Sale prices of parsed items
        :rtype: List[int]
        """
        return [dct.get('salePriceU') for dct in self.result]

    @property
    def picsAmt(self) -> List[int]:
        """Accesses the pictures amount property.

        :return: Picture amounts of parsed items
        :rtype: List[int]
        """
        return [dct.get('picsAmt') for dct in self.result]

    @property
    def colors(self) -> List[List[dict]]:
        """Accesses the color property.

        :return: Colors of parsed items
        :rtype: list[list[dict]]
        """
        return [dct.get('colors') for dct in self.result]

    @property
    def sizes(self) -> List[List[str]]:
        """Accesses the size property.

        :return: Size values of parsed items
        :rtype: list[list[str]]
        """
        return [dct.get('sizes') for dct in self.result]

    @property
    def qty(self) -> List[int]:
        """Accesses the qty property.

        :return: Amount of available products for each parsed item
        :rtype: list[int]
        """
        return [dct.get('qty') for dct in self.result]

    @property
    def supplierId(self) -> List[str]:
        """Accesses the supplier identifier property.

        :return: Supplier identifiers of parsed items
        :rtype: List[str]
        """
        return [dct.get('supplierId') for dct in self.result]

    @property
    def rating(self) -> List[float]:
        """Accesses the rating property.

        :return: Rating values of parsed items
        :rtype: List[float]
        """
        return [dct.get('rating') for dct in self.result]

    @property
    def feedbacksAmt(self) -> List[int]:
        """Accesses the number of feedbacks property.

        :return: Number of feedbacks of parsed items
        :rtype: List[int]
        """
        return [dct.get('feedbacksAmt') for dct in self.result]
