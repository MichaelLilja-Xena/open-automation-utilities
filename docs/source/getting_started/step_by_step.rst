.. role:: xbluethick
.. role:: xgreenthick

Step-by-Step Guide
===================

This section provides a step-by-step guide on how to use XOA Utility to do interactive ANLT test. 

The diagram below illustrates a basic flow of using XOA Utilities to do ANLT testing.

.. figure:: ../_static/anlt_use_flow.png
    :width: 100 %
    :align: center

.. note::

    ⚡️ You can use **tab key** to auto-complete a command to speed up your input speed.

.. important::

    Commands in :xgreenthick:`green blocks` instruct the tester to take action immediately.

    Commands in :xbluethick:`blue blocks` only configure the local state. You need to run ``anlt do`` to execute the configuration.


Connect
-------

First, you need to connect to your tester using the command :doc:`../cli_ref/mgmt/connect`.

If you don't know which ports you will use at the time of connecting to the port, just leave the option ``--ports`` empty as the example shows below. You can reserve ports later.

.. code-block:: text

    xoa-utils > connect 10.10.10.10 yourname


Reserve Port
------------

Then, reserve a port on the tester using the command :doc:`../cli_ref/mgmt/port`, as shown in the example below.

.. note::

    You can only work on one port at a time in one console window. If you want to simultaneously work on multiple ports, you can open multiple console windows.

.. code-block:: text

    xoa-utils[123456] > port 0/0


Disable Link Recovery
---------------------

Before doing ANLT testing, remember to disable link recovery on the port using command :doc:`../cli_ref/anlt/an_lt/anlt_recovery`. 

This is because the port always tries to re-do ANLT command sequence every five seconds if it detects no sync on the port. 

This will disturb your manual link training procedure if you don't disable it prior to your interactive test.

.. code-block:: text

    xoa-utils[123456][port0/0] > anlt recovery --off


Configure AN & LT
-----------------

After disabling link recovery on the port, you can start configuring AN and LT using :doc:`../cli_ref/anlt/an/an_config`, :doc:`../cli_ref/anlt/lt/lt_config`, and :doc:`../cli_ref/anlt/lt/lt_im` as the example shown below. 


.. code-block:: text

    xoa-utils[123456][port0/0] > an config --off --no-loopback

    xoa-utils[123456][port0/0] > lt config --on --preset0 --mode=interactive 

    xoa-utils[123456][port0/0] > lt im 0 nrz


.. note::

    The initial modulation of each lane on a port is by default PAM2 (NRZ). If you want to change them, you can use :doc:`../cli_ref/anlt/lt/lt_im`, otherwise do nothing.


.. important::

    :doc:`../cli_ref/anlt/an/an_config`, :doc:`../cli_ref/anlt/lt/lt_config`, and :doc:`../cli_ref/anlt/lt/lt_im` only change the local ANLT configuration state. To execute the configuration, you need to run :doc:`../cli_ref/anlt/an_lt/anlt_do`, otherwise your changes will not take effect on the tester.



Start ANLT
----------

After configuring the ANLT scenario on the port, you should execute :doc:`../cli_ref/anlt/an_lt/anlt_do` to let XOA Utilities application send low-level commands to the tester to start the ANLT procedure, either AN-only, or AN + LT, or LT (auto), or LT (interactive).

.. code-block:: text

    xoa-utils[123456][port0/0] > anlt do


Control LT Interactive
----------------------

If you run LT (interactive), you will need to manually control the LT parameters using the LT Control Commands shown in :doc:`../cli_ref/anlt/lt/index`, for example:


.. code-block:: text

    xoa-utils[123456][port0/0] > lt preset 0 2

    xoa-utils[123456][port0/0] > lt inc 0 pre3

    xoa-utils[123456][port0/0] > lt inc 0 main

    xoa-utils[123456][port0/0] > lt dec 0 post

    xoa-utils[123456][port0/0] > lt status 0

    xoa-utils[123456][port0/0] > lt trained 0

    xoa-utils[123456][port0/0] > lt txtagget 0

    xoa-utils[123456][port0/0] > lt txtagset 0 0 0 1 56 0


Check AN Status
---------------

Check AN statistics by :doc:`../cli_ref/anlt/an/an_status`.


Check LT Status
---------------

Check LT statistics by :doc:`../cli_ref/anlt/lt/lt_status`.


Check ANLT Log
--------------

Check ANLT logging by :doc:`../cli_ref/anlt/an_lt/anlt_log`.

.. code-block:: text

    xoa-utils[123456][port0/0] > anlt log -f mylog.log

.. note::

    This commands **continuously displays** the log messages on the screen so you can keep track of your ANLT actions. To **quit** the continuous display mode, press :kbd:`Control-z`.


Start Over
----------

If you want to start over on the port, you can reset the port by ``port <PORT> --reset`` as shown below.

This will bring the port back to its default state.

.. code-block:: text

    xoa-utils[123456][port0/0] > port 0/0 --reset


