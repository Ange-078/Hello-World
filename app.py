import html
import random
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hello World Motion Lab", page_icon="✨", layout="wide")

st.title("✨ Hello World Motion Lab")
st.write("Type a name, choose how it looks, and add a looping motion effect.")

with st.sidebar:
    st.header("Customize your name")
    name = st.text_input("Enter your name", value="Hello World", max_chars=80)
    font_family = st.selectbox(
        "Font type",
        ["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana", "Trebuchet MS", "Impact"],
    )
    font_size = st.slider("Font size", min_value=20, max_value=100, value=48, step=2)
    background = st.selectbox(
        "Background",
        ["Light", "Dark", "Ocean", "Sunset", "Forest", "Lavender"],
    )
    name_mode = st.selectbox("Name display mode", ["Centered", "Ticker Tape", "Repeated"])
    effect = st.selectbox(
        "Dynamic action",
        ["None", "Rain", "Snow", "Hail", "Wind Gust", "Confetti", "Tornado"],
    )
    speed = st.slider(
        "Animation speed",
        min_value=0.5,
        max_value=3.0,
        value=1.4,
        step=0.1,
        help="Higher values make the animation move faster.",
    )

backgrounds = {
    "Light": ("#f7f8fc", "#202433"),
    "Dark": ("#10131c", "#ffffff"),
    "Ocean": ("linear-gradient(135deg, #063b5c, #18a6a6)", "#ffffff"),
    "Sunset": ("linear-gradient(135deg, #54245f, #e66b58, #f6bd60)", "#ffffff"),
    "Forest": ("linear-gradient(135deg, #153b2d, #4c956c)", "#ffffff"),
    "Lavender": ("linear-gradient(135deg, #e7ddff, #fce1ec)", "#302447"),
}
bg, text_color = backgrounds[background]

# Escape user-provided text before placing it into HTML.
safe_name = html.escape(name or "Hello World")
safe_font = font_family  # Chosen only from the fixed allowlist above.

if name_mode == "Repeated":
    display_name = "<div class='repeated'>" + " &nbsp; • &nbsp; ".join([safe_name] * 5) + "</div>"
elif name_mode == "Ticker Tape":
    display_name = f"<div class='ticker-track'><span>{safe_name}</span><span>{safe_name}</span><span>{safe_name}</span></div>"
else:
    display_name = f"<div class='center-name'>{safe_name}</div>"

# Each effect is built from CSS-animated particles. The animation runs in the
# embedded browser frame, so it loops continuously without repeatedly rerunning Streamlit.
effect_settings = {
    "Rain": {"symbols": ["💧", "💦"], "count": 44, "class_name": "rain"},
    "Snow": {"symbols": ["❄", "❅", "❆", "✳"], "count": 34, "class_name": "snow"},
    "Hail": {"symbols": ["●", "◦", "🧊"], "count": 28, "class_name": "hail"},
    "Wind Gust": {"symbols": ["〰", "〜", "﹏", "➰"], "count": 22, "class_name": "wind"},
    "Confetti": {"symbols": ["🎉", "✦", "●", "■", "▲", "★"], "count": 42, "class_name": "confetti"},
    "Tornado": {"symbols": ["〰", "🌀", "·", "✦"], "count": 30, "class_name": "tornado"},
}

particles = []
if effect in effect_settings:
    settings = effect_settings[effect]
    for i in range(settings["count"]):
        symbol = random.choice(settings["symbols"])
        left = random.randint(0, 100)
        delay = random.uniform(-8, 0)
        duration = random.uniform(2.5, 7.0) / speed
        size = random.randint(12, 27)
        drift = random.randint(-90, 90)
        particles.append(
            f'<span class="particle {settings["class_name"]}" '
            f'style="left:{left}%; animation-delay:{delay:.2f}s; '
            f'animation-duration:{duration:.2f}s; font-size:{size}px; '
            f'--drift:{drift}px; --index:{i};">{symbol}</span>'
        )

particle_html = "".join(particles)
animation_duration = 18 / speed

