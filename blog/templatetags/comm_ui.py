from django import template

register = template.Library()

# 두개의 문자열 비교
# str1 : string
# str2 : string
@register.filter(name="compare_string")
def compare_string(str1, str2):
    rtn = str1.split(' ') == str2.split(' ')
    return rtn