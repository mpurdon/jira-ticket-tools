import argparse
import json
import os

from jira import JIRA

from jira_scripts import exos_jira

services = {
    'members': True,
    'clients': True,
    'dot connector': True,
    'coach hub': True,
    'staff': True,
    'workout engine': True,
}

if __name__ == '__main__':
    argparser = exos_jira.get_argparser(description='Create sub-tasks by service for the given parent task.')

    argparser.add_argument('-p', '--parent',
                           dest='parent',
                           help='The parent JIRA task')

    args = argparser.parse_args()

    jira_service = exos_jira.connect(args)

    project = jira_service.project('EX')
    print(f'Working with project {project}')

    story = jira_service.issue(args.parent)  # EX-1721
    print(f'Parent story: {story.fields.summary}')

    template = None
    with open(f'./templates/{args.parent}.json', 'r') as f:
        template = json.loads(f.read())

    print('Adding tasks for the following services:')
    for service in filter(services):
        print(template.summary.format(service=service))

    # for tasks in story.fields.subtasks:
    #     subtask_id = tasks.key
    #     print(f'\t{subtask_id}')
