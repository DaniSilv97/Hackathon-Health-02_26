-- Initial database setup for MySQL
-- Tables are managed by Flask-SQLAlchemy migrations
-- This file only ensures the database exists and has proper charset

-- Set charset
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- Grant privileges (for the application user)
GRANT ALL PRIVILEGES ON health_db.* TO 'health_user'@'%';
FLUSH PRIVILEGES;

-- Note: Use Flask CLI commands to manage data:
--   flask db:fresh --seed    # Reset database and seed
--   flask db:seed            # Run seeders only
--   flask db:factory user -c 10  # Create 10 users with factory
