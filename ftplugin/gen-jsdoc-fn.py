import sys
import string
import re
import fileinput
from functools import reduce
from functools import partial

arrow1 = r"(?:(?:var|let|const) *?[$_a-z][$_a-z0-9]* *?= *?)?"
arrow1 += r"([$_a-z][$_a-z0-9]*(?: *= * .*?)?) *=>"

rgx = {
    'function': {
        'named':  re.compile(r"function +[$_a-z][$_a-z0-9]*\((.*?)\) *\{", re.I),
        'anon':   re.compile(r"function *\((.*?)\) *\{", re.I),
        'short':  re.compile(r"[$_a-z][$_a-z0-9]* *\((.*?)\) *\{", re.I),
        'arrow1': re.compile(arrow1, re.I),
        'arrow':  re.compile(r"\((.*?)\) *=> *\{", re.I)
    },
    'types': {
        'Object':    re.compile(r"^\{.*\}$"),
        'Array':     re.compile(r"^(?:\[.*\]|\.\.\.([$_a-z][$_a-z0-9]*))$"),
        'boolean':   re.compile(r"^(true|false)$"),
        'string':    re.compile(r"^('|\"|`).*('|\"|`)$"),
        'number':    re.compile(r"^[-0-9]*\.?[0-9]*(?:e(?:[-0-9])+)?$", re.I),
        'null':      re.compile(r"^null$"),
        'undefined': re.compile(r"^undefined$")
    }
}

def compose(*funcs):
    return lambda x=None: reduce(lambda v, f: f(v), reversed(funcs), x)

def determineType(str):
    for k, v in rgx['types'].iteritems():
        if v.match(str):
            return k
    return 'type'

def getParamList(str):
    for k, v in rgx['function'].iteritems():
        match = v.search(str)
        if match != None:
            return match.group(1)
    return None

def getInput(*a):
    lines = []
    for line in fileinput.input():
        lines.append(line);
    return ''.join(lines).replace('\n', '')

def findPair(openToken, closeToken, text=''):
    level = 0
    start = -1
    end = -1

    for idx, char in enumerate(text):

        if char == openToken:
            level += 1

            if start < 0:
                start = idx + 1

        if char == closeToken:
            level -= 1

            if level == 0:
                end = idx - 1
                return [start, end]

def splitParams(text):
    params = []
    start, end, idx = (0,)*3
    addIdx = lambda x : x + idx

    while idx < len(text):

        if text[idx] == '{':
            bounds = findPair('{', '}', text[idx:])
            bounds = map(addIdx, bounds)
            idx = bounds[1]

        if text[idx] == ',':
            end = idx
            param = text[start:end]
            params.append(param)
            start = idx + 1

        idx += 1

    param = text[start:]

    if param != '':
        params.append(param)

    return params

def setName(pair):
    objTypRgx = rgx['types']['Object']
    arrTypRgx = rgx['types']['Array']

    if objTypRgx.match(pair[0]):
        return 'options'

    match = arrTypRgx.match(pair[0])
    if match and match.group(1):
        return match.group(1)

    return pair[0]

def setType(pair):
    arrTypRgx = rgx['types']['Array']
    if arrTypRgx.match(pair[0]):
        return 'Array'
    if len(pair) > 1:
        return determineType(pair[1])
    else:
        return 'type'

def formatParams(params):
    objTypRgx = rgx['types']['Object']
    splitEq   = partial(string.split, sep='=')
    strpStrs  = partial(map, string.strip)
    toDict    = lambda t : {'name': setName(t), 'type': setType(t)}
    fmt       = partial(map, compose(toDict, strpStrs, splitEq, string.strip))
    return fmt(params)

procParams = compose(formatParams, splitParams)

def parseFn(text):
    params = getParamList(text)

    if params == None:
        return None

    params = procParams(params)
    if len(params) > 0:
        return params

    return None

def genDoc(params):

    lines = []
    tabStopCnt = 1
    top = '/**\n * ${%d:description}\n *' % (tabStopCnt)
    lines.append(top)

    if params:

        for param in params:

            tabStopCnt += 1
            typ = param.get('type')
            name = param.get('name')
            vals = (tabStopCnt, typ, tabStopCnt + 1, name, tabStopCnt + 2)
            line = ' * @param {${%d:%s}} ${%d:%s} ${%d:description}' % vals
            lines.append(line)
            tabStopCnt += 2

        lines.append(' *')

    tabStopCnt += 1
    vals = (tabStopCnt, tabStopCnt + 1, tabStopCnt + 2)
    line = '${%d: * @return {${%d:void}} ${%d:description}}' % vals
    lines.append(line)

    lines.append(' */')
    return '\n'.join(lines)

def out(text):
    sys.stdout.write(text)
    sys.stdout.flush()

run = compose(out, genDoc, parseFn, getInput)
run()

