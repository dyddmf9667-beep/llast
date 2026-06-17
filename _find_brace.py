#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""buildEmoji 함수 내부의 중괄호 불균형을 찾는 스크립트"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('저축.html', 'r', encoding='utf-8') as f:
    content = f.read()

last_script_start = content.rfind('<script>')
script_end = content.find('</script>', last_script_start)
js = content[last_script_start+8:script_end]

# More precise brace tracker that handles template literals with ${} properly
# State machine: normal, in_single_quote, in_double_quote, in_template_literal
# For template literals, we need to track ${ depth

def check_braces(code):
    """Returns list of (line, char, depth, event) for brace events"""
    events = []
    i = 0
    depth = 0
    line = 1

    # State: 'code', 'sq' (single quote), 'dq' (double quote), 'tl' (template lit)
    # Stack for template literal nesting
    state_stack = ['code']
    tl_expr_depth = []  # tracks { depth inside ${ } in template literals

    while i < len(code):
        c = code[i]
        state = state_stack[-1]

        if c == '\n':
            line += 1

        if state == 'sq':
            if c == '\\':
                i += 2
                continue
            if c == "'":
                state_stack.pop()
        elif state == 'dq':
            if c == '\\':
                i += 2
                continue
            if c == '"':
                state_stack.pop()
        elif state == 'tl':  # inside template literal
            if c == '\\':
                i += 2
                continue
            if c == '`':
                state_stack.pop()  # end template literal
            elif code[i:i+2] == '${':
                state_stack.append('tl_expr')
                tl_expr_depth.append(1)
                i += 2
                continue
        elif state == 'tl_expr':  # inside ${ } of template literal
            if c == '\\':
                i += 2
                continue
            if c == '`':
                state_stack.append('tl')
            elif c == '"':
                state_stack.append('dq')
            elif c == "'":
                state_stack.append('sq')
            elif c == '{':
                tl_expr_depth[-1] += 1
            elif c == '}':
                tl_expr_depth[-1] -= 1
                if tl_expr_depth[-1] == 0:
                    state_stack.pop()
                    tl_expr_depth.pop()
        else:  # normal code
            if c == '`':
                state_stack.append('tl')
            elif c == '"':
                state_stack.append('dq')
            elif c == "'":
                state_stack.append('sq')
            elif c == '{':
                depth += 1
                events.append((line, i, depth, 'open'))
            elif c == '}':
                depth -= 1
                events.append((line, i, depth, 'close'))
        i += 1

    return depth, events

depth, events = check_braces(js)
print(f'Final depth: {depth}')

# Find where depth went wrong - look for the last few open braces
opens = [(l, i, d) for l, i, d, e in events if e == 'open']
closes = [(l, i, d) for l, i, d, e in events if e == 'close']
print(f'Total opens: {len(opens)}, closes: {len(closes)}')
print(f'Difference: {len(opens) - len(closes)}')

# Show the last 10 brace events
print('\nLast 15 brace events:')
for l, i, d, e in events[-15:]:
    snippet = js[max(0,i-20):i+20].replace('\n','↵')
    print(f'  line {l:4d}: {e:5s} depth={d:2d}  ...{snippet}...')
