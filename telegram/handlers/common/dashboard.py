from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.utils.markdown import hbold, hcode

from api.transaction import get_main_balance, get_current_month_transactions, get_saving_balance
from api.saving import get_savings_by_user_tg_id
from api.category import get_categories_by_filters

router = Router(name="dashboard_router")

@router.message(F.text == "Dashboard")
@router.message(Command("dashboard"))
async def show_dashboard(message: Message):
    try:
        user_id = message.from_user.id
        
        # Получаем баланс
        balance_data = await get_main_balance(user_id)
        balance = balance_data.get('balance', 0) if balance_data else 0
        
        # Получаем транзакции за месяц
        transactions = await get_current_month_transactions(user_id) or []
        
        # Разделяем на доходы и расходы
        income_transactions = [t for t in transactions if t.get("transaction_type") == 'income']
        expense_transactions = [t for t in transactions if t.get("transaction_type") == 'expense']
        
        # Считаем суммы
        total_income = sum(t.get('amount', 0) for t in income_transactions)
        total_expense = sum(t.get('amount', 0) for t in expense_transactions)
        
        # Получаем информацию о копилке
        savings = await get_savings_by_user_tg_id(user_id) or []
        saving_text = "Нет активных копилок"
        
        if savings:
            old_saving = min(savings, key=lambda x: x.get('created_at', ''))
            saving_id = old_saving.get("id")
            
            if saving_id:
                saving_balance_data = await get_saving_balance(saving_id=saving_id)
                current_balance = saving_balance_data.get('balance', 0) if saving_balance_data else 0
                final_amount = old_saving.get("final_amount", 0)
                
                saving_text = f"{old_saving.get('name', 'Копилка')} - {current_balance}/{final_amount} ₽"
    
        text = (
            f"{hbold('💰 Твой баланс:')} {hcode(str(balance))} ₽\n\n"
            f"{hbold('📊 Статистика за месяц:')}\n"
            f"• Расходы: {hcode(str(total_expense))} ₽ ({len(expense_transactions)} операций)\n"
            f"• Доходы: {hcode(str(total_income))} ₽ ({len(income_transactions)} операций)\n"
            f"• Разница: {hcode(str(total_income - total_expense))} ₽\n\n"
            f"{hbold('🐷 Копилка:')}\n{saving_text}"
        )
        
        await message.answer(text, parse_mode="HTML")
        
    except Exception as e:
        print(f"Ошибка в dashboard: {e}")
        await message.answer(
            "❌ Произошла ошибка при загрузке данных. "
            "Пожалуйста, попробуйте позже."
        )