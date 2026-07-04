from pathlib import Path
from itunes_api import APPS, get_app_data
from transform import transform_app_data, create_dataframe
from datetime import date, timedelta
from database import (
    get_app_id,
    insert_app,
    insert_snapshot
)


def main():

    print("=" * 60)
    print("STARTING DATA COLLECTION")
    print("=" * 60)

    rows = []

    simulate_days = 7

    for day_offset in range(simulate_days):

        snapshot_date = date.today() - timedelta(days=day_offset)

        print("\n" + "=" * 50)
        print(f"📅 SNAPSHOT DATE: {snapshot_date}")
        print("=" * 50)

        for app_name in APPS:

            print(f"\n📱 Processing: {app_name}")

            app = get_app_data(app_name)

            if app is None:
                continue

            app_data = transform_app_data(app, snapshot_date)

            rows.append(app_data)

            app_id = get_app_id(app_data["track_id"])

            if app_id is None:
                app_id = insert_app(app_data)
                print("✅ New app inserted")

            insert_snapshot(app_id, app_data)
            print("📊 Snapshot inserted")

    # Создаем DataFrame
    df = create_dataframe(rows)

    print("\n" + "=" * 60)
    print("DATAFRAME SUMMARY")
    print("=" * 60)

    print(df)

    print("\nStatistics:")
    print(df.describe(include="all"))

    # Создаем папку при необходимости
    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Сохраняем CSV
    output_file = output_dir / "apps_snapshot.csv"

    df.to_csv(output_file, index=False)

    print(f"\n✅ CSV saved: {output_file}")

    print("\n" + "=" * 60)
    print("ETL FINISHED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()