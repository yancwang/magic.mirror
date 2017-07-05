# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 16:27:24 2017

@author: yancw
"""

import os
import tensorflow as tf
import numpy as np
import pandas as pd
from six.moves import cPickle as pickle
from sklearn.model_selection import train_test_split

data = None;
cluster = None;

# import data
filepath = os.path.join(os.getcwd(), 'data.pickle');
try:
	with open(filepath, 'rb') as f:
		save = pickle.load(f, encoding='latin1');
		data = save['data'];
		cluster = save['cluster'];
		del save  # hint to help gc free up memory
		print('Data size:', data.shape, cluster.shape);
except Exception as e:
	print('Could not read file: ' + filepath);
	raise e;

cluster = (np.arange(6) == cluster[:,None]).astype(np.float32);
data = data.astype(np.float32);

data_train, data_test, cluster_train, cluster_test = train_test_split(data, cluster, test_size=0.2, random_state=0);
print('Training set size:', data_train.shape, cluster_train.shape);
print('Testing set size:', data_test.shape, cluster_test.shape);

# calculate accuracy
def accuracy(predictions, labels):
	return (100.0 * np.sum(np.argmax(predictions, 1) == np.argmax(labels, 1)) / predictions.shape[0])

tf.logging.set_verbosity(tf.logging.DEBUG)
# linear model
graph = tf.Graph();
with graph.as_default():
	train_data = tf.constant(data_train);
	train_cluster =  tf.constant(cluster_train);
	test_data = tf.constant(data_test);

	weights = tf.Variable(tf.truncated_normal([25, 6]));
	bias = tf.Variable(tf.zeros([6]));

	logits = tf.matmul(train_data, weights) + bias;
	loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=train_cluster, logits=logits));

	optimizer = tf.train.GradientDescentOptimizer(0.5).minimize(loss);
	train_prediction = tf.nn.softmax(logits);
	test_prediction = tf.nn.softmax(tf.matmul(test_data, weights) + bias);

	num_steps = 200;

with tf.Session(graph=graph) as session:
	tf.global_variables_initializer().run();
	print('Initialized');

	for step in range(0, num_steps):
		_, l, predictions = session.run([optimizer, loss, train_prediction]);

	print('Test accuracy: %.1f%%' % accuracy(test_prediction.eval(), cluster_test));

# neural network model
num_hidden_nodes = 16;

graph = tf.Graph()
with graph.as_default():
	train_data = tf.constant(data_train);
	train_cluster =  tf.constant(cluster_train);
	test_data = tf.constant(data_test);

	# variables
	weights1 = tf.Variable(tf.truncated_normal([25, num_hidden_nodes]));
	biases1 = tf.Variable(tf.zeros([num_hidden_nodes]));
	weights2 = tf.Variable(tf.truncated_normal([num_hidden_nodes, 6]));
	biases2 = tf.Variable(tf.zeros([6]));

	# training computation
	train_layer = tf.nn.relu(tf.matmul(train_data, weights1) + biases1);
	logits = tf.matmul(train_layer, weights2) + biases2;
	loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=train_cluster, logits=logits));

	# optimizer
	optimizer = tf.train.GradientDescentOptimizer(0.5).minimize(loss);

	# predictions for the training, validation, and test data
	train_prediction = tf.nn.softmax(logits);
	test_layer = tf.nn.relu(tf.matmul(test_data, weights1) + biases1);
	test_prediction = tf.nn.softmax(tf.matmul(test_layer, weights2) + biases2);

num_steps = 1001;

with tf.Session(graph=graph) as session:
	tf.global_variables_initializer().run()
	print("Initialized")
	for step in range(num_steps):
		_, l, predictions = session.run([optimizer, loss, train_prediction])
		if (step % 200 == 0):
			print("Training loss at step %d: %f" % (step, l))
			# print("Training accuracy: %.1f%%" % accuracy(predictions, train_cluster))
			print("Testing accuracy: %.1f%%" % accuracy(test_prediction.eval(), cluster_test))

# random forest model
from sklearn.ensemble import RandomForestClassifier


# cross validation
