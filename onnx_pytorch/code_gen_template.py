class CodeGenTemplate:

  @classmethod
  def autogen_head(cls):
    return '''# Autogenerated by onnx-pytorch.
'''

  @classmethod
  def imports(cls):
    return '''import glob
import os
import math

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
'''

  @classmethod
  def model(cls, model_init, model_forward, model_method, test_run_model):
    return f'''{cls.autogen_head()}
{cls.imports()}

class Model(nn.Module):
  def __init__(self):
    super(Model, self).__init__()
    self._vars = nn.ParameterDict()
    self._regularizer_params = []
    for b in glob.glob(
        os.path.join(os.path.dirname(__file__), "variables", "*.npy")):
      v = torch.from_numpy(np.load(b))
      requires_grad = v.dtype.is_floating_point or v.dtype.is_complex
      self._vars[os.path.basename(b)[:-4]] = nn.Parameter(v, requires_grad=requires_grad)
    {model_init}

  def forward(self, *inputs):
    {model_forward}

  {model_method}
{test_run_model}
'''
