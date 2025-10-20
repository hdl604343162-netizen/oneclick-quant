@echo off
setlocal
echo === 安装依赖（CSV安全版，无pyarrow/fastparquet） ===
python -m pip install --upgrade pip
python -m pip install -r requirements.txt || goto :pipfail

echo === 单独确保安装 PyInstaller ===
python -m pip install pyinstaller || goto :pipfail

echo === 打包桌面程序（OneFile/Windowed） ===
pyinstaller --clean --noconfirm --onefile --windowed --name OneClickQuant_CSV desktop_main_csv.py ^
  --add-data "app_desktop_csv.py;." ^
  --add-data "quant_tool.py;." ^
  --add-data "backtest_cli.py;." ^
  --add-data "ws_recorder_pro.py;." ^
  --add-data "ob_replay_pro.py;." ^
  --add-data "strategies;strategies" ^
  --add-data "allocators.py;." ^
  --add-data "io_helpers.py;." ^
  --add-data "data;data" ^
  --add-data "bt_out;bt_out" ^
  --add-data "presets;presets" || goto :buildfail

echo.
echo === Build done. Check dist\OneClickQuant_CSV.exe ===
pause
exit /b 0

:pipfail
echo.
echo !!! 依赖安装失败。请把命令行输出截图发我，我来处理。
pause
exit /b 1

:buildfail
echo.
echo !!! 打包失败。请把命令行输出截图发我，我来处理。
pause
exit /b 1
