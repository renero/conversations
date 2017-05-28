# Take only the elements starting with "Visitor ID" or "Timestamp", as we
# plan to use them as keys for every group of items in the Chat.
def get_key_headers(seq, key_headers):
    for el in seq:
        if el.startswith(key_headers):
            yield el.split(": ", 1)[1][:-1].replace(':','').replace('-','')

def extract_dialogue(seq):
    """
    This function considers only the questions made by the user in the chat
    disregarding the remaining lines.
    """
    for el in seq:
        if el.startswith('(') and 'Visitor' in el:
            first_part = el[el.find(')'):]
            yield first_part[first_part.find(':')+2:-1]
            
def remove_accents(s):
    return(s.replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').
           replace('à','a').replace('è','e').replace('ì','i').replace('ò','o').replace('ù','u').
           replace('ä','a').replace('ë','e').replace('ï','i').replace('ö','o').replace('ü','u'))

def remove_acc(sentence):
    """
    This function remove the accents in every word in a list (sentence)
    """
    newsent = []
    for word in sentence:
        if re.search(r'[áéíóúàèìòùäëïöü]', word):
            newsent.append(remove_accents(word))
        else:
            newsent.append(word)
    return newsent

def get_filepaths(directory):
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.
    return file_paths
    
# use itertools.groupby to group lines that occur after '=====' into lists
def extract_conversations(output_dir, filename, conversation_separator = '======='):
    """
    This function generates, from a set of conversation in a file (filename)
    separated by the separator specified, individual files with each of them.
    The name of the individual files are formed with the VisitorID and Timestamp.
    """
    key_headers = tuple(['Visitor ID: ', 'Timestamp: '])
    with open(filename,'r') as f:
        for key, group in itertools.groupby(f, lambda line: line.startswith(conversation_separator)):
            if not key:
                group = list(group)
                conversation_key = list(get_key_headers(group, key_headers))
                filename = output_dir + '_'.join(reversed(conversation_key))
                with io.open(filename, 'w', encoding='utf-8') as output:
                    conversation = remove_acc(list(extract_dialogue(group)))
                    for item in conversation:
                        output.write("%s\n" % item)

