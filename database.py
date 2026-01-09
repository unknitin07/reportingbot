import sqlite3
import json
from datetime import datetime
from typing import Optional, List, Dict
from config import DATABASE_PATH, STATUS_PENDING, STATUS_APPROVED, STATUS_BLOCKED, SUPER_ADMIN_ID

class Database:
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_db(self):
        """Initialize database schema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                status TEXT DEFAULT 'pending',
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                approved_at TIMESTAMP,
                approved_by INTEGER
            )
        ''')
        
        # Operations log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS operations_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                operation TEXT,
                params TEXT,
                success BOOLEAN,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, user_id: int, username: str = None, 
                 first_name: str = None, last_name: str = None) -> bool:
        """Add a new user or update existing user info"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Auto-approve super admin
            status = STATUS_APPROVED if user_id == SUPER_ADMIN_ID else STATUS_PENDING
            
            cursor.execute('''
                INSERT OR REPLACE INTO users (user_id, username, first_name, last_name, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, username, first_name, last_name, status))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding user: {e}")
            return False
        finally:
            conn.close()
    
    def is_user_approved(self, user_id: int) -> bool:
        """Check if user is approved"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT status FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        
        return result and result[0] == STATUS_APPROVED
    
    def approve_user(self, user_id: int, approved_by: int) -> bool:
        """Approve a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE users 
                SET status = ?, approved_at = ?, approved_by = ?
                WHERE user_id = ?
            ''', (STATUS_APPROVED, datetime.now(), approved_by, user_id))
            
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error approving user: {e}")
            return False
        finally:
            conn.close()
    
    def revoke_user(self, user_id: int) -> bool:
        """Revoke user access"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE users SET status = ? WHERE user_id = ?
            ''', (STATUS_PENDING, user_id))
            
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error revoking user: {e}")
            return False
        finally:
            conn.close()
    
    def block_user(self, user_id: int) -> bool:
        """Block a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE users SET status = ? WHERE user_id = ?
            ''', (STATUS_BLOCKED, user_id))
            
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error blocking user: {e}")
            return False
        finally:
            conn.close()
    
    def get_all_users(self) -> List[Dict]:
        """Get all users"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, username, first_name, last_name, status, added_at
            FROM users
            ORDER BY added_at DESC
        ''')
        
        users = []
        for row in cursor.fetchall():
            users.append({
                'user_id': row[0],
                'username': row[1],
                'first_name': row[2],
                'last_name': row[3],
                'status': row[4],
                'added_at': row[5]
            })
        
        conn.close()
        return users
    
    def get_pending_users(self) -> List[Dict]:
        """Get all pending users"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, username, first_name, last_name, added_at
            FROM users
            WHERE status = ?
            ORDER BY added_at DESC
        ''', (STATUS_PENDING,))
        
        users = []
        for row in cursor.fetchall():
            users.append({
                'user_id': row[0],
                'username': row[1],
                'first_name': row[2],
                'last_name': row[3],
                'added_at': row[4]
            })
        
        conn.close()
        return users
    
    def log_operation(self, user_id: int, operation: str, 
                      params: dict, success: bool) -> bool:
        """Log an operation"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO operations_log (user_id, operation, params, success)
                VALUES (?, ?, ?, ?)
            ''', (user_id, operation, json.dumps(params), success))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error logging operation: {e}")
            return False
        finally:
            conn.close()
    
    def get_user_stats(self) -> Dict:
        """Get user statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = ? THEN 1 ELSE 0 END) as approved,
                SUM(CASE WHEN status = ? THEN 1 ELSE 0 END) as pending,
                SUM(CASE WHEN status = ? THEN 1 ELSE 0 END) as blocked
            FROM users
        ''', (STATUS_APPROVED, STATUS_PENDING, STATUS_BLOCKED))
        
        result = cursor.fetchone()
        conn.close()
        
        return {
            'total': result[0],
            'approved': result[1],
            'pending': result[2],
            'blocked': result[3]
        }
