from injector import inject
from lib import log

class Strategy:
    @inject
    def __init__(self, logger: log.Logger):
        self.__logger = logger
        self.__long_state = False
        self.__long_price = 0.0
        self.__long_qty = 0.0

        self.__short_state = False
        self.__short_price = 0.0
        self.__short_qty = 0.0

        # aggregate variables
        self.__total_profit = 0.0
        self.__total_loss = 0.0
        self.__total_trade = 0
        self.__total_trade_win = 0

        # for max draw down calculation
        self.__max_profit = 0
        self.__max_loss = 0

    def long_entry(self, price: float, qty: int):
        if self.__long_state:
            # raise Exception(f"already long entered at {self.__long_price} {self.__long_qty}")
            return

        self.__long_price = price
        self.__long_qty = qty
        self.__long_state = True

    def long_exit(self, price: float, qty: int):
        if not self.__long_state:
            # raise Exception("no long entry!")
            return

        profit = price * qty - self.__long_price * self.__long_qty
        if profit > 0:
            self.__total_trade_win += 1
            self.__total_profit += profit
            self.__max_profit = max(self.__total_profit, self.__max_profit)
        else:
            self.__total_loss += profit
            self.__max_loss = min(self.__total_loss, self.__max_loss)
        print(f"profit: {profit}")
        self.__long_state = False
        self.__total_trade += 1


    def short_entry(self, price: float, qty: int):
        if self.__short_state:
            # raise Exception(f"already short entered at {self.__short_price} {self.__short_qty}")
            return

        self.__short_price = price
        self.__short_qty = qty
        self.__short_state = True

    def short_exit(self, price: float, qty: int):
        if not self.__short_state:
            raise Exception("no short entry!")

        profit = self.__short_price * self.__short_qty - price * qty
        if profit > 0:
            self.__total_trade_win += 1
            self.__total_profit += profit
            self.__max_profit = max(self.__total_profit, self.__max_profit)
        else:
            self.__total_loss += profit
            self.__max_loss = min(self.__total_loss, self.__max_loss)
        self.__short_state = False
        self.__total_trade += 1


    def show(self):
        self.__logger.info(f"actual_profit:{self.__total_profit + self.__total_loss} profit:{self.__total_profit} loss:{self.__total_loss} ")
        self.__logger.info(f"total_trade: {self.__total_trade} total_trade_win: {self.__total_trade_win} win_ratio: {self.__total_trade_win / self.__total_trade}")
        self.__logger.info(f"profit_factor: {self.__total_profit / ((-1.0)*self.__total_loss)} max_draw_down: {self.__max_profit + self.__max_loss} max_profit:{self.__max_profit} max_loss:{self.__max_loss}")


