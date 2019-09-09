import futu as ft


class Futu_Quant:
    def __init__(self,password):
        """
        https://futunnopen.github.io/futuquant/api/Market_API_Python_Doc.html
        """      
        self.quote_ctx = ft.OpenQuoteContext(host="127.0.0.1", port=11111)
        self.USTrade_ctx = ft.OpenUSTradeContext(host='127.0.0.1', port=11111)
        self.HKTrade_ctx = ft.OpenHKTradeContext(host='127.0.0.1', port=11111)
        self.quote_ctx.start()
        self.USTrade_ctx.start()
        self.HKTrade_ctx.start()
        self.password=password
    def MarketState(self):
        """
        NONE
    无交易,美股未开盘
    
    AUCTION
    竞价
    
    WAITING_OPEN
    早盘前等待开盘
    
    MORNING
    早盘
    
    REST
    午间休市
    
    AFTERNOON
    午盘
    
    CLOSED
    收盘
    
    PRE_MARKET_BEGIN
    盘前开始
    
    PRE_MARKET_END
    盘前结束
    
    AFTER_HOURS_BEGIN
    盘后开始
    
    AFTER_HOURS_END
    盘后结束
    
    NIGHT_OPEN
    夜市开盘
    
    NIGHT_END
    夜市收盘
    
    FUTURE_DAY_OPEN
    期指日市开盘
    
    FUTURE_DAY_BREAK
    期指日市休市
    
    FUTURE_DAY_CLOSE
    期指日市收盘
    
    FUTURE_DAY_WAIT_OPEN
    期指日市等待开盘
    
    HK_CAS
    港股盘后竞价
    """
        res=self.quote_ctx.get_global_state()
        return res
    def GetTicker(self,market,product_type):
        """
        market:
        港股	“HK”
        美股	“US”
        沪股	“SH”
        深股	“SZ”
        香港期货	“HK_FUTURE”
        
        stock_type:
        正股	“STOCK”
        指数	“IDX”
        ETF基金	“ETF”
        涡轮牛熊	“WARRANT”
        债券	“BOND”
        """
        ret_code,ret_data=self.quote_ctx.get_stock_basicinfo(market, stock_type=product_type) 
        return ret_data
    
    def QuerySubs(self):
        res=self.quote_ctx.query_subscription()
        return res
    def Subscri(self,codelist,subtype=["TICKER","QUOTE"],unsubs=False):
        """
        TICKER
        QUOTE
        ORDER_BOOK
        K_1M
        K_3M
        K_5M
        K_15M
        K_30M
        K_60M
        K_DAY
        K_WEEK
        K_MON
        K_QUARTER
        K_YEAR    
        RT_DATA
        BROKER
        """
        if unsubs == False:
            res=self.quote_ctx.subscribe(codelist,subtype )
        else:
            res=self.quote_ctx.unsubscribe(codelist,subtype)
        return res
    def GetDailyData(self,code):
        res=self.quote_ctx.get_cur_kline(code,1000)
        return res    
    def GetRealTimeData(self,code):
        res=self.quote_ctx.get_rt_data(code)
        return res
    def GetOrderBook(self,code):
        res=self.quote_ctx.get_order_book("US.GNK")
        return res
    ###Trading
    
    def UnLockTrade(self,account_market="US"):
        if account_market=="US":
            res=self.USTrade_ctx.unlock_trade(self.password,is_unlock=True)
            return res
        elif account_market=="HK":
            res=self.HKTrade_ctx.unlock_trade(self.password,is_unlock=True)
            return res
        else:
            return "error"
    def AccountInfo(self,code,account_market="US"):
        if account_market=="US":
            res=self.USTrade_ctx.accinfo_query()
            return res
        elif account_market=="HK":
            res=self.HKTrade_ctx.accinfo_query()
            return res
        else:
            return "error"
    def PositionsQuery(self,code,account_market="US"):
        if account_market=="US":
            res=self.USTrade_ctx.aposition_list_query()
            return res
        elif account_market=="HK":
            res=self.HKTrade_ctx.position_list_query()
            return res
        else:
            return "exception"
        
    def PlaceOrder(self,price, qty, code, trd_side,account_market="US"):
        """
        BUY
        SELL
        SELL_SHORT
        BUY_BACK
        """
        if account_market=="US":
            res=self.USTrade_ctx.place_order(price, qty, code, trd_side)
            return res
        elif account_market=="HK":
            res=self.HKTrade_ctx.place_order(price, qty, code, trd_side)
            return res
        else:
            return "exception"
    def ModifiedOrder(self,modify_order_op, order_id, qty, price,account_market="US"):
        if account_market=="US":
            res=self.USTrade_ctx.modify_order(modify_order_op, order_id, qty, price)
            return res
        elif account_market=="HK":
            res=self.HKTrade_ctx.modify_order(modify_order_op, order_id, qty, price)
            return res
        else:
            return "exception"
                       
    def OrderList(self,status_filter_list=[], code='', start='', end='',account_market="US"):
        """
        NONE
        未知
        UNSUBMITTED
        WAITING_SUBMIT
        SUBMITTING
        SUBMIT_FAILED
        SUBMITTED
        FILLED_PART
        FILLED_ALL
        CANCELLING_PART
        CANCELLING_ALL
        CANCELLED_PART
        CANCELLED_ALL
        FAILED
        DISABLED
        DELETED
        """
        if account_market=="US":
            res=self.USTrade_ctx.order_list_query(status_filter_list=status_filter_list, code=code, start=start, end=end)
            return res
        elif account_market=="HK":
            res=self.HKTrade_ctx.order_list_query(status_filter_list=status_filter_list, code=code, start=start, end=end)
            return res 
        else:
            return "exception"
        
    def CancellAllOrder(self,account_market="US"):
        if account_market=="US":
            res=self.USTrade_ctx.cancel_all_order()
            return res
        elif account_market=="HK":
            res=self.HKTrade_ctx.cancel_all_order()
            return res 
        else:
            return "exception"
    def Close(self):
        self.quote_ctx.close()
        self.USTrade_ctx.close()
        self.HKTrade_ctx.close()
