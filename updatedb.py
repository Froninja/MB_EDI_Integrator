from src.db.dbupdate import ExportReader

reader = ExportReader()
reader.collect_orders()
reader.check_orders()