import copy
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

import optuna

from .suggesters.base_suggester import Suggester


@dataclass(frozen=True)
class SuggesterSpace:
    suggesters: Sequence[Suggester]

    def suggest_hyperparameters(self, trial: optuna.Trial) -> dict[str, Any]:
        suggester_dict = {
            suggester.__class__.__name__: suggester for suggester in self.suggesters
        }

        suggester_names = list(suggester_dict.keys())
        suggester_name: str = trial.suggest_categorical("suggester", suggester_names)  # type: ignore # We know this is a string, because it must suggest from the suggester_names. Optuna should type-hint with a generic, but haven't. MB has created an issue here: https://github.com/optuna/optuna/issues/5104

        suggester = suggester_dict[suggester_name]
        return suggester.suggest_hyperparameters(trial=trial)


def suggest_hyperparams_from_cfg(
    base_cfg: dict[str, Any],
    trial: optuna.Trial,
) -> dict[str, Any]:
    """Suggest hyperparameters in a config.


    Base-cfg is a config dict representing a tree. For all nodes in the tree that are of type SearchSpace, replace the node with a suggested set of a hyperparameters.

    Args:
        base_cfg: The base config, a tree of options.
        trial: The optuna trial to use for suggesting hyperparameters.
    """
    cfg = copy.deepcopy(base_cfg)
    _suggest_hyperparams_for_nodes(d=cfg, trial=trial)
    return cfg


def _suggest_hyperparams_for_nodes(d: dict[str, Any], trial: optuna.Trial):
    for key, value in d.items():
        match value:
            case dict():
                _suggest_hyperparams_for_nodes(value, trial=trial)
            case SuggesterSpace() | Suggester():
                d[key] = value.suggest_hyperparameters(trial=trial)
            case _:
                # Values which do not require processing, pass
                pass
