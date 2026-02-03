"""
Migrations module - Flask-Migrate integration.

Flask-Migrate commands:
    flask db init       - Initialize migrations directory
    flask db migrate -m "message" - Create a new migration
    flask db upgrade    - Apply migrations
    flask db downgrade  - Rollback migration
    flask db history    - Show migration history
    flask db current    - Show current revision

Custom commands (Laravel-like):
    flask db:fresh      - Drop all tables and recreate
    flask db:fresh --seed - Fresh with seeding
    flask db:seed       - Run database seeders
    flask db:reset --seed - Reset and seed
"""
