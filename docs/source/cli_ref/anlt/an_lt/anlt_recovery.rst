anlt recovery
=============

Description
-----------

Enable/disable link recovery on the specified port.
If enable, the port will keep trying ANLT when no link-up signal is detected after five seconds of waiting.


Synopsis
--------

.. code-block:: text
    
    anlt recovery
    [--on/--off]


Arguments
---------


Options
-------

``--on/--off``

Should xenaserver automatically do link recovery when detecting down signal, default to ``--on``.


Examples
--------

.. code-block:: text

    xoa-utils[123456][port0/2] > anlt recovery
    Port 0/2 link recovery on

    xoa-utils[123456][port0/2] >


.. code-block:: text

    xoa-utils[123456][port0/2] > anlt recovery --off
    Port 0/2 link recovery off

    xoa-utils[123456][port0/2] >




