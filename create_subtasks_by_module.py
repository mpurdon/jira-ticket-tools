import json

from contextlib import suppress
from jinja2 import Template

from .src import helpers


def calculate_estimates(task_type_estimates: dict, task_data: dict) -> int:
    """
    Given a list of estimates and the task data, determine the total estimated time

    """
    total_estimate = 0

    for estimate_type, estimate_hours in task_type_estimates.items():
        with suppress(KeyError):
            total_estimate += len(task_data[estimate_type]) * estimate_hours

    return total_estimate


if __name__ == '__main__':
    argparser = helpers.get_argparser(description='List sub-tasks of the given task id.')

    argparser.add_argument('-p', '--parent',
                           dest='parent',
                           help='The parent JIRA task')
    argparser.add_argument('-t', '--template',
                           dest='template',
                           help='The template for the task description')
    argparser.add_argument('-d', '--data',
                           dest='data',
                           help='The data to populate the task descriptions')

    args = argparser.parse_args()

    jira_service = helpers.connect(args)

    # project = jira_service.project('EX')
    # print(f'Working with project {project}')

    parent_story = jira_service.issue(args.parent)
    print(f'Parent story: {parent_story.fields.summary}')

    project = parent_story.fields.project
    print(f'Working with project: {project}')

    print(f'Loading template {args.template}')
    with open(args.template, 'r') as f:
        template = json.load(f)

    summary_template = Template(template['summary'])
    description_template = Template(template['description'])

    print(f'Loading data from: {args.data}\n')
    with open(args.data, 'r') as f:
        data = json.load(f)

    estimates = data['estimates']
    issuetype = data['issuetype']
    assignee = data['assignee']
    if assignee['name'] == 'current_user':
        assignee['name'] = jira_service.current_user()

    for module, module_data in data['modules'].items():
        if not module_data:
            continue

        module_data['module'] = module.replace('_', ' ').title()
        summary = summary_template.render(module_data)
        description = description_template.render(module_data).lstrip()
        task_estimate = calculate_estimates(estimates, module_data)

        fields = {
            'project': {'key': project.key},
            'parent': {'key': parent_story.key},
            'assignee': assignee,
            'summary': summary,
            'description': description,
            'issuetype': issuetype,  # <JIRA IssueType: name='Technical task', id='7'>
            'timetracking': {
                'originalEstimate': f'{task_estimate}h',
                'remainingEstimate': f'{task_estimate}h',
            }
        }

        # pprint.pprint(fields)
        # print(f'{"=" * 79}\n')

        jira_service.create_issue(fields=fields)

    print('Done.')
