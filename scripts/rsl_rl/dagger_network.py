import torch
from torch.utils.data import Dataset
import random
import os

class CustomDataset(Dataset):
    def __init__(self, max_size=None):
        self.max_size = max_size
        self.depths = []
        self.states = []
        self.actions = []
    
    def add_sample(self, depth_data, state_data, action_data):
        depth_cpu = depth_data.clone().detach().cpu()
        state_cpu = state_data.clone().detach().cpu()
        action_cpu = action_data.clone().detach().cpu()
        
        self.depths.append(depth_cpu)
        self.states.append(state_cpu)
        self.actions.append(action_cpu)

        # Check if the buffer exceeds the maximum size
        if self.max_size is not None and len(self.depths) > self.max_size:
            # Remove a random sample to maintain the buffer size
            idx_to_remove = random.randint(0, len(self.depths) - 1)
            del self.depths[idx_to_remove]
            del self.states[idx_to_remove]
            del self.actions[idx_to_remove]

    def __len__(self):
        return len(self.depths)

    def __getitem__(self, idx):
        return self.depths[idx], self.states[idx], self.actions[idx]

import torch.nn as nn
import torch.nn.functional as F

class CNNEncoder(nn.Module):
    """
    Encodes an image (B, 1, H, W) -> (B, cnn_dim)
    """
    def __init__(self, cnn_dim: int = 256):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=8, stride=4),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=4, stride=2),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3, stride=1),
            nn.ReLU(),
        )
        self.fc = nn.LazyLinear(cnn_dim)

    def forward(self, x):
        x = self.net(x)
        x = x.flatten(1)
        x = self.fc(x)
        return x


class MLPEncoder(nn.Module):
    """
    Encodes numeric features (B, mlp_in) -> (B, mlp_dim)
    """
    def __init__(self, mlp_in: int, mlp_dim: int = 128):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(mlp_in, 128),
            nn.ReLU(),
            nn.Linear(128, mlp_dim),
            nn.ReLU(),
        )

    def forward(self, x):
        return self.net(x)


class DaggerNet(nn.Module):
    """
    Inputs:
      img_seq:  (B, T, C, H, W)
      vec_seq:  (B, T, F)

    Output:
      logits (or actions): (B, T, output_size) if return_sequences=True
                           (B, output_size)   if return_sequences=False (last step)
    """
    def __init__(
        self,
        vec_size: int,
        output_size: int,
        cnn_dim: int = 256,
        mlp_dim: int = 128,
        lstm_hidden: int = 256,
        lstm_layers: int = 1,
        dropout: float = 0.0,
        return_sequences: bool = True,
    ):
        super().__init__()
        self.return_sequences = return_sequences

        self.cnn = CNNEncoder(cnn_dim=cnn_dim)
        self.mlp = MLPEncoder(mlp_in=vec_size, mlp_dim=mlp_dim)

        self.dataset = CustomDataset(max_size=40000)

        lstm_in = cnn_dim + mlp_dim
        self.lstm = nn.LSTM(
            input_size=lstm_in,
            hidden_size=lstm_hidden,
            num_layers=lstm_layers,
            batch_first=True,
            dropout=dropout if lstm_layers > 1 else 0.0,
        )

        self.head = nn.Sequential(
            nn.Linear(lstm_hidden, 128),
            nn.ReLU(),
            nn.Linear(128, output_size),
        )

    def forward(self, depth_seq, vec_seq, hidden=None):
        B, T = depth_seq.shape[0], depth_seq.shape[1]

        # CNN per timestep
        depth_flat = depth_seq.reshape(B * T, *depth_seq.shape[2:])  # (B*T, 1, H, W)
        depth_emb = self.cnn(depth_flat).reshape(B, T, -1)           # (B, T, cnn_dim)

        # MLP per timestep
        vec_flat = vec_seq.reshape(B * T, vec_seq.shape[-1])         # (B*T, F)
        vec_emb = self.mlp(vec_flat).reshape(B, T, -1)               # (B, T, mlp_dim)

        # Fuse -> LSTM
        x = torch.cat([depth_emb, vec_emb], dim=-1)                  # (B, T, cnn_dim+mlp_dim)
        lstm_out, new_hidden = self.lstm(x, hidden)                  # (B, T, lstm_hidden)

        if self.return_sequences:
            out = self.head(lstm_out)                                # (B, T, output_size)
        else:
            out = self.head(lstm_out[:, -1])                         # (B, output_size)

        return out, new_hidden
    
    def train(self, batch_size=512, epochs=1000, learning_rate=1e-3, device='cpu', validation_split=0.2):
        """Train the network with validation loss tracking.
        
        Args:
            batch_size: Batch size for training
            epochs: Number of training epochs
            learning_rate: Learning rate for optimizer
            device: Device to train on ('cpu' or 'cuda')
            validation_split: Fraction of data to use for validation (0.0 to 1.0)
        """
        # Split dataset into training and validation
        dataset_size = len(self.dataset)
        if dataset_size == 0:
            print("Warning: Dataset is empty. Cannot train.")
            return
        
        val_size = int(dataset_size * validation_split)
        train_size = dataset_size - val_size
        train_dataset, val_dataset = torch.utils.data.random_split(self.dataset, [train_size,
                                                                                    val_size])
        train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        val_loader = torch.utils.data.DataLoader(val_dataset, batch_size=batch_size, shuffle=False
        )
        # Define optimizer and loss function
        optimizer = torch.optim.Adam(self.parameters(), lr=learning_rate)
        loss_fn = torch.nn.MSELoss()
        self.to(device)

        for epoch in range(epochs):
            self.train()
            total_train_loss = 0.0
            for batch in train_loader:
                depths, states, actions = batch
                depths = depths.to(device)
                states = states.to(device)
                actions = actions.to(device)

                #todo: handle hidden state properly for LSTM

                optimizer.zero_grad()
                outputs, _ = self.forward(depths, states, hidden=None)
                loss = loss_fn(outputs, actions)
                loss.backward()
                optimizer.step()
                total_train_loss += loss.item() * depths.size(0)

            avg_train_loss = total_train_loss / train_size

            # Validation phase
            self.eval()
            total_val_loss = 0.0
            with torch.no_grad():
                for batch in val_loader:
                    depths, states, actions = batch
                    depths = depths.to(device)
                    states = states.to(device)
                    actions = actions.to(device)

                    outputs, _ = self.forward(depths, states, hidden=None)
                    loss = loss_fn(outputs, actions)
                    total_val_loss += loss.item() * depths.size(0)

            avg_val_loss = total_val_loss / val_size

            print(f"Epoch [{epoch+1}/{epochs}], Train Loss: {avg_train_loss:.4f}, Val Loss: {avg_val_loss:.4f}")
    