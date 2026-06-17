#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('저축.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ── buildEmoji 교체 ──
start_marker = 'function buildEmoji(sid,colors){'
end_marker   = 'function showEmojiState(sid){'

s = content.find(start_marker)
e = content.find(end_marker)
assert s != -1, 'buildEmoji not found'
assert e != -1, 'showEmojiState not found'

NEW_BUILD_EMOJI = r'''function buildEmoji(sid,colors){
  const CHAR={
    cele: 'char_cele.png',
    fly:  'char_fly.png',
    stand:'char_stand.png',
    run:  'char_run.png',
    think:'char_think.png',
  };
  const ANIM={
    cele: 'coin-cele',
    fly:  'coin-fly',
    stand:'coin-stand',
    run:  'coin-run',
    think:'coin-think',
  };
  const key=sid===1?'cele':sid===2?'fly':sid<=4?'stand':sid<=6?'run':'think';
  return `<img src="${CHAR[key]}" class="coin-char-img ${ANIM[key]}" alt="골머니" draggable="false"/>`;
}

'''

content = content[:s] + NEW_BUILD_EMOJI + content[e:]

# ── buildRunnerSVG 교체 ──
runner_start = 'function buildRunnerSVG(sid){'
runner_end   = 'function spawnFX(container, sid){'

rs = content.find(runner_start)
re_ = content.find(runner_end)
assert rs != -1, 'buildRunnerSVG not found'
assert re_ != -1, 'spawnFX not found'

NEW_RUNNER = r'''function buildRunnerSVG(sid){
  const src=sid<=2?'char_fly.png':'char_run.png';
  return `<img src="${src}" style="width:100%;height:100%;object-fit:contain" alt="" draggable="false"/>`;
}

'''

content = content[:rs] + NEW_RUNNER + content[re_:]

with open('저축.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done!')
