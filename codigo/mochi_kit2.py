"""Mochi com visual novo: gradientes, sombras suaves, contorno e luz. Mesmas expressoes do mochi_kit."""
from mochi_kit import _eyes, _mouth, _headphones, CREAM, PINK, BLUSH, NOSE, INK, RED, RED_DARK, BAG, BAG_LIGHT

STYLES = {
    # A: suave, sem contorno, volume por gradiente
    "A": dict(outline=None, ow=0, c1="#FFC271", c2="#F2A14A", c3="#D9802C", shade=0.55, rim=0.0, big=1.0),
    # B: autocolante, contorno escuro grosso, sombra plana
    "B": dict(outline="#8A4A1E", ow=7, c1="#F7B35E", c2="#F2A14A", c3="#E08A34", shade=0.25, rim=0.0, big=1.0),
    # C: fofo, cabeça maior, luz de contorno
    "C": dict(outline="#B8661F", ow=3, c1="#FFC978", c2="#F4A650", c3="#D9802C", shade=0.45, rim=0.6, big=1.12),
}


def _defs(s):
    return (f'<defs>'
            f'<radialGradient id="gb" cx="0.38" cy="0.3" r="0.9"><stop offset="0" stop-color="{s["c1"]}"/>'
            f'<stop offset="0.6" stop-color="{s["c2"]}"/><stop offset="1" stop-color="{s["c3"]}"/></radialGradient>'
            f'<radialGradient id="gc" cx="0.4" cy="0.3" r="0.9"><stop offset="0" stop-color="#FFFFFF"/>'
            f'<stop offset="1" stop-color="#F3DEC4"/></radialGradient>'
            f'<radialGradient id="ge" cx="0.5" cy="0.7" r="0.8"><stop offset="0" stop-color="#F59A9A"/>'
            f'<stop offset="1" stop-color="#F8C2C2"/></radialGradient>'
            f'</defs>')


def _shadow():
    # sombra suave no chao: elipses empilhadas com pouca opacidade (o cairosvg nao tem blur)
    out = ""
    for i, (rx, ry, op) in enumerate([(150, 26, .05), (130, 22, .07), (110, 18, .09), (90, 14, .11)]):
        out += f'<ellipse cx="190" cy="372" rx="{rx}" ry="{ry}" fill="#3A2410" opacity="{op}"/>'
    return out


def mochi2(style="A", expr="normal", blink=False, headphones=False, mouth_open=0.0):
    s = STYLES[style]
    o = f'stroke="{s["outline"]}" stroke-width="{s["ow"]}" stroke-linejoin="round"' if s["outline"] else ""
    k = s["big"]
    head = f'transform="translate(190 168) scale({k}) translate(-190 -168)"'
    shade = s["shade"]
    rim = (f'<path d="M96 150 Q100 100 150 92" fill="none" stroke="#FFE2B0" stroke-width="7" stroke-linecap="round" opacity="{s["rim"]}"/>'
           f'<path d="M96 292 Q92 250 120 226" fill="none" stroke="#FFE2B0" stroke-width="7" stroke-linecap="round" opacity="{s["rim"]}"/>') if s["rim"] else ""
    angry = '<ellipse cx="190" cy="140" rx="90" ry="40" fill="#E5533D" opacity="0.18"/>' if expr == "angry" else ""
    blush_op = "0.9" if expr != "angry" else "0"
    return f"""{_defs(s)}{_shadow()}
<path d="M270 330 Q340 320 330 260 Q325 230 300 240" fill="none" stroke="{s['c3']}" stroke-width="24" stroke-linecap="round"/>
<path d="M270 330 Q340 320 330 260 Q325 230 300 240" fill="none" stroke="{s['c2']}" stroke-width="16" stroke-linecap="round"/>
<path d="M326 276 Q330 258 316 246" fill="none" stroke="#FFF1DC" stroke-width="9" stroke-linecap="round"/>
<rect x="262" y="235" width="48" height="62" rx="12" fill="{BAG}"/><rect x="270" y="250" width="32" height="18" rx="5" fill="{BAG_LIGHT}"/>
<ellipse cx="190" cy="290" rx="95" ry="78" fill="url(#gb)" {o}/>
<ellipse cx="190" cy="318" rx="80" ry="42" fill="#8A4A1E" opacity="{shade*0.22:.2f}"/>
<ellipse cx="190" cy="305" rx="55" ry="55" fill="url(#gc)"/>
<ellipse cx="145" cy="362" rx="28" ry="16" fill="url(#gc)" {o}/><ellipse cx="235" cy="362" rx="28" ry="16" fill="url(#gc)" {o}/>
<path d="M126 360 L126 370 M145 362 L145 372 M164 360 L164 370" stroke="#D9B58C" stroke-width="2" stroke-linecap="round"/>
<g {head}>
<polygon points="108,135 118,58 168,105" fill="url(#gb)" {o}/><polygon points="272,135 262,58 212,105" fill="url(#gb)" {o}/>
<polygon points="120,118 125,78 152,105" fill="url(#ge)"/><polygon points="260,118 255,78 228,105" fill="url(#ge)"/>
<ellipse cx="190" cy="168" rx="98" ry="80" fill="url(#gb)" {o}/>
<ellipse cx="190" cy="232" rx="86" ry="22" fill="#8A4A1E" opacity="{shade*0.18:.2f}"/>
{rim}
<path d="M175 92 Q180 110 172 122" fill="none" stroke="{s['c3']}" stroke-width="6" stroke-linecap="round"/>
<path d="M190 90 Q192 112 190 126" fill="none" stroke="{s['c3']}" stroke-width="6" stroke-linecap="round"/>
<path d="M205 92 Q200 110 208 122" fill="none" stroke="{s['c3']}" stroke-width="6" stroke-linecap="round"/>
<path d="M90 176 L74 168 M92 186 L72 188 M290 176 L306 168 M288 186 L308 188" stroke="{s['c3']}" stroke-width="5" stroke-linecap="round"/>
{angry}
<ellipse cx="148" cy="160" rx="34" ry="30" fill="url(#gc)"/>
<ellipse cx="190" cy="200" rx="48" ry="32" fill="url(#gc)"/>
{_eyes(expr, blink)}
<ellipse cx="125" cy="198" rx="15" ry="9" fill="{BLUSH}" opacity="{blush_op}"/><ellipse cx="255" cy="198" rx="15" ry="9" fill="{BLUSH}" opacity="{blush_op}"/>
<ellipse cx="190" cy="189" rx="9" ry="6.5" fill="{NOSE}"/><ellipse cx="187" cy="187" rx="3" ry="1.8" fill="#FFD0D6"/>
{_mouth(expr, mouth_open)}
<path d="M100 190 L56 182 M100 200 L58 206 M280 190 L324 182 M280 200 L322 206" stroke="#FFF1DC" stroke-width="2.5" stroke-linecap="round" opacity="0.9"/>
</g>
<rect x="112" y="228" width="156" height="24" rx="12" fill="{RED}"/><rect x="112" y="228" width="156" height="9" rx="4.5" fill="#EE5A60" opacity="0.7"/><rect x="200" y="240" width="22" height="48" rx="8" fill="{RED_DARK}"/>
{_headphones() if headphones else ""}
"""
