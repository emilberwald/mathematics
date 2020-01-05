r"""
.. |br| raw:: html

   <br/>

.. |A*-closure| replace:: closure: |br|
    :math:`\forall a,b\in A\colon\quad        A\ni\quad    a \underset{A}{\cdot} b`
.. |A*-left-zero| replace:: left zero (annihilating/absorbing element): |br|
    :math:`\forall a\in A\colon\quad        \underset{A}{0} \underset{A}{\cdot} a = \underset{A}{0}`
.. |A*-right-zero| replace:: right zero (annihilating/absorbing element): |br|
    :math:`\forall a\in A\colon\quad        a \underset{A}{\cdot} \underset{A}{0} = \underset{A}{0}`
.. |A*-idempotency| replace:: idempotency: |br|
    :math:`\forall a\in A\colon\quad        a \underset{A}{\cdot} a = a`
.. |A*-associative| replace:: associative: |br|
    :math:`\forall a,b,c\in A\colon\quad        (a \underset{A}{\cdot} b)\underset{A}{\cdot} c = a \underset{A}{\cdot} (b \underset{A}{\cdot} c )`
.. |A*-identity-element| replace:: (unique) identity element: |br|
    :math:`\exists \underset{A}{1}\in A\colon\forall a\in A\colon\quad        \underset{A}{1} \underset{A}{\cdot} a = a =  a \underset{A}{\cdot} \underset{A}{1}`
.. |A*-inverse-element| replace:: inverse element: |br|
    :math:`\forall a \in A \exists b \in A \colon\quad        a \underset{A}{\cdot} b = \underset{A}{1} = b \underset{A}{\cdot} a`
.. |A*-commutative| replace:: commutative:  |br|
    :math:`\forall a,b \in A \colon\quad        a \underset{A}{\cdot} b = b \underset{A}{\cdot} a`
.. |A*-latinsquare| replace:: latin square property:  |br|
    :math:`\forall a,b \in A !\exists x_L,x_R\in A \colon\quad        x_L \underset{A}{\cdot} a = b \land a \underset{A}{\cdot} x_R = b`

.. |A+-closure| replace:: closure: |br|
    :math:`\forall a,b\in A\colon\quad        A\ni\quad    a \underset{A}{+} b`
.. |A+-left-zero| replace:: left zero (absorbing element): |br|
    :math:`\forall a\in A\colon\quad        \underset{A}{0} \underset{A}{+} a = \underset{A}{0}`
.. |A+-right-zero| replace:: right zero (absorbing element): |br|
    :math:`\forall a\in A\colon\quad        a \underset{A}{+} \underset{A}{0} = \underset{A}{0}`
.. |A+-idempotency| replace:: idempotency: |br|
    :math:`\forall a\in A\colon\quad        a \underset{A}{+} a = a`
.. |A+-associative| replace:: associative: |br|
    :math:`\forall a,b,c\in A\colon\quad        (a \underset{A}{+} b)\underset{A}{+} c = a \underset{A}{+} (b \underset{A}{+} c )`
.. |A+-identity-element| replace:: (unique) identity element: |br|
    :math:`\exists \underset{A}{0}\in A\colon\forall a \in A\quad        \underset{A}{0} \underset{A}{+} a = a = a \underset{A}{+} \underset{A}{0}`
.. |A+-inverse-element| replace:: inverse element: |br|
    :math:`\forall a \in A \exists b \in A \colon\quad        a \underset{A}{+} b = \underset{A}{0} = b \underset{A}{+} a`
.. |A+-commutative| replace:: commutative:  |br|
    :math:`\forall a,b \in A \colon\quad        a \underset{A}{+} b = b \underset{A}{+} a`
.. |A*-left-distributive-A+| replace:: left distributivity of :math:`\underset{A}{\cdot}` with respect to :math:`\underset{A}{+}`: |br|
    :math:`\forall a_1, a_2, a_3\in A\colon\quad        a_1 \underset{A}{\cdot}(a_2 \underset{A}{+} a_3) = a_1 \underset{A}{\cdot} a_2 \underset{A}{+} a_1 \underset{A}{\cdot} a_3`
.. |A*-right-distributive-A+| replace:: right distributivity of :math:`\underset{A}{\cdot}` with respect to :math:`\underset{A}{+}`: |br|
    :math:`\forall a_1,a_2,a_3 \in A\colon\quad        (a_1 \underset{A}{+} a_2)\underset{A}{\cdot} a_3 = a_1 \underset{A}{\cdot} a_3 \underset{A}{+} a_2 \underset{A}{\cdot} a_3`
.. |A+A*-identities-different| replace:: The identity elements are different: |br|
    :math:`\underset{A}{1}\neq \underset{A}{0}`
.. |A+A*-absorption-law| replace:: NOTE: the absorption law is for meets :math:`\land` and joins :math:`\lor` in partially ordered sets (lattice structures): |br|
    :math:`\forall a,b\in A\colon\quad a \underset{A}{+}(a \underset{A}{*} b) = a \underset{A}{*}(a \underset{A}{+} b) = a`

.. |RA*-exist| replace:: Set action on group: |br|
	:math:`\forall r\in R \forall a\in A\colon\quad r \underset{{}_R A} a \in A`
.. |RA*-left-distributive-A+| replace:: left distributivity of :math:`\underset{{}_{R}A}{\cdot}` with respect to :math:`\underset{A}{+}`: |br|
    :math:`\forall r\in R\forall a_1,a_2\in A\colon\quad        r \underset{{}_{R}A}{\cdot}(a_1 \underset{A}{+} a_2) = r \underset{{}_{R}A}{\cdot} a_1 \underset{A}{+} r \underset{{}_{R}A}{\cdot} a_2`
.. |RA*-right-distributive-A+| replace:: right distributivity of :math:`\underset{{}_{R}A}{\cdot}` with respect to :math:`\underset{A}{+}`: |br|
    :math:`\forall r_1,r_2\in R\forall a\in A\colon\quad        (r_1 \underset{R}{+} r_2)\underset{{}_{R}A}{\cdot} a = r_1 \underset{{}_{R}A}{\cdot} a \underset{A}{+} r_2 \underset{{}_{R}A}{\cdot} a`
.. |R*-RA*-compat| replace:: compatability of scalar multiplication with ring multiplication: |br|
    :math:`\forall r_1,r_2\in R\forall a\in A\colon\quad        (r_1 \underset{R}{\cdot} r_2)\underset{{}_{R}A}{\cdot} a = r_1 \underset{{}_{R}A}{\cdot} (r_2 \underset{{}_{R}A}{\cdot} a)`
.. |R*1-RA*-compat| replace:: compatability of :math:`\underset{{}_{R}A}{\cdot}` with ring unit: |br|
    :math:`\forall a \in A \quad 1_R \underset{{}_{R}A}{\cdot} a = a`
.. |A+-direct-sum| replace:: direct sum decomposition (can be generalized to higher grades):
	:math:`\forall a_1,b_1\in A_1\forall a_2,b_2\in A_2\colon\quad (a_1,a_2)\underset{A_1\times A_2}{+}(b_1,b_2) = (a_1\underset{A_1}{+}b_1,a_2\underset{A_2}{+}b_2)`
.. |R*-A+-direct-sum-compat| replace:: direct sum decomposition, scalar product compatability (can be generalized to higher grades):
	:math:`\forall r\in R\forall a_1\in A_1\forall a_2\in A_2\colon\quad r\underset{{}_R A_1\times A_2}{\cdot}(a_1,a_2) = (r\underset{{}_R A_1}{\cdot}a_1,r\underset{{}_R A_2}{\cdot}a_2)`

.. |R*-RA*-A*-compat| replace:: compatability of (vector) multiplication, scalar multiplication and field multiplication |br|
    :math:`\forall r_1,r_2\in R \forall a_1,a_2\in A \quad    (r_1 \underset{{}_R A}{\cdot} a_1)\underset{A}{\cdot}(r_2\underset{{}_R A}{\cdot}a_2) = (r_1\underset{R}{\cdot}r_2)\underset{{}_R A}{\cdot}(a_1\underset{A}{\cdot}a_2)`
.. |R*-A*-associative| replace:: compatability/associativity(?) of (vector) multiplication with scalar multiplication |br|
    :math:`\forall r\in R\forall a_1,a_2\in A\quad  r \underset{{}_R A}{\cdot}(a_1 \underset{A}{\cdot} a_2) = (r \underset{{}_R A}{\cdot} a_1) \underset{A}{\cdot} a_2 = a_1\underset{A}{\cdot} (r \underset{{}_R A}{\cdot} a_2)`
.. |A*-normed| replace:: normed |br|
    :math:`\forall a_1,a_2\in A \quad \Vert a_1\underset{A}{\cdot} a_2 \Vert \leq \Vert a_1\Vert \underset{R}{\cdot} \Vert a_2\Vert\land \exists \underset{A}{1} \Rightarrow \Vert\underset{A}{1}\Vert = \underset{R}{1}`


================================
One binary operation (:math:`A`)
================================

+-----------------------+----------------+-----------+--------+-------+---------------+-------------+------------+------+
| Axiom                 | Magma/Groupoid | Semigroup | Monoid | Group | Abelian group | Semilattice | Quasigroup | Loop |
+=======================+================+===========+========+=======+===============+=============+============+======+
| |A*-closure|          | x              | x         | x      | x     | x             | x           | x          | x    |
+-----------------------+----------------+-----------+--------+-------+---------------+-------------+------------+------+
| |A*-associative|      |                | x         | x      | x     | x             | x           |            |      |
+-----------------------+----------------+-----------+--------+-------+---------------+-------------+------------+------+
| |A*-identity-element| |                |           | x      | x     | x             |             |            | x    |
+-----------------------+----------------+-----------+--------+-------+---------------+-------------+------------+------+
| |A*-inverse-element|  |                |           |        | x     | x             |             |            |      |
| [1]_                  |                |           |        |       |               |             |            |      |
+-----------------------+----------------+-----------+--------+-------+---------------+-------------+------------+------+
| |A*-commutative|      |                |           |        |       | x             | x           |            |      |
+-----------------------+----------------+-----------+--------+-------+---------------+-------------+------------+------+
| |A*-idempotency|      |                |           |        |       |               | x           |            |      |
+-----------------------+----------------+-----------+--------+-------+---------------+-------------+------------+------+
| |A*-latinsquare|      |                |           |        |       |               |             | x          | x    |
+-----------------------+----------------+-----------+--------+-------+---------------+-------------+------------+------+
| |A*-left-zero|        |                |           |        |       |               |             |            |      |
+-----------------------+----------------+-----------+--------+-------+---------------+-------------+------------+------+
| |A*-right-zero|       |                |           |        |       |               |             |            |      |
+-----------------------+----------------+-----------+--------+-------+---------------+-------------+------------+------+

=================================
Two binary operations (:math:`A`)
=================================

+----------------------------------------------+-----+--------------------+---------------+-------+------------------+--------------------+--------------------+--------------+------------------------------------------------+
| Axiom                                        | Rng | Ring with identity | Division ring | Field | Commutative ring | (right) near-ring  | (left) near ring   | Semiring/rig | Idempotent semiring/join-semilattice with zero |
+----------------------------------------------+-----+--------------------+---------------+-------+------------------+--------------------+--------------------+--------------+------------------------------------------------+
| |A+-closure|                                 | x   | x                  | x             | x     | x                | x                  | x                  | x            | x                                              |
+----------------------------------------------+-----+--------------------+---------------+-------+------------------+--------------------+--------------------+--------------+------------------------------------------------+
| |A+-associative|                             | x   | x                  | x             | x     | x                | x                  | x                  | x            | x                                              |
+----------------------------------------------+-----+--------------------+---------------+-------+------------------+--------------------+--------------------+--------------+------------------------------------------------+
| |A+-identity-element|                        | x   | x                  | x             | x     | x                | x                  | x                  | x            | x                                              |
+----------------------------------------------+-----+--------------------+---------------+-------+------------------+--------------------+--------------------+--------------+------------------------------------------------+
| |A+-inverse-element|                         | x   | x                  | x             | x     | x                | x                  | x                  |              |                                                |
+----------------------------------------------+-----+--------------------+---------------+-------+------------------+--------------------+--------------------+--------------+------------------------------------------------+
| |A+-commutative|                             | x   | x                  | x             | x     | x                |                    |                    | x            | x                                              |
+----------------------------------------------+-----+--------------------+---------------+-------+------------------+--------------------+--------------------+--------------+------------------------------------------------+
| |A*-closure|                                 | x   | x                  | x             | x     | x                | x                  | x                  | x            | x                                              |
+----------------------------------------------+-----+--------------------+---------------+-------+------------------+--------------------+--------------------+--------------+------------------------------------------------+
| |A*-associative|                             | x   | x                  | x             | x     | x                | x                  | x                  | x            | x                                              |
+----------------------------------------------+-----+--------------------+---------------+-------+------------------+--------------------+--------------------+--------------+------------------------------------------------+
| |A*-left-distributive-A+|                    | x   | x                  | x             | x     | x                |                    | x                  | x            | x                                              |
+----------------------------------------------+-----+--------------------+---------------+-------+------------------+--------------------+--------------------+--------------+------------------------------------------------+
| |A*-right-distributive-A+|                   | x   | x                  | x             | x     | x                | x                  |                    | x            | x                                              |
+----------------------------------------------+-----+--------------------+---------------+-------+------------------+--------------------+--------------------+--------------+------------------------------------------------+
| |A*-identity-element|                        |     | x                  | x             | x     | x                |                    |                    | x            | x                                              |
+----------------------------------------------+-----+--------------------+---------------+-------+------------------+--------------------+--------------------+--------------+------------------------------------------------+
| |A+A*-identities-different|                  |     |                    | x             | x     |                  |                    |                    |              |                                                |
+----------------------------------------------+-----+--------------------+---------------+-------+------------------+--------------------+--------------------+--------------+------------------------------------------------+
| |A*-inverse-element|                         |     |                    | x             | x     |                  |                    |                    |              |                                                |
| NOTE: no inverse for :math:`\underset{A}{0}` |     |                    |               |       |                  |                    |                    |              |                                                |
+----------------------------------------------+-----+--------------------+---------------+-------+------------------+--------------------+--------------------+--------------+------------------------------------------------+
| |A*-commutative|                             |     |                    |               | x     | x                |                    |                    |              |                                                |
+----------------------------------------------+-----+--------------------+---------------+-------+------------------+--------------------+--------------------+--------------+------------------------------------------------+
| |A*-left-zero|                               |     |                    |               |       |                  | :math:`\Downarrow` |                    | x            | x                                              |
+----------------------------------------------+-----+--------------------+---------------+-------+------------------+--------------------+--------------------+--------------+------------------------------------------------+
| |A*-right-zero|                              |     |                    |               |       |                  |                    | :math:`\Downarrow` | x            | x                                              |
+----------------------------------------------+-----+--------------------+---------------+-------+------------------+--------------------+--------------------+--------------+------------------------------------------------+
| |A+-idempotency|                             |     |                    |               |       |                  |                    |                    |              | x                                              |
+----------------------------------------------+-----+--------------------+---------------+-------+------------------+--------------------+--------------------+--------------+------------------------------------------------+
| |A+A*-absorption-law|                        |     |                    |               |       |                  |                    |                    |              |                                                |
+----------------------------------------------+-----+--------------------+---------------+-------+------------------+--------------------+--------------------+--------------+------------------------------------------------+

==============================================================================
(R:Two binary operations) + (A:One binary operation) + One composite operation
==============================================================================

R is a ring
NOTE: a vectorspace is a unital left-R module A with a division ring or field instead of a ring

+-----------------------------+----------------------+-----------------+--------------------------+---------------------+
| Axiom                       | Group with operators | left R-module A | unital left R-module A   | Graded vector space |
+-----------------------------+----------------------+-----------------+--------------------------+---------------------+
| |RA*-exist|                 | x                    | x               | x                        | x                   |
+-----------------------------+----------------------+-----------------+--------------------------+---------------------+
| |A+-closure|                | x                    | x               | x                        | x                   |
+-----------------------------+----------------------+-----------------+--------------------------+---------------------+
| |A+-associative|            | x                    | x               | x                        | x                   |
+-----------------------------+----------------------+-----------------+--------------------------+---------------------+
| |A+-identity-element|       | x                    | x               | x                        | x                   |
+-----------------------------+----------------------+-----------------+--------------------------+---------------------+
| |A+-inverse-element|        | x                    | x               | x                        | x                   |
+-----------------------------+----------------------+-----------------+--------------------------+---------------------+
| |A+-commutative|            |                      | x               | x                        | x                   |
+-----------------------------+----------------------+-----------------+--------------------------+---------------------+
| |RA*-left-distributive-A+|  |                      | x               | x                        | x                   |
+-----------------------------+----------------------+-----------------+--------------------------+---------------------+
| |RA*-right-distributive-A+| |                      | x               | x                        | x                   |
+-----------------------------+----------------------+-----------------+--------------------------+---------------------+
| |R*-RA*-compat|             |                      | x               | x                        | x                   |
+-----------------------------+----------------------+-----------------+--------------------------+---------------------+
| |R*1-RA*-compat|            |                      |                 | x                        | x                   |
+-----------------------------+----------------------+-----------------+--------------------------+---------------------+
| |A+-direct-sum|             |                      |                 |                          | x                   |
+-----------------------------+----------------------+-----------------+--------------------------+---------------------+
| |R*-A+-direct-sum-compat|   |                      |                 |                          | x                   |
+-----------------------------+----------------------+-----------------+--------------------------+---------------------+

Did not include quadratic spaces

================================================================================
(R:Two binary operations) + (A:Two binary operations) + One composite operation
================================================================================

R is a ring (or a division ring, or a field, ...)
A is a left-R module

+----------------------------+----------------+----------------------------+-----------------------+----------------------------+-----------------------+
| Axiom                      | Algebra over R | Associative algebra over R | Unital algebra over R | Commutative algebra over R | Normed algebra over R |
+----------------------------+----------------+----------------------------+-----------------------+----------------------------+-----------------------+
| |A*-left-distributive-A+|  | x              | x                          | x                     | x                          | x                     |
+----------------------------+----------------+----------------------------+-----------------------+----------------------------+-----------------------+
| |A*-right-distributive-A+| | x              | x                          | x                     | x                          | x                     |
+----------------------------+----------------+----------------------------+-----------------------+----------------------------+-----------------------+
| |R*-RA*-A*-compat|         | x              | x                          | x                     | x                          | x                     |
+----------------------------+----------------+----------------------------+-----------------------+----------------------------+-----------------------+
| |R*-A*-associative|        |                | x                          |                       |                            |                       |
+----------------------------+----------------+----------------------------+-----------------------+----------------------------+-----------------------+
| |A*-identity-element|      |                |                            | x                     |                            |                       |
+----------------------------+----------------+----------------------------+-----------------------+----------------------------+-----------------------+
| |A*-commutative|           |                |                            |                       | x                          |                       |
+----------------------------+----------------+----------------------------+-----------------------+----------------------------+-----------------------+
| |A*-normed|                |                |                            |                       |                            | x                     |
+----------------------------+----------------+----------------------------+-----------------------+----------------------------+-----------------------+

TODO: non-associative alternatives such as: alternation identity, jacobi identity, jordan identity
TODO: coalgebra
TODO: graded algebra
TODO: inner product space

Let A be an algebra over a ring R and I a subalgebra of A

left ideal

.. math::
    \forall a \in A \forall i \in I_L \colon\quad&I_L\ni\quad&    a \underset{A}{\cdot} i\\
    \Leftrightarrow\\
    \forall i_1\in I_L \forall i_2 \in I_L    \colon\quad&I_L\ni\quad&    i_1 \underset{A}{-} i_2\\
    \forall r\in R \forall i \in I_L         \colon\quad&I_L\ni\quad&    r \underset{{}_R A}{\cdot} i\\
    \forall a\in A \forall i \in I_L        \colon\quad&I_L\ni\quad&    a \underset{A}{\cdot} i

right ideal

.. math::
    \forall a \in A \forall i \in I_R \colon\quad&I_R\ni\quad&    i \underset{A}{\cdot} a\\

=================================================================================
(R:Two binary operations) + (A:Three binary operations) + One composite operation
=================================================================================

TODO

.. rubric:: Footnotes
.. [1] Possible notation? :math:`a^{-1} \quad {\underset{A}{\cdot}^{-1}}a \quad -a \quad {\underset{A}{+}^{-1}}a`
"""
