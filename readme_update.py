import requests
from github import Github
saved_projects = []


def get_github_downloads(user, save_projects):
    counted_downloads = 0
    g = Github()

    user = g.get_user(user)

    for repo in user.get_repos():
        if save_projects & repo.stargazers_count >= 1:
            saved_projects.add(repo.name)
        for release in repo.get_releases():
            for asset in release.get_assets():
                counted_downloads += asset.download_count

    return counted_downloads


def get_modrinth_downloads(user, save_projects):
    counted_downloads = 0
    url = "https://api.modrinth.com/v2/user/{}/projects".format(user)
    response = requests.get(url).json()

    for mod in response:
        counted_downloads += mod.get('downloads')

    return counted_downloads


def get_curseforge_downloads(user, save_projects):
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

total_downloads += get_github_downloads('Declipsonator', true)
total_downloads += get_modrinth_downloads('Declipsonator', false)
total_downloads += get_curseforge_downloads('dexlips', false)

project_string = ''
for project in saved_projects:
    project_string += '- [{}]({})\n'.format(project)

template = requests.get('https://raw.githubusercontent.com/Declipsonator/Declipsonator/main/template.md').text

print(template.replace('{downloads}', str(total_downloads)).replace('{projects}', project_string))
            
