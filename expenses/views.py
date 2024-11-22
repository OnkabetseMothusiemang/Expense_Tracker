from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense, Category, UserProfile  # Add UserProfile import here
from .forms import ExpenseForm, SalaryForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

@login_required
def delete_expense(request, expense_id):
    # Fetch the expense object by ID, making sure it belongs to the current user
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    # Delete the expense
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_summary')  # Redirect to expense summary page after deletion
    
    return redirect('home')


@login_required
def expense_summary(request):
    user_expenses = Expense.objects.filter(user=request.user)
    
    # Calculate total expenses for the month
    total_expenses = user_expenses.aggregate(Sum('amount'))['amount__sum'] or 0.0
    
    # Ensure that the user has a profile, if not, create one
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    salary = profile.salary if profile else 0.0
    
    savings_recommendation = ""
    if salary > 0:
        remaining_balance = salary - total_expenses
        savings_recommendation = f"Your remaining balance is ${remaining_balance:.2f}. It's recommended to save at least 20% of your income each month, which would be ${salary * 0.2:.2f}."
    
    return render(request, 'expense_summary.html', {
        'total_expenses': total_expenses,
        'salary': salary,
        'remaining_balance': remaining_balance,
        'savings_recommendation': savings_recommendation,
    })

def home(request):
    expenses = Expense.objects.all().order_by('-date')
    total_expenses = sum(exp.amount for exp in expenses)
    return render(request, 'home.html', {'expenses': expenses, 'total_expenses': total_expenses})

def add_expense(request):
    categories = Category.objects.all()  # Get all categories for the dropdown
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            # Save the expense with the selected category
            form.save()
            return redirect('home')
    else:
        form = ExpenseForm()

    return render(request, 'add_expense.html', {
        'form': form,
        'categories': categories,  # Pass the categories to the template
    })
