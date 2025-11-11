# Week5 - Assignment

## **Task 2: Create database and table in your MySQL server**

#### 👾Create a new database named website. & Create a new table named member

```bash
mysql> CREATE DATABASE website;
Query OK, 1 row affected (0.01 sec)

mysql> USE website;
Database changed

mysql> CREATE TABLE member (
	id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(255) NOT NULL,
	email VARCHAR(255) NOT NULL,
	password VARCHAR(255) NOT NULL,
	follower_count INT UNSIGNED NOT NULL DEFAULT 0,
	time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
Query OK, 0 rows affected (0.02 sec)

mysql> DESC member;
+----------------+--------------+------+-----+-------------------+-------------------+
| Field          | Type         | Null | Key | Default           | Extra             |
+----------------+--------------+------+-----+-------------------+-------------------+
| id             | int          | NO   | PRI | NULL              | auto_increment    |
| name           | varchar(255) | NO   |     | NULL              |                   |
| email          | varchar(255) | NO   |     | NULL              |                   |
| password       | varchar(255) | NO   |     | NULL              |                   |
| follower_count | int unsigned | NO   |     | 0                 |                   |
| time           | datetime     | NO   |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
+----------------+--------------+------+-----+-------------------+-------------------+
6 rows in set (0.00 sec)
```

