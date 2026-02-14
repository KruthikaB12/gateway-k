# Student CSV Import Guide

## Quick Start

1. **Prepare your CSV file** with student data
2. **Run the import script:**
   ```bash
   python3 import_students.py students.csv
   ```

## CSV Format

Your CSV file must have these columns (in any order):

| Column | Description | Example |
|--------|-------------|---------|
| email | Student college email | 25wh1a05d1@bvrithyderabad.edu.in |
| name | Full name | NAGA JAHNAVI BANDARUPALLI |
| roll_number | Roll number | 25WH1A05D1 |
| class | Class section | CS-A |
| department | Department | CSE |
| parent_email | Parent's email | parent@gmail.com |

## Example CSV

See `students_sample.csv` for an example.

```csv
email,name,roll_number,class,department,parent_email
25wh1a05d1@bvrithyderabad.edu.in,NAGA JAHNAVI BANDARUPALLI,25WH1A05D1,CS-A,CSE,watermelon37453@gmail.com
student2@bvrithyderabad.edu.in,Sample Student 2,25WH1A05D2,CS-A,CSE,parent2@gmail.com
```

## How to Create CSV

### Option 1: Excel/Google Sheets
1. Create a spreadsheet with the columns above
2. Fill in student data
3. Save as CSV (File → Download → CSV)

### Option 2: Text Editor
1. Copy the header line from `students_sample.csv`
2. Add one line per student
3. Save with `.csv` extension

## Running the Import

```bash
# Import students
python3 import_students.py students.csv

# The script will:
# - Add new students
# - Update existing students
# - Show summary of changes
# - Report any errors
```

## What Happens

- **New students**: Added to database
- **Existing students**: Updated with new information
- **Errors**: Displayed at the end (missing fields, invalid data)

## After Import

Students can now:
1. Login with their college email via Google OAuth
2. Submit permission requests
3. Parents receive approval emails

## Updating Students

To update student information:
1. Edit your CSV file
2. Run the import script again
3. Existing students will be updated

## Tips

- ✅ Use college email domain: @bvrithyderabad.edu.in
- ✅ Roll numbers are case-insensitive (converted to uppercase)
- ✅ Parent emails must be valid email addresses
- ✅ All fields are required
- ✅ You can import the same file multiple times (safe)

## Troubleshooting

**"Missing column" error:**
- Check your CSV has all required columns
- Column names must match exactly (case-sensitive)

**"Missing required fields" error:**
- Some rows have empty values
- Check the row number in the error message

**"Database is locked" error:**
- Stop the backend server first
- Run the import
- Restart the server

## Example: Bulk Import

```bash
# Stop server
lsof -ti:3000 | xargs kill -9

# Import students
python3 import_students.py all_students.csv

# Restart server
python3 server.py
```
