import json
import emoji

# Список русских стоп-слов
russian_stopwords = {
    'и', 'в', 'во', 'на', 'я', 'с', 'со', 'а', 'то', 'все', 'так',
    'да', 'ты', 'к', 'у', 'же', 'за', 'бы', 'по', 'только', 'мне', 'было', 'вот', 'от',
    'меня', 'о', 'из', 'теперь', 'ну', 'вдруг', 'ли', 'если', 'или', 'быть',
    'до', 'нибудь', 'опять', 'уж', 'ведь', 'там', 'потом', 'себя',
    'может', 'тут', 'есть', 'надо', 'для', 'мы', 'тебя', 'была', 'сам',
    'чтоб', 'будто', 'раз', 'тоже', 'себе', 'под', 'будет', 'ж', 'тогда', 'кто', 'этот', 'того',
    'потому', 'этого', 'ним', 'здесь', 'этом', 'почти', 'мой', 'тем', 'чтобы',
    'сейчас', 'были', 'всех', 'при', 'об',
    'хоть', 'после', 'над', 'больше', 'тот', 'через', 'эти', 'нас', 'про', 'всего', 'них',
    'эту', 'моя', 'впрочем', 'свою', 'этой', 'перед', 'чуть',
    'том', 'такой', 'более', 'всегда', 'конечно', 'всю', 'между', 'это', 'то'
}

cols = ['Нравится скорость отработки заявок',
        'Нравится качество выполнения заявки',
        'Нравится качество работы сотрудников',
        'Понравилось выполнение заявки',
        'Вопрос решен',
        'Жалобы и вопросы',
        'Вопрос не решен'
        ]



def clean_taxonomy(tax_str):
    try:
        # Заменяем нестандартные кавычки и парсим JSON
        tax_str = tax_str.replace('«', '"').replace('»', '"')
        data = json.loads(tax_str)
        
        # Извлекаем все элементы из вложенных списков
        classes = [
            cls 
            for sublist in data[0]["taxonomy"] 
            for cls in sublist
        ]
        
        # Фильтруем классы и удаляем дубликаты
        seen = set()
        return [
            cls for cls in classes 
            if cls in cols and not (cls in seen or seen.add(cls))
        ]
        
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        print(f"Ошибка обработки: {tax_str}")
        return []
    

def process_comment(comment):
    # Удаление спецсимволов и сохранение эмодзи
    cleaned_chars = []
    for char in comment:
        if emoji.is_emoji(char):
            cleaned_chars.append(char)
        elif char.isalnum() or char.isspace():
            cleaned_chars.append(char)
        else:
            cleaned_chars.append(' ')
    
    # Объединение в строку и обработка
    cleaned_str = ''.join(cleaned_chars)
    cleaned_str = cleaned_str.replace('\n', ' ')  # Удаление переносов
    cleaned_str = cleaned_str.lower()             # Приведение к нижнему регистру
    
    # Удаление стоп-слов
    words = cleaned_str.split()
    filtered_words = [word for word in words if word not in russian_stopwords]
    
    return ' '.join(filtered_words)