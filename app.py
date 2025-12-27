from flask import Flask, request, jsonify, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, timedelta
import os
import json
from dateutil.parser import parse as parse_date

# Initialize Flask app with static folder configuration
app = Flask(__name__, static_folder='public', static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///college_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)

db = SQLAlchemy(app)
CORS(app, supports_credentials=True)

# Database Models
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    position = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(50), unique=True, nullable=False)
    room_name = db.Column(db.String(200), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    floor = db.Column(db.String(20), nullable=True)
    building = db.Column(db.String(100), nullable=True)
    facilities = db.Column(db.Text, nullable=True)  # e.g., "Projector, AC, Whiteboard"
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'room_number': self.room_number,
            'room_name': self.room_name,
            'capacity': self.capacity,
            'floor': self.floor,
            'building': self.building,
            'facilities': self.facilities,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class Timetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    course_code = db.Column(db.String(50), nullable=False)
    course_name = db.Column(db.String(200), nullable=False)
    day = db.Column(db.String(20), nullable=False)  # Monday, Tuesday, etc.
    time_slot = db.Column(db.String(50), nullable=False)  # 09:00-10:30
    room = db.Column(db.String(50), nullable=False)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=True)  # Link to classroom
    batch = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    staff = db.relationship('Staff', backref='timetable_entries')
    classroom = db.relationship('Classroom', backref='timetable_entries')  # Classroom relationship

class Leave(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    leave_date = db.Column(db.Date, nullable=False)
    leave_type = db.Column(db.String(50), nullable=False)  # sick, casual, emergency
    reason = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_by = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=True)
    staff = db.relationship('Staff', backref='leave_requests')
    admin = db.relationship('Admin', backref='leave_approvals')

class ClassRescheduling(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_timetable_id = db.Column(db.Integer, db.ForeignKey('timetable.id'), nullable=False)
    original_staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    leave_id = db.Column(db.Integer, db.ForeignKey('leave.id'), nullable=False)
    reason = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    original_staff = db.relationship('Staff', foreign_keys=[original_staff_id], backref='leave_classes')
    assigned_staff = db.relationship('Staff', foreign_keys=[assigned_staff_id], backref='assigned_classes')
    leave = db.relationship('Leave', backref='rescheduling_records')

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    login_time = db.Column(db.DateTime, nullable=False)
    logout_time = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='present')  # present, absent, leave
    staff = db.relationship('Staff', backref='attendance_records')

class LoginLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=True)
    login_time = db.Column(db.DateTime, default=datetime.utcnow)
    logout_time = db.Column(db.DateTime, nullable=True)
    ip_address = db.Column(db.String(50), nullable=True)
    user_type = db.Column(db.String(20), nullable=False)  # admin, staff
    status = db.Column(db.String(20), default='logged_in')  # logged_in, logged_out
    staff = db.relationship('Staff', backref='login_logs')
    admin = db.relationship('Admin', backref='login_logs')

# Authentication Decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or 'user_type' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_type') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

