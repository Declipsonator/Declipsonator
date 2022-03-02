import requests
from github import Github
from datetime import datetime
from os import getenv

saved_projects = []
g = Github('s', getenv('ACCESS_TOKEN'))


def get_github_downloads(user, save_projects):
    counted_downloads = 0

    user = g.get_user(user)

    for repo in user.get_repos():
        if save_projects and repo.stargazers_count >= 1:
            saved_projects.append(repo.name)
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


def get_github_projects_string(projects, user):
    project_string = ''
    for project in projects:
        project_string += '- [{}](https://github.com/{}/{})\n'.format(project.replace('-', ' '), user, project)
    return project_string


total_downloads = 0

total_downloads += get_github_downloads('Declipsonator', True)
total_downloads += get_modrinth_downloads('Declipsonator')
total_downloads += get_curseforge_downloads('dexlips')

template = requests.get('https://raw.githubusercontent.com/Declipsonator/Declipsonator/main/template.md').text

tz = timezone('EST')
template = template.replace('{downloads}', str(total_downloads))\
    .replace('{projects}', get_github_projects_string(saved_projects, 'Declipsonator'))\
    .replace('{last_updated}', datetime.utcnow().strftime('%Y-%m-%d %H:%M (UTC)'))



with open('README.MD', 'w', encoding='UTF-8') as f:
    f.write(template)
    f.close()
