# -*- coding: utf-8 -*-
"""
:File: predict.py
:Author: Zhou Donglai
:Email: zhoudl@mail.ustc.edu.cn
"""
import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def load_data(file, use_im_freq=False):
    x = pd.read_excel(file, sheet_name='descriptors')
    y = pd.read_excel(file, sheet_name='predictive')
    if not use_im_freq:
        x.iloc[np.where(x['fre1'] < 0)[0], [0, 6]] = 0
        x.iloc[np.where(x['fre2'] < 0)[0], [1, 7]] = 0
        x.iloc[np.where(x['fre3'] < 0)[0], [2, 8]] = 0
    return x, y


class CustomModel:
    def __init__(self, layers=6, units=1024, rate=0., activation='relu', loss='mae', optimizer='adam',
                 max_learning_rate=1e-3, metrics=None, batch_size=120, max_epochs=10000, norm=None):
        self.layers = layers
        self.units = units
        self.rate = rate
        self.activation = activation
        self.loss = loss
        self.optimizer = optimizer
        self.max_learning_rate = max_learning_rate
        self.metrics = metrics
        self.batch_size = batch_size
        self.max_epochs = max_epochs
        self.norm = norm
        self._score_column = None

        self.model = tf.keras.models.Sequential()
        for i in range(self.layers - 1):
            self.model.add(tf.keras.layers.Dense(self.units, activation=self.activation))
            self.model.add(tf.keras.layers.Dropout(self.rate))
        self.model.add(tf.keras.layers.Dense(8))

    def fit(self, x, y, validation_data=None, **kwargs):
        self.model.compile(loss=self.loss, optimizer=tf.keras.optimizers.get(
            {'class_name': self.optimizer, 'config': {'learning_rate': self.max_learning_rate}}
        ), metrics=self.metrics)

        if self.norm is None:
            self.norm = [StandardScaler().fit(x), StandardScaler().fit(y)]
        x_ = self.norm[0].transform(x)
        y_ = self.norm[1].transform(y)

        if validation_data is not None:
            validation_data = (self.norm[0].transform(validation_data[0]),
                               self.norm[1].transform(validation_data[1]))
        return self.model.fit(x_, y_, batch_size=self.batch_size, epochs=self.max_epochs,
                              validation_data=validation_data, **kwargs)

    def predict(self, x, y_true=None, batch_size=12000, **kwargs):
        x_ = self.norm[0].transform(x)
        y_ = self.model.predict(x_, batch_size=batch_size, **kwargs)
        y_pred = self.norm[1].inverse_transform(y_)

        if y_true is not None:
            y_true = np.array(y_true)
            for i in range(y_pred.shape[0]):
                if y_pred[i, 5] - y_true[i, 5] < -180:
                    y_pred[i, 5] += 360
                if y_pred[i, 5] - y_true[i, 5] > 180:
                    y_pred[i, 5] -= 360
                if y_pred[i, 5] < -180:
                    y_pred[i, 5] = -180
                if y_pred[i, 5] > 180:
                    y_pred[i, 5] = 180

        return y_pred

    def score(self, x, y, norm=True, loss=None):
        y_pred = self.predict(x, y)

        if loss is None:
            loss_func = tf.keras.losses.get(self.loss)
        else:
            loss_func = tf.keras.losses.get(loss)

        if norm:
            ls = loss_func(self.norm[1].transform(y).T,
                           self.norm[1].transform(y_pred).T)
            return -ls.numpy()[self._score_column].mean()
        else:
            ls = loss_func(y.T, y_pred.T)
            return -ls.numpy()[self._score_column]

    def r2_score(self, x, y):
        return r2_score(y, self.predict(x, y), multioutput='raw_values')

    def save(self, file):
        self.model.save(file)
        joblib.dump(self.norm, file + '/norm.pkl')

    def load(self, file):
        # todo: Load params
        self.model = tf.keras.models.load_model(file)
        self.norm = joblib.load(file + '/norm.pkl')
        return self


class CustomCallback(tf.keras.callbacks.Callback):
    def __init__(self, decay_epoch=100, decay=0.5, min_delta=1e-5,
                 monitor='loss', patience=15, min_lr=1e-6, factor=0.5):
        super(CustomCallback, self).__init__()

        self.decay_epoch = decay_epoch
        self.decay = decay ** (1 / self.decay_epoch)
        self.min_delta = min_delta
        self.monitor = monitor
        self.patience = patience
        self.min_lr = min_lr
        self.factor = factor

        self.best = np.Inf
        self.wait = 0
        self.monitor_op = lambda a, b: np.less(a, b - self.min_delta)

    def on_epoch_end(self, epoch, logs=None):
        if epoch < self.decay_epoch:
            self.model.optimizer.lr.assign(self.model.optimizer.lr * self.decay)
        else:
            current = logs.get(self.monitor)
            if self.monitor_op(current, self.best):
                self.best = current
                self.wait = 0
            else:
                self.wait += 1
                if self.wait >= self.patience:
                    self.model.optimizer.lr.assign(
                        self.model.optimizer.lr * self.factor)
                    print('Reduce learning rate to %e.'
                          % self.model.optimizer.lr.numpy())
                    if self.model.optimizer.lr.numpy() < self.min_lr:
                        self.model.stop_training = True
                    self.best = np.Inf
                    self.wait = 0


