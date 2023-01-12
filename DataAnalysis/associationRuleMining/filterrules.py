


def delMultipleRules():
    ruleset = set()
    for rule in open("rules.csv", "r"):
        ruleset.add(rule)

    writerulefile = open("rules.csv", "w")
    for rule in ruleset:
        writerulefile.write(rule)

delMultipleRules()