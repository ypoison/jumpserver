# ~*~ coding: utf-8 ~*~
from celery import shared_task

@shared_task
def share_log_util(asset,record):
    from ops.inventory import JMSInventory
    from ops.ansible.runner import CommandRunner
    from assets.models import SystemUser
    run_as = SystemUser.objects.get(username='app')
    print('-'*10 + ' ' + 'Task start' + ' ' + '-'*10)
    inventory = JMSInventory([asset], run_as=run_as)
    runner = CommandRunner(inventory)
    try:
        cmd = 'scp -P 1932 /data/backup/%s 35.220.239.195:/home/devadmin/logs' % str(record)
        result = runner.execute(cmd, 'all')
        result = result.results_command
    except Exception as e:
        print("Error occur: {}".format(e))
        result = {"error": str(e)}

    print('-'*10 + ' ' + 'Task end' + ' ' + '-'*10)
    return True, ""

@shared_task
def update_node_log_record_util(asset, node, task_name):
    from ops.inventory import JMSInventory
    from ops.ansible.runner import CommandRunner
    from assets.models import SystemUser
    run_as = SystemUser.objects.get(username='app')
    print('-'*10 + ' ' + task_name + ' ' + '-'*10)
    inventory = JMSInventory([asset], run_as=run_as)
    runner = CommandRunner(inventory)
    try:
        cmd = '/data/scripts/Rsync_log.sh %s' % str(node)
        result = runner.execute(cmd, 'all')
        result = result.results_command
    except Exception as e:
        print("Error occur: {}".format(e))
        result = {"error": str(e)}

    print('-'*10 + ' ' + 'Task end' + ' ' + '-'*10)
    return True, ""

