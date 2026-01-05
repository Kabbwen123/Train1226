from Application.commandBus import CommandBus
from Application.eventBus import EventBus
from Domain.AnomalyAlign import Aligner
from Domain.AnomalyDetector import AlgorithmPort
from Infrastructure.logHandler import Logger
from Interface.qtBridge import QtBridge


class Controller:

    def __init__(
            self,
            event_bus: EventBus,
            command_bus: CommandBus,
            logger: Logger,
            qt_bridge:QtBridge,
            aligner: Aligner,
            algorithm: AlgorithmPort,

    ):
        self.event_bus = event_bus
        self.command_bus = command_bus
        self.logger = logger
        self.qt_bridge = qt_bridge
        self.algorithm= algorithm
        self.aligner = aligner