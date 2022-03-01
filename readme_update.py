import requests
from github import Github


def get_github_downloads(user):
    counted_downloads = 0
    g = Github()

    user = g.get_user(user)

    for repo in user.get_repos():
        for release in repo.get_releases():
            for asset in release.get_assets():
                counted_downloads += asset.download_count

    return counted_downloads


def get_modrinth_downloads(user):
    counted_downloads = 0
    url = "https://api.modrinth.com/v2/user/{}/projects".format(user)
    response = requests.get(url).json()

    for mod in response:
        counted_downloads += mod.get('downloads')

    return counted_downloads


def get_curseforge_downloads(user):
    counted_downloads = 0
    url = "https://api.cfwidget.com/author/search/{}".format(user)
    response = requests.get(url).json()

    for project in response.get('projects'):
        project_id = project.get('id')

        url = "https://api.cfwidget.com/{}".format(project_id)
        response = requests.get(url).json()
        counted_downloads += response.get('downloads').get('total')

    return counted_downloads


total_downloads = 0

total_downloads += get_github_downloads('Declipsonator')
total_downloads += get_modrinth_downloads('Declipsonator')
total_downloads += get_curseforge_downloads('dexlips')

print(total_downloads)
