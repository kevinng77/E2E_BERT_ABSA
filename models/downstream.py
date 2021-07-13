import torch.nn as nn
import torch


class SelfAttention(nn.Module):
    def __init__(self, d_model, num_heads, dropout):
        super(SelfAttention, self).__init__()
        self.self_attn = nn.MultiheadAttention(embed_dim=d_model,
                                               num_heads=num_heads,
                                               dropout=dropout)
        self.dropout = nn.Dropout(dropout)
        self.layer_norm = nn.LayerNorm(d_model)

    def forward(self, inputs, attention_mask=None, key_padding_mask=None):
        inputs_att, _ = self.self_attn(inputs, inputs, inputs,
                                       attn_mask=attention_mask,
                                       key_padding_mask=key_padding_mask)
        outputs = inputs + self.dropout(inputs_att)
        outputs = self.layer_norm(outputs)
        return outputs


class LSTM(nn.Module):
    def __init__(self, d_model, hidden_dim, num_layers, args):
        super(LSTM, self).__init__()
        self.hidden_dim = hidden_dim
        self.layer_dim = num_layers
        self.lstm = nn.LSTM(input_size=d_model, hidden_size=hidden_dim, num_layers=num_layers, batch_first=True)
        # （batch_size,seq_len,input_size)
        # self.fc = nn.Linear(hidden_dim, output_dim)
        self.h0 = torch.zeros(self.layer_dim, args.batch_size, self.hidden_dim).requires_grad_().to(args.device)
        self.c0 = torch.zeros(self.layer_dim, args.batch_size, self.hidden_dim).requires_grad_().to(args.device)

    def forward(self, x):
        out, (hn, cn) = self.lstm(x, (self.h0.detach(), self.c0.detach()))
        # out-->(batch_size,seq_len,hidden_size)
        # out[:, -1, :] --> just want last time step hidden states!
        # out = self.fc(out[:, -1, :])
        return out


class CRF(nn.Module):
    pass
