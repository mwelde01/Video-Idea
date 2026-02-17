#!/usr/bin/env python3
"""Generate a single HTML page with student scenario videos grouped by scenario and year."""

import openpyxl

SCENARIO_META = {
    "Scenario A": {
        "key": "scenario_a",
        "title": "Scenario A: Fast Takeoff / AGI Acceleration",
        "color_primary": "#B8860B",
        "color_dark": "#8B6914",
        "color_light": "#FFF8DC",
        "color_accent": "#DAA520",
        "image_alt": "Fast Takeoff / AGI Acceleration",
    },
    "Scenario B": {
        "key": "scenario_b",
        "title": "Scenario B: Slow and Steady Progress",
        "color_primary": "#4A6741",
        "color_dark": "#2E4028",
        "color_light": "#EEF4EC",
        "color_accent": "#6B8F61",
        "image_alt": "Slow and Steady Progress",
    },
    "Scenario C": {
        "key": "scenario_c",
        "title": "Scenario C: AI Plateau / AI Winter",
        "color_primary": "#4A6B8A",
        "color_dark": "#2C4A6B",
        "color_light": "#E8F0F8",
        "color_accent": "#6A9BC3",
        "image_alt": "AI Plateau / Winter",
    },
    "Scenario D": {
        "key": "scenario_d",
        "title": "Scenario D: Regulatory & Social Backlash",
        "color_primary": "#8B2500",
        "color_dark": "#5C1A00",
        "color_light": "#FDE8E0",
        "color_accent": "#CD3700",
        "image_alt": "Regulatory & Social Backlash",
    },
}

# Map spreadsheet scenario names to our keys
SCENARIO_MAP = {
    "Scenario A: Fast Takeoff / AGI Acceleration": "Scenario A",
    "Scenario B: Slow and Steady Progress": "Scenario B",
    "Scenario C: Plateau / AI Winter": "Scenario C",
    "Scenario D: Regulatory and Social Backlash": "Scenario D",
}


# Name corrections
NAME_OVERRIDES = {
    "Jagan Lakshmanan": "Jaganathan Lakshmanan",
}


def load_image_b64(key):
    with open(f"/home/user/Video-Idea/{key}_b64.txt") as f:
        return f.read().strip()


def build_student_card(name, year, link, color_primary, color_dark):
    link = link.strip()
    return f"""
          <a href="{link}" target="_blank" rel="noopener" class="student-card">
            <div class="student-avatar" style="background: {color_primary};">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            </div>
            <div class="student-info">
              <span class="student-name">{name}</span>
              <span class="student-meta">Year {year} Outlook</span>
            </div>
            <div class="play-btn" style="background: {color_primary};">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="#fff" stroke="none"><polygon points="5 3 19 12 5 21 5 3"/></svg>
            </div>
          </a>"""


def build_scenario_section(scenario_key, meta, students_by_year, image_b64):
    year_sections = ""
    for year in sorted(students_by_year.keys()):
        label = f"{year} — Looking 5 Years Ahead" if year == "2031" else f"{year} — Looking 10 Years Ahead"
        student_cards = ""
        for name, link in sorted(students_by_year[year], key=lambda x: x[0]):
            student_cards += build_student_card(name, year, link, meta["color_primary"], meta["color_dark"])

        year_sections += f"""
        <div class="year-group">
          <h3 class="year-label" style="color: {meta['color_dark']}; border-left: 4px solid {meta['color_accent']};">{label}</h3>
          <div class="student-grid">
{student_cards}
          </div>
        </div>"""

    return f"""
    <section class="scenario-section" id="{meta['key']}">
      <div class="scenario-hero">
        <img src="data:image/jpeg;base64,{image_b64}" alt="{meta['image_alt']}">
        <div class="scenario-hero-overlay" style="background: linear-gradient(transparent, {meta['color_dark']}ee);">
          <h2>{meta['title']}</h2>
        </div>
      </div>
      <div class="scenario-students">
{year_sections}
      </div>
    </section>"""


