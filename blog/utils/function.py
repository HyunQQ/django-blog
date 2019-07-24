import re 


def remove_html_tag(data):
    p = re.compile(r'<.*?>')
    return p.sub('\n',data)