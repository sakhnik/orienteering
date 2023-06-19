import abc


class Result(abc.ABC):
    @abc.abstractmethod
    def get_name(self) -> str:
        ...

    @abc.abstractmethod
    def get_club(self) -> str:
        ...

    @abc.abstractmethod
    def get_result(self) -> int:
        ...

    @abc.abstractmethod
    def get_position(self) -> int:
        ...

    def get_status(self) -> str:
        return "OK"
