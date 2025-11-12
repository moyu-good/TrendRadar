@echo off
echo 手动测试TrendRadar推送...
cd /d "D:\PROJECT\TrendRadar"
C:\Users\12495\.local\bin\uv run python main.py
echo 测试完成！
pause