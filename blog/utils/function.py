import re 


def remove_html_tag(data):
    p = re.compile(r'<.*?>')
    result = p.sub(' ',data)
    print(result)
    print(type(result))
    return result