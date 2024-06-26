import sys
from pathlib import Path

import hydra
import torch

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from yolo.config.config import Config
from yolo.model.yolo import get_model
from yolo.tools.data_loader import create_dataloader
from yolo.tools.solver import ModelTrainer
from yolo.utils.logging_utils import custom_logger, validate_log_directory


@hydra.main(config_path="../yolo/config", config_name="config", version_base=None)
def main(cfg: Config):
    custom_logger()
    save_path = validate_log_directory(cfg, cfg.name)
    dataloader = create_dataloader(cfg)
    # TODO: get_device or rank, for DDP mode
    device = torch.device(cfg.device)
    model = get_model(cfg).to(device)

    trainer = ModelTrainer(cfg, model, save_path, device)
    trainer.solve(dataloader, cfg.task.epoch)


if __name__ == "__main__":
    main()
