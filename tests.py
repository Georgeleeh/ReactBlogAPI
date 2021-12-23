import requests
import argparse
from datetime import datetime
import shortuuid

def get_base_url():
    parser = argparse.ArgumentParser(description='Test this Flask api')
    parser.add_argument(
        'url',
        metavar='-u',
        type=str,
        nargs='?',
        help='the host url to test',
        default='http://127.0.0.1:5000/'
        )

    base_url = parser.parse_args().url

    if base_url[-1] == '/':
        base_url = base_url[:-1]
    if base_url[:4] != 'http':
        raise parser.error('is the url http:// or https:// ?')
    
    return base_url

def test(url, method, response_code, json=None):
    print(f'Testing URL: {url}')
    
    switch = {
        'get' : requests.get,
        'put' : requests.put,
        'post' : requests.post,
        'patch' : requests.patch,
        'delete' : requests.delete
    }

    r = switch[method](url, json=json)

    print(f'Desired Code: {response_code}')
    print(f'Actual Code: {r.status_code}')

    if r.status_code == response_code:
        print('Success!\n')
    else:
        print('Failed!\n')
        raise Exception(f'{url} provided the wrong response:\n{r}')
    
    return r.json()


# The basic request URL - http://127.0.0.1 by default
base_url = get_base_url()

# Create a new blogpost json for testing and save the id
new_blogpost_id = shortuuid.uuid()
new_blogpost = {
    'id' : new_blogpost_id,
    'title' : 'New Blogpost Title',
    'one_liner' : 'The hottest new post in town',
    'posted' : int(datetime.now().timestamp()),
    'revised' : None,
    'content' : 'Hey hey hey, lok at this new post. Lotta text up in here.',
    'cover_image' : 'https://cdn.ebaumsworld.com/mediaFiles/picture/718392/84890877.jpg',
    'featured' : True,
    'tags' : ['test1', 'test2']
}


# Add new blogpost
print('Add new blogpost\n')
test(base_url+'/blogpost', 'post', 201, json=new_blogpost) # Correct request
print()

# Get the blogpost we just made
print('Get the blogpost we just made\n')
test(base_url+f'/blogpost/{new_blogpost_id}', 'get', 200) # Correct request
print()

# Get all blogposts
print('Get all blogposts\n')
content = test(base_url+'/blogpost', 'get', 200) # Correct request
print(f'{len( content["blogposts"] )} blogposts were found')
print(content['blogposts'])
print()

# Change the title of the blogpost we just made
print('Change the title of the blogpost we just made\n')
content = test(base_url+f'/blogpost/{new_blogpost_id}', 'patch', 200, json={'title' : 'Revised Title'}) # Correct request
test(base_url+f'/blogpost/{new_blogpost_id}', 'patch', 500, json={'rando' : 'diddly'}) # No such column exists
print(content['blogpost'])
print()

# Delete the blogpost we just made
print('Delete the blogpost we just made\n')
test(base_url+f'/blogpost/{new_blogpost_id}', 'delete', 200) # Correct request
test(base_url+f'/blogpost/{new_blogpost_id}', 'get', 404) # Checking it deleted
print()

print('All good, G!')