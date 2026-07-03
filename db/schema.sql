DROP TABLE IF EXISTS app_snapshots;
DROP TABLE IF EXISTS apps;


CREATE TABLE apps (
    id SERIAL PRIMARY KEY,

    track_id BIGINT NOT NULL UNIQUE,

    app_name VARCHAR(255) NOT NULL,

    developer VARCHAR(255),

    bundle_id VARCHAR(255) UNIQUE,

    primary_genre VARCHAR(100),

    country VARCHAR(10),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE app_snapshots (
    id SERIAL PRIMARY KEY,

    app_id INTEGER NOT NULL,

    snapshot_date DATE NOT NULL,

    average_rating NUMERIC(3,2),

    rating_count INTEGER,

    version VARCHAR(50),

    current_release_date TIMESTAMP,

    minimum_ios_version VARCHAR(20),

    file_size_mb NUMERIC(10,2),

    price NUMERIC(10,2),

    currency VARCHAR(10),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    supported_languages INTEGER,

    supported_devices INTEGER,
    
    CONSTRAINT fk_app
        FOREIGN KEY(app_id)
        REFERENCES apps(id)
        ON DELETE CASCADE,
    
    CONSTRAINT unique_snapshot
    UNIQUE(app_id, snapshot_date)
);


CREATE INDEX idx_snapshot_date
ON app_snapshots(snapshot_date);

CREATE INDEX idx_app_id
ON app_snapshots(app_id);

CREATE INDEX idx_rating
ON app_snapshots(average_rating);