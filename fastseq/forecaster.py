# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/07_forecaster.ipynb (unless otherwise specified).

__all__ = ['Forecaster']

# Cell
from fastcore.utils import *
from fastcore.imports import *
from fastai2.basics import *


# Cell
class Forecaster():
    """Handles training of a PyTorch model and can be used to generate samples
    from approximate posterior predictive distribution.
    Arguments:
        * model (``torch.nn.Module``): Instance of Deep4cast :class:`models`.
        * device (str): Device used for training (`cpu` or `cuda`).
        * verbose (bool): Verbosity of forecaster.

    """
    def __init__(self,
                 model,
                 device='cpu',
                 verbose=True):
        self.device = device if torch.cuda.is_available() and 'cuda' in device else 'cpu'
        self.model = model.to(device)
        self.history = {'training': [], 'validation': []}
        self.verbose = verbose

    def predict(self, dataloader, n_samples=100) -> np.array:
        """Generates predictions.
        Arguments:
            * dataloader (``torch.utils.data.DataLoader``): Data to make forecasts.
            * n_samples (int): Number of forecast samples.

        """
        with torch.no_grad():
            predictions = []
            for batch in dataloader:
                inputs = batch[0].to(self.device)
                samples = []
                for i in range(n_samples):
                    y = self.model(inputs)
#                     outputs = self.loss(**outputs).sample((1,)).cpu()
#                     y = outputs[0]

#                     outputs = copy.deepcopy(batch)
#                     outputs = dataloader.dataset.transform.untransform(outputs)
                    samples.append(y[None, :])
                samples = np.concatenate(samples, axis=0)
                predictions.append(samples)
            predictions = np.concatenate(predictions, axis=1)

        return predictions

    def embed(self, dataloader, n_samples=100) -> np.array:
        """Generate embedding vectors.
        Arguments:
            * dataloader (``torch.utils.data.DataLoader``): Data to make embedding vectors.
            * n_samples (int): Number of forecast samples.

        """
        with torch.no_grad():
            predictions = []
            for batch in dataloader:
                inputs = batch['X'].to(self.device)
                samples = []
                for i in range(n_samples):
                    outputs, __ = self.model.encode(inputs)
                    samples.append(outputs.cpu().numpy())
                samples = np.array(samples)
                predictions.append(samples)
            predictions = np.concatenate(predictions, axis=1)

        return predictions
