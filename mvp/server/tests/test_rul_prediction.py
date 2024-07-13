import unittest
from unittest.mock import MagicMock, patch

import numpy as np

from mvp.server.core.analysis.rul_prediction import svr_rul_prediction_fn
from mvp.server.core.machine.MachineState import OperationalParameters


class TestSVRRULPredictionFn(unittest.TestCase):

    # TODO: decide if to test with these mocks or actual model to verify actual behavior

    @patch('mvp.server.core.analysis.rul_prediction.session')
    def test_svr_rul_prediction_fn(self, mock_session):
        mock_session.get_inputs = MagicMock(return_value=[type('Foo', (object,), {'name': 'input'})()])
        mock_session.get_outputs = MagicMock(return_value=[type('Foo', (object,), {'name': 'output'})()])
        mock_session.run = MagicMock(return_value=np.array([100.0]))

        parameters = OperationalParameters(temperature=75.0, oil_age=500.0, mechanical_wear=0.3)
        purchased_sensors = ["temperature", "oil_age", "mechanical_wear"]
        current_timestep = 100

        result = svr_rul_prediction_fn(current_timestep, parameters, purchased_sensors)

        self.assertEqual(result, 100)

    @patch('mvp.server.core.analysis.rul_prediction.session')
    def test_error_handling(self, mock_session):
        mock_session.get_inputs = MagicMock(return_value=[type('Foo', (object,), {'name': 'input'})()])
        mock_session.get_outputs = MagicMock(return_value=[type('Foo', (object,), {'name': 'output'})()])
        mock_session.run = MagicMock(side_effect=Exception("Test exception"))

        parameters = OperationalParameters(temperature=75.0, oil_age=500.0, mechanical_wear=0.3)
        available_sensors = ["temperature", "oil_age", "mechanical_wear"]
        current_timestep = 100

        result = svr_rul_prediction_fn(current_timestep, parameters, available_sensors)

        self.assertIsNone(result)
