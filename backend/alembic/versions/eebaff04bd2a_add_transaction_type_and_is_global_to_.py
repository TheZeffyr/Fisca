# alembic/versions/eebaff04bd2a_add_transaction_type_and_is_global_to_.py
"""add transaction_type and is_global to categories

Revision ID: eebaff04bd2a
Revises:
Create Date: 2026-02-14 21:01:42.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'eebaff04bd2a'
down_revision = None
branch_labels = None
depends_on = None

# Определяем ENUM тип (должен совпадать с тем, что в вашей модели)
# Пример: если в модели используется Enum('INCOME', 'EXPENSE', name='transactiontype')
transaction_type_enum = sa.Enum('INCOME', 'EXPENSE', name='transactiontype')

def upgrade():
    # ### Шаг 1: Добавляем колонку с NULL
    op.add_column('category', sa.Column('transaction_type', transaction_type_enum, nullable=True))
    op.add_column('category', sa.Column('is_global', sa.Boolean(), nullable=True, server_default='false'))

    # ### Шаг 2: Заполняем существующие строки ЗНАЧЕНИЕМ ПО УМОЛЧАНИЮ
    # Выберите подходящее значение по умолчанию, например 'EXPENSE'
    op.execute("UPDATE category SET transaction_type = 'EXPENSE' WHERE transaction_type IS NULL")
    op.execute("UPDATE category SET is_global = false WHERE is_global IS NULL")

    # ### Шаг 3: Изменяем колонку на NOT NULL
    op.alter_column('category', 'transaction_type', nullable=False)
    op.alter_column('category', 'is_global', nullable=False, server_default=None) # Убираем server_default

def downgrade():
    # ### Откат изменений
    op.drop_column('category', 'transaction_type')
    op.drop_column('category', 'is_global')