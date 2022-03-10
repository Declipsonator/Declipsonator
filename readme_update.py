import requests
from github import Github
from datetime import datetime
from os import getenv

saved_projects = []
download_count = []
g = Github('s', getenv('ACCESS_TOKEN'))


def get_github_downloads(user):
    counted_downloads = 0

    user = g.get_user(user)

    for repo in user.get_repos():
        repo_download_count = 0
        print(repo.name)

        for release in repo.get_releases():
            for asset in release.get_assets():
                counted_downloads += asset.download_count
                repo_download_count += asset.download_count

        saved_projects.append(
            [repo.name, repo.description, repo.stargazers_count, repo.url, repo_download_count, 'Github'])
        download_count.append(repo_download_count)

    return counted_downloads


def get_modrinth_downloads(user):
    counted_downloads = 0
    url = "https://api.modrinth.com/v2/user/{}/projects".format(user)
    response = requests.get(url).json()

    for mod in response:
        counted_downloads += mod.get('downloads')
        print(mod.get('title'))
        saved_projects.append(
            [mod.get('title'), mod.get('description'), 0,
             'https://modrinth.com/' + mod.get('project_type') + '/' + mod.get('slug'), mod.get('downloads'),
             'Modrinth'])
        download_count.append(mod.get('downloads'))

    return counted_downloads


def get_curseforge_downloads(user):
    counted_downloads = 0
    url = "https://api.cfwidget.com/author/search/{}".format(user)
    response = requests.get(url).json()

    for project in response.get('projects'):
        project_id = project.get('id')
        url = "https://api.cfwidget.com/{}".format(project_id)
        response = requests.get(url).json()
        print(response.get('title'))
        counted_downloads += response.get('downloads').get('total')
        for gm_project in saved_projects:
            if gm_project[0].strip() == response.get('title').strip():
                og_downs = gm_project[4]
                gm_project[4] = gm_project[4] + response.get('downloads').get('total')
                for i in range(0, len(download_count)):
                    if download_count[i] == og_downs:
                        download_count[i] = og_downs + response.get('downloads').get('total')



    return counted_downloads


def get_github_projects_string(projects, user):
    project_string = ''
    for project in projects:
        if project[2] >= 1:
            project_string += '- [{}](https://github.com/{}/{}) - {}\n'.format(project[0].replace('-', ' '), user,
                                                                               project[0], project[1])
    return project_string


def get_most_downloaded_string(projects):
    downloaded_string = ''
    download_count.sort(reverse=True)
    for project in projects:
        try:
            for i in range(0, 4):
                if project[4] == download_count[i]:
                    downloaded_string += '- {} - {} downloads  \n'.format(project[0].replace('-', ' '), project[4])
                    download_count[i] = -1
                    break
        except:
            ''

    return downloaded_string


total_downloads = 0

total_downloads += get_github_downloads('Declipsonator')
total_downloads += get_modrinth_downloads('Declipsonator')
total_downloads += get_curseforge_downloads('dexlips')

template = requests.get('https://raw.githubusercontent.com/Declipsonator/Declipsonator/main/template.md').text

template = template.replace('{downloads}', str(total_downloads)) \
    .replace('{projects}', get_github_projects_string(saved_projects, 'Declipsonator')) \
    .replace('{last_updated}', datetime.utcnow().strftime('%Y-%m-%d %H:%M (UTC)')) \
    .replace('{top_three}', get_most_downloaded_string(saved_projects))


with open('README.md', 'w', encoding='UTF-8') as f:
    f.write(template)
    f.close()
