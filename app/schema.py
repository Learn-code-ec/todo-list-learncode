instructions = [
    'SET FOREIGN_KEY_CHECKS=0;',
    'DROP TABLE IF EXISTS todos;',
    'DROP TABLE IF EXISTS users',
    'SET FOREIGN_KEY_CHECKS=1;',
    """
        CREATE TABLE users(
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(60) NOT NULL UNIQUE,
            password VARCHAR(165) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
        )
    """,
    """
        CREATE TABLE todos(
            id INT AUTO_INCREMENT PRIMARY KEY,
            created_by INT NOT NULL,
            title VARCHAR(80) NOT NULL,
            description TEXT NOT NULL,
            completed BOOLEAN DEFAULT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    """
]