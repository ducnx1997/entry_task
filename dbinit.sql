CREATE DATABASE IF NOT EXISTS entry_task CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE entry_task;

CREATE TABLE IF NOT EXISTS user_tab (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(32) UNIQUE,
    email VARCHAR(128) UNIQUE,
    salt VARCHAR(8) NOT NULL,
    password_hash VARCHAR(64) NOT NULL ,
    is_admin bool NOT NULL,
    created_at BIGINT UNSIGNED NOT NULL,
    modified_at BIGINT UNSIGNED NOT NULL
);

CREATE TABLE IF NOT EXISTS event_tab (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(256) NOT NULL,
    description TEXT NOT NULL,
    event_datetime INT UNSIGNED NOT NULL,
    tag VARCHAR(256) NOT NULL,
    created_at BIGINT UNSIGNED NOT NULL,
    modified_at BIGINT UNSIGNED NOT NULL,

    INDEX (event_datetime),
    INDEX (tag, event_datetime)
);

CREATE TABLE IF NOT EXISTS event_image_mapping_tab (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    event_id BIGINT UNSIGNED NOT NULL,
    image_path VARCHAR(256) NOT NULL,
    created_at BIGINT UNSIGNED NOT NULL,
    modified_at BIGINT UNSIGNED NOT NULL,

    INDEX (event_id)
);

CREATE TABLE IF NOT EXISTS participation_tab (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    event_id BIGINT UNSIGNED NOT NULL,
    user_id BIGINT UNSIGNED NOT NULL,
    username VARCHAR(32),
    created_at BIGINT UNSIGNED NOT NULL,
    modified_at BIGINT UNSIGNED NOT NULL,

    UNIQUE (event_id, user_id)
);

CREATE TABLE IF NOT EXISTS like_tab (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    event_id BIGINT UNSIGNED NOT NULL,
    user_id BIGINT UNSIGNED NOT NULL,
    username VARCHAR(32),
    created_at BIGINT UNSIGNED NOT NULL,
    modified_at BIGINT UNSIGNED NOT NULL,

    UNIQUE (event_id, user_id)
);

CREATE TABLE IF NOT EXISTS comment_tab (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    event_id BIGINT UNSIGNED NOT NULL,
    user_id BIGINT UNSIGNED NOT NULL,
    username VARCHAR(32),
    body TEXT NOT NULL,
    created_at BIGINT UNSIGNED NOT NULL,
    modified_at BIGINT UNSIGNED NOT NULL,

    INDEX (event_id, created_at)
);

CREATE TABLE IF NOT EXISTS activities_tab (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    action VARCHAR(16) NOT NULL,
    event_id BIGINT UNSIGNED NOT NULL,
    event_title VARCHAR(256) NOT NULL,
    user_id BIGINT UNSIGNED NOT NULL,
    details TEXT NOT NULL,
    created_at BIGINT UNSIGNED NOT NULL,
    modified_at BIGINT UNSIGNED NOT NULL,

    INDEX (user_id, created_at)
)