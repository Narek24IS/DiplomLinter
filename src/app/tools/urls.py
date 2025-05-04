from enum import Enum


def convert_ssh_to_https(url: str) -> str:
    if url.startswith("ssh://git@"):
        url = url[len("ssh://git@") :]
        user_host, path = url.split(":", 1)
        path = path[4:]
        https_url = f"https://{user_host}{path}"
        return https_url
    return url


class ProjectType(Enum):
    CLI = 1
    VCS = 2


def convert_url_to_project_name(url: str, project_type: ProjectType=ProjectType.VCS) -> str:
    if url.endswith(".git"):
        url = url[: -len(".git")]
    if url.startswith("https://"):
        url = url[len("https://") :]
    elif url.startswith("http://"):
        url = url[len("http://") :]
    elif url.startswith("ssh://git@"):
        url = url[len("ssh://git@") :]
    user_host, project_name = url.split("/", 1)

    if project_type.value == ProjectType.CLI.value:
        project_name += "_cli"

    return project_name
