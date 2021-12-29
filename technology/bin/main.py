import os
import sys
from pathlib import Path
from src.StockService import StockService

sys.path.append(os.path.abspath('..'))

if __name__ == '__main__':
    dataPath = Path("../datas")
    if not dataPath.is_dir():  # datas目录不存在，则创建（因git不上传数据文件，因此git clone之后没有datas目录）
        dataPath.mkdir()
    StockService().startService()
