#!/usr/bin/env python3
"""Generate standalone HTML files for each AI Scenario Planning tab."""

import base64
import openpyxl

# Scenario metadata
SCENARIOS = {
    "Scenario A": {
        "title": "Scenario A: Fast Takeoff / AGI Acceleration",
        "subtitle": "AI progress is accelerating rapidly toward superintelligence",
        "color_primary": "#B8860B",
        "color_dark": "#8B6914",
        "color_light": "#FFF8DC",
        "color_accent": "#DAA520",
        "image_b64_file": "scenario_a_b64.txt",
        "image_alt": "Fast Takeoff / AGI Acceleration",
    },
    "Scenario B": {
        "title": "Scenario B: Slow and Steady Progress",
        "subtitle": "AI advances gradually with real-world integration challenges",
        "color_primary": "#4A6741",
        "color_dark": "#2E4028",
        "color_light": "#EEF4EC",
        "color_accent": "#6B8F61",
        "image_b64_file": "scenario_b_b64.txt",
        "image_alt": "Slow and Steady Progress",
    },
    "Scenario C": {
        "title": "Scenario C: AI Plateau / AI Winter",
        "subtitle": "Hype fades as AI hits technical and economic limits",
        "color_primary": "#4A6B8A",
        "color_dark": "#2C4A6B",
        "color_light": "#E8F0F8",
        "color_accent": "#6A9BC3",
        "image_b64_file": "scenario_c_b64.txt",
        "image_alt": "AI Plateau / Winter",
    },
    "Scenario D": {
        "title": "Scenario D: Regulatory & Social Backlash",
        "subtitle": "Public opposition and regulation reshape the AI landscape",
        "color_primary": "#8B2500",
        "color_dark": "#5C1A00",
        "color_light": "#FDE8E0",
        "color_accent": "#CD3700",
        "image_b64_file": "scenario_d_b64.txt",
        "image_alt": "Regulatory & Social Backlash",
    },
}

OUTPUT_FILES = {
    "Scenario A": "Scenario_A_Fast_Takeoff.html",
    "Scenario B": "Scenario_B_Slow_Steady.html",
    "Scenario C": "Scenario_C_AI_Winter.html",
    "Scenario D": "Scenario_D_Regulatory_Backlash.html",
}


def load_image_b64(filename):
    with open(f"/home/user/Video-Idea/{filename}") as f:
        return f.read().strip()


def build_article_card(index, article, brief, article_link, notebook_link, color_primary, color_accent):
    """Build an HTML card for a single article."""
    # Clean up non-breaking spaces
    if brief:
        brief = brief.replace('\xa0', ' ')
    if article:
        article = article.replace('\xa0', ' ')

    return f"""
    <div class="article-card">
      <div class="article-number">{index}</div>
      <div class="article-content">
        <h3 class="article-title">{article}</h3>
        <p class="article-brief">{brief}</p>
        <div class="article-links">
          <a href="{article_link}" target="_top" class="btn btn-article">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
            Read Article
          </a>
          <a href="{notebook_link}" target="_top" class="btn btn-notebook">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>
            NotebookLM Summary
          </a>
        </div>
      </div>
    </div>"""


