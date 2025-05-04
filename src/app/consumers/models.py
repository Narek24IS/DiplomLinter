from pydantic import BaseModel


class ProjectForLint(BaseModel):
    """
    Модель сообщения с запросом на линтинг проекта из RMQ
    :param id: номер задачи в бд
    :param repository_url: Ссылка на репозиторий с проектом. Может быть как ssh так и http
    :param branch_name: ветка откуда нужно брать код для линтинга
    """

    id: int
    repository_url: str
    branch_name: str


class ProjectLintResult(BaseModel):
    """
    Модель сообщения с результатами линтинг проекта из RMQ
    :param task_id: номер задачи в бд
    :param repository_url: ссылка на репозиторий с проектом. Может быть как ssh так и http
    :param sca_result_url: ссылка на страницу с результатами линтинга
    :param error: причина ошибки, если она есть, иначе пустая строка
    """
    task_id: int
    repository_url: str
    sca_result_url: str
    error: str
