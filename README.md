# jjuso
- Search address Example. (with Python, Open API)
- Windows application. (with PyQt5)
- Write old address and new address for excel.

## Environments
- Python 3.7
- OpenAPI (juso.go.kr)

## Lib
- openpyxl
- PyQt5
- requests

## Use for pyinstaller
```bash
pyinstaller -w -F app.py
```

## Tip
```bash
# 가상환경 셋팅 방법
python -m venv {프로젝트 디렉토리명}

# 패키지 관리
pip freeze > requirements.txt
pip install -r requirements.txt
pip uninstall -r requirements.txt
```