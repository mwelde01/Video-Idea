#!/usr/bin/env python3
"""
Generate an HTML table of AI case study topics and links for Microsoft Teams.

Creates a professional-looking HTML file with:
- Student names
- Positive AI case topics with "View Here" links
- Negative AI case topics with "View Here" links

Usage:
    python generate_case_study_table.py
"""

import html

def parse_data_file(filepath='case_topics_data.txt'):
    """Parse the tab-separated data file"""
    students = []

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Skip header
    for line in lines[1:]:
        if not line.strip():
            continue

        parts = line.strip().split('\t')
        if len(parts) >= 5:
            student = {
                'name': parts[0].strip(),
                'positive_topic': parts[1].strip(),
                'positive_link': parts[2].strip(),
                'negative_topic': parts[3].strip(),
                'negative_link': parts[4].strip()
            }
            students.append(student)

    return students

def generate_html(students, output_file='AI_Case_Studies.html'):
    """Generate HTML table"""

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Week 1 AI Case Studies</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}

        .container {{
            max-width: 1400px;
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
        }}

        .topic {{
            color: #333;
            line-height: 1.4;
            margin-bottom: 8px;
        }}

        .view-link {{
            display: inline-block;
            color: #0078d4;
            text-decoration: none;
            font-weight: 500;
            font-size: 14px;
            padding: 4px 0;
        }}

        .view-link:hover {{
            text-decoration: underline;
            color: #005a9e;
        }}

        .case-column {{
            min-width: 350px;
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
        <h1>Week 1: AI in Business - Case Study Topics</h1>
        <div class="subtitle">Click "View Here" to watch each case study presentation</div>

        <table>
            <thead>
                <tr>
                    <th style="width: 180px;">Student Name</th>
                    <th class="case-column">Positive AI Case</th>
                    <th class="case-column">Negative AI Case</th>
                </tr>
            </thead>
            <tbody>
"""

    # Add rows for each student
    for student in students:
        # Escape HTML in topics
        pos_topic = html.escape(student['positive_topic'])
        neg_topic = html.escape(student['negative_topic'])

        html_content += f"""                <tr>
                    <td class="student-name">{html.escape(student['name'])}</td>
                    <td class="case-column">
                        <div class="topic">{pos_topic}</div>
                        <a href="{student['positive_link']}" class="view-link" target="_blank">▶ View Here</a>
                    </td>
                    <td class="case-column">
                        <div class="topic">{neg_topic}</div>
                        <a href="{student['negative_link']}" class="view-link" target="_blank">▶ View Here</a>
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
    print("AI CASE STUDY TABLE GENERATOR")
    print("="*80)
    print()

    # Parse the data
    print("Reading case_topics_data.txt...")
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
    print("1. Open AI_Case_Studies.html in your browser to preview")
    print("2. In Microsoft Teams:")
    print("   - Create a new post")
    print("   - Copy and paste the HTML content")
    print("   OR")
    print("   - Attach the HTML file to your post")
    print("   OR")
    print("   - Host it on SharePoint and share the link")
    print()

if __name__ == "__main__":
    main()
