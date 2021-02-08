import argparse
import os

import numpy as np
import tensorflow as tf

import flwr as fl

# Make TensorFlow log less verbose
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


# Define Flower client
class CifarClient(fl.client.NumPyClient):
    def __init__(self, model, x_train, y_train, x_test, y_test):
        self.model = model
        self.x_train, self.y_train = x_train, y_train
        self.x_test, self.y_test = x_test, y_test

    def get_parameters(self):  # type: ignore
        return self.model.get_weights()

    def fit(self, parameters, config):  # type: ignore
        # Update local model parameters
        self.model.set_weights(parameters)

        # Get hyperparameters for this round
        batch_size: int = config["batch_size"]
        epochs: int = config["local_epochs"]

        # Train the model using hyperparameters from config
        history = self.model.fit(
            self.x_train, self.y_train, batch_size, epochs, validation_split=0.1
        )

        # Return updated model weights and results
        parameters_prime = self.model.get_weights()
        num_train_examples = len(self.x_train)
        results = {
            "loss": history.history["loss"][0],
            "accuracy": history.history["accuracy"][0],
            "val_loss": history.history["val_loss"][0],
            "val_accuracy": history.history["val_accuracy"][0],
        }
        return parameters_prime, num_train_examples, results

    def evaluate(self, parameters, config):  # type: ignore
        # Update local model with global parameters
        self.model.set_weights(parameters)

        # Get config values
        steps: int = config["val_steps"]

        # Evaluate global model parameter on the local test data
        loss, accuracy = self.model.evaluate(self.x_test, self.y_test, 32, steps=steps)

        # Populate the 3rd return value with a 0.0 float, it'll be removed in the future
        return len(self.x_test), loss, 0.0, {"loss": loss, "accuracy": accuracy}


def main() -> None:
    # Parse command line argument `partition`
    parser = argparse.ArgumentParser(description="Flower")
    parser.add_argument("--partition", type=int, choices=range(0, 10), required=True)
    args = parser.parse_args()

    # Load and compile Keras model
    model = tf.keras.applications.MobileNetV2((32, 32, 3), classes=10, weights=None)
    model.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])

    # Load a subset of CIFAR-10 to simulate the local data partition
    (x_train, y_train), (x_test, y_test) = load_partition(args.partition)

    # Start Flower client
    client = CifarClient(model, x_train, y_train, x_test, y_test)
    fl.client.start_numpy_client("[::]:8080", client=client)


def load_partition(idx: int):
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
    return (
        x_train[idx * 5000 : (idx + 1) * 5000],
        y_train[idx * 5000 : (idx + 1) * 5000],
    ), (
        x_test[idx * 1000 : (idx + 1) * 1000],
        y_test[idx * 1000 : (idx + 1) * 1000],
    )


if __name__ == "__main__":
    main()
