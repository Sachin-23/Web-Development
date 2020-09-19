CREATE TABLE reviews  (
  user_id INTEGER REFERENCES users,
  ISBN INTEGER REFERENCES books,
  rating INTEGER NOT NULL,
  text_review VARCHAR NOT NULL
);
