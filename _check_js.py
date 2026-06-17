#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('저축.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract last <script>...</script>
last_script_start = content.rfind('<script>')
script_end = content.find('</script>', last_script_start)
js = content[last_script_start+8:script_end]
print(f'Main script: {len(js)} chars, {js.count(chr(10))} lines')

# Check for suspicious patterns
# 1. Look for function definitions to confirm key functions exist
fns = ['function buildEmoji', 'function doStage1', 'function doLogin',
       'function showView', 'function hideLoginOverlay', 'function hashStr',
       'function initApp', 'function buildRunnerSVG']
for fn in fns:
    pos = js.find(fn)
    ln = js[:pos].count('\n') + 1 if pos >= 0 else -1
    print(f'  {fn}: {"line "+str(ln) if pos>=0 else "NOT FOUND!"}')

# 2. Simple brace depth check (ignoring strings naively)
depth = 0
max_depth = 0
in_single = False
in_double = False
in_template = 0  # template literal nesting
i = 0
while i < len(js):
    c = js[i]
    # Skip escape sequences
    if c == '\\' and i + 1 < len(js):
        i += 2
        continue
    if in_single:
        if c == "'":
            in_single = False
    elif in_double:
        if c == '"':
            in_double = False
    elif in_template > 0:
        if c == '`':
            in_template -= 1
        # Note: we skip template expression tracking for simplicity
    else:
        if c == "'":
            in_single = True
        elif c == '"':
            in_double = True
        elif c == '`':
            in_template += 1
        elif c == '{':
            depth += 1
            max_depth = max(max_depth, depth)
        elif c == '}':
            depth -= 1
    i += 1

print(f'\nBrace balance: final depth={depth} (expect 0), max_depth={max_depth}')

# 3. Look for template literal issues in buildEmoji
be_start = js.find('function buildEmoji(sid,colors){')
be_end = js.find('function showEmojiState(sid){')
be_func = js[be_start:be_end]
backtick_count = be_func.count('`')
print(f'\nbuildEmoji: {len(be_func)} chars, backticks={backtick_count} ({"even OK" if backtick_count%2==0 else "ODD - PROBLEM!"})')

# 4. Check for nested template literal depth issue (simplified)
# Count the max nesting depth of template literals in buildEmoji
tl_depth = 0
max_tl = 0
for ch in be_func:
    if ch == '`':
        tl_depth += 1 if tl_depth == 0 else -1
    max_tl = max(max_tl, tl_depth)
print(f'Template literal depth in buildEmoji: max={max_tl}')

print('\nDone.')
