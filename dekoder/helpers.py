striptTags=" ,.-_?!\n"

def dekoded2body(json):
    return [[w for w in par] for par in json]

def dekoded2footer(json):
    dic={}
    for par in json:
        for w in par:
            pureW=w.strip(striptTags).lower()
            pureT=par[w]["w"].strip(striptTags).lower()
            if pureW!="" and par[w]["w"].strip(striptTags)!="":
                if pureW not in dic: dic[pureW]=[pureT]
                elif pureT not in dic[pureW]: dic[pureW].append(pureT)
    dic2={w:dic[w] for w in sorted(dic, key=lambda v: v.lower())}
    for d in dic2: sorted(d)
    return splitDictLetters(dic2)

#splits a dict of words-translations to a dict of letters-dict(words-translations)
def splitDictLetters(d):
    abc={}
    for w, t in d.items():
        if len(w)>0 and w.strip(striptTags)!="": 
            if w[0].lower() not in abc: abc[w[0].lower()]={w:t}
            else:                       abc[w[0].lower()][w]=t
    return abc
