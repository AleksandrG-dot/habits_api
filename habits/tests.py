from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit

User = get_user_model()


class HabitTestCase(APITestCase):
    def setUp(self):
        """Подготовка данных для тестов"""
        self.user1 = User.objects.create(email="user1@example.com")
        self.user2 = User.objects.create(email="user2@example.com")

        # Приятная привычка пользователя 1
        self.pleasant_habit = Habit.objects.create(
            user=self.user1,
            place="Дом",
            time="08:00:00",
            action="Пить кофе",
            is_pleasant=True,
            periodicity=1,
            time_required=60,
        )

        # Публичная привычка пользователя 1
        self.public_habit = Habit.objects.create(
            user=self.user1,
            place="Парк",
            time="07:00:00",
            action="Бегать",
            is_pleasant=False,
            periodicity=1,
            time_required=120,
            reward="Выпить смузи",
            is_public=True,
        )

        # Приватная привычка пользователя 1
        self.private_habit = Habit.objects.create(
            user=self.user1,
            place="Дом",
            time="22:00:00",
            action="Читать книгу",
            is_pleasant=False,
            periodicity=2,
            time_required=90,
            reward="Посмотреть сериал",
        )

        # Привычка пользователя 2
        self.user2_habit = Habit.objects.create(
            user=self.user2,
            place="Спортзал",
            time="18:00:00",
            action="Тренироваться",
            is_pleasant=False,
            periodicity=3,
            time_required=110,
        )

    def test_create_habit_success(self):
        """Успешное создание привычки"""
        self.client.force_authenticate(user=self.user1)
        data = {
            "place": "Офис",
            "time": "09:00:00",
            "action": "Делать зарядку",
            "is_pleasant": False,
            "periodicity": 1,
            "time_required": 120,
            "reward": "Выпить кофе",
        }
        response = self.client.post("/api/habits/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 5)
        self.assertEqual(response.data["action"], "Делать зарядку")

    def test_create_habit_with_related_pleasant_habit(self):
        """Успешное создание привычки со связанной приятной привычкой"""
        self.client.force_authenticate(user=self.user1)
        data = {
            "place": "Парк",
            "time": "07:00:00",
            "action": "Бегать",
            "is_pleasant": False,
            "periodicity": 1,
            "time_required": 120,
            "related_habit": self.pleasant_habit.id,  # Приятная привычка - должно быть OK
        }
        response = self.client.post("/api/habits/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["related_habit"], self.pleasant_habit.id)

    def test_create_pleasant_habit_success(self):
        """Успешное создание приятной привычки без вознаграждения и связанной привычки"""
        self.client.force_authenticate(user=self.user1)
        data = {
            "place": "Дом",
            "time": "20:00:00",
            "action": "Принять ванну",
            "is_pleasant": True,
            "periodicity": 1,
            "time_required": 60,
            # Нет reward и related_habit - должно быть OK
        }
        response = self.client.post("/api/habits/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["is_pleasant"])

    def test_retrieve_own_habit(self):
        """Пользователь может получить свою привычку по ID"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(f"/api/habits/{self.private_habit.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["action"], self.private_habit.action)

    def test_retrieve_other_user_habit_denied(self):
        """Пользователь не может получить чужую привычку по ID"""
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(f"/api/habits/{self.private_habit.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_own_habit(self):
        """Пользователь может обновлять свою привычку"""
        self.client.force_authenticate(user=self.user1)
        data = {"action": "Обновленное действие"}
        response = self.client.patch(f"/api/habits/{self.private_habit.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["action"], "Обновленное действие")

    def test_user_cannot_update_other_users_habits(self):
        """Пользователь не может обновлять чужие привычки"""
        self.client.force_authenticate(user=self.user2)
        data = {"action": "Измененное действие"}
        response = self.client.patch(f"/api/habits/{self.private_habit.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_own_habit(self):
        """Пользователь может удалять свою привычку"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(f"/api/habits/{self.private_habit.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Проверяем, что привычка действительно удалена
        response = self.client.get(f"/api/habits/{self.private_habit.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cannot_delete_other_users_habits(self):
        """Пользователь не может удалять чужие привычки"""
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(f"/api/habits/{self.private_habit.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cannot_see_other_users_habits(self):
        """Пользователь не может видеть чужие привычки"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get("/api/habits/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что в ответе только привычки user1
        habit_ids = [habit["id"] for habit in response.data["results"]]
        self.assertIn(self.public_habit.id, habit_ids)
        self.assertIn(self.private_habit.id, habit_ids)
        self.assertIn(self.pleasant_habit.id, habit_ids)
        self.assertNotIn(self.user2_habit.id, habit_ids)

    def test_reward_and_related_habit_validation(self):
        """Валидация: нельзя одновременно указывать связанную привычку и вознаграждение."""
        self.client.force_authenticate(user=self.user1)
        data = {
            "place": "Парк",
            "time": "07:00:00",
            "action": "Бегать",
            "is_pleasant": False,
            "periodicity": 1,
            "time_required": 120,
            "reward": "Выпить смузи",
            "related_habit": self.pleasant_habit.id,  # Нельзя одновременно с вознаграждением
        }
        response = self.client.post("/api/habits/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Нельзя одновременно выбирать связанную привычку и вознаграждение",
            str(response.data),
        )

    def test_time_required_validation(self):
        """Валидация времени выполнения (не больше 120 секунд)."""
        self.client.force_authenticate(user=self.user1)
        data = {
            "place": "Парк",
            "time": "07:00:00",
            "action": "Бегать",
            "is_pleasant": False,
            "periodicity": 1,
            "time_required": 150,  # Больше 120 секунд
        }
        response = self.client.post("/api/habits/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Время выполнения не может быть больше 120 секунд", str(response.data)
        )

    def test_pleasant_habit_no_reward_validation(self):
        """Валидация: у приятной привычки не может быть вознаграждения."""
        self.client.force_authenticate(user=self.user1)
        data = {
            "place": "Дом",
            "time": "09:00:00",
            "action": "Слушать музыку",
            "is_pleasant": True,
            "periodicity": 1,
            "time_required": 60,
            "reward": "Награда",  # Не должно быть для приятной привычки
        }
        response = self.client.post("/api/habits/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "У приятной привычки не может быть вознаграждения или связанной привычки",
            str(response.data),
        )

    def test_pleasant_habit_no_related_habit_validation(self):
        """Валидация: у приятной привычки не может быть связанной привычки."""
        self.client.force_authenticate(user=self.user1)
        data = {
            "place": "Дом",
            "time": "09:00:00",
            "action": "Слушать музыку",
            "is_pleasant": True,
            "periodicity": 1,
            "time_required": 60,
            "related_habit": self.pleasant_habit.id,  # Не должно быть для приятной привычки
        }
        response = self.client.post("/api/habits/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "У приятной привычки не может быть вознаграждения или связанной привычки",
            str(response.data),
        )

    def test_periodicity_validation(self):
        """Валидация периодичности (от 1 до 7 дней)."""
        self.client.force_authenticate(user=self.user1)
        data = {
            "place": "Дом",
            "time": "08:00:00",
            "action": "Медитировать",
            "is_pleasant": False,
            "periodicity": 0,  # Меньше 1 дня
            "time_required": 60,
        }
        response = self.client.post("/api/habits/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Периодичность должна быть от 1 до 7 дней", str(response.data))

    def test_related_habit_is_pleasant_validation(self):
        """Валидация: в связанные привычки могут попадать только приятные привычки."""
        self.client.force_authenticate(user=self.user1)

        # НЕприятная привычка
        unpleasant_habit = Habit.objects.create(
            user=self.user1,
            place="Спортзал",
            time="18:00:00",
            action="Тренироваться",
            is_pleasant=False,
            periodicity=1,
            time_required=120,
        )

        data = {
            "place": "Парк",
            "time": "07:00:00",
            "action": "Бегать",
            "is_pleasant": False,
            "periodicity": 1,
            "time_required": 120,
            "related_habit": unpleasant_habit.id,  # Неприятная привычка
        }
        response = self.client.post("/api/habits/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "В связанные привычки могут попадать только привычки с признаком приятной привычки",
            str(response.data),
        )

    def test_unauthorized_access(self):
        """Неавторизованный доступ запрещен"""
        response = self.client.get("/api/habits/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_see_public_habits(self):
        """Пользователь может видеть публичные привычки других пользователей"""
        self.client.force_authenticate(user=self.user2)
        response = self.client.get("/api/habits_public/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что видна публичная привычка user1
        habit_actions = [habit["action"] for habit in response.data["results"]]
        self.assertIn(self.public_habit.action, habit_actions)
        self.assertNotIn(self.private_habit.action, habit_actions)

    def test_public_habits_read_only(self):
        """Публичные привычки доступны только для чтения"""
        self.client.force_authenticate(user=self.user2)

        # Пытаемся обновить публичную привычку
        data = {"action": "Измененное действие"}
        response = self.client.patch(f"/api/habits/{self.public_habit.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
