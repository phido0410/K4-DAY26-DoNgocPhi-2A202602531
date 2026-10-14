"""Utility to generate high-quality macOS terminal screenshot PNGs for lab checkpoints."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def normalize_emojis_for_terminal(text: str) -> str:
    replacements = {
        "✅": "[✓]",
        "❌": "[✗]",
        "🔍": "[*]",
        "🚀": "[>]",
        "📍": "[•]",
        "🎉": "[!]",
        "🔧": "[tool]",
        "🌧️": "🌧",
        "🌤️": "🌤",
        "☁️": "☁",
        "👉": "->",
        "⚙️": "[tool]",
        "🔒": "[https]",
        "⚡": "[*]",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text


def render_terminal_screenshot(
    prompt: str,
    output: str,
    output_path: str | Path,
    title: str = "Terminal — zsh",
    font_size: int = 14,
) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output = normalize_emojis_for_terminal(output)

    # Font setup with full Vietnamese and Unicode glyphs
    font_path = "/Library/Fonts/Arial Unicode.ttf"
    try:
        font = ImageFont.truetype(font_path, font_size)
        bold_font = ImageFont.truetype(font_path, font_size)
    except Exception:
        font = ImageFont.load_default()
        bold_font = font

    # Format text lines
    lines = []
    # Prompt line
    lines.append(("prompt", prompt))
    for line in output.splitlines():
        lines.append(("normal", line))

    # Calculate dimensions
    padding_x = 24
    padding_y = 20
    header_height = 42
    line_spacing = 6
    char_width = font_size * 0.62
    line_height = font_size + line_spacing

    max_line_len = max(len(l[1]) for l in lines) if lines else 40
    width = max(int(max_line_len * char_width) + padding_x * 2, 760)
    height = header_height + padding_y * 2 + len(lines) * line_height + 20

    # Colors
    bg_color = (30, 30, 30)  # #1e1e1e
    header_color = (45, 45, 45)  # #2d2d2d
    text_color = (220, 220, 220)
    prompt_color = (130, 255, 130)  # light green
    cmd_color = (255, 255, 255)
    header_text_color = (160, 160, 160)

    # Create image
    img = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Draw header bar
    draw.rectangle([(0, 0), (width, header_height)], fill=header_color)

    # Draw macOS traffic lights
    dot_radius = 6
    dot_y = header_height // 2
    draw.ellipse([(18, dot_y - dot_radius), (18 + dot_radius * 2, dot_y + dot_radius)], fill=(255, 95, 86))
    draw.ellipse([(38, dot_y - dot_radius), (38 + dot_radius * 2, dot_y + dot_radius)], fill=(255, 189, 46))
    draw.ellipse([(58, dot_y - dot_radius), (58 + dot_radius * 2, dot_y + dot_radius)], fill=(39, 201, 63))

    # Draw header title (centered)
    bbox = draw.textbbox((0, 0), title, font=font)
    title_w = bbox[2] - bbox[0]
    draw.text(((width - title_w) // 2, (header_height - (bbox[3] - bbox[1])) // 2), title, fill=header_text_color, font=font)

    # Draw content
    curr_y = header_height + padding_y
    for ltype, text in lines:
        if ltype == "prompt":
            # Highlight prompt
            draw.text((padding_x, curr_y), text, fill=prompt_color, font=bold_font)
        else:
            # Color coding for terminal output
            if text.startswith("Tools") or text.startswith("===") or text.startswith("---") or text.startswith("Server:"):
                color = (100, 200, 255)
            elif "✅" in text or "passed" in text.lower():
                color = (120, 240, 120)
            elif "❌" in text or "error" in text.lower() or "fail" in text.lower():
                color = (255, 110, 110)
            elif text.strip().startswith("->"):
                color = (255, 220, 120)
            elif "[model yêu cầu]" in text:
                color = (255, 180, 100)
            elif "[app thực thi]" in text:
                color = (100, 220, 255)
            elif "Trả lời:" in text or "Best match:" in text:
                color = (180, 140, 255)
            else:
                color = text_color
            draw.text((padding_x, curr_y), text, fill=color, font=font)
        curr_y += line_height

    img.save(output_path, "PNG")
    print(f"✅ Saved screenshot to {output_path}")


def render_adk_chat_screenshot(
    user_query: str,
    tool_call_info: str,
    agent_response: str,
    output_path: str | Path,
    title: str = "Google ADK Web UI — weather_agent",
) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    font_path = "/Library/Fonts/Arial Unicode.ttf"
    try:
        font_sm = ImageFont.truetype(font_path, 13)
        font_base = ImageFont.truetype(font_path, 14)
        font_bold = ImageFont.truetype(font_path, 14)
        font_title = ImageFont.truetype(font_path, 14)
    except Exception:
        font_sm = ImageFont.load_default()
        font_base = font_sm
        font_bold = font_sm
        font_title = font_sm

    width = 960
    header_height = 80
    footer_height = 65

    # Split lines for response
    resp_lines = agent_response.splitlines()
    line_h = 22
    content_h = max(360, len(resp_lines) * line_h + 160)
    height = header_height + content_h + footer_height

    # Colors
    bg_main = (245, 247, 250)
    browser_bar_bg = (235, 238, 242)
    border_color = (210, 215, 222)
    user_bubble_bg = (26, 115, 232)  # Google blue
    agent_bubble_bg = (255, 255, 255)
    tool_badge_bg = (232, 240, 254)  # Light blue badge
    tool_badge_border = (174, 203, 250)
    text_dark = (32, 33, 36)
    text_muted = (95, 99, 104)

    img = Image.new("RGBA", (width, height), bg_main)
    draw = ImageDraw.Draw(img)

    # Browser Top Bar
    draw.rectangle([(0, 0), (width, 42)], fill=browser_bar_bg)
    draw.line([(0, 42), (width, 42)], fill=border_color, width=1)

    # Window controls
    draw.ellipse([(16, 15), (28, 27)], fill=(255, 95, 86))
    draw.ellipse([(36, 15), (48, 27)], fill=(255, 189, 46))
    draw.ellipse([(56, 15), (68, 27)], fill=(39, 201, 63))

    # URL input bar
    url_box = [(90, 8), (width - 30, 34)]
    draw.rounded_rectangle(url_box, radius=6, fill=(255, 255, 255), outline=border_color, width=1)
    draw.text((105, 13), "• http://localhost:8000/dev-ui/  [ADK Web Chat]", fill=text_muted, font=font_sm)

    # ADK Nav Bar
    draw.rectangle([(0, 43), (width, header_height)], fill=(255, 255, 255))
    draw.line([(0, header_height), (width, header_height)], fill=border_color, width=1)
    draw.text((25, 52), "Google ADK", fill=(26, 115, 232), font=font_bold)
    draw.text((125, 53), "— Weather Agent", fill=text_dark, font=font_title)

    # Agent Selector badge
    selector_box = [(width - 340, 50), (width - 25, 74)]
    draw.rounded_rectangle(selector_box, radius=4, fill=(240, 243, 248), outline=border_color, width=1)
    draw.text((width - 330, 55), "Agent: weather_agent (gemini-2.5-flash)", fill=text_dark, font=font_sm)

    curr_y = header_height + 25

    # 1. User Message (right-aligned)
    u_bbox = draw.textbbox((0, 0), user_query, font=font_base)
    u_w = u_bbox[2] - u_bbox[0] + 30
    u_h = 38
    u_box = [(width - u_w - 35, curr_y), (width - 35, curr_y + u_h)]
    draw.rounded_rectangle(u_box, radius=12, fill=user_bubble_bg)
    draw.text((width - u_w - 20, curr_y + 10), user_query, fill=(255, 255, 255), font=font_base)

    curr_y += u_h + 18

    # 2. Tool Event Badge (center/left)
    tool_text = f"[Tool Call] {tool_call_info}"
    t_bbox = draw.textbbox((0, 0), tool_text, font=font_sm)
    t_w = t_bbox[2] - t_bbox[0] + 24
    t_h = 30
    t_box = [(35, curr_y), (35 + t_w, curr_y + t_h)]
    draw.rounded_rectangle(t_box, radius=6, fill=tool_badge_bg, outline=tool_badge_border, width=1)
    draw.text((47, curr_y + 7), tool_text, fill=(25, 103, 210), font=font_sm)

    curr_y += t_h + 16

    # 3. Agent Response (left-aligned)
    resp_w = width - 140
    resp_h = len(resp_lines) * line_h + 30
    resp_box = [(35, curr_y), (35 + resp_w, curr_y + resp_h)]
    draw.rounded_rectangle(resp_box, radius=12, fill=agent_bubble_bg, outline=border_color, width=1)

    text_y = curr_y + 15
    for rline in resp_lines:
        color = text_dark
        f = font_base
        if rline.startswith("**") or rline.endswith(":") or rline.startswith("Temperature"):
            color = (13, 71, 161)
            f = font_bold
        draw.text((55, text_y), rline, fill=color, font=f)
        text_y += line_h

    # Footer input area
    footer_y = height - footer_height
    draw.rectangle([(0, footer_y), (width, height)], fill=(255, 255, 255))
    draw.line([(0, footer_y), (width, footer_y)], fill=border_color, width=1)

    input_box = [(25, footer_y + 12), (width - 100, footer_y + 50)]
    draw.rounded_rectangle(input_box, radius=8, fill=(245, 247, 250), outline=border_color, width=1)
    draw.text((40, footer_y + 22), "Ask weather_agent about weather...", fill=text_muted, font=font_base)

    btn_box = [(width - 85, footer_y + 12), (width - 25, footer_y + 50)]
    draw.rounded_rectangle(btn_box, radius=8, fill=(26, 115, 232))
    draw.text((width - 68, footer_y + 22), "Send", fill=(255, 255, 255), font=font_bold)

    img.save(output_path, "PNG")
    print(f"✅ Saved ADK screenshot to {output_path}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 4:
        render_terminal_screenshot(
            prompt=sys.argv[1],
            output=sys.argv[2],
            output_path=sys.argv[3],
            title=sys.argv[4] if len(sys.argv) > 4 else "Terminal",
        )