def staff_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_type') != 'staff':
            return jsonify({'error': 'Staff access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

# Admin Routes
@app.route('/api/admin/register', methods=['POST'])
def admin_register():
    data = request.json
    if Admin.query.filter_by(email=data.get('email')).first():
        return jsonify({'error': 'Admin already exists'}), 400
    
    admin = Admin(
        email=data.get('email'),
        name=data.get('name')
    )
    admin.set_password(data.get('password'))
    db.session.add(admin)
    db.session.commit()
    return jsonify({'message': 'Admin registered successfully'}), 201

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    admin = Admin.query.filter_by(email=data.get('email')).first()
    
    if not admin or not admin.check_password(data.get('password')):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    session.permanent = True
    session['user_id'] = admin.id
    session['user_type'] = 'admin'
    session['name'] = admin.name
    
    # Log the login
    log = LoginLog(
        admin_id=admin.id,
        user_type='admin',
        ip_address=request.remote_addr,
        status='logged_in'
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({'message': 'Login successful', 'user': {'id': admin.id, 'name': admin.name}}), 200

@app.route('/api/admin/logout', methods=['POST'])
@login_required
def admin_logout():
    if session.get('user_type') == 'admin':
        log = LoginLog.query.filter_by(admin_id=session['user_id'], status='logged_in').order_by(LoginLog.login_time.desc()).first()
        if log:
            log.logout_time = datetime.utcnow()
            log.status = 'logged_out'
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

# Staff Routes
@app.route('/api/staff/login', methods=['POST'])
def staff_login():
    data = request.json
    staff = Staff.query.filter_by(email=data.get('email')).first()
    
    if not staff or not staff.check_password(data.get('password')):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    if not staff.is_active:
        return jsonify({'error': 'Staff account is deactivated'}), 403
    
    session.permanent = True
    session['user_id'] = staff.id
    session['user_type'] = 'staff'
    session['name'] = staff.name
    
    # Log the login
    log = LoginLog(
        staff_id=staff.id,
        user_type='staff',
        ip_address=request.remote_addr,
        status='logged_in'
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({'message': 'Login successful', 'user': {'id': staff.id, 'name': staff.name}}), 200

@app.route('/api/staff/logout', methods=['POST'])
@login_required
def staff_logout():
    if session.get('user_type') == 'staff':
        log = LoginLog.query.filter_by(staff_id=session['user_id'], status='logged_in').order_by(LoginLog.login_time.desc()).first()
        if log:
            log.logout_time = datetime.utcnow()
            log.status = 'logged_out'
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/api/session', methods=['GET'])
def get_session():
    if 'user_id' in session:
        return jsonify({'user': {'id': session.get('user_id'), 'name': session.get('name'), 'type': session.get('user_type')}}), 200
    return jsonify({'user': None}), 200

# Admin Dashboard Routes
@app.route('/api/admin/staff', methods=['GET'])
@admin_required
def get_all_staff():
    staff_list = Staff.query.filter_by(is_active=True).all()
    return jsonify({
        'staff': [{'id': s.id, 'employee_id': s.employee_id, 'name': s.name, 'email': s.email, 'department': s.department, 'position': s.position, 'is_active': s.is_active, 'phone': s.phone} for s in staff_list]
    }), 200

@app.route('/api/admin/staff', methods=['POST'])
@admin_required
def add_staff():
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['employee_id', 'email', 'name', 'department', 'position', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate email format
        if '@' not in data.get('email', ''):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate password length
        if len(data.get('password', '')) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        # Check if staff with same email already exists
        if Staff.query.filter_by(email=data.get('email')).first():
            return jsonify({'error': 'Staff member with this email already exists'}), 400
        
        # Check if staff with same employee_id already exists
        if Staff.query.filter_by(employee_id=data.get('employee_id')).first():
            return jsonify({'error': 'Staff member with this employee ID already exists'}), 400
        
        # Create new staff
        staff = Staff(
            employee_id=data.get('employee_id').strip(),
            email=data.get('email').strip(),
            name=data.get('name').strip(),
            department=data.get('department').strip(),
            phone=data.get('phone', '').strip(),
            position=data.get('position').strip()
        )
        staff.set_password(data.get('password'))
        
        db.session.add(staff)
        db.session.commit()
        
        return jsonify({'message': 'Staff member added successfully', 'staff_id': staff.id}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error adding staff: {str(e)}'}), 500

@app.route('/api/admin/staff/<int:staff_id>', methods=['PUT'])
@admin_required
def update_staff(staff_id):
    data = request.json
    staff = Staff.query.get(staff_id)
    
    if not staff:
        return jsonify({'error': 'Staff not found'}), 404
    
    staff.name = data.get('name', staff.name)
    staff.email = data.get('email', staff.email)
    staff.department = data.get('department', staff.department)
    staff.position = data.get('position', staff.position)
    staff.phone = data.get('phone', staff.phone)
    staff.is_active = data.get('is_active', staff.is_active)
    
    db.session.commit()
    return jsonify({'message': 'Staff updated successfully'}), 200

@app.route('/api/admin/staff/<int:staff_id>', methods=['DELETE'])
@admin_required
def deactivate_staff(staff_id):
    try:
        staff = Staff.query.get(staff_id)
        if not staff:
            return jsonify({'error': 'Staff not found'}), 404
        
        active_leaves = Leave.query.filter_by(staff_id=staff_id, status='pending').count()
        if active_leaves > 0:
            return jsonify({'error': 'Cannot delete staff with active leave requests'}), 400
        
        # Soft delete - mark as inactive
        staff.is_active = False
        db.session.commit()
        
        return jsonify({'message': 'Staff member deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Timetable Routes
@app.route('/api/admin/timetable', methods=['GET'])
@admin_required
def get_timetable():
    timetable = Timetable.query.all()
    return jsonify({
        'timetable': [{
            'id': t.id,
            'staff_id': t.staff_id,
            'staff_name': t.staff.name,
            'course_code': t.course_code,
            'course_name': t.course_name,
            'day': t.day,
            'time_slot': t.time_slot,
            'room': t.room,
            'batch': t.batch,
            'classroom': t.classroom.to_dict() if t.classroom else None
        } for t in timetable]
    }), 200

@app.route('/api/admin/timetable', methods=['POST'])
@admin_required
def add_timetable_entry():
    data = request.json
    timetable_entry = Timetable(
        staff_id=data.get('staff_id'),
        course_code=data.get('course_code'),
        course_name=data.get('course_name'),
        day=data.get('day'),
        time_slot=data.get('time_slot'),
        room=data.get('room'),
        classroom_id=data.get('classroom_id', None),
        batch=data.get('batch', '')
    )
    db.session.add(timetable_entry)
    db.session.commit()
    return jsonify({'message': 'Timetable entry added successfully', 'id': timetable_entry.id}), 201

@app.route('/api/admin/timetable/<int:timetable_id>', methods=['PUT'])
@admin_required
def update_timetable_entry(timetable_id):
    data = request.json
    timetable_entry = Timetable.query.get(timetable_id)
    
    if not timetable_entry:
        return jsonify({'error': 'Timetable entry not found'}), 404
    
    timetable_entry.staff_id = data.get('staff_id', timetable_entry.staff_id)
    timetable_entry.course_code = data.get('course_code', timetable_entry.course_code)
    timetable_entry.course_name = data.get('course_name', timetable_entry.course_name)
    timetable_entry.day = data.get('day', timetable_entry.day)
    timetable_entry.time_slot = data.get('time_slot', timetable_entry.time_slot)
    timetable_entry.room = data.get('room', timetable_entry.room)
    timetable_entry.classroom_id = data.get('classroom_id', timetable_entry.classroom_id)
    timetable_entry.batch = data.get('batch', timetable_entry.batch)
    
    db.session.commit()
    return jsonify({'message': 'Timetable entry updated successfully'}), 200

@app.route('/api/admin/timetable/<int:timetable_id>', methods=['DELETE'])
@admin_required
def delete_timetable_entry(timetable_id):
    timetable_entry = Timetable.query.get(timetable_id)
    if not timetable_entry:
        return jsonify({'error': 'Timetable entry not found'}), 404
    
    db.session.delete(timetable_entry)
    db.session.commit()
    return jsonify({'message': 'Timetable entry deleted successfully'}), 200

# Staff Timetable Route
@app.route('/api/staff/timetable', methods=['GET'])
@staff_required
def get_staff_timetable():
    staff_id = session['user_id']
    timetable = Timetable.query.filter_by(staff_id=staff_id).all()
    return jsonify({
        'timetable': [{
            'id': t.id,
            'course_code': t.course_code,
            'course_name': t.course_name,
            'day': t.day,
            'time_slot': t.time_slot,
            'room': t.room,
            'batch': t.batch,
            'classroom': t.classroom.to_dict() if t.classroom else None
        } for t in timetable]
    }), 200

# Leave Management Routes
@app.route('/api/staff/leave/apply', methods=['POST'])
@staff_required
def apply_leave():
    data = request.json
    staff_id = session['user_id']
    
    leave = Leave(
        staff_id=staff_id,
        leave_date=parse_date(data.get('leave_date')).date(),
        leave_type=data.get('leave_type'),
        reason=data.get('reason', '')
    )
    db.session.add(leave)
    db.session.commit()
    
    # Auto-reschedule classes
    reschedule_classes_for_leave(leave.id)
    
    return jsonify({'message': 'Leave applied successfully', 'leave_id': leave.id}), 201

def reschedule_classes_for_leave(leave_id, auto_mode=False):
    leave = Leave.query.get(leave_id)
    if not leave:
        return False
    
    # Find all classes of the staff on the leave date
    leave_day = leave.leave_date.strftime('%A')
    staff_classes = Timetable.query.filter_by(staff_id=leave.staff_id).all()
    
    rescheduled_count = 0
    for timetable_entry in staff_classes:
        if timetable_entry.day.lower() == leave_day.lower():
            # Check if already rescheduled
            existing = ClassRescheduling.query.filter_by(
                original_timetable_id=timetable_entry.id,
                leave_id=leave_id
            ).first()
            
            if existing:
                continue
            
            # Find available staff
            available_staff = find_available_staff(timetable_entry)
            
            if available_staff:
                rescheduling = ClassRescheduling(
                    original_timetable_id=timetable_entry.id,
                    original_staff_id=leave.staff_id,
                    assigned_staff_id=available_staff.id,
                    leave_id=leave_id,
                    reason='Auto-assigned due to leave' if auto_mode else 'Manual assignment'
                )
                db.session.add(rescheduling)
                rescheduled_count += 1
    
    db.session.commit()
    return rescheduled_count > 0

def find_available_staff(timetable_entry):
    """Find an available staff member without conflicts for the given time slot"""
    all_staff = Staff.query.filter_by(is_active=True).all()
    
    for staff in all_staff:
        if staff.id == timetable_entry.staff_id:
            continue
        
        # Check if staff has any class at the same time
        conflict = Timetable.query.filter(
            Timetable.staff_id == staff.id,
            Timetable.day == timetable_entry.day,
            Timetable.time_slot == timetable_entry.time_slot
        ).first()
        
        if not conflict:
            return staff
    
    return None

@app.route('/api/admin/leave/pending', methods=['GET'])
@admin_required
def get_pending_leaves():
    pending_leaves = Leave.query.filter_by(status='pending').all()
    return jsonify({
        'leaves': [{
            'id': l.id,
            'staff_id': l.staff_id,
            'staff_name': l.staff.name,
            'leave_date': l.leave_date.strftime('%Y-%m-%d'),
            'leave_type': l.leave_type,
            'reason': l.reason,
            'applied_at': l.applied_at.strftime('%Y-%m-%d %H:%M:%S')
        } for l in pending_leaves]
    }), 200

@app.route('/api/admin/leave/<int:leave_id>/approve', methods=['POST'])
@admin_required
def approve_leave(leave_id):
    try:
        leave = Leave.query.get(leave_id)
        if not leave:
            return jsonify({'error': 'Leave not found'}), 404
        
        leave.status = 'approved'
        leave.approved_by = session['user_id']
        db.session.commit()
        
        # Auto-reschedule classes when leave is approved
        reschedule_classes_for_leave(leave_id)
        
        return jsonify({
            'message': 'Leave approved successfully',
            'leave_id': leave_id
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/leave/<int:leave_id>/reject', methods=['POST'])
@admin_required
def reject_leave(leave_id):
    try:
        leave = Leave.query.get(leave_id)
        if not leave:
            return jsonify({'error': 'Leave not found'}), 404
        
        leave.status = 'rejected'
        leave.approved_by = session['user_id']
        
        # Remove all rescheduling records for this leave
        reschedulings = ClassRescheduling.query.filter_by(leave_id=leave_id).all()
        for rescheduling in reschedulings:
            db.session.delete(rescheduling)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Leave rejected successfully',
            'leave_id': leave_id
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/rescheduling/<int:rescheduling_id>/override', methods=['POST'])
@admin_required
def override_rescheduling(rescheduling_id):
    data = request.json
    rescheduling = ClassRescheduling.query.get(rescheduling_id)
    if not rescheduling:
        return jsonify({'error': 'Rescheduling record not found'}), 404
    
    rescheduling.assigned_staff_id = data.get('assigned_staff_id')
    db.session.commit()
    return jsonify({'message': 'Rescheduling overridden successfully'}), 200

@app.route('/api/admin/leave/<int:leave_id>/auto-reschedule', methods=['POST'])
@admin_required
def auto_reschedule_leave(leave_id):
    """Automatically reschedule all classes for the leave"""
    try:
        reschedule_classes_for_leave(leave_id, auto_mode=True)
        return jsonify({'message': 'Classes auto-rescheduled successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Dashboard Statistics Routes
@app.route('/api/admin/stats/staff-count', methods=['GET'])
@admin_required
def get_staff_count():
    total_staff = Staff.query.count()
    active_staff = Staff.query.filter_by(is_active=True).count()
    
    return jsonify({'total_staff': total_staff, 'active_staff': active_staff}), 200

@app.route('/api/admin/stats/login-activity', methods=['GET'])
@admin_required
def get_login_activity():
    try:
        logs = LoginLog.query.order_by(LoginLog.login_time.desc()).limit(50).all()
        
        log_data = []
        for log in logs:
            user_name = ''
            if log.user_type == 'admin' and log.admin_id:
                admin = Admin.query.get(log.admin_id)
                user_name = admin.name if admin else 'Unknown Admin'
            elif log.user_type == 'staff' and log.staff_id:
                staff = Staff.query.get(log.staff_id)
                user_name = staff.name if staff else 'Unknown Staff'
            
            log_data.append({
                'id': log.id,
                'user_name': user_name,
                'user_type': log.user_type,
                'login_time': log.login_time.strftime('%Y-%m-%d %H:%M:%S'),
                'logout_time': log.logout_time.strftime('%Y-%m-%d %H:%M:%S') if log.logout_time else None,
                'ip_address': log.ip_address,
                'status': log.status
            })
        
        return jsonify({'logs': log_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/leave-presence', methods=['GET'])
@admin_required
def get_leave_presence():
    try:
        staff_id = request.args.get('staff_id')
        
        if staff_id:
            leaves = Leave.query.filter_by(staff_id=int(staff_id)).all()
        else:
            leaves = Leave.query.all()
        
        leave_data = []
        for leave in leaves:
            staff = Staff.query.get(leave.staff_id)
            leave_data.append({
                'id': leave.id,
                'staff_name': staff.name if staff else 'Unknown',
                'staff_id': leave.staff_id,
                'leave_date': leave.leave_date.strftime('%Y-%m-%d'),
                'leave_type': leave.leave_type,
                'status': leave.status
            })
        
        return jsonify({'leaves': leave_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/rescheduling', methods=['GET'])
@admin_required
def get_rescheduling_records():
    try:
        records = ClassRescheduling.query.order_by(ClassRescheduling.created_at.desc()).all()
        
        record_data = []
        for record in records:
            original_staff = Staff.query.get(record.original_staff_id)
            assigned_staff = Staff.query.get(record.assigned_staff_id)
            timetable = Timetable.query.get(record.original_timetable_id)
            
            record_data.append({
                'id': record.id,
                'original_staff_name': original_staff.name if original_staff else 'Unknown',
                'assigned_staff_name': assigned_staff.name if assigned_staff else 'Unknown',
                'course_code': timetable.course_code if timetable else 'Unknown',
                'course_name': timetable.course_name if timetable else 'Unknown',
                'reason': record.reason,
                'created_at': record.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return jsonify({'records': record_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Classroom Management API
@app.route('/api/admin/classrooms', methods=['GET'])
@admin_required
def get_classrooms():
    try:
        classrooms = Classroom.query.filter_by(is_active=True).all()
        return jsonify({
            'classrooms': [classroom.to_dict() for classroom in classrooms]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/classrooms', methods=['POST'])
@admin_required
def create_classroom():
    try:
        data = request.get_json()
        
        required_fields = ['room_number', 'room_name', 'capacity']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if room number already exists
        existing = Classroom.query.filter_by(room_number=data['room_number']).first()
        if existing:
            return jsonify({'error': 'Room number already exists'}), 409
        
        classroom = Classroom(
            room_number=data['room_number'],
            room_name=data['room_name'],
            capacity=int(data['capacity']),
            floor=data.get('floor', ''),
            building=data.get('building', ''),
            facilities=data.get('facilities', '')
        )
        db.session.add(classroom)
        db.session.commit()
        
        return jsonify({
            'message': 'Classroom created successfully',
            'classroom': classroom.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/classrooms/<int:classroom_id>', methods=['PUT'])
@admin_required
def update_classroom(classroom_id):
    try:
        classroom = Classroom.query.get(classroom_id)
        if not classroom:
            return jsonify({'error': 'Classroom not found'}), 404
        
        data = request.get_json()
        
        if 'room_number' in data:
            classroom.room_number = data['room_number']
        if 'room_name' in data:
            classroom.room_name = data['room_name']
        if 'capacity' in data:
            classroom.capacity = int(data['capacity'])
        if 'floor' in data:
            classroom.floor = data['floor']
        if 'building' in data:
            classroom.building = data['building']
        if 'facilities' in data:
            classroom.facilities = data['facilities']
        
        db.session.commit()
        return jsonify({
            'message': 'Classroom updated successfully',
            'classroom': classroom.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/classrooms/<int:classroom_id>', methods=['DELETE'])
@admin_required
def delete_classroom(classroom_id):
    try:
        classroom = Classroom.query.get(classroom_id)
        if not classroom:
            return jsonify({'error': 'Classroom not found'}), 404
        
        classroom.is_active = False
        db.session.commit()
        
        return jsonify({'message': 'Classroom deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Staff Leave History Route
@app.route('/api/staff/leave-history', methods=['GET'])
@staff_required
def get_staff_leave_history():
    try:
        staff_id = session['user_id']
        leaves = Leave.query.filter_by(staff_id=staff_id).order_by(Leave.applied_at.desc()).all()
        
        leave_data = []
        for leave in leaves:
            leave_data.append({
                'id': leave.id,
                'leave_date': leave.leave_date.strftime('%Y-%m-%d'),
                'leave_type': leave.leave_type,
                'reason': leave.reason,
                'status': leave.status,
                'applied_at': leave.applied_at.strftime('%Y-%m-%d %H:%M:%S') if leave.applied_at else None
            })
        
        return jsonify({'leaves': leave_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return send_from_directory('public', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('public', filename)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
