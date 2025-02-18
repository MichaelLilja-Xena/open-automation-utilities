lt dec
======

Description
-----------

To request the remote link training partner to decrease its emphasis value by 1 bit.



Synopsis
--------

.. code-block:: text
    
lt dec <LANE> <EMPHASIS>


Arguments
---------

``<LANE>`` (integer)

Specifies the transceiver lane index.


``<EMPHASIS>`` (text)
    
The emphasis (coefficient) of the link partner.

Allowed values:

* `pre3`

* `pre2`

* `pre``

* `main`

* `post`


Options
-------



Examples
--------

.. code-block:: text

    xoa-utils[123456][port0/2] > lt dec 0 pre3
    Port 0/2 requests: decrease c(-3) by 1 on Lane 0

    xoa-utils[123456][port0/2] >

.. code-block:: text

    xoa-utils[123456][port0/2] > lt dec 1 main
    Port 0/2 requests: decrease c(0) by 1 on Lane 1

    xoa-utils[123456][port0/2] >

.. code-block:: text

    xoa-utils[123456][port0/2] > lt dec 0 pre3
    Port 0/2 requests: decrease c(-3) by 1 on Lane 0

    xoa-utils[123456][port0/2] >




