import pytest
from app import create_app
from app.extensions import db as _db
from app.models.user import User
from app.models.role import Role


@pytest.fixture(scope="session")
def app():
    application = create_app("testing")
    with application.app_context():
        _db.create_all()
        yield application
        _db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


@pytest.fixture(scope="function", autouse=True)
def clean_db(app):
    yield
    with app.app_context():
        for table in reversed(_db.metadata.sorted_tables):
            _db.session.execute(table.delete())
        _db.session.commit()


@pytest.fixture(scope="function", autouse=True)
def clean_blocklist():
    from app.services.auth_service import _token_blocklist
    yield
    _token_blocklist.clear()


@pytest.fixture
def active_user(app):
    with app.app_context():
        role = Role(name="admin_local")
        _db.session.add(role)
        _db.session.flush()
        user = User(
            full_name="Admin Test",
            email="admin@test.com",
            role_id=role.id,
            status="active",
        )
        user.set_password("Admin1234!")
        _db.session.add(user)
        _db.session.commit()
        return {"id": user.id, "email": user.email, "password": "Admin1234!"}


@pytest.fixture
def inactive_user(app):
    with app.app_context():
        role = Role(name="resident")
        _db.session.add(role)
        _db.session.flush()
        user = User(
            full_name="Inactive User",
            email="inactive@test.com",
            role_id=role.id,
            status="inactive",
        )
        user.set_password("Pass1234!")
        _db.session.add(user)
        _db.session.commit()
        return {"id": user.id, "email": user.email, "password": "Pass1234!"}
