from celery.signals import task_prerun, task_postrun, task_failure, task_retry, task_revoked, task_sent
from ai.core.history.task_event_hook import TaskEventHook
from ai.core.history.product_history_hook import ProductHistoryHook


task_event_hook = TaskEventHook()
product_history_hook = ProductHistoryHook()

@task_sent.connect
def on_task_sent(sender=None, task_id=None, args=None, kwargs=None, **other):
    """任务创建时的初始状态"""
    try:
        task_input = args[0] if args and isinstance(args[0], dict) else {}
        task_event = task_event_hook.pending(task_id, sender, task_input)
        if task_event:
            product_history = product_history_hook.pending(task_event, task_input)
        
    except Exception as e:
        print(f"Error recording task sent: {e}")

@task_prerun.connect
def before_task_run(sender=None, task_id=None, task=None, args=None, kwargs=None, **other):
    """任务开始执行时的状态"""
    try:
        task_input = args[0] if args and isinstance(args[0], dict) else {}
        task_event = task_event_hook.started(task_id, sender, task_input)
        if task_event:
            product_history = product_history_hook.started(task_event, task_input)
        
    except Exception as e:
        print(f"Error recording task prerun: {e}")


@task_postrun.connect
def after_task_run(sender=None, task_id=None,args=None, retval=None, **other):
    """任务执行完成后的状态更新"""
    try:
        # 添加简单日志确认状态更新被触发
        if 'storage' in str(sender):
            print(f"Storage task completed: {task_id}, updating generate_status to SUCCESS")
        
        task_input = args[0] if args and isinstance(args[0], dict) else {}
        
        # 第一步：更新任务事件状态
        try:
            task_event = task_event_hook.success(task_id, sender, task_input,retval)
            if task_event:
                print(f"Task event updated successfully for {task_id}")
            else:
                print(f"Warning: Task event update returned None for {task_id}")
        except Exception as e:
            print(f"Error updating task event for {task_id}: {e}")
            import traceback
            traceback.print_exc()
            return  # 如果任务事件更新失败，不继续处理产品历史
        
        # 第二步：更新产品历史状态
        if task_event:
            try:
                product_history = product_history_hook.success(task_event, task_input,retval)
                if 'storage' in str(sender):
                    print(f"Storage task status update result")
                if product_history:
                    print(f"Product history updated successfully for {task_id}")
                else:
                    print(f"Warning: Product history update returned None for {task_id}")
            except Exception as e:
                print(f"Error updating product history for {task_id}: {e}")
                import traceback
                traceback.print_exc()
        
    except Exception as e:
        print(f"Critical error in task postrun for {task_id}: {e}")
        import traceback
        traceback.print_exc()



@task_failure.connect
def on_task_failure(sender=None, task_id=None, exception=None, traceback=None, **other):
    """任务执行失败时的状态更新"""
    try:
        print(f"Task failed: {task_id}, exception: {exception}")
        
        # 更新任务事件状态为失败
        try:
            task_event = task_event_hook.failure(task_id, sender)
            if task_event:
                print(f"Task event failure status updated for {task_id}")
            else:
                print(f"Warning: Task event failure update returned None for {task_id}")
        except Exception as e:
            print(f"Error updating task event failure status for {task_id}: {e}")
            import traceback
            traceback.print_exc()
            return
        
        # 更新产品历史状态为失败
        if task_event:
            try:
                product_history = product_history_hook.failure(task_event)
                if product_history:
                    print(f"Product history failure status updated for {task_id}")
                else:
                    print(f"Warning: Product history failure update returned None for {task_id}")
            except Exception as e:
                print(f"Error updating product history failure status for {task_id}: {e}")
                import traceback
                traceback.print_exc()
        
    except Exception as e:
        print(f"Critical error in task failure handler for {task_id}: {e}")
        import traceback
        traceback.print_exc()

@task_retry.connect
def on_task_retry(sender=None, task_id=None, **other):
    try:
        task_event = task_event_hook.retry(task_id, sender)
        if task_event:
            product_history = product_history_hook.retry(task_event)
        
    except Exception as e:
        print(f"Error recording task retry: {e}")

@task_revoked.connect
def on_task_revoked(sender=None, task_id=None, **other):
    try:
        task_event = task_event_hook.revoked(task_id, sender)
        if task_event:
            product_history = product_history_hook.revoked(task_event)
        
    except Exception as e:
        print(f"Error recording task revoked: {e}")

