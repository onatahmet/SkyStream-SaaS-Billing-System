Project Overview
SkyStream is a rapidly growing SaaS platform. This repository contains the core database architecture designed to manage user subscriptions, recurring payments, and financial analytics with high precision.

The primary goals of this architecture are:

Data Integrity: Ensuring consistency through robust relational constraints and Foreign Keys.

Audit Trail: Comprehensive tracking of critical user actions for security and debugging.

Financial Analytics: Providing the underlying data structure to calculate business metrics like MRR and Churn Rate.

Database Architecture (ER Diagram)
The system's core structure is illustrated in the Entity-Relationship Diagram below:

Key Architectural Decisions:
payments Table: Includes a payment_status field (e.g., success, failed, refunded) to ensure financial traceability.

activity_logs Table: Utilizes action_timestamp to maintain a chronological record of system-wide modifications.

Relationship Logic: The subscriptions table serves as a central hub, effectively bridging users and account_plans.

Tech Stack & Roadmap
Design: Draw.io

Database: SQLite / MySQL (Implementation In Progress)

Data Generation: Python & Faker (Implementation In Progress)