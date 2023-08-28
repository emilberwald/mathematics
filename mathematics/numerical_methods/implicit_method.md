The Taylor expansion for a function $f$ based on its values and derivatives at $\mathbf{a}$ is:

$
T(\mathbf{x}) = \sum_{|\alpha| \geq 0}\frac{(\mathbf{x}-\mathbf{a})^\alpha}{\alpha !} \left({\mathrm{\partial}^{\alpha}}f\right)(\mathbf{a})
$

If one applies this expansion at each stencil point $\mathbf{a}_i$ one gets a system of equations at a interpolation target point $\mathbf{x}$. The choice of $\mathbf{x}$ affects if the system is explicit or implicit.

$
T(\mathbf{x}) = \sum_{|\alpha| \geq 0}\frac{(\mathbf{x}-\mathbf{a}_i)^\alpha}{\alpha !} \left({\mathrm{\partial}^{\alpha}}f\right)(\mathbf{a}_i), \;1\leq i \leq n\\
$

If one chooses $\mathbf{x}$ so that the system has unknown values for the derivatives at a stencil point, one should be able to rephrase it as a root finding problem where each component of the jet at the unknown stencil points (all orders of derivatives of interest) are unknown scalars, and maybe add some kind of energy constraint or something ...? I don't remember the details...