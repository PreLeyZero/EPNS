import torch
import torch.nn as nn
import numpy as np
import os

from epns.modules.N_Body_Sim import N_Body_Simulator
from epns.datasets import N_Body_Dataset

config_dict = dict(
    ###### general ######
    device='cuda' if torch.cuda.is_available() else 'cpu',
    # device='cpu',
    ###### data ######
    dataset=N_Body_Dataset,  # dataset class to use (from datasets directory)
    data_directory=os.path.join('data', 'celestial_dynamics'),  # path to data -- must contain train, val, test subdirectories
    limit_num_data_points_to=np.inf,  # put an integer to limit the training set size to this many data points
    batch_size=64,
    dynamic_channels=(1,2,3,4,5,6),  # channels that actually change over time (everything except the mass in this case)
    im_dim=7,  # total amount of feautures/channels
    pred_stepsize=10,  # how many timesteps to predict ahead in one go

    ###### model ######
    model=N_Body_Simulator,
    model_params=dict(
        num_layers=5,  # num layers in the 'processor' (\approx forward model)
        emb_dim=128,  # hidden dimensionality throughout the model
        nonlinearity=nn.ReLU(),  # activation function
        processor='gnn',  # processor type -- 'mlp', 'gnn', or 'fagnn' ('eqgnn' might still work)
        decoder='vae_decoder',  # 'vae_decoder' -- do not change. If you want a deterministic model, set num_latent_dim to 0 and sample_from_pred to False
        num_latent_dim=16,  # number of latent dimensions -- set to 0 for deterministic model or model without latents
        do_node_aggregation=False,  # whether to aggregate node embeddings before inferring prior/posterior distribution -- set to True for permutation invariant latents
        sample_from_pred=False,  # whether to sample from the decoding distribution or take the mean
    ),



    ###### training etc ######
    loss_func=nn.MSELoss(reduction='sum'),  # only used for calculating some validation statistics
    optimizer=torch.optim.Adam,  # optimizer
    opt_kwargs={'lr': 1e-4, 'weight_decay': 1e-4},  # optimizer parameters
    num_epochs=200,  # number of epochs to train for
    training_strategy='multi-step',  # either 'one-step' or 'multi-step' -- see paper

    ###### save state dict as ######
    experiment={'state_dict_fname': 'n_body_PNS.pt'},
)
