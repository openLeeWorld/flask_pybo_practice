#import locale
#locale.setlocal(local.LC_ALL, '')
#위 주석은 UnicodeEncodeError가 나면 수정

def format_datetime(value, fmt="%Y년 %m월 %d일 %p %I:%M"):
    return value.strftime(fmt)
# 년, 월, 일, AM/PM, 시간(0~12시):분