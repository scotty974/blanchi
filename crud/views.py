from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
from .neo4j_service import Neo4jService

# Dashboard view
def dashboard(request):
    with Neo4jService() as neo4j:
        persons = neo4j.get_all_persons()
        companies = neo4j.get_all_companies()
        bank_accounts = neo4j.get_all_bank_accounts()
        transactions = neo4j.get_all_transactions()
        suspicious_transactions = neo4j.get_suspicious_transactions()
    context = {
        'persons_count': len(persons),
        'companies_count': len(companies),
        'bank_accounts_count': len(bank_accounts),
        'transactions_count': len(transactions),
        'suspicious_transactions': suspicious_transactions
    }
    return render(request, 'crud/dashboard.html', context)

# Person views
def person_list(request):
    with Neo4jService() as neo4j:
        persons = neo4j.get_all_persons()
    return render(request, 'crud/person_list.html', {'persons': persons})

def person_create(request):
    if request.method == 'POST':
        try:
            with Neo4jService() as neo4j:
                person = neo4j.create_person(
                    id=request.POST['id'],
                    name=request.POST['name'],
                    national_id=request.POST['national_id'],
                    nationality=request.POST['nationality'],
                    risk_score=request.POST['risk_score']
                )
                if person:
                    messages.success(request, 'Person created successfully!')
                    return redirect('person_list')
                else:
                    messages.error(request, 'Failed to create person.')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'crud/person_form.html', {'action': 'Create'})

def person_edit(request, person_id):
    with Neo4jService() as neo4j:
        person = neo4j.get_person(person_id)
        
        if not person:
            messages.error(request, 'Person not found.')
            return redirect('person_list')
        
        if request.method == 'POST':
            try:
                updated_person = neo4j.update_person(
                    id=person_id,
                    name=request.POST['name'],
                    national_id=request.POST['national_id'],
                    nationality=request.POST['nationality'],
                    risk_score=request.POST['risk_score']
                )
                if updated_person:
                    messages.success(request, 'Person updated successfully!')
                    return redirect('person_list')
                else:
                    messages.error(request, 'Failed to update person.')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'crud/person_form.html', {'person': person, 'action': 'Edit'})

def person_delete(request, person_id):
    if request.method == 'POST':
        with Neo4jService() as neo4j:
            if neo4j.delete_person(person_id):
                messages.success(request, 'Person deleted successfully!')
            else:
                messages.error(request, 'Failed to delete person.')
    return redirect('person_list')

# Company views
def company_list(request):
    with Neo4jService() as neo4j:
        companies = neo4j.get_all_companies()
    return render(request, 'crud/company_list.html', {'companies': companies})

def company_create(request):
    if request.method == 'POST':
        try:
            with Neo4jService() as neo4j:
                company = neo4j.create_company(
                    id=request.POST['id'],
                    name=request.POST['name'],
                    country=request.POST['country'],
                    type=request.POST['type'],
                    risk_score=request.POST['risk_score']
                )
                if company:
                    messages.success(request, 'Company created successfully!')
                    return redirect('company_list')
                else:
                    messages.error(request, 'Failed to create company.')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'crud/company_form.html', {'action': 'Create'})

def company_edit(request, company_id):
    with Neo4jService() as neo4j:
        company = neo4j.get_company(company_id)
        
        if not company:
            messages.error(request, 'Company not found.')
            return redirect('company_list')
        
        if request.method == 'POST':
            try:
                updated_company = neo4j.update_company(
                    id=company_id,
                    name=request.POST['name'],
                    country=request.POST['country'],
                    type=request.POST['type'],
                    risk_score=request.POST['risk_score']
                )
                if updated_company:
                    messages.success(request, 'Company updated successfully!')
                    return redirect('company_list')
                else:
                    messages.error(request, 'Failed to update company.')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'crud/company_form.html', {'company': company, 'action': 'Edit'})

def company_delete(request, company_id):
    if request.method == 'POST':
        with Neo4jService() as neo4j:
            if neo4j.delete_company(company_id):
                messages.success(request, 'Company deleted successfully!')
            else:
                messages.error(request, 'Failed to delete company.')
    return redirect('company_list')

