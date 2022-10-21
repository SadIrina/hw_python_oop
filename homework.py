from dataclasses import asdict, dataclass
from typing import ClassVar


@dataclass(init=True, order=False,
           unsafe_hash=False, frozen=False)
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str  # вид тренировки
    duration: float     # длительность тренировки в часах
    distance: float     # дистанция в километрах
    speed: float        # средняя скорость
    calories: float     # количество израсходованных килокалорий
    MESSAGE: ClassVar[str] = ('Тип тренировки: {training_type}; '
                              'Длительность: {duration:.3f} ч.; '
                              'Дистанция: {distance:.3f} км; '
                              'Ср. скорость: {speed:.3f} км/ч; '
                              'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65  # расстояние, преодоленное за 1 действие
    M_IN_KM: int = 1000     # перевод километры в метры
    MIN_IN_H: int = 60      # количество минут в часе

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:

        self.action = action     # количество действий за тренировку
        self.duration = duration
        self.weight = weight     # вес пользователя

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18    # константа  для рассчета
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79       # константа  для рассчета

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * self.duration * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER: float = 0.035        # константа для рассчета
    KMH_IN_MSEC = 0.278                              # ср. скорость в м в сек.
    CM_IN_M = 100                                    # перевод из м в см
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029  # константа для рассчета
    INDICATOR = 2                                    # константа для рассчета

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:

        super().__init__(action, duration, weight)
        self.height = height            # рост пользователя

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + ((self.get_mean_speed() * self.KMH_IN_MSEC)
                 ** 2 / (self.height / self.CM_IN_M))
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                * self.weight) * self.duration * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38          # расстояние за 1 гребок
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_WEIGHT_MULTIPLIER: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:

        super().__init__(action, duration, weight)

        self.length_pool = length_pool      # длина бассейна в м
        self.count_pool = count_pool        # сколько раз переплыл бассейн

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    type_dict: dict[str, type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return type_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
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
