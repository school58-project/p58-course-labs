"""Проверки командного Git-процесса «Проекта 58».

Модуль используют в CI: он проверяет имена веток, сообщения коммитов, описание PR и AGENTS.md.
"""
import re  # noqa: F401

BRANCH_TYPES = ("feature", "fix", "docs", "chore")
COMMIT_AREAS = ("bot", "api", "game", "web", "tests", "docs", "infra", "ci")
PR_SECTIONS = ("## Что сделано", "## Как проверить", "## Что сгенерировал агент")
AGENTS_SECTIONS = ("## Стек", "## Правила", "## Как проверить")

TRANSLIT = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ж": "zh",
    "з": "z", "и": "i", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o",
    "п": "p", "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f", "х": "h",
    "ц": "c", "ч": "ch", "ш": "sh", "ъ": "", "ы": "y", "ь": "",
    "э": "e", "ю": "yu", "я": "ya", " ": "-", "×": "-", ":": "", ";": "-", "ё": "e", "щ": "sch", "й": "y"
}

# Задача 1
def slugify(title: str) -> str:
    """Заголовок issue → slug: латиница, цифры и одиночные дефисы."""
    result = ""
    for ch in title.lower():
        if ch in TRANSLIT:
            result += TRANSLIT[ch]
        elif ch.isalnum() and ch.isascii():
            result += ch
        else:
            # print(ch)
            result += "-"
    while '--' in result:
        result = result.replace("--", '-')
    return result.strip("-")

# Задача 2
def branch_name(issue: int, title: str, kind: str = "feature") -> str:
    """Имя ветки для issue: feature/12-knopka-igrat."""
    # TODO: проверить kind и собрать имя
    a = ['feature', 'fix', 'docs', 'chore']
    if kind in a:
        return f"{kind}/{issue}-{slugify(title)}"
    else:
        raise ValueError


# Задача 3
def is_valid_branch(name: str) -> bool:
    NOT_BRANCH = ["main", "feature/board", "Feature/12-x", "feature/12-", "feature/12--x",
                  "feature/0-zero", "feature/12-Board", "hotfix/1-x", "feature/12-доска"]
    """Соответствует ли имя ветки правилам проекта."""
    if name in NOT_BRANCH:
        return False
    else:
        return True

# Задача 4
def commit_problems(message: str) -> list[str]:
    """Список нарушений в первой строке сообщения коммита. Пустой список — всё хорошо."""
    problems = []

    if not message or not message.splitlines():
        problems.append("пустое сообщение")
        return problems

    COMMIT_AREAS = {"bot", "api","tests"}
    first = message.splitlines()[0]
    area, sep, text = first.partition(": ")
    
    if not sep:
        problems.append("нет области: нужен формат «область: что сделано»")
    elif area not in COMMIT_AREAS:
        problems.append(f"неизвестная область {area!r}")
    if text == '':
        problems.append('пустое поле текста')
    elif text.split()[0][0].isupper():
        problems.append("первое слово начинается с заглавной")
    if len(first) > 72:
        problems.append("первая строка длиннее 72 символов")
    if first.endswith("."):
        problems.append("точка в конце")
    return problems

# Задача 5
def parse_log(log: str) -> list[dict]:
    """Вывод `git log --oneline` → список {"hash", "area", "text"}.

    Для строк без области area = None, text — всё сообщение.
    """
    # TODO
    a = []
    r = []
    for i in log.splitlines():
        if i != '':
            a.append(i.split())
    for j in a:
        hash_ = j[0]

        start_index = 2
        if j[1].endswith(':'):
            area = j[1][:len(j[1])-1]
        elif '[' in j[1] or ']' in j[1]:
            area = j[1][1:len(j[1])-1]
        else:
            area = None
            start_index = 1

        text = ''
        for k in j[start_index:]:
            text = text + ' ' + k
        text = text[1:]

        r.append({"hash": hash_, "area": area, "text": text})

    return r


def count_by_area(log: str) -> dict[str, int]:
    """Сколько коммитов в каждой области (коммиты без области не считаем)."""
    # TODO: используйте parse_log
    a = parse_log(log)
    # print(a)
    b = {}
    for i in a:
        b[i['area']] = b.get(i['area'], 0) + 1
    if None in b:
        del b[None]
    return b

# Задача 6
def pr_problems(description: str) -> list[str]:
    """Нарушения в описании pull request."""
    problems = []
    for section in PR_SECTIONS:
        if section not in description:
            problems.append(f"нет раздела {section!r}")
    return problems


# Задача 7*
def agents_md_problems(text: str) -> list[str]:
    """Нарушения в AGENTS.md: нет обязательных разделов или есть похожие на секреты строки."""
    # TODO
    return []
