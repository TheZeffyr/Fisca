import pytest
from decimal import Decimal
from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import BaseModel, User, Currency, Account
from app.enums import AccountType


@pytest.fixture(scope="session")
def engine():
    engine = create_engine("sqlite:///:memory:", echo=False)
    BaseModel.metadata.create_all(engine)
    return engine


@pytest.fixture
def db_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def test_currency(db_session):
    currency = Currency(
        code="RUB",
        name="Российский рубль",
        symbol="₽"
    )
    db_session.add(currency)
    db_session.flush()
    return currency


@pytest.fixture
def test_user(db_session, test_currency):
    user = User(
        tg_id=123456789,
        currency_id=test_currency.id
    )
    db_session.add(user)
    db_session.flush()
    return user


@pytest.fixture
def test_account_cash(db_session, test_user):
    account = Account(
        name="Наличные",
        type=AccountType.CASH,
        user_id=test_user.id,
        balance=Decimal("10000.00")
    )
    db_session.add(account)
    db_session.flush()
    db_session.refresh(test_user)
    return account


@pytest.fixture
def test_account_card(db_session, test_user):
    account = Account(
        name="Карта",
        type=AccountType.CARD,
        user_id=test_user.id,
        balance=Decimal("5000.00")
    )
    db_session.add(account)
    db_session.flush()
    db_session.refresh(test_user)
    return account


@pytest.fixture
def test_account_savings(db_session, test_user):
    account = Account(
        name="Накопления",
        type=AccountType.SAVINGS,
        user_id=test_user.id,
        target_amount=Decimal("100000.00"),
        end_date=date(2025, 12, 31),
        balance=Decimal("25000.00"),
        is_completed=False
    )
    db_session.add(account)
    db_session.flush()
    return account


@pytest.fixture
def test_user_with_accounts(
    db_session,
    test_user,
    test_account_cash,
    test_account_card
):
    db_session.refresh(test_user)
    return test_user
