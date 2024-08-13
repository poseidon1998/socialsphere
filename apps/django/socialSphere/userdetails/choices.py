OPTIONS = {
    'FriendRequest': {
        'status': {
            'request sent': 1,
            'request pending': 2,
            'accepted': 3,
            'rejected': 4,
            'cancelled': 5,
        }
        
    },
    'SS_User':{
        'category':{
            'user':1,
            'admin':2,
            'moderator':3
        }
    }
}

def get_choices(classname,fieldname):
    data = OPTIONS[classname][fieldname]
    choices = []
    for text in data:
        choices.append((data[text],text))

    return tuple(choices)
