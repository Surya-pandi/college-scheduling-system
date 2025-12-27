#!/usr/bin/env python3
"""
Initialize the College Management System with an admin account
Run this once after first setup: python setup_admin.py
"""

from app import app, db, Admin
import sys

def create_admin():
    """Create the initial admin account"""
    try:
        with app.app_context():
            # Create tables
            db.create_all()
            print("✓ Database tables created/verified")
            
            # Check if admin exists
            existing_admin = Admin.query.filter_by(email="admin@college.edu").first()
            if existing_admin:
                print("\n⚠️  Admin account already exists!")
                print(f"Email: admin@college.edu")
                print("\nTo reset:")
                print("1. Delete college_management.db")
                print("2. Run this script again")
                return False
            
            # Create admin account
            admin = Admin(
                email="admin@college.edu",
                name="System Administrator"
            )
            admin.set_password("admin123")
            
            db.session.add(admin)
            db.session.commit()
            
            print("\n" + "="*50)
            print("✓ ADMIN ACCOUNT CREATED SUCCESSFULLY")
            print("="*50)
            print(f"\nEmail:    admin@college.edu")
            print(f"Password: admin123")
            print("\n" + "="*50)
            print("IMPORTANT SECURITY NOTES:")
            print("="*50)
            print("\n1. CHANGE THE PASSWORD IMMEDIATELY after first login")
            print("2. Don't share default credentials")
            print("3. Use strong passwords for all accounts")
            print("\nNext Steps:")
            print("-" * 50)
            print("1. Start the server: python app.py")
            print("2. Open http://localhost:5000")
            print("3. Click 'Admin Login'")
            print("4. Enter credentials above")
            print("5. Change password immediately")
            print("6. Add staff members and timetable entries")
            print("\n" + "="*50 + "\n")
            
            return True
            
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        print("\nTroubleshooting:")
        print("- Make sure all dependencies are installed: pip install -r requirements.txt")
        print("- Make sure you're in the correct directory")
        print("- Delete college_management.db and try again")
        return False

def main():
    print("\n" + "="*50)
    print("College Management System - Setup")
    print("="*50 + "\n")
    
    success = create_admin()
    
    if success:
        print("Setup complete! You can now start the application.")
        sys.exit(0)
    else:
        print("Setup failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