file = 'model'
model = CustomModel().load(file)
x, y = load_data('data.xlsx')
seed = 0
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=seed)
train_pred = model.predict(x_train, y_train)
test_pred = model.predict(x_test, y_test)

with pd.ExcelWriter(f'prediction.xlsx') as writer:
    y_train.to_excel(writer, sheet_name='y_train', index=False)
    pd.DataFrame(train_pred, columns=y.columns).to_excel(writer, sheet_name='train_pred', index=False)
    y_test.to_excel(writer, sheet_name='y_test', index=False)
    pd.DataFrame(test_pred, columns=y.columns).to_excel(writer, sheet_name='test_pred', index=False)

plt.rc('font', size=12)
fig = plt.figure(figsize=(20, 10))

l = 0.2
b = 0.16
w1 = 0.56
w2 = 0.2
s = 0.02

axes = [[] for i in range(8)]
for i, ax in enumerate(axes[:4]):
    ax.append(fig.add_axes([(i + l) / 4, (1 + b) / 2, w1 / 4, w1 / 2]))
    ax.append(fig.add_axes([(i + l) / 4, (1 + b + w1 + s) / 2, w1 / 4, w2 / 2]))
    ax.append(fig.add_axes([(i + l + w1 + s) / 4, (1 + b) / 2, w2 / 4, w1 / 2]))
for i, ax in enumerate(axes[4:]):
    ax.append(fig.add_axes([(i + l) / 4, b / 2, w1 / 4, w1 / 2]))
    ax.append(fig.add_axes([(i + l) / 4, (b + w1 + s) / 2, w1 / 4, w2 / 2]))
    ax.append(fig.add_axes([(i + l + w1 + s) / 4, b / 2, w2 / 4, w1 / 2]))

fig.text(0, 1, '$\\mathbf{a}$', fontsize=24, ha='left', va='top')
fig.text(1 / 4, 1, '$\\mathbf{b}$', fontsize=24, ha='left', va='top')
fig.text(1 / 2, 1, '$\\mathbf{c}$', fontsize=24, ha='left', va='top')
fig.text(3 / 4, 1, '$\\mathbf{d}$', fontsize=24, ha='left', va='top')
fig.text(0, 1 / 2, '$\\mathbf{e}$', fontsize=24, ha='left', va='top')
fig.text(1 / 4, 1 / 2, '$\\mathbf{f}$', fontsize=24, ha='left', va='top')
fig.text(1 / 2, 1 / 2, '$\\mathbf{g}$', fontsize=24, ha='left', va='top')
fig.text(3 / 4, 1 / 2, '$\\mathbf{h}$', fontsize=24, ha='left', va='top')

for i, ax in enumerate(axes):
    for a in ax:
        a.tick_params(direction='in')
    y_min = min(y_test.iloc[:, i].min(), test_pred[:, i].min())
    y_max = max(y_test.iloc[:, i].max(), test_pred[:, i].max())
    lim = [y_min - (y_max - y_min) * 0.05, y_max + (y_max - y_min) * 0.05]

    ax[0].set_aspect('equal')
    ax[0].plot(lim, lim, '--', lw=1, c='k', zorder=2)
    ax[0].set_xticks(ax[0].get_xticks())
    ax[0].set_yticks(ax[0].get_xticks())
    ax[0].set_xlim(lim)
    ax[0].set_ylim(lim)
    ax[0].scatter(y_test.iloc[:, i], test_pred[:, i], s=10, zorder=1)
    ax[0].text(y_min, y_max, f"$r={np.corrcoef(y_test.iloc[:, i], test_pred[:, i])[0, 1]:.3f}$",
               ha='left', va='top', fontsize=16)

    ax[0].set_xlabel(f'$\\mathrm{{{y_test.columns[i]}\\ (Cal.)}}$', fontsize=20)
    ax[0].set_ylabel(f'$\\mathrm{{{y_test.columns[i]}\\ (NN)}}$', fontsize=20)

    ax[1].set_xticks(ax[0].get_xticks())
    ax[1].set_xlim(lim)
    ax[1].tick_params(labelbottom=False)
    ax[1].hist(y_test.iloc[:, i], bins=np.linspace(y_min, y_max, 16))
    ax[1].set_yticks([])
    ax[1].set_ylabel('$\\mathrm{Cal.\\ Distr.}$', fontsize=16)

    ax[2].set_yticks(ax[0].get_xticks())
    ax[2].set_ylim(lim)
    ax[2].tick_params(labelleft=False)
    ax[2].hist(test_pred[:, i], bins=np.linspace(y_min, y_max, 16), orientation='horizontal')
    ax[2].set_xticks([])
    ax[2].set_xlabel('$\\mathrm{NN\\ Distr.}$', fontsize=16)

fig.savefig(f'prediction.png', dpi=300)
