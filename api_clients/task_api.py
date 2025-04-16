
import requests
import allure


@allure.feature("Работа с задачами через API")
class TaskAPI:
    def __init__(self, base_url, api_key):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": api_key,
            "Content-Type": "application/json"
        })
        self.base_url = base_url

    task_update = {
        "name": "API test update",
        "description": "https://www.markdownguide.org/cheat-sheet/"
    }

    @allure.step("Получение команды")
    def get_team(self):
        with allure.step("GET /team"):
            return self.session.get(f"{self.base_url}/team")

    @allure.step("Получение пространств команды с ID: {team_id}")
    def get_space(self, team_id):
        with allure.step(f"GET /team/{team_id}/space"):
            return self.session.get(f"{self.base_url}/team/{team_id}/space")

    @allure.step("Получение папок пространства с ID: {space_id}")
    def get_folder(self, space_id):
        with allure.step(f"GET /space/{space_id}/folder"):
            return self.session.get(f"{self.base_url}/space/{space_id}/folder")

    @allure.step("Получение списков папки с ID: {folder_id}")
    def get_list(self, folder_id):
        with allure.step(f"GET /folder/{folder_id}/list"):
            return self.session.get(f"{self.base_url}/folder/{folder_id}/list")

    @allure.step("Создание задачи в списке с ID: {list_id}")
    def create_task(self, list_id, task_data):
        with allure.step(f"POST /list/{list_id}/task"):
            return self.session.post(
                f"{self.base_url}/list/{list_id}/task",
                json=task_data
            )

    @allure.step("Получение задачи по ID: {task_id}")
    def get_task(self, task_id):
        with allure.step(f"GET /task/{task_id}"):
            return self.session.get(f"{self.base_url}/task/{task_id}")

    @allure.step("Обновление задачи по ID: {task_id}")
    def update_task(self, task_id, task_update):
        with allure.step(f"PUT /task/{task_id}"):
            return self.session.put(f"{self.base_url}/task/{task_id}", json=task_update)

    @allure.step("Удаление задачи по ID: {task_id}")
    def delete_task(self, task_id):
        with allure.step(f"DELETE /task/{task_id}"):
            return self.session.delete(f"{self.base_url}/task/{task_id}")
