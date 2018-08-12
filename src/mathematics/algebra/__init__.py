r"""
.. |br| raw:: html

   <br/>

.. |A*-closure| replace:: closure: |br|
	:math:`\forall a,b\in A\colon\quad		A\ni\quad	a \underset{A}{\cdot} b`
.. |A*-left-zero| replace:: left zero (absorbing element): |br| 
	:math:`\forall a\in A\colon\quad		\underset{A}{0} \underset{A}{\cdot} a = \underset{A}{0}`
.. |A*-right-zero| replace:: right zero (absorbing element): |br|
	:math:`\forall a\in A\colon\quad		a \underset{A}{\cdot} \underset{A}{0} = \underset{A}{0}`
.. |A*-associativity| replace:: associativity: |br| 
	:math:`\forall a,b,c\in A\colon\quad		(a \underset{A}{\cdot} b)\underset{A}{\cdot} c = a \underset{A}{\cdot} (b \underset{A}{\cdot} c )`
.. |A*-identity-element| replace:: (unique) identity element: |br|
	:math:`\exists \underset{A}{1}\in A\colon\forall a\in A\colon\quad		\underset{A}{1} \underset{A}{\cdot} a = a =  a \underset{A}{\cdot} \underset{A}{1}`
.. |A*-inverse-element| replace:: inverse element: |br|
	:math:`\forall a \in A \exists b \in A \colon\quad		a \underset{A}{\cdot} b = \underset{A}{1} = b \underset{A}{\cdot} a`
.. |A*-commutativity| replace:: commutativity:  |br| 
	:math:`\forall a,b \in A \colon\quad		a \underset{A}{\cdot} b = b \underset{A}{\cdot} a`

.. |A+-closure| replace:: closure: |br|
	:math:`\forall a,b\in A\colon\quad		A\ni\quad	a \underset{A}{+} b`
.. |A+-left-zero| replace:: left zero (absorbing element): |br| 
	:math:`\forall a\in A\colon\quad		\underset{A}{0} \underset{A}{+} a = \underset{A}{0}`
.. |A+-right-zero| replace:: right zero (absorbing element): |br|
	:math:`\forall a\in A\colon\quad		a \underset{A}{+} \underset{A}{0} = \underset{A}{0}`
.. |A+-associativity| replace:: associativity: |br| 
	:math:`\forall a,b,c\in A\colon\quad		(a \underset{A}{+} b)\underset{A}{+} c = a \underset{A}{+} (b \underset{A}{+} c )`
.. |A+-identity-element| replace:: (unique) identity element: |br|
	:math:`\exists \underset{A}{0}\in A\colon\forall a \in A\quad		\underset{A}{0} \underset{A}{+} a = a = a \underset{A}{+} \underset{A}{0}`
.. |A+-inverse-element| replace:: inverse element: |br|
	:math:`\forall a \in A \exists b \in A \colon\quad		a \underset{A}{+} b = \underset{A}{0} = b \underset{A}{+} a`
.. |A+-commutativity| replace:: commutativity:  |br| 
	:math:`\forall a,b \in A \colon\quad		a \underset{A}{+} b = b \underset{A}{+} a`
.. |A*-left-distributive-A+| replace:: left distributivity of :math:`\underset{A}{\cdot}` with respect to :math:`\underset{A}{+}`: |br|
	:math:`\forall a_1, a_2, a_3\in A\colon\quad		a_1 \underset{A}{\cdot}(a_2 \underset{A}{+} a_3) = a_1 \underset{A}{\cdot} a_2 \underset{A}{+} a_1 \underset{A}{\cdot} a_3`
.. |A*-right-distributive-A+| replace:: right distributivity of :math:`\underset{A}{\cdot}` with respect to :math:`\underset{A}{+}`: |br|
	:math:`\forall a_1,a_2,a_3 \in A\colon\quad		(a_1 \underset{A}{+} a_2)\underset{A}{\cdot} a = a_1 \underset{A}{\cdot} a_3 \underset{A}{+} a_2 \underset{A}{\cdot} a_3`
.. |A+A*-identities-different| replace:: The identity elements are different: |br| 
	:math:`\underset{A}{1}\neq \underset{A}{0}`


.. |RA*-left-distributive-A+| replace:: left distributivity of :math:`\underset{{}_{R}A}{\cdot}` with respect to :math:`\underset{A}{+}`: |br| 
	:math:`\forall r\in R\forall a_1,a_2\in A\colon\quad		r \underset{{}_{R}A}{\cdot}(a_1 \underset{A}{+} a_2) = r \underset{{}_{R}A}{\cdot} a_1 \underset{A}{+} r \underset{{}_{R}A}{\cdot} a_2`
.. |RA*-right-distributive-A+| replace:: right distributivity of :math:`\underset{{}_{R}A}{\cdot}` with respect to :math:`\underset{A}{+}`: |br|
	:math:`\forall r_1,r_2\in R\forall a\in A\colon\quad		(r_1 \underset{R}{+} r_2)\underset{{}_{R}A}{\cdot} a = r_1 \underset{{}_{R}A}{\cdot} a \underset{A}{+} r_2 \underset{{}_{R}A}{\cdot} a`
.. |R*-RA*-compat| replace:: compatability of scalar multiplication with ring multiplication: |br|
	:math:`\forall r_1,r_2\in R\forall a\in A\colon\quad		(r_1 \underset{R}{\cdot} r_2)\underset{{}_{R}A}{\cdot} a = r_1 \underset{{}_{R}A}{\cdot} (r_2 \underset{{}_{R}A}{\cdot} a)`
.. |R*1-RA*-compat| replace:: compatability of :math:`\underset{{}_{R}A}{\cdot}` with ring unit: |br|
	:math:`1_R \underset{{}_{R}A}{\cdot} a = a`
	
===================
Magma (:math:`A`)
===================
----------------
Basic structure:
----------------
|A*-closure|

----------------
Extra structure:
----------------
|A*-left-zero|

|A*-right-zero|

===================
Group (:math:`A`)
===================

----------------
Basic structure:
----------------
|A*-closure|

|A*-associativity|

|A*-identity-element|

|A*-inverse-element|
[1]_

----------------
Extra structure:
----------------
|A*-commutativity|

===================
Ring (:math:`A`)
===================

------------------------------------
Basic structure:
------------------------------------
|A+-closure|

|A+-associativity|

|A+-identity-element|

|A+-inverse-element|

|A+-commutativity|

|A*-associativity|

|A*-left-distributive-A+|

|A*-right-distributive-A+|

-----------------------
Extra structure:
-----------------------

|A*-identity-element|

=> Ring with identity

|A+A*-identities-different|

|A*-inverse-element|

NOTE: no inverse for :math:`\underset{A}{0}`

=> Division ring

|A*-commutativity|

=> Field

========================================================
left R-Module (:math:`R`:ring, :math:`A`: abelian group)
========================================================

----------------
Basic structure:
----------------

|A+-closure|

|A+-associativity|

|A+-identity-element|

|A+-inverse-element|

|A+-commutativity|

|RA*-left-distributive-A+|

|RA*-right-distributive-A+|

|R*-RA*-compat|

----------------
Extra structure:
----------------

|R*1-RA*-compat|

=============================================================================
Algebra over a ring (:math:`R`:ring, :math:`A`: left R-module :math:`{}_R A`)
=============================================================================

----------------
Basic structure:
----------------

left distributive 

.. math::
	a_1 \underset{A}{\otimes}(a_2 \underset{A}{+} a_3) = a_1 \underset{A}{\otimes} a_2 \underset{A}{+} a_1 \underset{A}{\otimes} a_3

right distributive

.. math::
	(a_1 \underset{A}{+} a_2)\underset{A}{\otimes} a_3 = a_1 \underset{A}{\otimes} a_3 \underset{A}{+} a_2 \underset{A}{\otimes} a_3

compatability with scalars

.. math::
	k \underset{A}{\cdot}(a_1 \underset{A}{\otimes} a_2) = (k \underset{A}{\cdot} a_1) \underset{A}{\otimes} a_2 = a_1\underset{A}{\otimes} (k \underset{A}{\cdot} a_2)

----------------
Extra structure:
----------------

associative

.. math::
	(a_1\underset{A}{\otimes} a_2)\underset{A}{\otimes} a_3 = a_1\underset{A}{\otimes} (a_2\underset{A}{\otimes} a_3) = a_1\underset{A}{\otimes} a_2 \underset{A}{\otimes} a_3

commutative

.. math::
	a_1\underset{A}{\otimes} a_2 = a_2\underset{A}{\otimes} a_1

unital

.. math::
	\underset{A}{1} \underset{A}{\otimes} a = a \underset{A}{\otimes} \underset{A}{1} = a

normed

.. math::
	||a_1\underset{A}{\otimes} a_2|| \leq ||a_1||\cdot_{||\cdot||}||a_2||

Let A be an algebra over a ring R and I a subalgebra of A 

left ideal 

.. math::
	\forall a \in A \forall i \in I_L \colon\quad&I_L\ni\quad&	a \underset{A}{\otimes} i\\
	\Leftrightarrow\\
	\forall i_1\in I_L \forall i_2 \in I_L	\colon\quad&I_L\ni\quad&	i_1 \underset{A}{-} i_2\\
	\forall r\in R \forall i \in I_L 		\colon\quad&I_L\ni\quad&	r \underset{A}{\cdot} i\\
	\forall a\in A \forall i \in I_L		\colon\quad&I_L\ni\quad&	a \underset{A}{\otimes} i
right ideal

.. math::
	\forall a \in A \forall i \in I_R \colon\quad&I_R\ni\quad&	i \underset{A}{\otimes} a\\

.. rubric:: Footnotes
.. [1] Possible notation? :math:`a^{-1} \quad {\underset{A}{\cdot}^{-1}}a \quad -a \quad {\underset{A}{+}^{-1}}a`
"""
