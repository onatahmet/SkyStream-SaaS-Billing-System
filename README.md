# SkyStream SaaS Billing System 🚀

**A scalable database architecture design for a SaaS billing and subscription management system.**

---

### 📌 Project Overview
SkyStream is a rapidly growing SaaS platform. This repository contains a robust database architecture designed to manage user subscriptions, recurring payments, and financial analytics with high precision.

Key engineering goals:
* **Data Integrity:** Ensuring consistency through relational constraints and Foreign Keys.
* **Audit Trail:** Comprehensive tracking of critical user actions for security and debugging.
* **Financial Analytics:** Providing a clean data structure to calculate business-critical metrics like MRR and Churn Rate.

---

### 🏗️ Database Architecture (ER Diagram)
The system's core structure is illustrated in the Entity-Relationship Diagram below:

![SkyStream ER Diagram](docs/ER.png)

#### Key Architectural Decisions:
* **`payments` Table:** Includes a `payment_status` field (e.g., success, failed, refunded) to ensure financial traceability.
* **`activity_logs` Table:** Utilizes `action_timestamp` to maintain a chronological record of system-wide modifications.
* **Relational Logic:** The `subscriptions` table serves as a central hub, bridging `users` and `account_plans` effectively.

---

### 📊 Analytical Metrics
This design is optimized to provide instant answers to key business questions using the following formulas:

1. **Monthly Recurring Revenue (MRR):**
$$MRR = \sum (\text{Price of all 'active' subscriptions})$$

2. **Customer Churn Rate:**
$$\text{Churn Rate} = \left( \frac{\text{Total Canceled Users in Period}}{\text{Total Active Users at Start of Period}} \right) \times 100$$

---

### 🛠️ Tech Stack & Roadmap
* **Design:** Draw.io
* **Database:** SQLite / MySQL (Implementation In Progress)
* **Data Generation:** Python & Faker (Implementation In Progress)

---

### 🧑‍💻 Developer
**Ahmet** - Computer Engineer / Aspiring Data Engineer