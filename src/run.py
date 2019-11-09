import sys
import time
from multiprocessing import Process, Queue

from PyQt5.QtCore import QSharedMemory
from PyQt5.QtWidgets import QApplication, QMessageBox

from engine.engine import StrategyEngine
from qtui.control import Controller
from qtui.view import QuantApplication
from utils.logger import Logger

##################################################################
# 系统任务栏图标，区分系统
##################################################################
import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")


def run_log_process(logger):
    logger.run()


def run_engine_process(engine):
    engine.run()


def main():
    # 创建日志模块
    logger = Logger()
    log_process = Process(target=run_log_process, args=(logger,))
    log_process.start()

    logger.info("Start epolestar equant version:%s!" % ("EquantV1.0.8.20190903"))

    # 创建策略引擎到界面的队列，发送资金数据
    eg2ui_q = Queue(10000)
    # 创建界面到策略引擎的队列，发送策略全路径
    ui2eg_q = Queue(10000)

    # 创建策略引擎
    engine = StrategyEngine(logger, eg2ui_q, ui2eg_q)
    engine_process = Process(target=run_engine_process, args=(engine,))
    engine_process.start()

    control = Controller(logger, ui2eg_q, eg2ui_q)
    control.run()

    time.sleep(3)
    import atexit
    def exitHandler():
        control.receiveEgThread.stop()
        # 1. 先关闭策略进程, 现在策略进程会成为僵尸进程
        # todo 此处需要重载engine的terminate函数
        # 2. 关闭engine进程
        engine_process.terminate()
        engine_process.join()
        log_process.terminate()
        log_process.join()
    atexit.register(exitHandler)


if __name__ == '__main__':
    # ------------任务栏显示app的图标-----------------
    import ctypes
    myappid = 'equant.ui.view.QuantApplication'  # app路径
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    # ------------------------------------------------
    main()

