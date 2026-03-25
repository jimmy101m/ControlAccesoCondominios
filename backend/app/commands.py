import click
from flask.cli import with_appcontext
from app.extensions import db
from app.models.role import Role
from app.models.user import User


@click.command("seed")
@with_appcontext
def seed():
    """Inserta los roles base y un usuario administrador de prueba."""
    # Crear roles base
    base_roles = ["admin_local", "resident", "guard"]
    role_objects = {}

    for role_name in base_roles:
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name)
            db.session.add(role)
            print(f"Rol '{role_name}' insertado.")
        else:
            print(f"Rol '{role_name}' ya existe.")
        role_objects[role_name] = role

    db.session.commit()

    # Crear usuario administrador
    admin_email = "admin@example.com"
    admin_user = User.query.filter_by(email=admin_email).first()

    if not admin_user:
        admin_user = User(
            full_name="Administrador de Sistema",
            email=admin_email,
            role_id=role_objects["admin_local"].id,
            status="active",
        )
        admin_user.set_password("admin123")
        db.session.add(admin_user)
        print(f"Administrador '{admin_email}' (clave: admin123) insertado.")
    else:
        print(f"Administrador '{admin_email}' ya existe.")

    db.session.commit()
    print("Seed completado exitosamente.")


def register_commands(app):
    app.cli.add_command(seed)