![image.png](https://github.com/eriiic0225/wehelp_phase1/blob/main/week5/screenshots/task2.png)

## **Task 3: SQL CRUD**

#### 👾INSERT a new row to the member table where name, email and password must be set to test ,test@test.com, and test. INSERT additional 4 rows with arbitrary data.

```bash
mysql> INSERT INTO member (name, email, password) VALUES('test', 'test@test.com', 'test');
Query OK, 1 row affected (0.05 sec)

mysql> INSERT INTO member (name, email, password) VALUES('test2', 'test2@test.com', 'test2');
Query OK, 1 row affected (0.00 sec)

mysql>
mysql> INSERT INTO member (name, email, password) VALUES('test3', 'test3@test.com', 'test3');
Query OK, 1 row affected (0.00 sec)

mysql>
mysql> INSERT INTO member (name, email, password) VALUES('test4', 'test4@test.com', 'test4');
Query OK, 1 row affected (0.00 sec)

mysql>
mysql> INSERT INTO member (name, email, password) VALUES('test5', 'test5@test.com', 'test5');
Query OK, 1 row affected (0.00 sec)
```

![image.png](https://github.com/eriiic0225/wehelp_phase1/blob/main/week5/screenshots/task3-1.png)

---

#### 👾SELECT all rows from the member table.

```bash
mysql> SELECT * FROM member;
+----+-------+----------------+----------+----------------+---------------------+
| id | name  | email          | password | follower_count | time                |
+----+-------+----------------+----------+----------------+---------------------+
|  1 | test  | test@test.com  | test     |              0 | 2025-11-11 13:47:03 |
|  2 | test2 | test2@test.com | test2    |              0 | 2025-11-11 13:48:21 |
|  3 | test3 | test3@test.com | test3    |              0 | 2025-11-11 13:48:21 |
|  4 | test4 | test4@test.com | test4    |              0 | 2025-11-11 13:48:21 |
|  5 | test5 | test5@test.com | test5    |              0 | 2025-11-11 13:48:23 |
+----+-------+----------------+----------+----------------+---------------------+
5 rows in set (0.01 sec)
```

![image.png](https://github.com/eriiic0225/wehelp_phase1/blob/main/week5/screenshots/task3-2.png)

---

#### 👾SELECT all rows from the member table, in descending order of time.

```bash
mysql> SELECT * FROM member ORDER BY time DESC;
+----+-------+----------------+----------+----------------+---------------------+
| id | name  | email          | password | follower_count | time                |
+----+-------+----------------+----------+----------------+---------------------+
|  5 | test5 | test5@test.com | test5    |              0 | 2025-11-11 13:48:23 |
|  2 | test2 | test2@test.com | test2    |              0 | 2025-11-11 13:48:21 |
|  3 | test3 | test3@test.com | test3    |              0 | 2025-11-11 13:48:21 |
|  4 | test4 | test4@test.com | test4    |              0 | 2025-11-11 13:48:21 |
|  1 | test  | test@test.com  | test     |              0 | 2025-11-11 13:47:03 |
+----+-------+----------------+----------+----------------+---------------------+
5 rows in set (0.01 sec)
```

![image.png](https://github.com/eriiic0225/wehelp_phase1/blob/main/week5/screenshots/task3-3.png)

---

#### 👾SELECT total 3 rows, second to fourth, from the member table, in descending order of time. Note: it does not mean SELECT rows where id are 2, 3, or 4.

```bash
mysql> SELECT * FROM member ORDER BY time DESC LIMIT 3 OFFSET 1;
+----+-------+----------------+----------+----------------+---------------------+
| id | name  | email          | password | follower_count | time                |
+----+-------+----------------+----------+----------------+---------------------+
|  2 | test2 | test2@test.com | test2    |              0 | 2025-11-11 13:48:21 |
|  3 | test3 | test3@test.com | test3    |              0 | 2025-11-11 13:48:21 |
|  4 | test4 | test4@test.com | test4    |              0 | 2025-11-11 13:48:21 |
+----+-------+----------------+----------+----------------+---------------------+
3 rows in set (0.00 sec)
```

![image.png](https://github.com/eriiic0225/wehelp_phase1/blob/main/week5/screenshots/task3-4.png)

---

#### 👾SELECT rows where email equals to test@test.com.

```bash
mysql> SELECT * FROM member WHERE email='test@test.com';
+----+------+---------------+----------+----------------+---------------------+
| id | name | email         | password | follower_count | time                |
+----+------+---------------+----------+----------------+---------------------+
|  1 | test | test@test.com | test     |              0 | 2025-11-11 13:47:03 |
+----+------+---------------+----------+----------------+---------------------+
1 row in set (0.04 sec)
```

![image.png](https://github.com/eriiic0225/wehelp_phase1/blob/main/week5/screenshots/task3-5.png)

---

#### 👾SELECT rows where name includes the es keyword.

###### 💡<方法一> `like` %

```bash
mysql> SELECT * FROM member WHERE name LIKE '%es%';
+----+-------+----------------+----------+----------------+---------------------+
| id | name  | email          | password | follower_count | time                |
+----+-------+----------------+----------+----------------+---------------------+
|  1 | test  | test@test.com  | test     |              0 | 2025-11-11 13:47:03 |
|  2 | test2 | test2@test.com | test2    |              0 | 2025-11-11 13:48:21 |
|  3 | test3 | test3@test.com | test3    |              0 | 2025-11-11 13:48:21 |
|  4 | test4 | test4@test.com | test4    |              0 | 2025-11-11 13:48:21 |
|  5 | test5 | test5@test.com | test5    |              0 | 2025-11-11 13:48:23 |
+----+-------+----------------+----------+----------------+---------------------+
5 rows in set (0.00 sec)
```

![image.png](https://github.com/eriiic0225/wehelp_phase1/blob/main/week5/screenshots/task3-6.1.png)

###### 💡<方法二> `REGEXP` 正則表達式

```bash
mysql> SELECT * FROM member WHERE name REGEXP 'es';
+----+-------+----------------+----------+----------------+---------------------+
| id | name  | email          | password | follower_count | time                |
+----+-------+----------------+----------+----------------+---------------------+
|  1 | test  | test@test.com  | test     |              0 | 2025-11-11 13:47:03 |
|  2 | test2 | test2@test.com | test2    |              0 | 2025-11-11 13:48:21 |
|  3 | test3 | test3@test.com | test3    |              0 | 2025-11-11 13:48:21 |
|  4 | test4 | test4@test.com | test4    |              0 | 2025-11-11 13:48:21 |
|  5 | test5 | test5@test.com | test5    |              0 | 2025-11-11 13:48:23 |
+----+-------+----------------+----------+----------------+---------------------+
5 rows in set (0.01 sec)
```

![image.png](https://github.com/eriiic0225/wehelp_phase1/blob/main/week5/screenshots/task3-6.2.png)

###### 💡<方法三> `INSTR()` 函數

```bash
mysql> SELECT * FROM member WHERE INSTR(name, 'es') > 0;
+----+-------+----------------+----------+----------------+---------------------+
| id | name  | email          | password | follower_count | time                |
+----+-------+----------------+----------+----------------+---------------------+
|  1 | test  | test@test.com  | test     |              0 | 2025-11-11 13:47:03 |
|  2 | test2 | test2@test.com | test2    |              0 | 2025-11-11 13:48:21 |
|  3 | test3 | test3@test.com | test3    |              0 | 2025-11-11 13:48:21 |
|  4 | test4 | test4@test.com | test4    |              0 | 2025-11-11 13:48:21 |
|  5 | test5 | test5@test.com | test5    |              0 | 2025-11-11 13:48:23 |
+----+-------+----------------+----------+----------------+---------------------+
5 rows in set (0.00 sec)
```

![image.png](https://github.com/eriiic0225/wehelp_phase1/blob/main/week5/screenshots/task3-6.3.png)

---

#### 👾SELECT rows where email equals to test@test.com and password equals to test.

```bash
mysql> SELECT * FROM member WHERE email='test@test.com' AND password='test';
+----+------+---------------+----------+----------------+---------------------+
| id | name | email         | password | follower_count | time                |
+----+------+---------------+----------+----------------+---------------------+
|  1 | test | test@test.com | test     |              0 | 2025-11-11 13:47:03 |
+----+------+---------------+----------+----------------+---------------------+
1 row in set (0.00 sec)
```

![image.png](https://github.com/eriiic0225/wehelp_phase1/blob/main/week5/screenshots/task3-7.png)

---

#### 👾UPDATE data in name column to test2 where email equals to test@test.com.

```bash
mysql> UPDATE member SET name='test2' WHERE email='test@test.com';
Query OK, 1 row affected (0.04 sec)
Rows matched: 1  Changed: 1  Warnings: 0
```

![image.png](https://github.com/eriiic0225/wehelp_phase1/blob/main/week5/screenshots/task3-8.png)

## **Task 4: SQL Aggregation Functions**

#### 👾SELECT how many rows from the member table.

```bash
mysql> SELECT COUNT(*) FROM member;
+----------+
| COUNT(*) |
+----------+
|        5 |
+----------+
1 row in set (0.04 sec)
```

![image.png](https://github.com/eriiic0225/wehelp_phase1/blob/main/week5/screenshots/task4-1.png)

---

#### 👾SELECT the sum of follower_count of all the rows from the member table.

```bash
mysql> SELECT SUM(follower_count) FROM member;
+---------------------+
| SUM(follower_count) |
+---------------------+
|                 500 |
+---------------------+
1 row in set (0.01 sec)
```

![image.png](https://github.com/eriiic0225/wehelp_phase1/blob/main/week5/screenshots/task4-2.png)

---

#### 👾SELECT the average of follower_count of all the rows from the member table.

```bash
mysql> SELECT AVG(follower_count) FROM member;
+---------------------+
| AVG(follower_count) |
+---------------------+
|            100.0000 |
+---------------------+
1 row in set (0.01 sec)
```

![image.png](https://github.com/eriiic0225/wehelp_phase1/blob/main/week5/screenshots/task4-3.png)

---

#### 👾SELECT the average of follower_count of the first 2 rows, in descending order of follower_count, from the member table.

```bash
mysql> SELECT AVG(follower_count) FROM (SELECT follower_count FROM member ORDER BY follower_count DESC LIMIT 2) AS TOP2_AVG;
+---------------------+
| AVG(follower_count) |
+---------------------+
|            115.0000 |
+---------------------+
1 row in set (0.01 sec)

-------------------

mysql> SELECT AVG(follower_count) FROM (SELECT * FROM member ORDER BY follower_count DESC
LIMIT 2) AS TOP2_AVG;
+---------------------+
| AVG(follower_count) |
+---------------------+
|            115.0000 |
+---------------------+
1 row in set (0.00 sec)
```

![image.png](https://github.com/eriiic0225/wehelp_phase1/blob/main/week5/screenshots/task4-4.png)

## **Task 5: SQL JOIN**

#### 👾Create a new table named message , in the website database.

```bash
mysql> CREATE TABLE message(
    -> id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    -> member_id INT NOT NULL,
    -> content TEXT NOT NULL,
    -> like_count INT UNSIGNED NOT NULL DEFAULT 0,
    -> time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -> FOREIGN KEY (member_id) REFERENCES member(id)
    -> );
Query OK, 0 rows affected (0.06 sec)

mysql> DESC message;
+------------+--------------+------+-----+-------------------+-------------------+
| Field      | Type         | Null | Key | Default           | Extra             |
+------------+--------------+------+-----+-------------------+-------------------+
| id         | int unsigned | NO   | PRI | NULL              | auto_increment    |
| member_id  | int          | NO   | MUL | NULL              |                   |
| content    | text         | NO   |     | NULL              |                   |
| like_count | int unsigned | NO   |     | 0                 |                   |
| time       | datetime     | NO   |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
+------------+--------------+------+-----+-------------------+-------------------+
5 rows in set (0.02 sec)
```

![image.png](https://github.com/eriiic0225/wehelp_phase1/blob/main/week5/screenshots/task5-1.png)

**_<填入資料內容如下>_**

```bash
mysql> SELECT * FROM message;
+----+-----------+--------------+------------+---------------------+
| id | member_id | content      | like_count | time                |
+----+-----------+--------------+------------+---------------------+
|  1 |         1 | hello!       |         80 | 2025-11-11 21:35:44 |
|  2 |         2 | Hi!          |        100 | 2025-11-11 21:36:07 |
|  3 |         3 | Hello World! |        120 | 2025-11-11 21:36:31 |
|  4 |         4 | Hola!        |         90 | 2025-11-11 21:37:14 |
|  5 |         1 | 你好!        |        110 | 2025-11-11 21:37:34 |
|  6 |         5 | Bonjour!     |        100 | 2025-11-11 21:38:30 |
+----+-----------+--------------+------------+---------------------+
6 rows in set (0.00 sec)
```

---

#### 👾SELECT all messages, including sender names. We have to JOIN the member table to get that.

```bash
mysql> SELECT member.name, message.content FROM member INNER JOIN message on member.id = message.member_id;
+-------+--------------+
| name  | content      |
+-------+--------------+
| test2 | hello!       |
| test2 | 你好!        |
| test2 | Hi!          |
| test3 | Hello World! |
| test4 | Hola!        |
| test5 | Bonjour!     |
+-------+--------------+
6 rows in set (0.00 sec)
```

![image.png](https://github.com/eriiic0225/wehelp_phase1/blob/main/week5/screenshots/task5-2.png)

---

#### 👾SELECT all messages, including sender names, where sender email equals to test@test.com . We have to JOIN the member table to filter and get that.

```bash
mysql> SELECT member.name, message.content, member.email FROM member INNER JOIN message on member.id = message.member_id WHERE member.email='test@test.com';
+-------+---------+---------------+
| name  | content | email         |
+-------+---------+---------------+
| test2 | hello!  | test@test.com |
| test2 | 你好!   | test@test.com |
+-------+---------+---------------+
2 rows in set (0.00 sec)
```

![image.png](https://github.com/eriiic0225/wehelp_phase1/blob/main/week5/screenshots/task5-3.png)

---

#### 👾Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages where sender email equals to test@test.com .

```bash
mysql> SELECT AVG(like_count)
    -> FROM member INNER JOIN message
    -> on member.id = message.member_id
    -> WHERE member.email='test@test.com';
+-----------------+
| AVG(like_count) |
+-----------------+
|         95.0000 |
+-----------------+
1 row in set (0.00 sec)
```

![image.png](https://github.com/eriiic0225/wehelp_phase1/blob/main/week5/screenshots/task5-4.png)

---

#### 👾Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages GROUP BY sender email.

```bash
mysql> SELECT member.email, AVG(like_count) AS avg_like
    -> FROM member INNER JOIN message on member.id = message.member_id
    -> GROUP BY member.email;
+----------------+----------+
| email          | avg_like |
+----------------+----------+
| test@test.com  |  95.0000 |
| test2@test.com | 100.0000 |
| test3@test.com | 120.0000 |
| test4@test.com |  90.0000 |
| test5@test.com | 100.0000 |
+----------------+----------+
5 rows in set (0.00 sec)
```

![image.png](https://github.com/eriiic0225/wehelp_phase1/blob/main/week5/screenshots/task5-5.png)
