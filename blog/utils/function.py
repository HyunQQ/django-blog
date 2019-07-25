import re 


def remove_html_tag(data):
    # p = re.compile(r'<.*?>')
    data = re.sub(r'<.*?>','',data)
    data = re.sub('\n')
    return p.sub('\n',data)