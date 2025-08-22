-- Optional relational metadata store (not required for MVP)
--D:\pixelexplore\db\schema.sql
CREATE TABLE IF NOT EXISTS photos (
id TEXT PRIMARY KEY,
user_id TEXT,
path TEXT NOT NULL,
thumb_path TEXT,
caption TEXT,
taken_at TIMESTAMP NULL,
gps_lat REAL NULL,
gps_lng REAL NULL,
emotion TEXT NULL,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);