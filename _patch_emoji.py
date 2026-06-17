#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""buildEmoji 함수를 고퀄리티 SVG 버전으로 교체"""

with open(r'C:/Users/kyu26/savings-tracker/저축.html', 'r', encoding='utf-8') as f:
    content = f.read()

START_MARKER = 'function buildEmoji(sid,colors){'
NEXT_FN = 'function showEmojiState(sid){'

start = content.find(START_MARKER)
if start == -1:
    print("ERROR: start marker not found"); exit(1)

end_pos = content.find(NEXT_FN, start)
if end_pos == -1:
    print("ERROR: end marker not found"); exit(1)

# 함수 마지막 '}' 위치 (닫힘 중괄호 = 열 0에 있는 \n})
func_end = content.rindex('\n}', start, end_pos) + 2
print(f"function chars: {start} ~ {func_end} ({func_end-start} chars)")

NEW_FUNCTION = r'''function buildEmoji(sid,colors){
  // ── 색상 팔레트 ──
  const type   = animalType || 'cat';
  const def    = ANIMAL_DEF[type] || ANIMAL_DEF.cat;
  const mainC  = colors?.hair  || def.main;
  const bellyC = colors?.skin  || def.belly;
  const eyeC   = colors?.eye   || def.eye;
  const OL     = '#2a1a10';
  const PINK   = '#f4a8b8';
  const NOSE   = '#e88a9a';

  // ── 색상 유틸 (밝게/어둡게) ──
  const hl=(h,a)=>{
    h=h.replace('#','');
    if(h.length===3)h=h[0]+h[0]+h[1]+h[1]+h[2]+h[2];
    const n=(s)=>Math.max(0,Math.min(255,parseInt(h.substr(s,2),16)+Math.round(a*255))).toString(16).padStart(2,'0');
    return `#${n(0)}${n(2)}${n(4)}`;
  };
  const dk=(h,a)=>hl(h,-a);
  const uid=`${sid}${type}`;

  // ── 상태별 애니메이션 ──
  const [aN,aD] =
    sid===1 ? ['bounce','.5s'] :
    sid===2 ? ['bounce','.7s'] :
    sid<=4  ? ['bob',  '1.0s'] :
    sid<=6  ? ['sway', '1.8s'] :
    sid<=8  ? ['droop','2.4s'] :
             ['slump','3.0s'];
  const twag=sid<=3?'.7s':sid<=5?'1.8s':'3.5s';
  const trot=sid<=3?14:5;

  const css=`
.hb{animation:${aN} ${aD} cubic-bezier(.4,0,.2,1) infinite;transform-origin:80px 95px}
.tl{animation:tf 2s .2s ease-in infinite}
.tr{animation:tf 2s 1.0s ease-in infinite}
.tw{animation:tailW ${twag} ease-in-out infinite;transform-origin:130px 168px}
@keyframes bounce{
  0%,100%{transform:translateY(0) rotate(-1.5deg) scaleY(1)}
  42%{transform:translateY(-13px) rotate(1.5deg) scaleY(1.05)}
  55%{transform:translateY(-10px) rotate(.5deg) scaleY(1.02)}
  82%{transform:translateY(-1px) scaleY(.97)}
}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
@keyframes sway{0%,100%{transform:rotate(0)}50%{transform:rotate(-2deg)}}
@keyframes droop{0%,100%{transform:translateY(0)}50%{transform:translateY(4px)}}
@keyframes slump{0%,100%{transform:translateY(0) rotate(0)}50%{transform:translateY(6px) rotate(-3deg)}}
@keyframes tf{0%{transform:translateY(0);opacity:.9}100%{transform:translateY(54px);opacity:0}}
@keyframes tailW{0%,100%{transform:rotate(-${trot}deg)}50%{transform:rotate(${trot}deg)}}`;

  // ── 배경 글로우 ──
  const bgFX={
    1:`<circle cx="80" cy="98" r="80" fill="rgba(255,220,50,.12)"/>`,
    2:`<circle cx="80" cy="98" r="76" fill="rgba(60,220,160,.10)"/>`,
    9:`<circle cx="80" cy="98" r="74" fill="rgba(120,130,150,.10)"/>`,
   10:`<circle cx="80" cy="98" r="74" fill="rgba(80,90,110,.12)"/>`,
  }[sid]||'';

  // ── SVG 그라디언트 & 필터 ──
  const defs=`<defs>
  <style>${css}</style>
  <radialGradient id="hG${uid}" cx="38%" cy="28%" r="68%">
    <stop offset="0%" stop-color="${hl(mainC,.38)}"/>
    <stop offset="65%" stop-color="${mainC}"/>
    <stop offset="100%" stop-color="${dk(mainC,.14)}"/>
  </radialGradient>
  <radialGradient id="bG${uid}" cx="36%" cy="26%" r="68%">
    <stop offset="0%" stop-color="${hl(mainC,.28)}"/>
    <stop offset="100%" stop-color="${dk(mainC,.1)}"/>
  </radialGradient>
  <radialGradient id="vG${uid}" cx="50%" cy="28%" r="65%">
    <stop offset="0%" stop-color="${hl(bellyC,.28)}"/>
    <stop offset="100%" stop-color="${bellyC}"/>
  </radialGradient>
  <radialGradient id="eG${uid}" cx="36%" cy="28%" r="65%">
    <stop offset="0%" stop-color="${hl(eyeC,.5)}"/>
    <stop offset="55%" stop-color="${eyeC}"/>
    <stop offset="100%" stop-color="${dk(eyeC,.25)}"/>
  </radialGradient>
  <radialGradient id="earG${uid}" cx="44%" cy="32%" r="62%">
    <stop offset="0%" stop-color="${hl(mainC,.25)}"/>
    <stop offset="100%" stop-color="${mainC}"/>
  </radialGradient>
  <filter id="blr${uid}" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur in="SourceGraphic" stdDeviation="4"/>
  </filter>
  <filter id="sft${uid}" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur in="SourceGraphic" stdDeviation="2"/>
  </filter>
  <filter id="dsh${uid}" x="-15%" y="-10%" width="130%" height="130%">
    <feDropShadow dx="0" dy="5" stdDeviation="6" flood-color="#1a0a05" flood-opacity="0.16"/>
  </filter>
</defs>`;

  // ── 눈 ──
  const lx=58, rx_=102, ey=80;

  const happyEye=(cx)=>`
    <path d="M${cx-15} ${ey+4} Q${cx} ${ey-16} ${cx+15} ${ey+4}" stroke="${OL}" stroke-width="5.5" fill="none" stroke-linecap="round"/>
    <ellipse cx="${cx+6}" cy="${ey-3}" rx="5" ry="4" fill="white" opacity=".78"/>`;

  const eyeInner=(cx)=>`
    <circle cx="${cx}" cy="${ey}" r="17" fill="white"/>
    <circle cx="${cx}" cy="${ey}" r="16.5" fill="none" stroke="${OL}" stroke-width="1.8"/>
    <circle cx="${cx}" cy="${ey+1}" r="12.5" fill="url(#eG${uid})"/>
    <circle cx="${cx}" cy="${ey+1}" r="7.5" fill="${dk(eyeC,.35)}" opacity=".85"/>
    <circle cx="${cx}" cy="${ey+1}" r="5.5" fill="#0d0608"/>
    <circle cx="${cx}" cy="${ey+1}" r="12.5" fill="none" stroke="${dk(eyeC,.28)}" stroke-width="2" opacity=".5"/>
    <ellipse cx="${cx+5}" cy="${ey-6}" rx="4.8" ry="4.2" fill="white" opacity=".95"/>
    <ellipse cx="${cx+5.5}" cy="${ey-6.5}" rx="2.5" ry="2.2" fill="white"/>
    <ellipse cx="${cx-5}" cy="${ey+5.5}" rx="2.5" ry="2" fill="white" opacity=".4"/>`;

  const normalEye=(cx)=>`<g>${eyeInner(cx)}</g>`;

  const sadEye=(cx)=>`
    <g>
      ${eyeInner(cx)}
      <path d="M${cx-16} ${ey-8} Q${cx+2} ${ey+6} ${cx+15} ${ey-2}" fill="${mainC}"/>
      <path d="M${cx-16} ${ey-8} Q${cx+2} ${ey+6} ${cx+15} ${ey-2}" stroke="${OL}" stroke-width="4.5" fill="none" stroke-linecap="round"/>
    </g>`;

  const xEye=(cx)=>`
    <g>
      <line x1="${cx-12}" y1="${ey-12}" x2="${cx+12}" y2="${ey+12}" stroke="${OL}" stroke-width="7" stroke-linecap="round"/>
      <line x1="${cx+12}" y1="${ey-12}" x2="${cx-12}" y2="${ey+12}" stroke="${OL}" stroke-width="7" stroke-linecap="round"/>
      <line x1="${cx-12}" y1="${ey-12}" x2="${cx+12}" y2="${ey+12}" stroke="rgba(255,255,255,.28)" stroke-width="2.5" stroke-linecap="round"/>
      <line x1="${cx+12}" y1="${ey-12}" x2="${cx-12}" y2="${ey+12}" stroke="rgba(255,255,255,.28)" stroke-width="2.5" stroke-linecap="round"/>
    </g>`;

  // ── 눈썹 ──
  const browHappy=`
    <path d="M${lx-11} ${ey-25} Q${lx} ${ey-30} ${lx+11} ${ey-25}" stroke="${OL}" stroke-width="3.2" fill="none" stroke-linecap="round" opacity=".65"/>
    <path d="M${rx_-11} ${ey-25} Q${rx_} ${ey-30} ${rx_+11} ${ey-25}" stroke="${OL}" stroke-width="3.2" fill="none" stroke-linecap="round" opacity=".65"/>`;
  const browWorried=`
    <path d="M${lx-12} ${ey-24} Q${lx+2} ${ey-17} ${lx+12} ${ey-24}" stroke="${OL}" stroke-width="3.5" fill="none" stroke-linecap="round"/>
    <path d="M${rx_-12} ${ey-24} Q${rx_+2} ${ey-17} ${rx_+12} ${ey-24}" stroke="${OL}" stroke-width="3.5" fill="none" stroke-linecap="round"/>`;
  const browSad=`
    <path d="M${lx-12} ${ey-20} Q${lx+2} ${ey-13} ${lx+12} ${ey-20}" stroke="${OL}" stroke-width="3.5" fill="none" stroke-linecap="round"/>
    <path d="M${rx_-12} ${ey-20} Q${rx_+2} ${ey-13} ${rx_+12} ${ey-20}" stroke="${OL}" stroke-width="3.5" fill="none" stroke-linecap="round"/>`;

  // ── 입 ──
  const my=122;
  const mouths={
    grin:   `<path d="M55 ${my} Q80 ${my+22} 105 ${my}" stroke="${OL}" stroke-width="3" stroke-linecap="round" fill="rgba(190,50,70,.5)"/>
             <path d="M60 ${my+4} Q80 ${my+20} 100 ${my+4}" fill="rgba(190,50,70,.4)"/>
             <ellipse cx="65" cy="${my+5}" rx="4.5" ry="3.5" fill="rgba(255,255,255,.55)"/>`,
    smile:  `<path d="M62 ${my} Q80 ${my+15} 98 ${my}" stroke="${OL}" stroke-width="2.8" fill="none" stroke-linecap="round"/>`,
    slight: `<path d="M68 ${my} Q80 ${my+9} 92 ${my}" stroke="${OL}" stroke-width="2.5" fill="none" stroke-linecap="round"/>`,
    neutral:`<path d="M68 ${my+4} L92 ${my+4}" stroke="${OL}" stroke-width="2.5" stroke-linecap="round"/>`,
    frown_s:`<path d="M68 ${my+9} Q80 ${my+3} 92 ${my+9}" stroke="${OL}" stroke-width="2.5" fill="none" stroke-linecap="round"/>`,
    frown:  `<path d="M62 ${my+11} Q80 ${my+3} 98 ${my+11}" stroke="${OL}" stroke-width="2.8" fill="none" stroke-linecap="round"/>`,
    frown_b:`<path d="M54 ${my+14} Q80 ${my+1} 106 ${my+14}" stroke="${OL}" stroke-width="3" fill="none" stroke-linecap="round"/>`,
  };

  // ── 홍조 (블러로 자연스럽게) ──
  const cheekBig  =`
    <ellipse cx="39"  cy="104" rx="21" ry="14" fill="rgba(255,95,80,.25)" filter="url(#blr${uid})"/>
    <ellipse cx="121" cy="104" rx="21" ry="14" fill="rgba(255,95,80,.25)" filter="url(#blr${uid})"/>`;
  const cheekLight=`
    <ellipse cx="41"  cy="106" rx="17" ry="11" fill="rgba(255,95,80,.15)" filter="url(#blr${uid})"/>
    <ellipse cx="119" cy="106" rx="17" ry="11" fill="rgba(255,95,80,.15)" filter="url(#blr${uid})"/>`;

  // ── 눈물 ──
  const tearsEl=`
    <ellipse class="tl" cx="40"  cy="96" rx="5" ry="8.5" fill="rgba(110,180,255,.92)"/>
    <ellipse class="tr" cx="120" cy="96" rx="5" ry="8.5" fill="rgba(110,180,255,.92)"/>`;

  // ── 공통 몸통 (그라디언트) ──
  const gndShadow=`<ellipse cx="80" cy="200" rx="52" ry="7" fill="rgba(0,0,0,.12)" filter="url(#sft${uid})"/>`;
  const body=`
    <ellipse cx="80" cy="164" rx="48" ry="32" fill="url(#bG${uid})" stroke="${OL}" stroke-width="2.5"/>
    <ellipse cx="80" cy="165" rx="34" ry="23" fill="url(#vG${uid})"/>
    <ellipse cx="68" cy="147" rx="15" ry="9"  fill="white" opacity=".1"/>`;
  const arms=`
    <path d="M32 148 Q15 156 15 171 Q15 185 32 186 Q51 186 52 170 Q52 158 32 148Z" fill="url(#bG${uid})" stroke="${OL}" stroke-width="2.3"/>
    <ellipse cx="26"  cy="182" rx="14" ry="9" fill="url(#vG${uid})"/>
    <path d="M128 148 Q145 156 145 171 Q145 185 128 186 Q109 186 108 170 Q108 158 128 148Z" fill="url(#bG${uid})" stroke="${OL}" stroke-width="2.3"/>
    <ellipse cx="134" cy="182" rx="14" ry="9" fill="url(#vG${uid})"/>`;
  const legs=`
    <ellipse cx="56"  cy="192" rx="24" ry="13" fill="url(#bG${uid})" stroke="${OL}" stroke-width="2.2"/>
    <ellipse cx="56"  cy="191" rx="16" ry="8"  fill="url(#vG${uid})"/>
    <ellipse cx="104" cy="192" rx="24" ry="13" fill="url(#bG${uid})" stroke="${OL}" stroke-width="2.2"/>
    <ellipse cx="104" cy="191" rx="16" ry="8"  fill="url(#vG${uid})"/>`;

  // ── 상태별 감정 조합 ──
  let eyesEl, browEl='', mouthEl, cheekEl='', extraEl='', tearEl='';
  if(sid===1){
    browEl=browHappy; eyesEl=happyEye(lx)+happyEye(rx_); mouthEl=mouths.grin; cheekEl=cheekBig;
    extraEl=`<g style="animation:bounce .5s ease-in-out infinite;transform-origin:80px 22px">
      <path d="M60 46 L68 20 L80 40 L92 20 L100 46Z" fill="#fbbf24" stroke="#f59e0b" stroke-width="2" stroke-linejoin="round"/>
      <circle cx="60" cy="46" r="4" fill="#ef4444"/><circle cx="80" cy="42" r="4.5" fill="#60a5fa"/><circle cx="100" cy="46" r="4" fill="#ef4444"/>
      <ellipse cx="80" cy="33" rx="6" ry="3" fill="rgba(255,255,255,.4)"/>
    </g>
    <text x="2" y="44" font-size="18">✨</text><text x="132" y="44" font-size="18">✨</text>
    <text x="4" y="200" font-size="16">🎉</text><text x="126" y="200" font-size="16">🎊</text>`;
  } else if(sid===2){
    browEl=browHappy; eyesEl=happyEye(lx)+happyEye(rx_); mouthEl=mouths.grin; cheekEl=cheekBig;
    extraEl=`<text x="4" y="46" font-size="18">💚</text><text x="132" y="46" font-size="18">💚</text>`;
  } else if(sid===3){
    browEl=browHappy; eyesEl=normalEye(lx)+normalEye(rx_); mouthEl=mouths.smile; cheekEl=cheekBig;
  } else if(sid===4){
    eyesEl=normalEye(lx)+normalEye(rx_); mouthEl=mouths.smile; cheekEl=cheekLight;
  } else if(sid===5){
    eyesEl=normalEye(lx)+normalEye(rx_); mouthEl=mouths.slight; cheekEl=cheekLight;
  } else if(sid===6){
    eyesEl=normalEye(lx)+normalEye(rx_); mouthEl=mouths.neutral;
  } else if(sid===7){
    browEl=browWorried; eyesEl=normalEye(lx)+normalEye(rx_); mouthEl=mouths.frown_s;
    extraEl=`<text x="4" y="56" font-size="15">💧</text>`;
  } else if(sid===8){
    browEl=browSad; eyesEl=sadEye(lx)+sadEye(rx_); mouthEl=mouths.frown; tearEl=tearsEl;
  } else if(sid===9){
    browEl=browSad; eyesEl=sadEye(lx)+sadEye(rx_); mouthEl=mouths.frown_b; tearEl=tearsEl;
  } else {
    eyesEl=xEye(lx)+xEye(rx_); mouthEl=mouths.frown_b; tearEl=tearsEl;
    extraEl=`<text x="118" y="194" font-size="16">💸</text>`;
  }

  // ══════════════════════════════════════════════════════════
  //  동물별 신체 구조
  // ══════════════════════════════════════════════════════════
  let ears='', head='', nose='', faceOver='', whiskers='', tail='';

  if(type==='dog'){
    // 🐶 강아지
    tail=`<g class="tw">
      <path d="M120 162 Q144 150 147 166 Q149 181 134 186" fill="${mainC}" stroke="${OL}" stroke-width="13" stroke-linecap="round"/>
      <path d="M121 164 Q143 153 146 167 Q148 179 135 184" fill="none" stroke="${hl(mainC,.32)}" stroke-width="5" stroke-linecap="round" opacity=".65"/>
    </g>`;
    ears=`
      <ellipse cx="22"  cy="68" rx="21" ry="36" fill="url(#earG${uid})" stroke="${OL}" stroke-width="2.5" transform="rotate(-10 22 68)"/>
      <ellipse cx="22"  cy="68" rx="13" ry="27" fill="${PINK}" opacity=".5" transform="rotate(-10 22 68)"/>
      <ellipse cx="22"  cy="60" rx="7"  ry="14" fill="${hl(PINK,.25)}" opacity=".4" transform="rotate(-10 22 68)"/>
      <ellipse cx="138" cy="68" rx="21" ry="36" fill="url(#earG${uid})" stroke="${OL}" stroke-width="2.5" transform="rotate(10 138 68)"/>
      <ellipse cx="138" cy="68" rx="13" ry="27" fill="${PINK}" opacity=".5" transform="rotate(10 138 68)"/>
      <ellipse cx="138" cy="60" rx="7"  ry="14" fill="${hl(PINK,.25)}" opacity=".4" transform="rotate(10 138 68)"/>`;
    head=`
      <circle cx="80" cy="88" r="62" fill="url(#hG${uid})" stroke="${OL}" stroke-width="2.8"/>
      <ellipse cx="66" cy="59" rx="21" ry="13" fill="white" opacity=".1"/>
      <ellipse cx="80" cy="106" rx="36" ry="28" fill="url(#vG${uid})"/>`;
    nose=`
      <ellipse cx="80" cy="112" rx="12" ry="10" fill="${OL}"/>
      <ellipse cx="80" cy="110" rx="7"  ry="4"  fill="rgba(255,255,255,.2)"/>
      <ellipse cx="77" cy="109" rx="3.2" ry="2.4" fill="rgba(255,255,255,.32)"/>`;
    faceOver=`
      <circle cx="54"  cy="65" r="4.5" fill="${hl(mainC,.1)}" stroke="${OL}" stroke-width="1.2"/>
      <circle cx="106" cy="65" r="4.5" fill="${hl(mainC,.1)}" stroke="${OL}" stroke-width="1.2"/>`;

  } else if(type==='hamster'){
    // 🐹 햄스터
    tail=`<g class="tw">
      <path d="M116 170 Q136 165 138 178 Q139 187 126 185" fill="${mainC}" stroke="${OL}" stroke-width="9" stroke-linecap="round"/>
    </g>`;
    ears=`
      <circle cx="52"  cy="38" r="21" fill="url(#earG${uid})" stroke="${OL}" stroke-width="2.5"/>
      <circle cx="52"  cy="38" r="13" fill="${PINK}"/>
      <ellipse cx="50" cy="32" rx="7.5" ry="5.5" fill="${hl(PINK,.28)}" opacity=".65"/>
      <circle cx="108" cy="38" r="21" fill="url(#earG${uid})" stroke="${OL}" stroke-width="2.5"/>
      <circle cx="108" cy="38" r="13" fill="${PINK}"/>
      <ellipse cx="106" cy="32" rx="7.5" ry="5.5" fill="${hl(PINK,.28)}" opacity=".65"/>`;
    faceOver=`
      <ellipse cx="14"  cy="106" rx="27" ry="23" fill="url(#bG${uid})" stroke="${OL}" stroke-width="2.2"/>
      <ellipse cx="14"  cy="108" rx="19" ry="16" fill="url(#vG${uid})"/>
      <ellipse cx="146" cy="106" rx="27" ry="23" fill="url(#bG${uid})" stroke="${OL}" stroke-width="2.2"/>
      <ellipse cx="146" cy="108" rx="19" ry="16" fill="url(#vG${uid})"/>`;
    head=`
      <ellipse cx="80" cy="90" rx="66" ry="60" fill="url(#hG${uid})" stroke="${OL}" stroke-width="2.8"/>
      <ellipse cx="65" cy="61" rx="20" ry="12" fill="white" opacity=".1"/>
      <ellipse cx="80" cy="106" rx="30" ry="24" fill="url(#vG${uid})"/>`;
    nose=`
      <ellipse cx="80" cy="110" rx="6"  ry="5"   fill="#e06070" stroke="${OL}" stroke-width="1.3"/>
      <ellipse cx="79" cy="109" rx="3"  ry="2"   fill="rgba(255,255,255,.38)"/>`;

  } else if(type==='horse'){
    // 🐴 말
    tail=`<g class="tw">
      <path d="M126 158 Q150 146 154 164 Q158 181 138 188 Q130 192 122 186" fill="${mainC}" stroke="${OL}" stroke-width="11" stroke-linecap="round"/>
      <path d="M128 162 Q148 151 152 166 Q155 179 139 185" fill="none" stroke="${hl(mainC,.32)}" stroke-width="4.5" stroke-linecap="round" opacity=".58"/>
    </g>`;
    ears=`
      <path d="M48 54 L52 6 L74 46Z"   fill="url(#earG${uid})" stroke="${OL}" stroke-width="2.5" stroke-linejoin="round"/>
      <path d="M53 51 L57 13 L71 46Z"  fill="${PINK}"/>
      <path d="M57 50 L60 20 L70 46Z"  fill="${hl(PINK,.22)}" opacity=".5"/>
      <path d="M112 54 L108 6 L86 46Z" fill="url(#earG${uid})" stroke="${OL}" stroke-width="2.5" stroke-linejoin="round"/>
      <path d="M107 51 L103 13 L89 46Z" fill="${PINK}"/>
      <path d="M103 50 L100 20 L90 46Z" fill="${hl(PINK,.22)}" opacity=".5"/>`;
    faceOver=`
      <path d="M48 38 Q58 8 80 4 Q102 8 112 38 Q100 16 80 12 Q60 16 48 38Z" fill="url(#hG${uid})" stroke="${OL}" stroke-width="1.8"/>
      <path d="M56 36 Q64 14 80 10 Q96 14 104 36 Q96 22 80 18 Q64 22 56 36Z" fill="${hl(mainC,.3)}" opacity=".28"/>`;
    head=`
      <circle cx="80" cy="84" r="60" fill="url(#hG${uid})" stroke="${OL}" stroke-width="2.8"/>
      <ellipse cx="65" cy="57" rx="19" ry="12" fill="white" opacity=".1"/>
      <ellipse cx="80" cy="106" rx="34" ry="28" fill="url(#vG${uid})"/>`;
    nose=`
      <ellipse cx="72" cy="116" rx="10" ry="8.5" fill="${dk(mainC,.1)}" stroke="${OL}" stroke-width="1.5" opacity=".62"/>
      <ellipse cx="88" cy="116" rx="10" ry="8.5" fill="${dk(mainC,.1)}" stroke="${OL}" stroke-width="1.5" opacity=".62"/>
      <ellipse cx="71" cy="115" rx="5.5" ry="4"  fill="rgba(255,255,255,.22)"/>
      <ellipse cx="87" cy="115" rx="5.5" ry="4"  fill="rgba(255,255,255,.22)"/>`;

  } else if(type==='fox'){
    // 🦊 여우
    tail=`<g class="tw">
      <path d="M125 154 Q152 138 157 159 Q162 180 146 188 Q136 195 124 186" fill="${mainC}" stroke="${OL}" stroke-width="2"/>
      <path d="M128 158 Q150 144 155 163 Q159 179 146 186" fill="none" stroke="${hl(mainC,.38)}" stroke-width="6" stroke-linecap="round" opacity=".58"/>
      <ellipse cx="142" cy="188" rx="13" ry="10" fill="${hl(bellyC,.15)}" stroke="${OL}" stroke-width="1.6"/>
    </g>`;
    ears=`
      <path d="M14 68 L32 4 L74 50Z"    fill="url(#earG${uid})" stroke="${OL}" stroke-width="2.6" stroke-linejoin="round"/>
      <path d="M22 66 L37 11 L70 50Z"   fill="${PINK}"/>
      <path d="M30 64 L42 18 L68 50Z"   fill="${hl(PINK,.18)}" opacity=".5"/>
      <path d="M146 68 L128 4 L86 50Z"  fill="url(#earG${uid})" stroke="${OL}" stroke-width="2.6" stroke-linejoin="round"/>
      <path d="M138 66 L123 11 L90 50Z" fill="${PINK}"/>
      <path d="M130 64 L118 18 L92 50Z" fill="${hl(PINK,.18)}" opacity=".5"/>`;
    head=`
      <circle cx="80" cy="88" r="62" fill="url(#hG${uid})" stroke="${OL}" stroke-width="2.8"/>
      <ellipse cx="66" cy="60" rx="20" ry="12" fill="white" opacity=".1"/>
      <ellipse cx="80" cy="104" rx="34" ry="28" fill="url(#vG${uid})"/>`;
    faceOver=`
      <ellipse cx="56"  cy="80"  rx="23" ry="19" fill="${OL}" opacity=".12"/>
      <ellipse cx="104" cy="80"  rx="23" ry="19" fill="${OL}" opacity=".12"/>
      <ellipse cx="43"  cy="109" rx="20" ry="26" fill="url(#vG${uid})" opacity=".9"/>
      <ellipse cx="117" cy="109" rx="20" ry="26" fill="url(#vG${uid})" opacity=".9"/>`;
    nose=`
      <ellipse cx="80" cy="108" rx="8"  ry="6.5" fill="${OL}"/>
      <ellipse cx="79" cy="107" rx="4"  ry="2.5" fill="rgba(255,255,255,.18)"/>`;
    whiskers=sid<=6
      ?`<line x1="5"   y1="106" x2="52"  y2="112" stroke="${OL}" stroke-width="1.8" stroke-linecap="round" opacity=".58"/>
        <line x1="5"   y1="116" x2="50"  y2="118" stroke="${OL}" stroke-width="1.8" stroke-linecap="round" opacity=".46"/>
        <line x1="12"  y1="126" x2="52"  y2="124" stroke="${OL}" stroke-width="1.5" stroke-linecap="round" opacity=".3"/>
        <line x1="108" y1="112" x2="155" y2="106" stroke="${OL}" stroke-width="1.8" stroke-linecap="round" opacity=".58"/>
        <line x1="110" y1="118" x2="155" y2="116" stroke="${OL}" stroke-width="1.8" stroke-linecap="round" opacity=".46"/>
        <line x1="108" y1="124" x2="148" y2="126" stroke="${OL}" stroke-width="1.5" stroke-linecap="round" opacity=".3"/>`
      :`<line x1="5"   y1="110" x2="50"  y2="115" stroke="${OL}" stroke-width="1.5" stroke-linecap="round" opacity=".28"/>
        <line x1="110" y1="115" x2="155" y2="110" stroke="${OL}" stroke-width="1.5" stroke-linecap="round" opacity=".28"/>`;

  } else {
    // 🐱 고양이 (기본)
    tail=`<g class="tw">
      <path d="M124 162 Q150 148 153 166 Q155 181 138 186" fill="${mainC}" stroke="${OL}" stroke-width="10" stroke-linecap="round"/>
      <path d="M126 165 Q148 153 151 168 Q152 179 139 184" fill="none" stroke="${hl(mainC,.32)}" stroke-width="4" stroke-linecap="round" opacity=".58"/>
    </g>`;
    ears=`
      <path d="M20 72 L40 10 L78 54Z"   fill="url(#earG${uid})" stroke="${OL}" stroke-width="2.6" stroke-linejoin="round"/>
      <path d="M28 70 L46 18 L73 54Z"   fill="${PINK}"/>
      <path d="M35 68 L51 24 L70 54Z"   fill="${hl(PINK,.2)}" opacity=".5"/>
      <path d="M140 72 L120 10 L82 54Z" fill="url(#earG${uid})" stroke="${OL}" stroke-width="2.6" stroke-linejoin="round"/>
      <path d="M132 70 L114 18 L87 54Z" fill="${PINK}"/>
      <path d="M125 68 L109 24 L90 54Z" fill="${hl(PINK,.2)}" opacity=".5"/>`;
    head=`
      <circle cx="80" cy="88" r="62" fill="url(#hG${uid})" stroke="${OL}" stroke-width="2.8"/>
      <ellipse cx="66" cy="60" rx="21" ry="13" fill="white" opacity=".1"/>
      <ellipse cx="80" cy="104" rx="36" ry="30" fill="url(#vG${uid})"/>`;
    nose=`
      <ellipse cx="80" cy="108" rx="8"   ry="6"   fill="${NOSE}" stroke="${OL}" stroke-width="1.4"/>
      <ellipse cx="79" cy="107" rx="3.8" ry="2.2" fill="rgba(255,255,255,.38)"/>`;
    whiskers=sid<=6
      ?`<line x1="6"   y1="107" x2="54"  y2="113" stroke="${OL}" stroke-width="1.8" stroke-linecap="round" opacity=".6"/>
        <line x1="6"   y1="117" x2="52"  y2="119" stroke="${OL}" stroke-width="1.8" stroke-linecap="round" opacity=".48"/>
        <line x1="12"  y1="127" x2="52"  y2="125" stroke="${OL}" stroke-width="1.5" stroke-linecap="round" opacity=".32"/>
        <line x1="106" y1="113" x2="154" y2="107" stroke="${OL}" stroke-width="1.8" stroke-linecap="round" opacity=".6"/>
        <line x1="108" y1="119" x2="154" y2="117" stroke="${OL}" stroke-width="1.8" stroke-linecap="round" opacity=".48"/>
        <line x1="108" y1="125" x2="148" y2="127" stroke="${OL}" stroke-width="1.5" stroke-linecap="round" opacity=".32"/>`
      :`<line x1="6"   y1="110" x2="52"  y2="115" stroke="${OL}" stroke-width="1.6" stroke-linecap="round" opacity=".3"/>
        <line x1="108" y1="115" x2="154" y2="110" stroke="${OL}" stroke-width="1.6" stroke-linecap="round" opacity=".3"/>`;
  }

  return `<svg viewBox="0 0 160 200" fill="none" xmlns="http://www.w3.org/2000/svg">
  ${defs}
  ${bgFX}
  ${gndShadow}
  <g class="hb" filter="url(#dsh${uid})">
    ${tail}
    ${body}${arms}${legs}
    ${type==='hamster'?faceOver:''}
    ${ears}
    ${head}
    ${type!=='hamster'?faceOver:''}
    ${browEl}
    ${eyesEl}
    ${nose}
    ${whiskers}
    ${mouthEl}
    ${cheekEl}
    ${tearEl}
  </g>
  ${extraEl}
</svg>`;
}'''

new_content = content[:start] + NEW_FUNCTION + content[func_end:]

with open(r'C:/Users/kyu26/savings-tracker/저축.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"SUCCESS! {len(content)} -> {len(new_content)} chars")
print(f"Diff: {len(new_content)-len(content):+d} chars")
