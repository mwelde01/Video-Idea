#!/usr/bin/env python3
"""
Generate an HTML table of Week 2 AI Tool Use for Microsoft Teams.

Creates a professional-looking HTML file with:
- Student names
- AI tools used
- What they did with the tools
- "View Here" links to videos

Usage:
    python generate_week2_ai_tools_table.py
"""

import html

def parse_data_file(filepath='week2_ai_tools_data.txt'):
    """Parse the tab-separated data file"""
    students = []

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Skip header
    for line in lines[1:]:
        if not line.strip():
            continue

        parts = line.strip().split('\t')
        if len(parts) >= 4:
            student = {
                'name': parts[0].strip(),
                'video_url': parts[1].strip(),
                'tools_used': parts[2].strip(),
                'what_they_did': parts[3].strip()
            }
            students.append(student)

    return students

def generate_html(students, output_file='AI_Tools_Week2.html'):
    """Generate HTML table"""

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Week 2: AI Tool Use</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}

        .container {{
            max-width: 1600px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        h1 {{
            color: #464775;
            text-align: center;
            margin-bottom: 10px;
            font-size: 28px;
        }}

        .subtitle {{
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 16px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}

        th {{
            background-color: #464775;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            font-size: 14px;
            border: 1px solid #ddd;
        }}

        td {{
            padding: 12px 15px;
            border: 1px solid #ddd;
            vertical-align: top;
        }}

        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}

        tr:hover {{
            background-color: #f0f0f0;
        }}

        .student-name {{
            font-weight: 600;
            color: #333;
            white-space: nowrap;
        }}

        .tools-used {{
            color: #0078d4;
            font-weight: 500;
        }}

        .description {{
            color: #333;
            line-height: 1.5;
        }}

        .view-link {{
            display: inline-block;
            color: #0078d4;
            text-decoration: none;
            font-weight: 500;
            font-size: 14px;
            padding: 4px 8px;
            border: 1px solid #0078d4;
            border-radius: 4px;
            transition: all 0.2s;
        }}

        .view-link:hover {{
            background-color: #0078d4;
            color: white;
        }}

        .name-column {{
            width: 150px;
        }}

        .tools-column {{
            width: 220px;
        }}

        .description-column {{
            min-width: 400px;
        }}

        .video-column {{
            width: 100px;
            text-align: center;
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 15px;
            }}

            table {{
                font-size: 13px;
            }}

            th, td {{
                padding: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Week 2: AI Tool Use</h1>
        <div class="subtitle">Student presentations on practical AI tool applications</div>

        <table>
            <thead>
                <tr>
                    <th class="name-column">Student</th>
                    <th class="tools-column">AI Tool(s) Used</th>
                    <th class="description-column">What They Did</th>
                    <th class="video-column">Video</th>
                </tr>
            </thead>
            <tbody>
"""

    # Add rows for each student (sorted alphabetically)
    for student in sorted(students, key=lambda x: x['name']):
        # Escape HTML in content
        tools = html.escape(student['tools_used'])
        description = html.escape(student['what_they_did'])

        html_content += f"""                <tr>
                    <td class="student-name">{html.escape(student['name'])}</td>
                    <td class="tools-used">{tools}</td>
                    <td class="description">{description}</td>
                    <td class="video-column">
                        <a href="{student['video_url']}" class="view-link" target="_blank">▶ View</a>
                    </td>
                </tr>
"""

    html_content += """            </tbody>
        </table>
    </div>
</body>
</html>
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return output_file

def main():
    print("="*80)
    print("WEEK 2 AI TOOL USE TABLE GENERATOR")
    print("="*80)
    print()

    # Parse the data
    print("Reading week2_ai_tools_data.txt...")
    students = parse_data_file()
    print(f"Found {len(students)} students\n")

    # Generate HTML
    print("Generating HTML table...")
    output_file = generate_html(students)

    print(f"\n{'='*80}")
    print("SUCCESS!")
    print("="*80)
    print(f"✓ Created: {output_file}")
    print(f"✓ Total students: {len(students)}")
    print()
    print("Next steps:")
    print("1. Open AI_Tools_Week2.html in your browser to preview")
    print("2. For Microsoft Teams:")
    print("   - Attach the HTML file to your post")
    print("   OR")
    print("   - Upload to SharePoint and share the link")
    print()
    print("Note: The table shows:")
    print("  - Student names")
    print("  - AI tools they used")
    print("  - What they accomplished")
    print("  - Clickable 'View' button for each video")
    print()

if __name__ == "__main__":
    main()
