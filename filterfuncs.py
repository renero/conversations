def first_filter(input):
    """Removes email address from raw tokens"""
    refined_words = []
    for word in input.split():
        if '@' not in word:
            refined_words.append(word)
    return(' '.join(refined_words))

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def valid_tokens(tokens):
    return filter(lambda t: not hasNumbers(t) and len(t) > 2 and len(t) <= 15, tokens)

def extract_tokens(filename):
    tokenizer = RegexpTokenizer(r'\w+')
    # Tokenization segments a document into its atomic elements
    f = open(filename,'r')
    raw = f.read().lower()
    tokens = tokenizer.tokenize(first_filter(raw))
    return(valid_tokens(tokens))

def generate_stopwords():
    """
    Generate stopwords from the current list of spanish stopwords, and copy
    words with accents, but without them.
    """
    all_stopwords = stopwords.words('spanish')
    for word in all_stopwords:
        if re.search(r'[áéíóúàèìòùäëïöü]', word):
            all_stopwords.append(remove_accents(word))
    return(all_stopwords)

def remove_stopwords(tokens):
    # Remove Stop words from Spanish stop words list, and numbers.
    all_stopwords = generate_stopwords()
    stopped_tokens=[]
    for word in tokens:
        if word not in all_stopwords and not word.isdigit():
            stopped_tokens.append(word)
    return(stopped_tokens)

def extract_stems(stopped_tokens):
    # Stem words in spanish
    stemmer = SnowballStemmer("spanish")
    stemmed_tokens = [stemmer.stem(i) for i in stopped_tokens]
    return(stemmed_tokens)


