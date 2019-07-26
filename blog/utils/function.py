import re 


def remove_html_tag(data):
    
    result = re.sub(r'<.*?>', '',data)
    print(result)
    return result