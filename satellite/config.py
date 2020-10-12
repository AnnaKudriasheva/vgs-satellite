import dataclasses

from pathlib import Path

import marshmallow_dataclass

from ruamel.yaml import YAML


DEFAULT_CONFIG_PATH = '~/.vgs-satellite/config.yml'


@dataclasses.dataclass(frozen=True)
class SatelliteConfig:
    web_server_port: int = 8089
    reverse_proxy_port: int = 9098
    forward_proxy_port: int = 9099


SatelliteConfigSchema = marshmallow_dataclass.class_schema(SatelliteConfig)


class InvalidConfigError(Exception):
    pass


def configure(config_path: str = None, **kwargs):
    params_from_file = _get_params_from_config_file(config_path)
    params = {**params_from_file, **kwargs}

    schema = SatelliteConfigSchema(unknown='EXCLUDE')
    errors = schema.validate(params)
    if errors:
        raise InvalidConfigError(errors)

    return SatelliteConfig(**schema.dump(params))


def _get_params_from_config_file(config_path: str = None) -> dict:
    for path in filter(None, [config_path, DEFAULT_CONFIG_PATH]):
        path = Path(path).expanduser().resolve()
        if path.exists():
            try:
                with open(path) as stream:
                    return YAML().load(stream)
            except Exception as exc:
                raise InvalidConfigError(str(exc)) from exc
    return {}