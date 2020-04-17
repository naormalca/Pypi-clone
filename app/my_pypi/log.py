import logging

logFormatStr = '[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s'
logging.basicConfig(format = logFormatStr, filename = "global.log", level=logging.DEBUG)
formatter = logging.Formatter(logFormatStr,'%m-%d %H:%M:%S')
fileHandler = logging.FileHandler("summary.log")
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(formatter)
streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.DEBUG)
streamHandler.setFormatter(formatter)
    