# Bank Account views
def bank_account_list(request):
    with Neo4jService() as neo4j:
        bank_accounts = neo4j.get_all_bank_accounts()
    return render(request, 'crud/bank_account_list.html', {'bank_accounts': bank_accounts})

def bank_account_create(request):
    if request.method == 'POST':
        try:
            with Neo4jService() as neo4j:
                bank_account = neo4j.create_bank_account(
                    id=request.POST['id'],
                    account_number=request.POST['account_number'],
                    bank_name=request.POST['bank_name'],
                    country=request.POST['country'],
                    currency=request.POST['currency']
                )
                if bank_account:
                    messages.success(request, 'Bank Account created successfully!')
                    return redirect('bank_account_list')
                else:
                    messages.error(request, 'Failed to create bank account.')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'crud/bank_account_form.html', {'action': 'Create'})

def bank_account_edit(request, account_id):
    with Neo4jService() as neo4j:
        bank_account = neo4j.get_bank_account(account_id)
        
        if not bank_account:
            messages.error(request, 'Bank Account not found.')
            return redirect('bank_account_list')
        
        if request.method == 'POST':
            try:
                updated_account = neo4j.update_bank_account(
                    id=account_id,
                    account_number=request.POST['account_number'],
                    bank_name=request.POST['bank_name'],
                    country=request.POST['country'],
                    currency=request.POST['currency']
                )
                if updated_account:
                    messages.success(request, 'Bank Account updated successfully!')
                    return redirect('bank_account_list')
                else:
                    messages.error(request, 'Failed to update bank account.')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'crud/bank_account_form.html', {'bank_account': bank_account, 'action': 'Edit'})

def bank_account_delete(request, account_id):
    if request.method == 'POST':
        with Neo4jService() as neo4j:
            if neo4j.delete_bank_account(account_id):
                messages.success(request, 'Bank Account deleted successfully!')
            else:
                messages.error(request, 'Failed to delete bank account.')
    return redirect('bank_account_list')

# Transaction views
def transaction_list(request):
    with Neo4jService() as neo4j:
        transactions = neo4j.get_all_transactions()
    return render(request, 'crud/transaction_list.html', {'transactions': transactions})

def transaction_create(request):
    if request.method == 'POST':
        try:
            with Neo4jService() as neo4j:
                transaction = neo4j.create_transaction(
                    id=request.POST['id'],
                    amount=request.POST['amount'],
                    date=request.POST['date'],
                    currency=request.POST['currency'],
                    suspicious_score=request.POST['suspicious_score']
                )
                if transaction:
                    messages.success(request, 'Transaction created successfully!')
                    return redirect('transaction_list')
                else:
                    messages.error(request, 'Failed to create transaction.')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'crud/transaction_form.html', {'action': 'Create'})

def transaction_edit(request, transaction_id):
    with Neo4jService() as neo4j:
        transaction = neo4j.get_transaction(transaction_id)
        
        if not transaction:
            messages.error(request, 'Transaction not found.')
            return redirect('transaction_list')
        
        if request.method == 'POST':
            try:
                updated_transaction = neo4j.update_transaction(
                    id=transaction_id,
                    amount=request.POST['amount'],
                    date=request.POST['date'],
                    currency=request.POST['currency'],
                    suspicious_score=request.POST['suspicious_score']
                )
                if updated_transaction:
                    messages.success(request, 'Transaction updated successfully!')
                    return redirect('transaction_list')
                else:
                    messages.error(request, 'Failed to update transaction.')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'crud/transaction_form.html', {'transaction': transaction, 'action': 'Edit'})

def transaction_delete(request, transaction_id):
    if request.method == 'POST':
        with Neo4jService() as neo4j:
            if neo4j.delete_transaction(transaction_id):
                messages.success(request, 'Transaction deleted successfully!')
            else:
                messages.error(request, 'Failed to delete transaction.')
    return redirect('transaction_list')

# Suspicious Transactions
def suspicious_transactions(request):
    with Neo4jService() as neo4j:
        transactions = neo4j.get_suspicious_transactions()
    return render(request, 'crud/suspicious_transactions.html', {'transactions': transactions})


