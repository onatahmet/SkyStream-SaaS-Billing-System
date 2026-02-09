
PRAGMA foreign_keys = ON;
/*
users tablosu kullanıcının kullanıcı adını,mailini aynı zamanda kayıt oldugu tarıhı tutuyoruz
*/

CREATE TABLE IF NOT EXISTS "users" (
   id INTEGER,
   user_name TEXT NOT NULL UNIQUE,
   email TEXT NOT NULL UNIQUE,
   creation_date TEXT DEFAULT CURRENT_TIMESTAMP ,
   PRIMARY KEY ("id")
);
/*
account_plans tablosu planları,planların fiyatlarinı,suresini gosteren bir tablodur
plan name check ile gırısler kısıtlanmıstır.mevcut planlar basıt standart ve premıumdur

*/
CREATE TABLE IF NOT EXISTS "account_plans"(
   id INTEGER,
   plan_name TEXT CHECK(plan_name IN ('free','standart','premium')),
   price REAL CHECK(price>=0), 
   duration_month INTEGER NOT NULL,
   PRIMARY KEY("id")
);
/*
subscriptions tablosu aboneliklerin baslangıc tarıhı btis tarihi ve su an guncel abonelık durumunu tutar
status active ve passive degerlerini alır ,
aynı zamanda subscrptions tablosunda user_id ve plans_id foreıgn keylerı kullanılmıstır.
*/
CREATE TABLE IF NOT EXISTS "subscriptions"(
   id INTEGER,
   user_id INTEGER,
   plans_id INTEGER,
   start_date TEXT NOT NULL,
   end_date TEXT NOT NULL CHECK(end_date>start_date),
   status TEXT CHECK(status IN ('active','passive')),
   PRIMARY KEY("id")
   FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE CASCADE,
   FOREIGN KEY ("plans_id") REFERENCES "account_plans"("id") ON DELETE CASCADE
);
/*
payments tablosunda odeme tutartları odeme zamanı odenıp odenmedıgı bılgılerı saklanır odenme durumu check ile kısıtlanmıstır.
aynı zamanda subs_id foregın keyi kullanılmıstır.
*/
CREATE TABLE IF NOT EXISTS "payments"(
   id INTEGER ,
   subs_id INTEGER,
   amount REAL,
   payment_date TEXT DEFAULT CURRENT_TIMESTAMP,
   payment_status TEXT CHECK(payment_status IN ('paid','unpaid')),
   PRIMARY KEY("id"),
   FOREIGN KEY ("subs_id") REFERENCES "subscriptions"("id") ON DELETE CASCADE

);
/*
activity_logs tablosunda kullanıcı aktivitelerini gormek ıcın olusturulmustur
*/
CREATE TABLE IF NOT EXISTS "activity_logs"(
   id INTEGER,
   user_id INTEGER,
   action_type TEXT NOT NULL CHECK (action_type IN ('login','logout','plan_change','payment_failed')),
   action_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
   descriptions TEXT,
   PRIMARY KEY("id"),
   FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE CASCADE 
);

CREATE VIEW "user_summary" AS
SELECT "user_name","email","plan_name" FROM "users"
JOIN
"subscriptions" ON "users"."id" = "subscriptions"."user_id"
JOIN 
"account_plans" ON "subscriptions"."plans_id" = "account_plans"."id"
;

CREATE INDEX "subs_index" 
ON "subscriptions"("user_id")
;

CREATE INDEX  "payments_index"
ON "payments"("subs_id")
;

CREATE TRIGGER "log_plan_change"
AFTER UPDATE OF "plans_id" ON "subscriptions" -- Sadece plans_id değişirse çalışır
FOR EACH ROW
BEGIN
    INSERT INTO "activity_logs" ("user_id", "action_type", "descriptions")
    VALUES (
        NEW.user_id, 
        'plan_change', 
        'Kullanıcı planını ' || OLD.plans_id || ' IDli plandan ' || NEW.plans_id || ' IDli plana yükseltti.'
    );
END;

CREATE TRIGGER "log_payment_failure"
AFTER INSERT ON "payments"
FOR EACH ROW
WHEN NEW.payment_status = 'unpaid' -- Sadece ödeme yapılmadıysa çalış
BEGIN
    INSERT INTO "activity_logs" ("user_id", "action_type", "descriptions")
    VALUES (
        (SELECT user_id FROM subscriptions WHERE id = NEW.subs_id), -- subs_id üzerinden user_id'yi çekiyoruz
        'payment_failed',
        'Abonelik ID: ' || NEW.subs_id || ' için ' || NEW.amount || ' tutarındaki ödeme başarısız oldu.'
    );
END;