html_doc = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; padding: 0; width: 100%; height: 100%; }}
  .stage {{
    position: relative; width: 100%; height: 620px; overflow: hidden;
    border-radius: 18px; background: {bg}; color: {text_color};
    font-family: {safe_font}, sans-serif;
    isolation: isolate;
  }}
  .effects {{ position: absolute; inset: 0; overflow: hidden; z-index: 1; pointer-events: none; }}
  .particle {{ position: absolute; top: -45px; display: block; opacity: .85; user-select: none; }}
  .rain {{ animation-name: rain-fall; animation-timing-function: linear; animation-iteration-count: infinite; }}
  .snow {{ animation-name: snow-fall; animation-timing-function: linear; animation-iteration-count: infinite; }}
  .hail {{ animation-name: hail-fall; animation-timing-function: linear; animation-iteration-count: infinite; }}
  .wind {{ animation-name: wind-blow; animation-timing-function: ease-in-out; animation-iteration-count: infinite; }}
  .confetti {{ animation-name: confetti-fall; animation-timing-function: linear; animation-iteration-count: infinite; }}
  .tornado {{ top: 50%; left: 50%; animation-name: tornado-spin; animation-timing-function: linear; animation-iteration-count: infinite; }}
  @keyframes rain-fall {{ 0% {{ transform: translate3d(0,-50px,0) rotate(12deg); opacity: 0; }} 10% {{opacity:.9}} 100% {{ transform: translate3d(var(--drift),700px,0) rotate(20deg); opacity: .15; }} }}
  @keyframes snow-fall {{ 0% {{ transform: translate3d(0,-50px,0) rotate(0); opacity: 0; }} 15% {{opacity:.95}} 100% {{ transform: translate3d(var(--drift),700px,0) rotate(360deg); opacity: .25; }} }}
  @keyframes hail-fall {{ 0% {{ transform: translate3d(0,-50px,0); opacity: 0; }} 10% {{opacity:1}} 75% {{transform:translate3d(calc(var(--drift) * .3),520px,0)}} 85% {{transform:translate3d(var(--drift),490px,0)}} 100% {{transform:translate3d(var(--drift),700px,0); opacity:.1}} }}
  @keyframes wind-blow {{ 0%,100% {{ transform: translateX(-160px) rotate(-8deg); opacity: 0; }} 15%,80% {{opacity:.8}} 50% {{ transform: translateX(650px) rotate(8deg); }} }}
  @keyframes confetti-fall {{ 0% {{ transform: translate3d(0,-60px,0) rotate(0); opacity: 0; }} 10% {{opacity:1}} 100% {{ transform: translate3d(var(--drift),700px,0) rotate(720deg); opacity:.2; }} }}
  @keyframes tornado-spin {{
    0% {{ transform: translate(-50%,-50%) rotate(0deg) translateX(35px) scale(.65); opacity:.25; }}
    50% {{ transform: translate(-50%,-50%) rotate(180deg) translateX(190px) scale(1.25); opacity:.9; }}
    100% {{ transform: translate(-50%,-50%) rotate(360deg) translateX(35px) scale(.65); opacity:.25; }}
  }}
  .name-layer {{ position: absolute; z-index: 5; inset: 0; display: flex; align-items: center; justify-content: center; padding: 28px; overflow: hidden; }}
  .center-name {{ max-width: 100%; overflow-wrap: anywhere; text-align: center; font-size: {font_size}px; font-weight: 800; text-shadow: 0 2px 10px rgba(0,0,0,.12); }}
  .ticker-track {{ display: flex; gap: 70px; width: max-content; white-space: nowrap; font-size: {font_size}px; font-weight: 800; animation: ticker {animation_duration:.2f}s linear infinite; }}
  .ticker-track span {{ flex: 0 0 auto; }}
  @keyframes ticker {{ from {{ transform: translateX(35vw); }} to {{ transform: translateX(-70%); }} }}
  .repeated {{ width: 100%; text-align: center; font-size: {font_size}px; line-height: 1.55; font-weight: 800; overflow-wrap: anywhere; text-shadow: 0 2px 10px rgba(0,0,0,.12); }}
  .caption {{ position: absolute; z-index: 6; left: 14px; bottom: 12px; font: 12px/1.3 Arial, sans-serif; opacity: .75; }}
  @media (prefers-reduced-motion: reduce) {{
    .particle, .ticker-track {{ animation-duration: 30s !important; }}
  }}
</style>
</head>
<body>
  <div class="stage">
    <div class="effects">{particle_html}</div>
    <div class="name-layer">{display_name}</div>
    <div class="caption">Hello World Motion Lab · {html.escape(effect)} effect</div>
  </div>
</body>
</html>
"""

components.html(html_doc, height=640, scrolling=False)
st.caption("Tip: Change the font, size, background, or action in the sidebar. The motion loops inside the preview.")
