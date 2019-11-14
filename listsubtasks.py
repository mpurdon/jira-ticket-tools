from src import helpers

if __name__ == '__main__':
    argparser = helpers.get_argparser(description='List sub-tasks of the given task id.')

    argparser.add_argument('-p', '--project',
                           dest='project',
                           help='The JIRA project to work with')

    argparser.add_argument('-t', '--parent',
                           dest='parent',
                           help='The parent JIRA task')

    args = argparser.parse_args()

    jira_service = helpers.connect(args)

    project = jira_service.project(args.project)
    print(f'Working with project {project}')

    story = jira_service.issue(args.parent)  # EX-1721
    print(f'Parent story: {story.fields.summary}')

    print(f'Subtasks:')
    for tasks in story.fields.subtasks:
        subtask_id = tasks.key
        print(f'\t{subtask_id}')