def generate_html(sheet_name, meta, articles_data):
    image_b64 = load_image_b64(meta["image_b64_file"])

    cards_html = ""
    for i, (article, brief, article_link, notebook_link) in enumerate(articles_data, 1):
        cards_html += build_article_card(
            i, article, brief, article_link, notebook_link,
            meta["color_primary"], meta["color_accent"]
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{meta['title']}</title>
  <style>
    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }}

    body {{
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background-color: #f5f5f5;
      color: #333;
      line-height: 1.6;
    }}

    .hero {{
      position: relative;
      width: 100%;
      max-height: 400px;
      overflow: hidden;
      background: {meta['color_dark']};
    }}

    .hero img {{
      width: 100%;
      height: auto;
      display: block;
      opacity: 0.85;
    }}

    .hero-overlay {{
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: linear-gradient(transparent, rgba(0,0,0,0.7));
      padding: 40px 30px 20px;
    }}

    .hero-overlay h1 {{
      color: #fff;
      font-size: 1.8rem;
      font-weight: 700;
      text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
    }}

    .hero-overlay p {{
      color: rgba(255,255,255,0.9);
      font-size: 1rem;
      margin-top: 4px;
      text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }}

    .container {{
      max-width: 900px;
      margin: 0 auto;
      padding: 30px 20px 50px;
    }}

    .section-header {{
      text-align: center;
      margin-bottom: 30px;
    }}

    .section-header h2 {{
      font-size: 1.4rem;
      color: {meta['color_dark']};
      border-bottom: 3px solid {meta['color_accent']};
      display: inline-block;
      padding-bottom: 6px;
    }}

    .article-card {{
      background: #fff;
      border-radius: 10px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.08);
      margin-bottom: 20px;
      display: flex;
      overflow: hidden;
      transition: box-shadow 0.2s ease, transform 0.2s ease;
    }}

    .article-card:hover {{
      box-shadow: 0 4px 16px rgba(0,0,0,0.14);
      transform: translateY(-2px);
    }}

    .article-number {{
      background: {meta['color_primary']};
      color: #fff;
      min-width: 50px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.4rem;
      font-weight: 700;
    }}

    .article-content {{
      padding: 18px 22px;
      flex: 1;
    }}

    .article-title {{
      font-size: 1.1rem;
      color: {meta['color_dark']};
      margin-bottom: 8px;
    }}

    .article-brief {{
      font-size: 0.92rem;
      color: #555;
      margin-bottom: 14px;
      line-height: 1.55;
    }}

    .article-links {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }}

    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 8px 16px;
      border-radius: 6px;
      text-decoration: none;
      font-size: 0.85rem;
      font-weight: 600;
      transition: background 0.2s ease, transform 0.1s ease;
    }}

    .btn:hover {{
      transform: translateY(-1px);
    }}

    .btn-article {{
      background: {meta['color_primary']};
      color: #fff;
    }}

    .btn-article:hover {{
      background: {meta['color_dark']};
    }}

    .btn-notebook {{
      background: {meta['color_light']};
      color: {meta['color_dark']};
      border: 1.5px solid {meta['color_accent']};
    }}

    .btn-notebook:hover {{
      background: {meta['color_accent']};
      color: #fff;
    }}

    .footer {{
      text-align: center;
      padding: 20px;
      color: #999;
      font-size: 0.8rem;
      border-top: 1px solid #e0e0e0;
      margin-top: 20px;
    }}

    @media (max-width: 600px) {{
      .hero-overlay h1 {{
        font-size: 1.3rem;
      }}
      .article-card {{
        flex-direction: column;
      }}
      .article-number {{
        min-width: auto;
        padding: 8px;
        font-size: 1rem;
      }}
      .article-links {{
        flex-direction: column;
      }}
      .btn {{
        justify-content: center;
      }}
    }}
  </style>
</head>
<body>

  <div class="hero">
    <img src="data:image/jpeg;base64,{image_b64}" alt="{meta['image_alt']}">
    <div class="hero-overlay">
      <h1>{meta['title']}</h1>
      <p>{meta['subtitle']}</p>
    </div>
  </div>

  <div class="container">
    <div class="section-header">
      <h2>Articles &amp; Resources</h2>
    </div>

{cards_html}

    <div class="footer">
      AI Scenario Planning Exercise &mdash; University of Louisville
    </div>
  </div>

</body>
</html>"""


def main():
    wb = openpyxl.load_workbook("/home/user/Video-Idea/Scenario Planning.xlsx")

    for sheet_name, meta in SCENARIOS.items():
        ws = wb[sheet_name]
        articles_data = []
        for row in ws.iter_rows(min_row=2, values_only=True):
            article, brief, article_link, notebook_link = row
            if article is None:
                continue
            articles_data.append((article, brief, article_link, notebook_link))

        html = generate_html(sheet_name, meta, articles_data)
        output_path = f"/home/user/Video-Idea/{OUTPUT_FILES[sheet_name]}"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Created: {OUTPUT_FILES[sheet_name]} ({len(articles_data)} articles)")

    print("\nAll 4 HTML files generated successfully!")


if __name__ == "__main__":
    main()
