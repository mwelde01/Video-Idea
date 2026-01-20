# How to Reorganize Transcripts by Case Type

This script creates a second version of your transcripts organized by case type (all Positive cases together, all Negative cases together).

## Quick Start

```cmd
python reorganize_by_case_type.py
```

That's it!

## What It Does

**Input:** `compiled_transcripts.md` (organized by student name)

**Output:** `transcripts_by_case_type.md` (organized by case type)

The new file will have:
1. **Positive AI Cases Section** - All positive case transcripts grouped together
2. **Negative AI Cases Section** - All negative case transcripts grouped together

Each section lists students alphabetically with their transcript.

## Workflow

### Adding More Transcripts

When you need to add more video transcripts:

1. **Create manual transcript files** (e.g., `Student_Name_Positive_manual.txt`)
2. **Run the manual transcript processor:**
   ```cmd
   python add_manual_transcripts.py
   ```
   This updates `compiled_transcripts.md`

3. **Regenerate the case-type version:**
   ```cmd
   python reorganize_by_case_type.py
   ```
   This creates a fresh `transcripts_by_case_type.md` with all transcripts

### Your Two Files

**`compiled_transcripts.md`** (Master file)
- Organized by student name
- Update this with `add_manual_transcripts.py`
- Keep this as your primary/master document

**`transcripts_by_case_type.md`** (Alternative view)
- Organized by case type (Positive/Negative)
- Generate anytime with `reorganize_by_case_type.py`
- Recreate this whenever you update the master file

## Example Output Structure

```markdown
# AI Case Video Transcripts - Organized by Case Type

## Table of Contents
- Positive AI Cases
- Negative AI Cases

---

# Positive AI Cases

## Student Name 1
[Their positive case transcript...]

## Student Name 2
[Their positive case transcript...]

---

# Negative AI Cases

## Student Name 1
[Their negative case transcript...]

## Student Name 2
[Their negative case transcript...]
```

## Notes

- The script automatically excludes error messages and missing transcripts
- Only actual transcript content is included in the output
- Students are listed alphabetically within each section
- You can run this script as many times as you want - it always reads from `compiled_transcripts.md`

## Full Workflow Example

```cmd
# 1. Add new manual transcripts
python add_manual_transcripts.py

# 2. Regenerate the case-type organized version
python reorganize_by_case_type.py

# Both files are now updated!
```
