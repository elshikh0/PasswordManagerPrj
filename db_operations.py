import sqlite3
from cryptography.fernet import Fernet
import bcrypt



class DbOperations:
    def __init__(self):
        with open("encryption_key.key", "rb") as key_file:
            self.key = key_file.read()
        self.cipher = Fernet(self.key)

    def encrypt_password(self, password):
        """Encrypt the password before saving it to the database."""
        return self.cipher.encrypt(password.encode()).decode()

    def decrypt_password(self, encrypted_password):
        """Decrypt the password when showing it to the user."""
        return self.cipher.decrypt(encrypted_password.encode()).decode()
        
    def connect_to_db(self):
        conn = sqlite3.connect('password_records.db')
        return conn
    
    def create_table(self, table_name="password_info"): 
        conn = self.connect_to_db()
        query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
          ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
          created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          website TEXT NOT NULL,
          username VARCHAR(200),
          password VARCHAR(50)
        );
        '''
        with conn as conn: 
            cursor = conn.cursor()
            cursor.execute(query)

    def create_record(self, data, table_name="password_info"):
        website = data['website']
        username = data['username']
        password = data['password']

        encrypted_password = self.encrypt_password(password)


        conn = self.connect_to_db()
        query = f'''
        INSERT INTO {table_name} (website, username, password) VALUES (?, ?, ?);
        '''
        with conn as conn: 
            cursor = conn.cursor()
            cursor.execute(query, (website, username, encrypted_password))

    def show_records(self, table_name="password_info"):
        conn = self.connect_to_db()
        query = f'''
        SELECT * FROM {table_name};
        '''
        with conn as conn: 
            cursor = conn.cursor()
            list_records = cursor.execute(query).fetchall()

            decrypted_records = []
            for record in list_records:
                decrypted_password = self.decrypt_password(record[5])  
                decrypted_record = record[:5] + (decrypted_password,)  # Replace the encrypted password with decrypted
                decrypted_records.append(decrypted_record)
            return decrypted_records
        
        
    def update_record(self, data, table_name="password_info"):
        ID = data['ID']
        website = data['website']
        username = data['username']
        password = data['password']

        encrypted_password = self.encrypt_password(password)


        conn = self.connect_to_db()
        query = f'''
        UPDATE {table_name} 
        SET website = ?, username = ?, password = ?
        WHERE ID = ?;
        '''
        with conn as conn: 
            cursor = conn.cursor()
            cursor.execute(query, (website, username, encrypted_password, ID))
    
    def delete_record(self, ID, table_name="password_info"):
        conn = self.connect_to_db()
        query = f'''
        DELETE FROM {table_name} WHERE ID = ?;
        '''
        with conn as conn: 
            cursor = conn.cursor()
            cursor.execute(query, (ID,))
    def search_records(self, keyword, table_name="password_info"):
        conn = self.connect_to_db()
        query = f'''
        SELECT * FROM {table_name} WHERE 
        website LIKE ? OR 
        username LIKE ?;
        '''
        with conn as conn:
          cursor = conn.cursor()
          results = cursor.execute(query, (f"%{keyword}%", f"%{keyword}%")).fetchall()
          return results