def main():
    wb = openpyxl.load_workbook("/home/user/Video-Idea/Week_5_ Links.xlsx")
    ws = wb["Sheet1"]

    # Organize students: { "Scenario A": { "2031": [(name, link), ...], "2036": [...] } }
    data = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        name, year, scenario, link = row
        if name is None:
            continue
        name = NAME_OVERRIDES.get(name, name)
        scenario_key = SCENARIO_MAP.get(scenario)
        if scenario_key is None:
            print(f"Warning: Unknown scenario '{scenario}' for {name}")
            continue
        year = str(year).strip()
        if scenario_key not in data:
            data[scenario_key] = {}
        if year not in data[scenario_key]:
            data[scenario_key][year] = []
        data[scenario_key][year].append((name, link))

    # Load images
    images = {}
    for sc_key, meta in SCENARIO_META.items():
        images[sc_key] = load_image_b64(meta["key"])

    # Build scenario sections
    scenario_sections = ""
    nav_links = ""
    for sc_key in ["Scenario A", "Scenario B", "Scenario C", "Scenario D"]:
        meta = SCENARIO_META[sc_key]
        students_by_year = data.get(sc_key, {})
        if not students_by_year:
            continue
        total = sum(len(v) for v in students_by_year.values())
        scenario_sections += build_scenario_section(sc_key, meta, students_by_year, images[sc_key])
        nav_links += f"""
        <a href="#{meta['key']}" class="nav-pill" style="background: {meta['color_primary']};">{meta['title'].split(':')[0].strip()} <span class="nav-count">{total}</span></a>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI Scenario Planning — Student Video Presentations</title>
  <style>
    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }}

    body {{
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: #f0f2f5;
      color: #333;
      line-height: 1.6;
    }}

    .page-header {{
      background: #1a1a2e;
      color: #fff;
      text-align: center;
      padding: 40px 20px 30px;
    }}

    .page-header h1 {{
      font-size: 2rem;
      font-weight: 700;
      margin-bottom: 6px;
    }}

    .page-header p {{
      color: rgba(255,255,255,0.7);
      font-size: 1rem;
    }}

    .nav-bar {{
      background: #16213e;
      padding: 14px 20px;
      display: flex;
      justify-content: center;
      gap: 10px;
      flex-wrap: wrap;
      position: sticky;
      top: 0;
      z-index: 100;
      box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }}

    .nav-pill {{
      color: #fff;
      text-decoration: none;
      padding: 8px 18px;
      border-radius: 20px;
      font-size: 0.85rem;
      font-weight: 600;
      transition: opacity 0.2s ease, transform 0.1s ease;
    }}

    .nav-pill:hover {{
      opacity: 0.85;
      transform: translateY(-1px);
    }}

    .nav-count {{
      background: rgba(255,255,255,0.25);
      padding: 2px 8px;
      border-radius: 10px;
      font-size: 0.75rem;
      margin-left: 6px;
    }}

    .container {{
      max-width: 950px;
      margin: 0 auto;
      padding: 0 20px 50px;
    }}

    .scenario-section {{
      margin-top: 35px;
      background: #fff;
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    }}

    .scenario-hero {{
      position: relative;
      width: 100%;
      max-height: 300px;
      overflow: hidden;
    }}

    .scenario-hero img {{
      width: 100%;
      height: auto;
      display: block;
    }}

    .scenario-hero-overlay {{
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      padding: 50px 25px 18px;
    }}

    .scenario-hero-overlay h2 {{
      color: #fff;
      font-size: 1.5rem;
      font-weight: 700;
      text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
    }}

    .scenario-students {{
      padding: 20px 25px 25px;
    }}

    .year-group {{
      margin-bottom: 22px;
    }}

    .year-group:last-child {{
      margin-bottom: 0;
    }}

    .year-label {{
      font-size: 1rem;
      font-weight: 600;
      padding: 6px 0 6px 14px;
      margin-bottom: 12px;
    }}

    .student-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 10px;
    }}

    .student-card {{
      display: flex;
      align-items: center;
      background: #f8f9fa;
      border-radius: 8px;
      padding: 12px 14px;
      text-decoration: none;
      color: #333;
      transition: background 0.2s ease, box-shadow 0.2s ease, transform 0.15s ease;
      gap: 12px;
    }}

    .student-card:hover {{
      background: #eef0f3;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      transform: translateY(-1px);
    }}

    .student-avatar {{
      width: 38px;
      height: 38px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }}

    .student-info {{
      flex: 1;
      display: flex;
      flex-direction: column;
    }}

    .student-name {{
      font-weight: 600;
      font-size: 0.95rem;
      color: #222;
    }}

    .student-meta {{
      font-size: 0.78rem;
      color: #888;
    }}

    .play-btn {{
      width: 32px;
      height: 32px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      transition: transform 0.15s ease;
    }}

    .student-card:hover .play-btn {{
      transform: scale(1.1);
    }}

    .footer {{
      text-align: center;
      padding: 25px;
      color: #999;
      font-size: 0.8rem;
    }}

    @media (max-width: 600px) {{
      .page-header h1 {{
        font-size: 1.4rem;
      }}
      .nav-pill {{
        font-size: 0.75rem;
        padding: 6px 12px;
      }}
      .student-grid {{
        grid-template-columns: 1fr;
      }}
      .scenario-hero-overlay h2 {{
        font-size: 1.2rem;
      }}
    }}
  </style>
</head>
<body>

  <div class="page-header">
    <h1>AI Scenario Planning</h1>
    <p>Student Video Presentations</p>
  </div>

  <div class="nav-bar">
{nav_links}
  </div>

  <div class="container">
{scenario_sections}

    <div class="footer">
      AI Scenario Planning Exercise &mdash; University of Louisville
    </div>
  </div>

</body>
</html>"""

    output_path = "/home/user/Video-Idea/Student_Scenario_Videos.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    # Print summary
    print("Created: Student_Scenario_Videos.html\n")
    for sc_key in ["Scenario A", "Scenario B", "Scenario C", "Scenario D"]:
        if sc_key in data:
            total = sum(len(v) for v in data[sc_key].values())
            years = ", ".join(f"{y} ({len(v)})" for y, v in sorted(data[sc_key].items()))
            print(f"  {sc_key}: {total} students — {years}")


if __name__ == "__main__":
    main()
