"""
Unit testing for modelling functions located in ../starters
"""

import os
import sys
import pytest
import pandas as pd
import pickle as pkl
from sklearn.model_selection import train_test_split


try:
    import starter.config as config
    from starter.ml.data import process_data
    from starter.ml.model import (train_model, inference,
                                compute_model_metrics, compute_metrics_by_slice)
except ModuleNotFoundError:
    sys.path.append('./')
    import starter.config as config
    from starter.ml.data import process_data
    from starter.ml.model import (train_model, inference,
                        compute_model_metrics, compute_metrics_by_slice)

@pytest.fixture()
def input_df():
    df = pd.read_csv(config.DATA_PATH)
    train, test = train_test_split(df, test_size=config.TEST_SPLIT_SIZE)
    return train, test


def test_inference(input_df):
    """
    Assert that inference function returns correct
    amount of predictions with respect to the input
    """

    train_df, _ = input_df

    X_train, y_train, _, _ = process_data(
        X=train_df,
        categorical_features=config.cat_features,
        label=config.TARGET,
        training=True
    )

    clf = train_model(X_train, y_train)
    preds = inference(clf, X_train)

    assert len(preds) == len(X_train)


def test_process_data(input_df):
    """
    Make sure processed data is the right shape for both training
    and testing sets after processing
    """
    train_df, test_df = input_df

    X_train, y_train, _, _ = process_data(
        X=train_df,
        categorical_features=config.cat_features,
        label=config.TARGET,
        training=True
    )

    X_test, y_test, _, _ = process_data(
        X=test_df,
        categorical_features=config.cat_features,
        label=config.TARGET,
        training=True,

    )

    assert len(X_train) == len(y_train)
    assert len(X_test) == len(y_test)

def test_compute_metrics(input_df):
    """
    Unit test for testing the outputs of the metrics produced
    by compute_metrics()
    """
    train, _ = input_df

    X_train, y_train, encoder, lb = process_data(
        X=train,
        categorical_features=config.cat_features,
        label=config.TARGET,
        training=True
    )

    clf = train_model(X_train, y_train)
    preds = inference(clf, X_train)

    precision, recall, f_one = compute_model_metrics(y_train, preds)

    # Assert no metric has a value above 1.0
    for metric in [precision, recall, f_one]:
        assert metric <= 1.0