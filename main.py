from src import FishCapture, WallstreetBets, Trader

# # get ticker from fish
# fish_ticker = FishCapture.init_fish_capture()
#
# # get ticker from fish
# reddit_ticker = WallstreetBets.prepare_reddit_trade()
#
# print("fish choice: " + fish_ticker)
# print("reddit choice: " + reddit_ticker)

# trade with ticker
Trader.execute_trade("test1", "test2")
# Trader.execute_trade("test")

# visualize trade data
# Visualizer.createGraph()
