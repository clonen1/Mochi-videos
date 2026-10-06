"""Kit do Mochi: gera o gato em SVG com varias expressoes e acessorios."""

ORANGE = "#F2A14A"
ORANGE_DARK = "#D9802C"
CREAM = "#FFF6EA"
PINK = "#F5B5B5"
BLUSH = "#F7A9A0"
NOSE = "#E77C8A"
INK = "#2B2B2B"
RED = "#D8343A"
RED_DARK = "#B8262C"
BAG = "#3F6FB0"
BAG_LIGHT = "#5A8BCC"


def _eyes(expr, blink):
    if blink or expr == "sleep":
        return (
            f'<path d="M134 162 Q148 172 162 162" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
            f'<path d="M218 162 Q232 172 246 162" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
        )
    if expr == "happy":
        return (
            f'<path d="M134 166 Q148 148 162 166" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
            f'<path d="M218 166 Q232 148 246 166" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
        )
    eyes = (
        f'<circle cx="148" cy="162" r="12" fill="{INK}"/><circle cx="232" cy="162" r="12" fill="{INK}"/>'
        f'<circle cx="152" cy="157" r="4" fill="#fff"/><circle cx="236" cy="157" r="4" fill="#fff"/>'
    )
    if expr == "angry":
        eyes += (
            f'<path d="M130 138 L166 150" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
            f'<path d="M250 138 L214 150" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
        )
    return eyes


def _mouth(expr):
    if expr == "happy":
        return f'<path d="M176 202 Q190 224 204 202 Z" fill="#C2414E" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>'
    if expr == "angry":
        return f'<path d="M178 210 Q190 200 202 210" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
    if expr == "eat":
        return f'<ellipse cx="190" cy="208" rx="9" ry="7" fill="#C2414E" stroke="{INK}" stroke-width="2.5"/>'
    return f'<path d="M178 202 Q184 210 190 202 Q196 210 202 202" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'


def _headphones():
    return (
        f'<path d="M98 160 Q100 70 190 68 Q280 70 282 160" fill="none" stroke="#333" stroke-width="12" stroke-linecap="round"/>'
        f'<rect x="80" y="140" width="34" height="52" rx="12" fill="#333"/><rect x="266" y="140" width="34" height="52" rx="12" fill="#333"/>'
        f'<rect x="86" y="150" width="22" height="32" rx="8" fill="#4FD1C5"/><rect x="272" y="150" width="22" height="32" rx="8" fill="#4FD1C5"/>'
    )


def mochi(expr="normal", blink=False, headphones=False):
    """Devolve o Mochi como grupo SVG num espaco de 380x400."""
    blush_op = "1" if expr != "angry" else "0"
    angry_tint = '<ellipse cx="190" cy="140" rx="90" ry="40" fill="#E5533D" opacity="0.18"/>' if expr == "angry" else ""
    return f"""
<path d="M270 330 Q340 320 330 260 Q325 230 300 240" fill="none" stroke="#E8913A" stroke-width="22" stroke-linecap="round"/>
<rect x="262" y="235" width="48" height="62" rx="12" fill="{BAG}"/><rect x="270" y="250" width="32" height="18" rx="5" fill="{BAG_LIGHT}"/>
<ellipse cx="190" cy="290" rx="95" ry="78" fill="{ORANGE}"/>
<ellipse cx="190" cy="305" rx="55" ry="55" fill="{CREAM}"/>
<ellipse cx="145" cy="362" rx="28" ry="16" fill="{CREAM}"/><ellipse cx="235" cy="362" rx="28" ry="16" fill="{CREAM}"/>
<polygon points="108,135 118,58 168,105" fill="{ORANGE}"/><polygon points="272,135 262,58 212,105" fill="{ORANGE}"/>
<polygon points="120,118 125,78 152,105" fill="{PINK}"/><polygon points="260,118 255,78 228,105" fill="{PINK}"/>
<ellipse cx="190" cy="168" rx="98" ry="80" fill="{ORANGE}"/>
<path d="M175 92 Q180 110 172 122" fill="none" stroke="{ORANGE_DARK}" stroke-width="6" stroke-linecap="round"/>
<path d="M190 90 Q192 112 190 126" fill="none" stroke="{ORANGE_DARK}" stroke-width="6" stroke-linecap="round"/>
<path d="M205 92 Q200 110 208 122" fill="none" stroke="{ORANGE_DARK}" stroke-width="6" stroke-linecap="round"/>
{angry_tint}
<ellipse cx="148" cy="160" rx="34" ry="30" fill="{CREAM}"/>
<ellipse cx="190" cy="200" rx="48" ry="32" fill="{CREAM}"/>
{_eyes(expr, blink)}
<ellipse cx="125" cy="198" rx="14" ry="8" fill="{BLUSH}" opacity="{blush_op}"/><ellipse cx="255" cy="198" rx="14" ry="8" fill="{BLUSH}" opacity="{blush_op}"/>
<polygon points="182,186 198,186 190,195" fill="{NOSE}"/>
{_mouth(expr)}
<path d="M100 190 L60 184 M100 200 L62 204 M280 190 L320 184 M280 200 L318 204" stroke="#C9703A" stroke-width="2" stroke-linecap="round"/>
<rect x="112" y="228" width="156" height="24" rx="12" fill="{RED}"/><rect x="200" y="240" width="22" height="48" rx="8" fill="{RED_DARK}"/>
{_headphones() if headphones else ""}
"""
