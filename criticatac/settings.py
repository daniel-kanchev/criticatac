BOT_NAME = 'criticatac'
SPIDER_MODULES = ['criticatac.spiders']
NEWSPIDER_MODULE = 'criticatac.spiders'
ROBOTSTXT_OBEY = True
LOG_LEVEL = 'WARNING'
ITEM_PIPELINES = {
   'criticatac.pipelines.DatabasePipeline': 300,
}