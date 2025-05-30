from neo4j import GraphDatabase
from django.conf import settings

class Neo4jService:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            settings.NEO4J_CONFIG['URI'],
            auth=(settings.NEO4J_CONFIG['USER'], settings.NEO4J_CONFIG['PASSWORD'])
        )

    def close(self):
        self.driver.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # Person CRUD operations
    def create_person(self, id, name, national_id, nationality, risk_score):
        with self.driver.session() as session:
            result = session.run(
                """
                CREATE (p:Person {
                    id: $id,
                    name: $name,
                    national_id: $national_id,
                    nationality: $nationality,
                    risk_score: $risk_score
                })
                RETURN p
                """,
                id=id, name=name, national_id=national_id,
                nationality=nationality, risk_score=float(risk_score)
            )
            record = result.single()
            return dict(record['p']) if record else None

    def get_person(self, id):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (p:Person {id: $id}) RETURN p",
                id=id
            )
            record = result.single()
            return dict(record['p']) if record else None

    def get_all_persons(self):
        with self.driver.session() as session:
            result = session.run("MATCH (p:Person) RETURN p")
            return [dict(record['p']) for record in result]

    def update_person(self, id, **properties):
        with self.driver.session() as session:
            # Convert risk_score to float if present
            if 'risk_score' in properties:
                properties['risk_score'] = float(properties['risk_score'])
            
            set_clause = ", ".join([f"p.{k} = ${k}" for k in properties.keys()])
            query = f"""
            MATCH (p:Person {{id: $id}})
            SET {set_clause}
            RETURN p
            """
            result = session.run(query, id=id, **properties)
            record = result.single()
            return dict(record['p']) if record else None

    def delete_person(self, id):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (p:Person {id: $id}) DELETE p RETURN count(p) as deleted",
                id=id
            )
            record = result.single()
            return record['deleted'] > 0 if record else False

    # Company CRUD operations
    def create_company(self, id, name, country, type, risk_score):
        with self.driver.session() as session:
            result = session.run(
                """
                CREATE (c:Company {
                    id: $id,
                    name: $name,
                    country: $country,
                    type: $type,
                    risk_score: $risk_score
                })
                RETURN c
                """,
                id=id, name=name, country=country,
                type=type, risk_score=float(risk_score)
            )
            record = result.single()
            return dict(record['c']) if record else None

    def get_company(self, id):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (c:Company {id: $id}) RETURN c",
                id=id
            )
            record = result.single()
            return dict(record['c']) if record else None

    def get_all_companies(self):
        with self.driver.session() as session:
            result = session.run("MATCH (c:Company) RETURN c")
            return [dict(record['c']) for record in result]

    def update_company(self, id, **properties):
        with self.driver.session() as session:
            if 'risk_score' in properties:
                properties['risk_score'] = float(properties['risk_score'])
            
            set_clause = ", ".join([f"c.{k} = ${k}" for k in properties.keys()])
            query = f"""
            MATCH (c:Company {{id: $id}})
            SET {set_clause}
            RETURN c
            """
            result = session.run(query, id=id, **properties)
            record = result.single()
            return dict(record['c']) if record else None

    def delete_company(self, id):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (c:Company {id: $id}) DELETE c RETURN count(c) as deleted",
                id=id
            )
            record = result.single()
            return record['deleted'] > 0 if record else False

    # BankAccount CRUD operations
    def create_bank_account(self, id, account_number, bank_name, country, currency):
        with self.driver.session() as session:
            result = session.run(
                """
                CREATE (a:BankAccount {
                    id: $id,
                    account_number: $account_number,
                    bank_name: $bank_name,
                    country: $country,
                    currency: $currency
                })
                RETURN a
                """,
                id=id, account_number=account_number, bank_name=bank_name,
                country=country, currency=currency
            )
            record = result.single()
            return dict(record['a']) if record else None

    def get_bank_account(self, id):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (a:BankAccount {id: $id}) RETURN a",
                id=id
            )
            record = result.single()
            return dict(record['a']) if record else None

    def get_all_bank_accounts(self):
        with self.driver.session() as session:
            result = session.run("MATCH (a:BankAccount) RETURN a")
            return [dict(record['a']) for record in result]

    def update_bank_account(self, id, **properties):
        with self.driver.session() as session:
            set_clause = ", ".join([f"a.{k} = ${k}" for k in properties.keys()])
            query = f"""
            MATCH (a:BankAccount {{id: $id}})
            SET {set_clause}
            RETURN a
            """
            result = session.run(query, id=id, **properties)
            record = result.single()
            return dict(record['a']) if record else None

    def delete_bank_account(self, id):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (a:BankAccount {id: $id}) DELETE a RETURN count(a) as deleted",
                id=id
            )
            record = result.single()
            return record['deleted'] > 0 if record else False

    # Transaction CRUD operations
    def create_transaction(self, id, amount, date, currency, suspicious_score):
        with self.driver.session() as session:
            result = session.run(
                """
                CREATE (t:Transaction {
                    id: $id,
                    amount: $amount,
                    date: date($date),
                    currency: $currency,
                    suspicious_score: $suspicious_score
                })
                RETURN t
                """,
                id=id, amount=float(amount), date=date,
                currency=currency, suspicious_score=float(suspicious_score)
            )
            record = result.single()
            if record:
                transaction = dict(record['t'])
                # Convert Neo4j date to string for JSON serialization
                if 'date' in transaction:
                    transaction['date'] = str(transaction['date'])
                return transaction
            return None

    def get_transaction(self, id):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (t:Transaction {id: $id}) RETURN t",
                id=id
            )
            record = result.single()
            if record:
                transaction = dict(record['t'])
                if 'date' in transaction:
                    transaction['date'] = str(transaction['date'])
                return transaction
            return None

    def get_all_transactions(self):
        with self.driver.session() as session:
            result = session.run("MATCH (t:Transaction) RETURN t")
            transactions = []
            for record in result:
                transaction = dict(record['t'])
                if 'date' in transaction:
                    transaction['date'] = str(transaction['date'])
                transactions.append(transaction)
            return transactions

    def update_transaction(self, id, **properties):
        with self.driver.session() as session:
            if 'amount' in properties:
                properties['amount'] = float(properties['amount'])
            if 'suspicious_score' in properties:
                properties['suspicious_score'] = float(properties['suspicious_score'])
            if 'date' in properties:
                # Handle date conversion if needed
                pass
            
            set_clause = ", ".join([f"t.{k} = ${k}" for k in properties.keys()])
            query = f"""
            MATCH (t:Transaction {{id: $id}})
            SET {set_clause}
            RETURN t
            """
            result = session.run(query, id=id, **properties)
            record = result.single()
            if record:
                transaction = dict(record['t'])
                if 'date' in transaction:
                    transaction['date'] = str(transaction['date'])
                return transaction
            return None

    def delete_transaction(self, id):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (t:Transaction {id: $id}) DELETE t RETURN count(t) as deleted",
                id=id
            )
            record = result.single()
            return record['deleted'] > 0 if record else False

    def get_suspicious_transactions(self, threshold=0.8):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (sender:Person)-[:OWNS]->(s:BankAccount)-[:SENDS]->(t:Transaction)-[:TO]->(r:BankAccount)<-[:OWNS]-(receiver:Person)
                WHERE t.suspicious_score > $threshold
                RETURN sender.name AS from, receiver.name AS to, t.amount AS amount, 
                       t.suspicious_score AS score, t.date AS date, t.currency AS currency
                """,
                threshold=float(threshold)
            )
            transactions = []
            for record in result:
                transaction = {
                    'from': record['from'],
                    'to': record['to'],
                    'amount': record['amount'],
                    'score': record['score'],
                    'date': str(record['date']) if record['date'] else None,
                    'currency': record['currency']
                }
                transactions.append(transaction)
            return transactions 
        
    def get_person_relations(self, person_id):
        """Get all relations for a specific person for graph visualization"""
        with self.driver.session() as session:
            # Get the complete network around a person
            result = session.run(
                """
                MATCH (p:Person {id: $person_id})
                OPTIONAL MATCH (p)-[:OWNS]->(a:BankAccount)
                OPTIONAL MATCH (a)-[:SENDS]->(t:Transaction)
                OPTIONAL MATCH (t)-[:TO]->(a2:BankAccount)
                OPTIONAL MATCH (a2)<-[:OWNS]-(p2:Person)
                OPTIONAL MATCH (p)-[:WORKS_FOR]->(c:Company)
                RETURN p, a, t, a2, p2, c
                """,
                person_id=person_id
            )
            
            nodes = {}
            links = []
            
            for record in result:
                # Add person node
                if record['p']:
                    person = dict(record['p'])
                    nodes[person['id']] = {
                        'id': person['id'],
                        'type': 'Person',
                        'label': person['name'],
                        'details': f"Risk: {person.get('risk_score', 'N/A')}\nNationality: {person.get('nationality', 'N/A')}",
                        'risk_score': person.get('risk_score', 0)
                    }
                
                # Add bank account node
                if record['a']:
                    account = dict(record['a'])
                    nodes[account['id']] = {
                        'id': account['id'],
                        'type': 'BankAccount',
                        'label': f"{account['bank_name']}\n{account['account_number'][:8]}...",
                        'details': f"Bank: {account['bank_name']}\nCountry: {account['country']}\nCurrency: {account['currency']}"
                    }
                    
                    # Add OWNS relationship
                    if record['p']:
                        links.append({
                            'source': person['id'],
                            'target': account['id'],
                            'type': 'OWNS'
                        })
                
                # Add transaction node
                if record['t']:
                    transaction = dict(record['t'])
                    transaction_date = str(transaction['date']) if transaction.get('date') else 'N/A'
                    nodes[transaction['id']] = {
                        'id': transaction['id'],
                        'type': 'Transaction',
                        'label': f"${transaction['amount']}\n{transaction_date}",
                        'details': f"Amount: ${transaction['amount']}\nDate: {transaction_date}\nSuspicious: {transaction.get('suspicious_score', 'N/A')}",
                        'suspicious_score': transaction.get('suspicious_score', 0)
                    }
                    
                    # Add SENDS relationship
                    if record['a']:
                        links.append({
                            'source': account['id'],
                            'target': transaction['id'],
                            'type': 'SENDS'
                        })
                
                # Add receiving bank account
                if record['a2'] and record['a2']['id'] != record['a']['id'] if record['a'] else True:
                    account2 = dict(record['a2'])
                    nodes[account2['id']] = {
                        'id': account2['id'],
                        'type': 'BankAccount',
                        'label': f"{account2['bank_name']}\n{account2['account_number'][:8]}...",
                        'details': f"Bank: {account2['bank_name']}\nCountry: {account2['country']}\nCurrency: {account2['currency']}"
                    }
                    
                    # Add TO relationship
                    if record['t']:
                        links.append({
                            'source': transaction['id'],
                            'target': account2['id'],
                            'type': 'TO'
                        })
                
                # Add receiving person
                if record['p2'] and record['p2']['id'] != person_id:
                    person2 = dict(record['p2'])
                    nodes[person2['id']] = {
                        'id': person2['id'],
                        'type': 'Person',
                        'label': person2['name'],
                        'details': f"Risk: {person2.get('risk_score', 'N/A')}\nNationality: {person2.get('nationality', 'N/A')}",
                        'risk_score': person2.get('risk_score', 0)
                    }
                    
                    # Add OWNS relationship for receiving person
                    if record['a2']:
                        links.append({
                            'source': person2['id'],
                            'target': account2['id'],
                            'type': 'OWNS'
                        })
                
                # Add company node
                if record['c']:
                    company = dict(record['c'])
                    nodes[company['id']] = {
                        'id': company['id'],
                        'type': 'Company',
                        'label': company['name'],
                        'details': f"Type: {company.get('type', 'N/A')}\nCountry: {company.get('country', 'N/A')}\nRisk: {company.get('risk_score', 'N/A')}"
                    }
                    
                    # Add WORKS_FOR relationship
                    links.append({
                        'source': person['id'],
                        'target': company['id'],
                        'type': 'WORKS_FOR'
                    })
            
            return {
                'nodes': list(nodes.values()),
                'links': links
            }

    def get_suspicious_network(self, threshold=0.8, limit=20, analysis_type='network'):
        """Get suspicious transactions network for graph visualization"""
        with self.driver.session() as session:
            # Get suspicious transactions with full context
            result = session.run(
                """
                MATCH (sender:Person)-[:OWNS]->(s:BankAccount)-[:SENDS]->(t:Transaction)-[:TO]->(r:BankAccount)<-[:OWNS]-(receiver:Person)
                WHERE t.suspicious_score > $threshold
                RETURN sender, s, t, r, receiver
                ORDER BY t.suspicious_score DESC
                LIMIT $limit
                """,
                threshold=float(threshold), limit=int(limit)
            )
            
            nodes = {}
            links = []
            
            for record in result:
                # Add sender person
                if record['sender']:
                    sender = dict(record['sender'])
                    nodes[sender['id']] = {
                        'id': sender['id'],
                        'type': 'Person',
                        'label': sender['name'],
                        'details': f"Risk: {sender.get('risk_score', 'N/A')}\nNationality: {sender.get('nationality', 'N/A')}",
                        'risk_score': sender.get('risk_score', 0)
                    }
                
                # Add sender bank account
                if record['s']:
                    s_account = dict(record['s'])
                    nodes[s_account['id']] = {
                        'id': s_account['id'],
                        'type': 'BankAccount',
                        'label': f"{s_account['bank_name']}\n{s_account['account_number'][:8]}...",
                        'details': f"Bank: {s_account['bank_name']}\nCountry: {s_account['country']}\nCurrency: {s_account['currency']}"
                    }
                    
                    # Add OWNS relationship (sender -> account)
                    if record['sender']:
                        links.append({
                            'source': sender['id'],
                            'target': s_account['id'],
                            'type': 'OWNS'
                        })
                
                # Add transaction
                if record['t']:
                    transaction = dict(record['t'])
                    transaction_date = str(transaction['date']) if transaction.get('date') else 'N/A'
                    nodes[transaction['id']] = {
                        'id': transaction['id'],
                        'type': 'Transaction',
                        'label': f"${transaction['amount']}\n{transaction_date}",
                        'details': f"Amount: ${transaction['amount']}\nDate: {transaction_date}\nSuspicious: {transaction.get('suspicious_score', 'N/A')}",
                        'suspicious_score': transaction.get('suspicious_score', 0),
                        'amount': transaction.get('amount', 0)
                    }
                    
                    # Add SENDS relationship (account -> transaction)
                    if record['s']:
                        links.append({
                            'source': s_account['id'],
                            'target': transaction['id'],
                            'type': 'SENDS',
                            'suspicious_score': transaction.get('suspicious_score', 0)
                        })
                
                # Add receiver bank account
                if record['r']:
                    r_account = dict(record['r'])
                    nodes[r_account['id']] = {
                        'id': r_account['id'],
                        'type': 'BankAccount',
                        'label': f"{r_account['bank_name']}\n{r_account['account_number'][:8]}...",
                        'details': f"Bank: {r_account['bank_name']}\nCountry: {r_account['country']}\nCurrency: {r_account['currency']}"
                    }
                    
                    # Add TO relationship (transaction -> account)
                    if record['t']:
                        links.append({
                            'source': transaction['id'],
                            'target': r_account['id'],
                            'type': 'TO',
                            'suspicious_score': transaction.get('suspicious_score', 0)
                        })
                
                # Add receiver person
                if record['receiver']:
                    receiver = dict(record['receiver'])
                    nodes[receiver['id']] = {
                        'id': receiver['id'],
                        'type': 'Person',
                        'label': receiver['name'],
                        'details': f"Risk: {receiver.get('risk_score', 'N/A')}\nNationality: {receiver.get('nationality', 'N/A')}",
                        'risk_score': receiver.get('risk_score', 0)
                    }
                    
                    # Add OWNS relationship (receiver -> account)
                    if record['r']:
                        links.append({
                            'source': receiver['id'],
                            'target': r_account['id'],
                            'type': 'OWNS'
                        })
            
            return {
                'nodes': list(nodes.values()),
                'links': links
            }
        
