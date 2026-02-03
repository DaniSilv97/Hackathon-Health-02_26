"""
Database CLI Commands - Laravel-like artisan commands for Flask.

Commands:
    flask db:seed          - Run database seeders
    flask db:fresh         - Drop all tables and re-run migrations
    flask db:fresh --seed  - Fresh migration with seeding
    flask db:factory       - Create records using factories
"""

import click
from flask import current_app
from flask.cli import with_appcontext
from app import db


def register_commands(app):
    """Register database CLI commands with the Flask app."""

    @app.cli.command('db:seed')
    @with_appcontext
    def seed_command():
        """Run database seeders."""
        click.echo('Seeding database...')
        from database.seeders import DatabaseSeeder
        DatabaseSeeder.run()
        click.echo('Database seeding completed!')

    @app.cli.command('db:fresh')
    @click.option('--seed', is_flag=True, help='Run seeders after migration')
    @with_appcontext
    def fresh_command(seed):
        """Drop all tables and re-run migrations."""
        click.echo('Dropping all tables...')
        db.drop_all()
        click.echo('Creating all tables...')
        db.create_all()
        click.echo('Database fresh migration completed!')

        if seed:
            click.echo('Seeding database...')
            from database.seeders import DatabaseSeeder
            DatabaseSeeder.run()
            click.echo('Database seeding completed!')

    @app.cli.command('db:reset')
    @click.option('--seed', is_flag=True, help='Run seeders after reset')
    @with_appcontext
    def reset_command(seed):
        """Reset database (drop, create, migrate)."""
        click.echo('Resetting database...')
        db.drop_all()
        db.create_all()
        click.echo('Database reset completed!')

        if seed:
            click.echo('Seeding database...')
            from database.seeders import DatabaseSeeder
            DatabaseSeeder.run()
            click.echo('Database seeding completed!')

    @app.cli.command('db:factory')
    @click.argument('model')
    @click.option('--count', '-c', default=1, help='Number of records to create')
    @click.option('--state', '-s', default=None, help='Factory state to apply')
    @with_appcontext
    def factory_command(model, count, state):
        """Create records using factories.

        Example:
            flask db:factory user --count 10
            flask db:factory user --count 5 --state admin
        """
        model_lower = model.lower()

        if model_lower == 'user':
            from database.factories import UserFactory
            factory = UserFactory
        else:
            click.echo(f'Factory for model "{model}" not found.')
            return

        click.echo(f'Creating {count} {model}(s)...')

        if state:
            factory.state(state).create_many(count)
        else:
            factory.create_many(count)

        click.echo(f'Created {count} {model}(s) successfully!')

    @app.cli.command('db:show-users')
    @with_appcontext
    def show_users_command():
        """Show all users in the database."""
        from app.models.user import User
        users = User.query.all()

        if not users:
            click.echo('No users found.')
            return

        click.echo(f'\n{"ID":<5} {"Name":<25} {"Email":<30} {"Role":<12} {"Active":<8}')
        click.echo('-' * 80)

        for user in users:
            click.echo(
                f'{user.id:<5} {user.name:<25} {user.email:<30} '
                f'{user.role:<12} {"Yes" if user.is_active else "No":<8}'
            )

        click.echo(f'\nTotal: {len(users)} users')

    @app.cli.command('make:migration')
    @click.argument('name')
    @with_appcontext
    def make_migration_command(name):
        """Create a new migration file (placeholder - use flask db migrate)."""
        click.echo('To create migrations, use Flask-Migrate commands:')
        click.echo('  flask db init     - Initialize migrations directory')
        click.echo('  flask db migrate -m "message" - Create migration')
        click.echo('  flask db upgrade  - Apply migrations')
        click.echo('  flask db downgrade - Rollback migration')
