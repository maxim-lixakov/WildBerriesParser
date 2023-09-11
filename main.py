from dataclasses import dataclass

from scrapy.crawler import CrawlerProcess, CrawlerRunner
from twisted.internet import reactor, defer

from wildberries.wildberries.spiders.goods import GoodsSpider


@dataclass
class WB_parser:
    """

    Example:
    .. code:: python

            parser = WB_parser(<product_id>)
            parser.parse_data()
            print(parser.result)
    """

    id: int | str
    result: dict = None

    def _crawl(self, runner):
        deferred = runner.crawl(GoodsSpider, id=self.id, wb_parser=self)
        deferred.addBoth(lambda _: reactor.stop())
        return deferred

    def parse_data(self) -> dict:
        runner = CrawlerRunner()
        reactor.callLater(0, self._crawl, runner)
        reactor.run()
        return self.result
