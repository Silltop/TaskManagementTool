from typing import Optional, Protocol


class TaskOnProjectPort(Protocol):
    def link_task_to_project(self, project_id: str, task_id: str, session) -> None:
        pass

    def unlink_task_from_project(self, project_id: str, task_id: str, session) -> None:
        pass

    def get_project_tasks(self, project_id: str, session) -> Optional[list]:
        pass
