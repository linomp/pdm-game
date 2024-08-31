import unittest
from unittest.mock import MagicMock, patch

import numpy as np

from mvp.server.analysis.rul_prediction import svr_rul_prediction_fn
from mvp.server.core.Machine import Machine


class TestSVRRULPredictionFn(unittest.TestCase):

    # TODO: decide if to test with these mocks or actual model to verify actual behavior

    @patch('mvp.server.analysis.rul_prediction.session')
    def test_svr_rul_prediction_fn(self, mock_session):
        mock_session.get_inputs = MagicMock(return_value=[type('Foo', (object,), {'name': 'input'})()])
        mock_session.get_outputs = MagicMock(return_value=[type('Foo', (object,), {'name': 'output'})()])
        mock_session.run = MagicMock(return_value=np.array([100.0]))

        machine = Machine.new_machine()
        current_timestep = 100
        feature_vec = np.array([[current_timestep], [machine.temperature], [machine.oil_age],
                                [machine.mechanical_wear]])

        result = svr_rul_prediction_fn(feature_vec)

        self.assertEqual(result, 100)

    @patch('mvp.server.analysis.rul_prediction.session')
    def test_error_handling(self, mock_session):
        mock_session.get_inputs = MagicMock(return_value=[type('Foo', (object,), {'name': 'input'})()])
        mock_session.get_outputs = MagicMock(return_value=[type('Foo', (object,), {'name': 'output'})()])
        mock_session.run = MagicMock(side_effect=Exception("Test exception"))

        machine = Machine.new_machine()
        current_timestep = 100
        feature_vec = np.array([[current_timestep], [machine.temperature], [machine.oil_age],
                                [machine.mechanical_wear]])

        result = svr_rul_prediction_fn(feature_vec)

        self.assertIsNone(result)
