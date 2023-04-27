from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        self.message_to_print: str = (
            'Тип тренировки: {0}; Длительность:'
            + ' {1:.3f} ч.; '
            + 'Дистанция: {2:.3f} км; Ср. скорость:'
            + ' {3:.3f} км/ч;'
            + ' Потрачено ккал: {4:.3f}.')
        message_dict: dict = asdict(self)
        return self.message_to_print.format(*message_dict.values())


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MINUTE_IN_HOUR: int = 60

    def __init__(
            self, action: int, duration: float,
            weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        raise Exception('it is necessary to use a specific type of training')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__, self.duration,
            self.get_distance(), self.get_mean_speed(),
            self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * self.duration * self.MINUTE_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    COEFF_WEIGHT: float = 0.035
    COEFF_2_WEIGHT: float = 0.029
    COEFF_SPEED_IN_M_V_S: float = 0.278
    COEFF_HEIGHT_IN_M: int = 100

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.COEFF_WEIGHT * self.weight
                + (self.get_mean_speed()
                 * self.COEFF_SPEED_IN_M_V_S)
                ** 2 / (self.height / self.COEFF_HEIGHT_IN_M)
                * self.COEFF_2_WEIGHT * self.weight)
                * self.duration * self.MINUTE_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    M_IN_KM: int = 1000
    COEFF_SPEED: float = 1.1
    COEFF_CALORIES: int = 2

    def __init__(self, action: int, duration: float,
                 weight: float, length_pool: float, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEFF_SPEED)
                * self.COEFF_CALORIES
                * self.weight * self.duration)


def read_package(workout_type: str, data: list):
    """Прочитать данные полученные от датчиков."""
    workout: dict = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }
    if workout_type in workout:
        some_training = workout[workout_type](*data)
        return some_training
    else:
        raise ValueError('incorrect package')


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
