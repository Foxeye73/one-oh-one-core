
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

    
def upsert_fixture(apps, app_label, model_name, filename, unique_field='name'):
    """
    Insert or update to a model from a fixture file.
    """
    _model = apps.get_model(app_label, model_name)

    with open(BASE_DIR / app_label / "fixtures" / filename) as f:
        data = json.load(f)

    for item in data:
        _model.objects.update_or_create(
            **{unique_field: item[unique_field]},
            defaults=item
        )


# noinspection SqlWithoutWhere
def truncate_table(apps, app_label, model_name, schema_editor):
    _model = apps.get_model(app_label, model_name)
    table = _model._meta.db_table
    vendor = schema_editor.connection.vendor

    if vendor == "postgresql":
        schema_editor.execute(
            f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE"
        )

    elif vendor == "sqlite":
        schema_editor.execute(f"DELETE FROM {table}")
        schema_editor.execute(
            f"DELETE FROM sqlite_sequence WHERE name='{table}'"
        )