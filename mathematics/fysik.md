 https://en.wikipedia.org/wiki/Derivation_(differential_algebra) 

$A$: graded algebra

$D$: homogeneous linear map D of grade $|D|$ on A is a homogeneous derivation if

$D(ab) = D(a)b + \varepsilon^{|a||D|}aD(b)$

$\varepsilon\in\{-1,1\}$

A graded derivation is a sum of homogeneous derivations with the same $\varepsilon$.

https://en.wikipedia.org/wiki/Connection_(algebraic_framework) 

$A$: commutative ring

$P$: $A$-module

$D(A)$: module of derivations of a ring $A$

$\nabla_d(ap) = d(a)p + a\nabla_d(p)$

$R^\nabla(d_1,d_2) = [\nabla_{d_1},\nabla_{d_2}]-\nabla_{[d_1,d_2]}$

 https://en.wikipedia.org/wiki/Tangent_bundle 

$TM = \bigsqcup_{x \in M} T_xM = \bigcup_{x \in M} \left\{x\right\} \times T_xM = \bigcup_{x \in M} \left\{(x, y) \mid y \in T_xM\right\} = \left\{ (x, y) \mid x \in M,\, y \in T_xM \right\}$

natural projection: $\pi : TM \twoheadrightarrow M$ $\triangleq $ $\pi(x, v) = x$

https://en.wikipedia.org/wiki/Connection_(vector_bundle) 

$\nabla\colon\Gamma(E)\to\Gamma(E\otimes T^*M)$
$\sigma\in\Gamma(E)$
$f\in \mathcal{C}^\infty(M,\mathbb{R})$

$X\in\Gamma(TM)=\mathcal{C}^\infty(M\mathrm{T}M)$
$\nabla_X\colon\Gamma(E)\to\Gamma(E)$

$\nabla(\sigma f) = (\nabla\sigma)f + \sigma\otimes df$

$\nabla_X\sigma=(\nabla\sigma)(X)$

$\nabla_X(\sigma_1 + \sigma_2) = \nabla_X\sigma_1 + \nabla_X\sigma_2$

$\nabla_{X_1 + X_2}\sigma = \nabla_{X_1}\sigma + \nabla_{X_2}\sigma$

$\nabla_{X}(f\sigma) = f\nabla_X\sigma + X(f)\sigma$

$\nabla_{fX}\sigma = f\nabla_X\sigma$



Affine connection

$\nabla\colon C^\infty(M,\mathrm{T}M)\times C^\infty(M,\mathrm{T}M) \to C^\infty(M,\mathrm{T}M)\colon(X,Y) \mapsto \nabla_X Y$

$\nabla$ is $C^\infty(M,\mathbb{R})$-linear in first variable:
$\nabla_{fX}Y=f\nabla_{X}Y$

$\nabla$ satisfies the Liebniz rule in the second variable:

$\nabla_X(fY)=df(X)Y+f\nabla_{X}Y$



Covariant derivative

$\left(\nabla_\mathbf{v} f\right)_p = \left(f \circ \phi\right)'\left(0\right) = \lim_{t \to 0}t^{-1}\left(f\left[\phi\left(t\right)\right] - f\left[p\right]\right).$

$\left(\nabla_{g\mathbf{x} + h\mathbf{y}} \mathbf{u}\right)_p = \left(\nabla_\mathbf{x} \mathbf{u}\right)_p g + \left(\nabla_\mathbf{y} \mathbf{u}\right)_p h$

$\left(\nabla_\mathbf{v}\left[\mathbf{u} + \mathbf{w}\right]\right)_p = \left(\nabla_\mathbf{v} \mathbf{u}\right)_p + \left(\nabla_\mathbf{v} \mathbf{w}\right)_p$

$\left(\nabla_\mathbf{v} \left[f\mathbf{u}\right]\right)_p = f(p)\left(\nabla_\mathbf{v} \mathbf{u})_p + (\nabla_\mathbf{v}f\right)_p\mathbf{u}_p$

$\left(\nabla_\mathbf{v}\alpha\right)_p \left(\mathbf{u}_p\right) = \nabla_\mathbf{v}\left[\alpha\left(\mathbf{u}\right)\right]_p - \alpha_p\left[\left(\nabla_\mathbf{v}\mathbf{u}\right)_p\right].$

$\nabla_\mathbf{v}\left(\varphi \otimes \psi\right)_p = \left(\nabla_\mathbf{v}\varphi\right)_p \otimes \psi(p) + \varphi(p) \otimes \left(\nabla_\mathbf{v}\psi\right)_p$

