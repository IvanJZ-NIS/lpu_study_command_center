-- Users & Auth Table
CREATE TABLE IF NOT EXISTS users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  student_number VARCHAR(50) UNIQUE NOT NULL,
  lpu_email VARCHAR(100) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  program VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 1. Subjects & Grade Calculator
CREATE TABLE IF NOT EXISTS subjects (
  subject_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  subject_code VARCHAR(20) NOT NULL,
  subject_name VARCHAR(100) NOT NULL,
  target_grade DECIMAL(4,2),
  current_standing DECIMAL(4,2),
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS grade_items (
  item_id INT AUTO_INCREMENT PRIMARY KEY,
  subject_id INT NOT NULL,
  item_name VARCHAR(100) NOT NULL,
  weight_percent DECIMAL(5,2) NOT NULL,
  score_obtained DECIMAL(5,2) NOT NULL,
  max_score DECIMAL(5,2) DEFAULT 100.00,
  FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE
);

-- 2. Quiz & Flashcard Hub
CREATE TABLE IF NOT EXISTS flashcard_decks (
  deck_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  title VARCHAR(100) NOT NULL,
  subject_id INT,
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS flashcards (
  card_id INT AUTO_INCREMENT PRIMARY KEY,
  deck_id INT NOT NULL,
  question TEXT NOT NULL,
  answer TEXT NOT NULL,
  FOREIGN KEY (deck_id) REFERENCES flashcard_decks(deck_id) ON DELETE CASCADE
);

-- 3. Notes & Course Materials
CREATE TABLE IF NOT EXISTS notes (
  note_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  subject_id INT,
  title VARCHAR(150) NOT NULL,
  content LONGTEXT,
  file_path VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 4. Tasks & Deadline Management
CREATE TABLE IF NOT EXISTS tasks (
  task_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  title VARCHAR(150) NOT NULL,
  description TEXT,
  due_date DATETIME NOT NULL,
  priority ENUM('Low', 'Medium', 'High') DEFAULT 'Medium',
  status ENUM('Pending', 'In Progress', 'Completed') DEFAULT 'Pending',
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 5. Integrated Calendar Planner
CREATE TABLE IF NOT EXISTS calendar_events (
  event_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  title VARCHAR(150) NOT NULL,
  start_time DATETIME NOT NULL,
  end_time DATETIME NOT NULL,
  event_type ENUM('Academic', 'Personal') DEFAULT 'Academic',
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 6. Professor Module Import
CREATE TABLE IF NOT EXISTS professor_modules (
  module_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  subject_id INT,
  module_title VARCHAR(150) NOT NULL,
  file_path VARCHAR(255) NOT NULL,
  uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 7. Study Session Tracker
CREATE TABLE IF NOT EXISTS study_sessions (
  session_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  subject_id INT,
  duration_minutes INT NOT NULL,
  session_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
