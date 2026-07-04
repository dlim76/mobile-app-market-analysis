import os
from sqlalchemy import create_engine, text
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = BASE_DIR / ".env"

load_dotenv(dotenv_path=str(dotenv_path))

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)


engine = create_engine(DATABASE_URL)

def get_app_id(track_id):

    with engine.begin() as conn:

        result = conn.execute(
            text("""
                SELECT id
                FROM apps
                WHERE track_id = :track_id
            """),
            {"track_id": track_id}
        )

        row = result.fetchone()

        if row:
            return row[0]

        return None
    

def insert_app(app_data):

    with engine.begin() as conn:

        result = conn.execute(
            text("""
                INSERT INTO apps (
                    track_id,
                    app_name,
                    developer,
                    bundle_id,
                    primary_genre,
                    country
                )
                VALUES (
                    :track_id,
                    :app_name,
                    :developer,
                    :bundle_id,
                    :primary_genre,
                    :country
                )
                RETURNING id;
            """),
            app_data
        )

        return result.scalar()
    
def insert_snapshot(app_id, app_data):

    params = {
        **app_data,
        "app_id": app_id
    }

    with engine.begin() as conn:

        conn.execute(
            text("""
                INSERT INTO app_snapshots (
                    app_id,
                    snapshot_date,
                    average_rating,
                    rating_count,
                    version,
                    current_release_date,
                    minimum_ios_version,
                    file_size_mb,
                    price,
                    currency
                )
                VALUES (
                    :app_id,
                    :snapshot_date,
                    :average_rating,
                    :rating_count,
                    :version,
                    :current_release_date,
                    :minimum_ios_version,
                    :file_size_mb,
                    :price,
                    :currency
                )
                ON CONFLICT (app_id, snapshot_date)
                DO NOTHING;
            """),
            params
        )

if __name__ == "__main__":
    with engine.connect() as conn:
        print("✅ Connection successful!")

    