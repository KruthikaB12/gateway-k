import csv
import sqlite3
import sys

def import_students(csv_file):
    """Import students from CSV file into database"""
    
    conn = sqlite3.connect('gateway.db')
    c = conn.cursor()
    
    added = 0
    updated = 0
    errors = []
    
    try:
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            
            for row_num, row in enumerate(reader, start=2):
                try:
                    email = row['email'].strip().lower()
                    name = row['name'].strip()
                    roll_number = row['roll_number'].strip().upper()
                    class_name = row['class'].strip()
                    department = row['department'].strip()
                    parent_email = row['parent_email'].strip().lower()
                    
                    # Validate required fields
                    if not all([email, name, roll_number, parent_email]):
                        errors.append(f"Row {row_num}: Missing required fields")
                        continue
                    
                    # Check if student exists
                    c.execute('SELECT id FROM users WHERE email = ?', (email,))
                    existing = c.fetchone()
                    
                    if existing:
                        # Update existing student
                        c.execute('''
                            UPDATE users 
                            SET name = ?, roll_number = ?, class = ?, department = ?, parent_email = ?
                            WHERE email = ?
                        ''', (name, roll_number, class_name, department, parent_email, email))
                        updated += 1
                    else:
                        # Insert new student
                        c.execute('''
                            INSERT INTO users (role, email, name, roll_number, class, department, parent_email, parent_phone)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        ''', ('student', email, name, roll_number, class_name, department, parent_email, '0000000000'))
                        added += 1
                    
                except Exception as e:
                    errors.append(f"Row {row_num}: {str(e)}")
        
        conn.commit()
        
        # Print summary
        print("\n" + "="*60)
        print("IMPORT SUMMARY")
        print("="*60)
        print(f"✅ Added: {added} students")
        print(f"🔄 Updated: {updated} students")
        
        if errors:
            print(f"\n❌ Errors: {len(errors)}")
            for error in errors[:10]:  # Show first 10 errors
                print(f"  - {error}")
            if len(errors) > 10:
                print(f"  ... and {len(errors) - 10} more errors")
        
        print("\n" + "="*60)
        
        # Show sample of imported students
        c.execute('SELECT email, name, roll_number, class, parent_email FROM users WHERE role = "student" LIMIT 5')
        students = c.fetchall()
        
        if students:
            print("\nSAMPLE IMPORTED STUDENTS:")
            print("-"*60)
            for student in students:
                print(f"Email: {student[0]}")
                print(f"Name: {student[1]}, Roll: {student[2]}, Class: {student[3]}")
                print(f"Parent: {student[4]}")
                print()
        
    except FileNotFoundError:
        print(f"❌ Error: File '{csv_file}' not found")
        sys.exit(1)
    except KeyError as e:
        print(f"❌ Error: Missing column {e} in CSV file")
        print("\nRequired columns: email, name, roll_number, class, department, parent_email")
        sys.exit(1)
    finally:
        conn.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 import_students.py <csv_file>")
        print("\nCSV Format:")
        print("email,name,roll_number,class,department,parent_email")
        print("student1@bvrithyderabad.edu.in,John Doe,21A01,CS-A,CSE,parent1@gmail.com")
        sys.exit(1)
    
    import_students(sys.argv[1])
