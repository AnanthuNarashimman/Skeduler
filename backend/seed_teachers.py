"""
Seed script to create teacher accounts from staff data
Generates usernames and passwords for all teachers
"""
import json
import csv
import secrets
import string
from database import init_db, create_teacher
from auth import hash_password


def generate_username(name):
    """
    Generate username from teacher name
    Format: firstname.lastname (lowercase, no spaces)
    """
    # Remove titles and clean name
    name = name.replace("Mr.", "").replace("Mrs.", "").replace("Ms.", "").replace("Dr.", "").strip()

    # Split into parts and take first and last
    parts = [p.strip() for p in name.split() if p.strip()]

    if len(parts) >= 2:
        username = f"{parts[0].lower()}.{parts[-1].lower()}"
    elif len(parts) == 1:
        username = parts[0].lower()
    else:
        username = "teacher"

    return username


def generate_password(length=8):
    """Generate a random password"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def seed_teachers():
    """Create teacher accounts from data.json"""
    print("=" * 80)
    print("SEEDING TEACHER ACCOUNTS")
    print("=" * 80)

    # Initialize database
    init_db()

    # Load staff data
    with open('data.json', 'r') as f:
        data = json.load(f)

    staff_list = data['staff']
    credentials = []

    print(f"\nCreating accounts for {len(staff_list)} staff members...\n")

    for staff_name in staff_list:
        # Skip generic entries
        if staff_name in ['Other Faculty', 'HOD', 'Mentors']:
            print(f"Skipping: {staff_name} (generic entry)")
            continue

        # Generate credentials
        username = generate_username(staff_name)
        password = generate_password()
        password_hash = hash_password(password)

        # Create teacher account
        teacher_id = create_teacher(
            name=staff_name,
            username=username,
            password_hash=password_hash,
            email=f"{username}@skeduler.edu",  # Generic email
            department="CSE"
        )

        if teacher_id:
            print(f"✓ Created: {staff_name:30s} | Username: {username:20s} | Password: {password}")
            credentials.append({
                'name': staff_name,
                'username': username,
                'password': password,
                'email': f"{username}@skeduler.edu"
            })
        else:
            print(f"✗ Failed: {staff_name} (username already exists)")

    # Save credentials to CSV file
    csv_filename = 'teacher_credentials.csv'
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['name', 'username', 'password', 'email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for cred in credentials:
            writer.writerow(cred)

    print("\n" + "=" * 80)
    print(f"✓ Successfully created {len(credentials)} teacher accounts")
    print(f"✓ Credentials saved to: {csv_filename}")
    print("=" * 80)

    return credentials


if __name__ == '__main__':
    seed_teachers()
