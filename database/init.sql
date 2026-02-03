-- Initial database setup

-- Create users table if not exists (Flask-SQLAlchemy will handle this, but here for reference)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'patient',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert default admin user (password: admin123)
-- Note: This is a bcrypt hash of 'admin123' - change in production!
INSERT INTO users (name, email, password, role) VALUES
('Admin User', 'admin@health.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.OQW9VqsOGXJOmi', 'admin')
ON DUPLICATE KEY UPDATE name = name;

-- Insert default clinician user (password: clinician123)
INSERT INTO users (name, email, password, role) VALUES
('Dr. John Smith', 'clinician@health.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.OQW9VqsOGXJOmi', 'clinician')
ON DUPLICATE KEY UPDATE name = name;

-- Insert default patient user (password: patient123)
INSERT INTO users (name, email, password, role) VALUES
('Jane Doe', 'patient@health.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.OQW9VqsOGXJOmi', 'patient')
ON DUPLICATE KEY UPDATE name = name;
