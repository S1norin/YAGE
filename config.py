# Здесь находятся постоянные
DB_FILENAME = "words_db.sqlite"
TASK_NUMBERS = ["N/A", "9", "10", "11", "12"]  # Пустая строка отвечает за выбор, когда задание не определено


def null_fill(potentional_null):
    if potentional_null == 0 or potentional_null == "":
        return None
    return potentional_null
