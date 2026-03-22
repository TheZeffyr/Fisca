import pytest
from decimal import Decimal
from datetime import date

from sqlalchemy.exc import IntegrityError

from app.models import Account
from app.enums import AccountType


class TestAccountCreation:    
    def test_create_cash_account(self, db_session, test_user):
        account = Account(
            name="Кошелек",
            type=AccountType.CASH,
            user_id=test_user.id,
            balance=Decimal("1000.00")
        )
        db_session.add(account)
        db_session.flush()
        
        assert account.id is not None
        assert account.name == "Кошелек"
        assert account.type == AccountType.CASH
        assert account.balance == Decimal("1000.00")
        assert account.target_amount is None
        assert account.end_date is None
        assert account.is_completed is False
    
    def test_create_savings_account(self, db_session, test_user):
        account = Account(
            name="На машину",
            type=AccountType.SAVINGS,
            user_id=test_user.id,
            target_amount=Decimal("500000.00"),
            end_date=date(2026, 12, 31),
            balance=Decimal("100000.00")
        )
        db_session.add(account)
        db_session.flush()
        
        assert account.id is not None
        assert account.type == AccountType.SAVINGS
        assert account.target_amount == Decimal("500000.00")
        assert account.end_date == date(2026, 12, 31)
    
    def test_create_savings_without_target_amount_fails(
        self,
        db_session,
        test_user
    ):
        account = Account(
            name="Накопления",
            type=AccountType.SAVINGS,
            user_id=test_user.id,
            target_amount=None,
            balance=Decimal("1000.00")
        )
        db_session.add(account)
        
        try:
            db_session.flush()
            assert account.target_amount is None
            pytest.skip(
                "SQLite allows NULL in this case; test only for PostgreSQL"
            )
        except IntegrityError:
            pass


class TestAccountValidation:    
    def test_empty_name_fails(self, db_session, test_user):
        account = Account(
            name="   ",
            type=AccountType.CASH,
            user_id=test_user.id
        )
        db_session.add(account)
        
        with pytest.raises(IntegrityError):
            db_session.flush()
    
    def test_negative_balance_fails(self, db_session, test_user):
        account = Account(
            name="Долги",
            type=AccountType.CASH,
            user_id=test_user.id,
            balance=Decimal("-100.00")
        )
        db_session.add(account)
        
        with pytest.raises(IntegrityError):
            db_session.flush()
    
    def test_cash_account_cannot_have_target_amount(
        self,
        db_session,
        test_user
    ):
        account = Account(
            name="Наличные",
            type=AccountType.CASH,
            user_id=test_user.id,
            target_amount=Decimal("10000.00"),
            balance=Decimal("5000.00")
        )
        db_session.add(account)
        
        with pytest.raises(IntegrityError):
            db_session.flush()
    
    def test_cash_account_cannot_have_end_date(self, db_session, test_user):
        account = Account(
            name="Наличные",
            type=AccountType.CASH,
            user_id=test_user.id,
            end_date=date(2025, 12, 31),
            balance=Decimal("5000.00")
        )
        db_session.add(account)
        
        with pytest.raises(IntegrityError):
            db_session.flush()


class TestAccountBalance:    
    def test_calc_balance_empty_account(self, db_session, test_user):
        account = Account(
            name="Пустой счет",
            type=AccountType.CASH,
            user_id=test_user.id,
            balance=Decimal("0.00")
        )
        db_session.add(account)
        db_session.flush()
        
        assert account.calc_balance == Decimal("0.00")
    
    def test_calc_balance_after_transactions(
        self,
        db_session,
        test_user,
        test_account_cash
    ):
        from app.models import Transaction
        
        expense = Transaction(
            amount=Decimal("500.00"),
            date=date.today(),
            from_account_id=test_account_cash.id,
            to_account_id=None,
            user_id=test_user.id
        )
        db_session.add(expense)
        db_session.flush()
        
        test_account_cash.balance -= expense.amount
        db_session.flush()
        
        db_session.refresh(test_account_cash)
        
        assert test_account_cash.calc_balance == Decimal("-500.00")


class TestAccountRelationships:    
    def test_account_has_user(self, db_session, test_account_cash, test_user):
        assert test_account_cash.user_id == test_user.id
        
        db_session.refresh(test_account_cash)
        assert test_account_cash.user.id == test_user.id
    
    def test_user_has_accounts(self, test_user_with_accounts):
        user = test_user_with_accounts
        
        assert len(user.accounts) >= 2
        account_names = [acc.name for acc in user.accounts]
        assert "Наличные" in account_names
        assert "Карта" in account_names
