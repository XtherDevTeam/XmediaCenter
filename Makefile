# Makefile is for setup your environment quickly
init:
	pip install -i https://pypi.tuna.tsinghua.edu.cn/simple flask requests urllib3 websockets beautifulsoup4
	chmod +x XmediaCenter.py

run: XmediaCenter.py
	./XmediaCenter.py config-http.json