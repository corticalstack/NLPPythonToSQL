from nltk import load_parser
feature_cfg = load_parser('grammar_017.fcfg', trace=2)
nlquery = 'drama about'

trees = list(feature_cfg.parse(nlquery.split()))  # Put all tuples into list
print("trees")
print(trees)
print("")
top_tree_semantics = trees[0].label()['SEM']  # get first list entry with semantics
top_tree_semantics = [s for s in top_tree_semantics if s]  # first SEM entry from tuple to list
print("top tree semantics")
print(top_tree_semantics)
print("")
sqlquery = ''
try:
    sqlquery = ' '.join(top_tree_semantics)
except TypeError:
    for items in top_tree_semantics:
        for item in items:
            sqlquery += item
            sqlquery += ' '

print("sql query")
print(sqlquery)