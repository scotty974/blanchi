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