import pandas as pd
import json
import re
import unicodedata

def correctSingleQuoteJSON(s):
    """
        Aave's IPFS strings are not valid JSON
        JSON requires keys to be double-quoted (not single quoted) (https://www.w3schools.com/js/js_json_syntax.asp)
        Unfortunately, many of Aave's descriptions have single-quoted names
        We can't blindly replace single quotes with double quotes because:
            1) Some single-quotes are escaped (e.g. when they're in a single-quoted string and used as apostrophes)
            2) Some single-quotes are not escaped, (e.g. when they're in a double-quoted string)
        So we have to separate those cases
    """
    if not type(s) == str:
        print( f"Error in correctSingleQuoteJSON" )
        print( f"type(s) == {type(s)}" )
        return str(s) 
    if s == "":
        return None
    rstr = ""
    wasInsideDouble = False
    wasInsideSingle= False
    t = s.replace('\\xa0', u' ') #https://stackoverflow.com/questions/10993612/how-to-remove-xa0-from-string-in-python
    t = t.replace( "\\n","" )

    for inc in t:
        outc = inc
        if inc == "'":
            if len(rstr) == 0:
                outc = '"' #Replace single quote with double
                wasInsideSingle = True
            elif not wasInsideDouble and rstr[-1] != "\\": #A single quote that wasn't inside a double quote and wasn't escaped becomes a double quote
                outc = '"' #Replace single quote with double
                wasInsideSingle = ~wasInsideSingle
            if rstr[-1] == "\\": #An escaped single quote becomes unescaped
                rstr = rstr[:-1] #Remove escape
        if inc == '"':
            if wasInsideSingle:
                outc = "'"
            else: 
                outc = inc
                wasInsideDouble = ~wasInsideDouble
        
        #if outc != "\\":
        rstr += outc

    rstr = re.sub( '([a-z]+)"([a-z]+)', r"\1'\2", rstr )
    return rstr

def parse(s,cols = ['title','description','shortDescription'] ):
    #assert type(s) == str
    row = { c: "" for c in cols }
    if s is None or s == "" or s == "nan" or pd.isna(s):
        print( f"Error in parse" )
        print( f"Type(s) = {type(s)}" )
        print( f"s = {s}" )
        return pd.Series( data=row.values(), index=row.keys() )
    try:
        #d = json.loads( s.replace('"','DBLQT').replace("'",'"').replace('DBLQT',"'") )
        d = json.loads( correctSingleQuoteJSON(s) )
    except Exception as e:
        print( "===================" )
        print( e )
        print( "-------------------" )
        print( s )
        print( "-------------------" )
        print( correctSingleQuoteJSON(s) )
        print( "===================" )
        return pd.Series( data=row.values(), index=row.keys() )

    for k in row.keys():
        if k in d.keys():
            row[k] = d[k]

    return pd.Series( data=row.values(), index=row.keys() )

df = pd.read_csv("data/aave_descriptions_fixed.csv", dtype={'ipfsHash': str, 'description': str} )

df.rename( columns={'description':'json'}, inplace=True )

print( f"len(df) = {df.shape[0]}" )

for i in range(len(df.json)):
    s = df.json.iloc[i]
    ps = correctSingleQuoteJSON(s)
    if ps == "":
        print( f"Empty entry" )
        continue
    if ps == "nan":
        print( f"nan" )
        continue
    try:
        print( json.loads( ps ) )
    except Exception as e:
        print( i )
        print( "==============" )
        print( e )
        print( "-------------------" )
        print( s )
        print( "-------------------" )
        print( ps )
        print( "-------------------" )
        print( ps[770:790] )
        print( "============" )
        break

cols = set()
for i in range(len(df.json)):
    s = df.json.iloc[i]
    ps = correctSingleQuoteJSON(s)
    if ps == "":
        print( f"Empty entry" )
        continue
    if ps == "nan":
        print( f"nan" )
        continue
    try:
        d = json.loads( ps )
    except Exception as e:
        continue

    cols = cols.union(d.keys())

print( cols )
#{'requires', 'discussions', 'created', 'updated (*optional)', 'discussion', 'updated', 'basename', 'description', 'title', 'aip', 'preview', 'status', 'author', 'requires (*optional)', 'shortDescription'}

df[['title','shortDescription','description']] = df.json.apply(parse)

df.to_csv('data/aave_descriptions_parsed.csv')