$\nabla_\mathbf{v}(\varphi + \psi)_p = (\nabla_\mathbf{v}\varphi)_p + (\nabla_\mathbf{v}\psi)_p.$

$(\nabla_Y T)\left(\alpha_1, \alpha_2, \ldots, X_1, X_2, \ldots\right) = Y\left(T\left(\alpha_1,\alpha_2, \ldots, X_1, X_2, \ldots\right)\right) - T\left(\nabla_Y\alpha_1, \alpha_2, \ldots, X_1, X_2, \ldots\right) - T\left(\alpha_1, \nabla_Y\alpha_2, \ldots, X_1, X_2, \ldots\right) - \ldots - T\left(\alpha_1, \alpha_2, \ldots, \nabla_YX_1, X_2, \ldots\right) -  T\left(\alpha_1, \alpha_2, \ldots, X_1, \nabla_YX_2, \ldots\right) - \ldots$



Metric connection

$d \langle \sigma,\tau\rangle = \langle D\sigma,\tau\rangle + \langle \sigma,D \tau\rangle,\quad D_X \langle \sigma,\tau\rangle = d_X \langle \sigma,\tau\rangle \equiv X\langle \sigma,\tau\rangle.$

Riemannian connection $\nabla$ on pseudo-Riemannian manifold (M,g):

$\nabla_Xg(Y,Z)=g(\nabla_XY,Z)+g(Y,\nabla_XZ)$



Torsion tensor

$T(X, Y) := \nabla_X Y - \nabla_Y X - [X,Y]$

$R(X, Y)Z = \nabla_X\nabla_YZ - \nabla_Y\nabla_XZ - \nabla_{[X, Y]}Z.$



Lie derivative

$$[X,Y]: C^\infty(M) \rightarrow C^\infty(M)$$

$[X,Y](f) = X(Y(f)) - Y(X(f))$



Guesses...

$\nabla(X,f)_p=\lim_{t \to 0}t^{-1}\left(f\left[\phi\left(t\right)\right] - f\left[\phi(0)\right]\right),\quad \lim_{t \to 0}t^{-1}(\phi(t) - \phi(0))= X_{\phi(0)},\quad \phi(0)=p$

$\nabla(fX,Y) = f\nabla(X,Y)$

$\nabla(fX,Y)=\nabla(X,fY)-\nabla(X,f)Y$

$\nabla(X,Y)-\nabla(Y,X)=T^\nabla(X,Y)-(X\circ Y - Y\circ X)$

$\nabla(X,\nabla(Y,Z))-\nabla(Y,\nabla(X,Z)) = R^\nabla(X,Y)(Z) + \nabla(X\circ Y - Y\circ X,Z)$



$\nabla_X Y = g(\nabla_X Y,e_k)e^k = \frac{1}{2}(\partial_X(g(Y,e_k)) + \partial_Y(g(X,e_k)) -\partial_{e_k}(g(X,Y)) + g([X,Y],e_k) - g([X,e_k],Y) - g([Y,e_k],X))e^k$

$R(X,Y)Z = \nabla_X(\nabla_Y Z)-\nabla_Y(\nabla_X Z) - \nabla_{[X,Y]}Z$

$\newcommand{Commutator}[2]{(#1\circ#2-#2\circ#1)}$

$\newcommand{KoszulExpand}[3]{
\overbrace{
\frac{1}{2}
\left[
{#1}(g({#2},e_{#3}))
+
{#2}(g({#1},e_{#3}))
-e_{#3}(g({#1},{#2}))
+g(\Commutator{#1}{#2},e_{#3})
-g(\Commutator{#1}{e_{#3}},{#2})
-g(\Commutator{#2}{e_{#3}},{#1})
\right]
e^{#3}
}
^{[\nabla_{#1}(#2)]^{#3}}
}$


$\KoszulExpand{X}{Y}{k} $

$\newcommand{RiemannTensor}[3]{\Commutator{\nabla_{#1}}{\nabla_{#2}}({#3}) - \nabla_{[#1,#2]})(#3)}$

$\RiemannTensor{X}{Y}{Z}$

$\newcommand{RiemannTensorKoszulExpand}[5]{\KoszulExpand{#1}{\KoszulExpand{#2}{#3}{#4}}{#5} + \KoszulExpand{#2}{\KoszulExpand{#1}{#3}{#4}}{#5} - \KoszulExpand{\Commutator{#1}{#2}}{#3}{#5}$

$\RiemannTensorKoszulExpand{X}{Y}{Z}{m}{k}$





