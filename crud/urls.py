from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Person URLs
    path('persons/', views.person_list, name='person_list'),
    path('persons/create/', views.person_create, name='person_create'),
    path('persons/<str:person_id>/edit/', views.person_edit, name='person_edit'),
    path('persons/<str:person_id>/delete/', views.person_delete, name='person_delete'),
    
    # Company URLs
    path('companies/', views.company_list, name='company_list'),
    path('companies/create/', views.company_create, name='company_create'),
    path('companies/<str:company_id>/edit/', views.company_edit, name='company_edit'),
    path('companies/<str:company_id>/delete/', views.company_delete, name='company_delete'),
    
    # Bank Account URLs
    path('bank-accounts/', views.bank_account_list, name='bank_account_list'),
    path('bank-accounts/create/', views.bank_account_create, name='bank_account_create'),
    path('bank-accounts/<str:account_id>/edit/', views.bank_account_edit, name='bank_account_edit'),
    path('bank-accounts/<str:account_id>/delete/', views.bank_account_delete, name='bank_account_delete'),
    
    # Transaction URLs
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/create/', views.transaction_create, name='transaction_create'),
    path('transactions/<str:transaction_id>/edit/', views.transaction_edit, name='transaction_edit'),
    path('transactions/<str:transaction_id>/delete/', views.transaction_delete, name='transaction_delete'),
    
    # Suspicious Transactions
    path('suspicious-transactions/', views.suspicious_transactions, name='suspicious_transactions'),
    
    # Neo4j Queries Reference
    path('neo4j-queries/', views.neo4j_queries, name='neo4j_queries'),
    
    # Person Relations
    path('person-relations/', views.person_relations, name='person_relations'),
    path('person-relations-data/<str:person_id>/', views.person_relations_data, name='person_relations_data'),
    
    # Suspicious Network API
    path('suspicious-network-data/', views.suspicious_network_data, name='suspicious_network_data'),
] 