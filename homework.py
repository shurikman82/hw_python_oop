class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; Длительность:'
                f'{self.duration: .3f} ч;'
                f' Дистанция: {self.distance: .3f} км; Ср. скорость:'
                f'{self.speed: .3f} км/ч;'
                f' Потрачено ккал: {self.calories: .3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        self.distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return self.distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        self.speed: float = self.distance / self.duration
        return self.speed

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(),
                           self.get_mean_speed(), self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_distance(self) -> float:
        return super().get_distance()

    def get_mean_speed(self) -> float:
        return super().get_mean_speed()

    def show_training_info(self) -> InfoMessage:
        return super().show_training_info()

    def get_spent_calories(self) -> float:
        self.calories: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                                * self.speed + self.CALORIES_MEAN_SPEED_SHIFT)
                                * self.weight / self.M_IN_KM
                                * self.duration * 60)
        return self.calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    COEFF_WEIGHT: float = 0.035
    COEFF_2_WEIGHT: float = 0.029
    COEFF_SPEED_IN_M_V_S: float = 1000 / 3600
    COEFF_HEIGHT_IN_M: float = 0.01

    def __init__(self, action: int, duration: float,
                 weight: float, height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_distance(self) -> float:
        return super().get_distance()

    def get_mean_speed(self) -> float:
        return super().get_mean_speed()

    def show_training_info(self) -> InfoMessage:
        return super().show_training_info()

    def get_spent_calories(self) -> float:
        self.calories: float = ((self.COEFF_WEIGHT * self.weight
                                + (self.speed * self.COEFF_SPEED_IN_M_V_S) ** 2
                                / (self.height * self.COEFF_HEIGHT_IN_M)
                                * self.COEFF_2_WEIGHT * self.weight)
                                * self.duration * 60)
        return self.calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    M_IN_KM: int = 1000
    COEFF_SPEED: float = 1.1

    def __init__(self, action: int, duration: float,
                 weight: float, length_pool: float, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    def get_distance(self) -> float:
        self.LEN_STEP: float = 1.38
        return super().get_distance()

    def show_training_info(self) -> InfoMessage:
        return super().show_training_info()

    def get_mean_speed(self) -> float:
        self.speed: float = (self.length_pool * self.count_pool
                             / self.M_IN_KM / self.duration)
        return self.speed

    def get_spent_calories(self) -> float:
        self.calories: float = ((self.speed + self.COEFF_SPEED) * 2
                                * self.weight * self.duration)
        return self.calories


def read_package(workout_type: str, data: list):
    """Прочитать данные полученные от датчиков."""

    workout: dict = {'RUN': Running,
                     'WLK': SportsWalking,
                     'SWM': Swimming}
    if workout_type in workout:
        some_training = workout[workout_type](*data)
        return some_training
    else:
        print('incorrect package')


def main(training: Training) -> None:
    """Главная функция."""

    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
