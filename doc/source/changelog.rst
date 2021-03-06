Changelog
=========

Unreleased
----------

What's new?

* **Generalized** :code:`Client.fit` **and** :code:`Client.evaluate` **return values** (`#610 <https://github.com/adap/flower/pull/610>`_, `#572 <https://github.com/adap/flower/pull/572>`_)

  Clients can now return an additional dictionary mapping :code:`str` keys to values of the following types: :code:`bool`, :code:`bytes`, :code:`float`, :code:`int`, :code:`str`. This means one can return almost arbitrary values from :code:`fit`/:code:`evaluate` and make use of them on the server side!
  
  In case you wondered: this feature is compatible with existing projects. The additional dictionary return value is optional, which means that :code:`NumPyClient` can handle either three or four return values. See the example below for details.

  *Code example:* note the additional dictionary return values in both :code:`FlwrClient.fit` and :code:`FlwrClient.evaluate`: 

  .. code-block:: python

    class FlwrClient(fl.client.NumPyClient):
        def fit(self, parameters, config):
            net.set_parameters(parameters)
            train_loss = train(net, trainloader)
            return net.get_weights(), len(trainloader), {"train_loss": train_loss}

        def evaluate(self, parameters, config):
            net.set_parameters(parameters)
            loss, accuracy, custom_metric = test(net, testloader)
            return len(testloader), loss, accuracy, {"custom_metric": custom_metric}

* **Generalized** :code:`config` **argument in** :code:`Client.fit` **and** :code:`Client.evaluate` (`#595 <https://github.com/adap/flower/pull/595>`_)

  The :code:`config` argument used to be of type :code:`Dict[str, str]`, which means that dictionary values were expected to be strings. The new release generalizes this to enable values of the following types: :code:`bool`, :code:`bytes`, :code:`float`, :code:`int`, :code:`str`.
  
  This means one can now pass almost arbitrary values to :code:`fit`/:code:`evaluate` using the :code:`config` dictionary. Yay, no more :code:`str(epochs)` on the server-side and :code:`int(config["epochs"])` on the client side!

  *Code example:* note that the :code:`config` dictionary now contains non-:code:`str` values in both :code:`Client.fit` and :code:`Client.evaluate`: 

  .. code-block:: python
  
    class FlwrClient(fl.client.NumPyClient):
        def fit(self, parameters, config):
            net.set_parameters(parameters)
            epochs: int = config["epochs"]
            train_loss = train(net, trainloader, epochs)
            return net.get_weights(), len(trainloader), {"train_loss": train_loss}

        def evaluate(self, parameters, config):
            net.set_parameters(parameters)
            batch_size: int = config["batch_size"]
            loss, accuracy, custom_metric = test(net, testloader, batch_size)
            return len(testloader), loss, accuracy, {"custom_metric": custom_metric}

* New built-in strategies (`#549 <https://github.com/adap/flower/pull/549>`_)
    * (abstract) FedOpt
    * FedAdagrad


v0.13.0 (2021-01-08)
--------------------

What's new?

* New example: PyTorch From Centralized To Federated (`#549 <https://github.com/adap/flower/pull/549>`_)
* Improved documentation
    * New documentation theme (`#551 <https://github.com/adap/flower/pull/551>`_)
    * New API reference (`#554 <https://github.com/adap/flower/pull/554>`_)
    * Updated examples documentation (`#549 <https://github.com/adap/flower/pull/549>`_)
    * Removed obsolete documentation (`#548 <https://github.com/adap/flower/pull/548>`_)

Bugfix:

* :code:`Server.fit` does not disconnect clients when finished, disconnecting the clients is now handled in :code:`flwr.server.start_server` (`#553 <https://github.com/adap/flower/pull/553>`_, `#540 <https://github.com/adap/flower/issues/540>`_).


v0.12.0 (2020-12-07)
--------------------

Important changes:

* Added an example for embedded devices (`#507 <https://github.com/adap/flower/pull/507>`_)
* Added a new NumPyClient (in addition to the existing KerasClient) (`#504 <https://github.com/adap/flower/pull/504>`_, `#508 <https://github.com/adap/flower/pull/508>`_)
* Deprecated `flwr_examples` package and started to migrate examples into the top-level `examples` directory (`#494 <https://github.com/adap/flower/pull/494>`_, `#512 <https://github.com/adap/flower/pull/512>`_)


v0.11.0 (2020-11-30)
--------------------

Incompatible changes:

* Renamed strategy methods (`#486 <https://github.com/adap/flower/pull/486>`_) to unify the naming of Flower's public APIs. Other public methods/functions (e.g., every method in :code:`Client`, but also :code:`Strategy.evaluate`) do not use the :code:`on_` prefix, which is why we're removing it from the four methods in Strategy. To migrate rename the following :code:`Strategy` methods accordingly:
    * :code:`on_configure_evaluate` => :code:`configure_evaluate`
    * :code:`on_aggregate_evaluate` => :code:`aggregate_evaluate`
    * :code:`on_configure_fit` => :code:`configure_fit`
    * :code:`on_aggregate_fit` => :code:`aggregate_fit`

Important changes:

* Deprecated :code:`DefaultStrategy` (`#479 <https://github.com/adap/flower/pull/479>`_). To migrate use :code:`FedAvg` instead.
* Simplified examples and baselines (`#484 <https://github.com/adap/flower/pull/484>`_).
* Removed presently unused :code:`on_conclude_round` from strategy interface (`#483 <https://github.com/adap/flower/pull/483>`_).
* Set minimal Python version to 3.6.1 instead of 3.6.9 (`#471 <https://github.com/adap/flower/pull/471>`_).
* Improved :code:`Strategy` docstrings (`#470 <https://github.com/adap/flower/pull/470>`_).
