import json

def load_json(path):
    with open(path) as f:
        data = json.load(f)
    return(data)

def select(hellowords, array, defaultChoose = None, **kwargs):
    # This function helps you use input function to select a key value from an array.
    # It list the elements and use choose the element by idx. Based on the idx, the 
    # function return the value. if you want to add some extra words, use extra_note = 'xxx'.
    if (defaultChoose != None):
        hellowords = hellowords + ' Press Enter for %s' % array[defaultChoose]
    print(hellowords)
    
    for i in range(len(array)):
        print('%d ---> %s' % (i, array[i]))
    x = input('Select by idx: ')
    if x == '':
        if defaultChoose != None:
            final = array[defaultChoose]
        else:
            pass
    else:
        final = array[int(x)]

    try:
        final = final + ' (' + kwargs['extra_note'] + ')'
    except:
        pass

    return(final)