from datetime import date

import pandas as pd


def transform_app_data(app: dict) -> dict:
    """
    Преобразует JSON приложения из iTunes API
    в словарь для последующей загрузки в PostgreSQL.
    """

    return {
        # ---------- Таблица apps ----------
        "track_id": app.get("trackId"),
        "app_name": app.get("trackName"),
        "developer": app.get("artistName"),
        "bundle_id": app.get("bundleId"),
        "primary_genre": app.get("primaryGenreName"),
        "country": "US",          # App Store, из которого собираем данные
        "seller_name": app.get("sellerName"),
        "release_date": app.get("releaseDate"),

        # ---------- Таблица app_snapshots ----------
        "snapshot_date": date.today(),

        "average_rating": app.get("averageUserRating"),
        "rating_count": app.get("userRatingCount"),

        "average_rating_current_version": app.get(
            "averageUserRatingForCurrentVersion"
        ),
        "rating_count_current_version": app.get(
            "userRatingCountForCurrentVersion"
        ),

        "version": app.get("version"),
        "current_release_date": app.get("currentVersionReleaseDate"),
        "minimum_ios_version": app.get("minimumOsVersion"),

        "file_size_mb": round(
            int(app.get("fileSizeBytes", 0)) / 1024 / 1024,
            2
        ),

        "price": app.get("price"),
        "currency": app.get("currency"),

        "supported_languages": len(
            app.get("languageCodesISO2A", [])
        ),

        "supported_devices": len(
            app.get("supportedDevices", [])
        ),
    }


def create_dataframe(apps: list) -> pd.DataFrame:
    return pd.DataFrame(apps)