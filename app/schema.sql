-- Drop tables if they exist
DROP TABLE IF EXISTS bookRequest;
DROP TABLE IF EXISTS eBook;
DROP TABLE IF EXISTS section;
DROP TABLE IF EXISTS sectionToeBook;
DROP TABLE IF EXISTS user;

-- Create section table
CREATE TABLE IF NOT EXISTS section (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create eBook table
CREATE TABLE IF NOT EXISTS eBook (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    content TEXT,
    author TEXT,
    prologue TEXT,
    price REAL,
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create sectionToeBook table (assuming it's a many-to-many relationship between section and eBook)
CREATE TABLE IF NOT EXISTS sectionToeBook (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    eBookId INTEGER NOT NULL,
    sectionId INTEGER NOT NULL,
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (eBookId) REFERENCES eBook (id),
    FOREIGN KEY (sectionId) REFERENCES section (id),
    UNIQUE(eBookId, sectionId)
);

-- Create bookRequest table
CREATE TABLE IF NOT EXISTS bookRequest (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userId INTEGER NOT NULL,
    bookId INTEGER NOT NULL,
    isApproved INTEGER DEFAULT 0,
    isRejected INTEGER DEFAULT 0,
    isReturned INTEGER DEFAULT 0,
    isRevoked INTEGER DEFAULT 0,
    isBought INTEGER DEFAULT 0,
    isDeleted INTEGER DEFAULT 0,
    rejectionReason TEXT,
    issueDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    returnDate DATETIME,
    feedback TEXT,
    rating INTEGER,
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userId) REFERENCES user (id),
    FOREIGN KEY (bookId) REFERENCES eBook (id)
);

-- Create user table
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    active INTEGER DEFAULT 1,
    currentBooks INTEGER DEFAULT 0, 
    role TEXT DEFAULT 'USER',
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
);