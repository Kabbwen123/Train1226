from __future__ import annotations
from dependency_injector import containers, providers

from Application.commandBus import CommandBus
from Application.controller import Controller
from Application.eventBus import EventBus
from Domain.AnomalyAlign import Aligner
from Domain.AnomalyDetector import AnomalyDetector
from Infrastructure.sqlDB import SqlDB

from Infrastructure.logHandler import Logger

from Interface.mainWindow import MainWindow
from Interface.qtBridge import QtBridge
from portimp.PatchCorePort import PatchCorePort


class Application(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["Application.handlers"]
    )

    config = providers.Configuration(yaml_files=["./Config/config.yaml"])

    logger = providers.Singleton(
        Logger,
        enable_file=config.logger.enable_file_logging.as_(bool),
    )

    event_bus = providers.Singleton(EventBus)
    command_bus = providers.Singleton(CommandBus)

    qt_bridge = providers.Singleton(
        QtBridge,
        event_bus=event_bus,
    )

    sql_db = providers.Singleton(
        SqlDB,
        logger=logger,
        db_path=config.sqlite.db_path.as_(str),
        table=config.sqlite.table.as_(dict),
    )

    main_ui = providers.Singleton(
        MainWindow,
        sql_db=sql_db,
        bridge=qt_bridge,
    )

    aligner = providers.Singleton(Aligner, bus=event_bus)

    algorithm = providers.Singleton(PatchCorePort)

    controller = providers.Singleton(
        Controller,
        event_bus=event_bus,
        command_bus=command_bus,
        logger=logger,
        qt_bridge=qt_bridge,
        aligner=aligner,
        algorithm=algorithm
    )
