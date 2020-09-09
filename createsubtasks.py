import argparse
import os
import pprint

from jira import JIRA

JIRA_OPTIONS = {
    'server': os.getenv('jira_base_url', 'https://<jira-subdomain>.atlassian.net'),
    'auth': ('mdjpurdon', 'ikissandtell'),
}

argparser = argparse.ArgumentParser()
argparser.add_argument('parent_task', help='The JIRA id the of parent task')
argparser.add_argument('task_template', help='The template for the task')
argparser.add_argument('task_data', help='The data for the tasks')

models = [
    'apps.members.MemberListSummary',
    'apps.members.UserDevice',
    'apps.members.UserProfileNote',
    'apps.members.UserStateFlag',
    'apps.members.UserTimezoneHistory',

    'apps.reports.AbstractActivitySummary',
    'apps.reports.UserActivity',
]

applications = {
    'members': False,
    'clients': True,
    'dot connector': True,
    'workouts': True,
    'coach hub': True,
}


if __name__ == '__main__':
    jira_service = JIRA(**JIRA_OPTIONS)

    project = jira_service.project('EX')
    print(f'Working with project {project}')

    story = jira_service.issue('EX-1721')
    print(f'Parent story: {story.fields.summary}')

    modules = {}
    for model in models:
        module = model.split('.')[1]
        if module not in modules:
            modules[module] = []

        modules[module].append(model)

    issue_list = []
    for module in modules:
        print(module)
        description = f'Add GUID field as described in the parent story to the following models in the {module} module:\n\n'
        model_list = '\n'.join(f'* {model}' for model in modules[module])
        description += model_list
        description += f'\n\nUpdate unit tests to account for the changes.'

        print(f' - adding task for module {module}')
        jira_service.create_issue(fields={
                'project': {'key': project.key},
                'parent': {'key': story.key},
                'assignee': {'name': jira_service.current_user()},
                'summary': f'Multi-tenancy: Members: Add GUID to {module} module models.',
                'description': description,
                'issuetype': {'name': 'Technical task'},  # <JIRA IssueType: name='Technical task', id='7'>
                'timetracking': {
                    'originalEstimate': f'{2*len(modules[module])}h',
                    'remainingEstimate': f'{2*len(modules[module])}h',
                }
            }
        )

    pprint.pprint(issue_list, width=120)
    issues = jira_service.create_issues(field_list=issue_list)

    print('Done.')
