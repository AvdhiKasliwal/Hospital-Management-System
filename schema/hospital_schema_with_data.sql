DROP DATABASE IF EXISTS hospital_db;
CREATE DATABASE hospital_db;
USE hospital_db;

CREATE TABLE IF NOT EXISTS rooms (
  id INT AUTO_INCREMENT PRIMARY KEY,
  room_number VARCHAR(50),
  type VARCHAR(50),
  status VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS doctors (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(200),
  specialization VARCHAR(200),
  phone VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS patients (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(200),
  age INT,
  gender VARCHAR(20),
  disease VARCHAR(255),
  room_id INT,
  doctor_id INT,
  FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE SET NULL,
  FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE SET NULL
);

INSERT INTO rooms (room_number, type, status) VALUES
  ('101', 'General', 'Occupied'),
  ('102', 'ICU', 'Vacant'),
  ('103', 'Private', 'Occupied');

INSERT INTO doctors (name, specialization, phone) VALUES
  ('Dr. Neha Sharma','Cardiology','9876543210'),
  ('Dr. Raj Mehta','Orthopedics','9876509876'),
  ('Dr. Priya Nair','Dermatology','9867123456');

INSERT INTO patients (name, age, gender, disease, room_id, doctor_id) VALUES
  ('Amit Verma',45,'Male','Heart Disease',1,1),
  ('Sneha Rao',28,'Female','Skin Allergy',2,3),
  ('Vikas Gupta',60,'Male','Arthritis',3,2);
