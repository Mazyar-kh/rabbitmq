import urllib.request


url = 'http://www.python.org/'


try:
    with urllib.request.urlopen(url, timeout=10) as f:
        print(f.read())
        raise ValueError('hi')
except ConnectionResetError:
    print('A ConnectionResetError occurred')
except TimeoutError:
    print('A TimeoutError occurred')
except BaseException as e:
    print('A generic error occurred', e)
