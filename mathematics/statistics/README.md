Probability space $(S_1, \Sigma_1,  \mu_1)$
Measurable space $(S_2, \Sigma_2)$
Random variable $F\colon S_1\to S_2$
Expected value $\mathbb{E}_{\mu_1}(F) \triangleq \int_{S_1} F d\mu_1$

Preimage: $\forall (F\colon S_1 \to S_2)\land\forall (\hat{S}_2 \subseteq S_2)\colon  F^{-1}(\hat{S}_2) \triangleq \{s_1\in S_1\colon F(s_1) \in \hat{S}_2\}$



Countably-additive vector measure:

$\forall ((\sigma_{i})_{i=1\ldots\infty}\colon i\neq j \Rightarrow \sigma_i \cap \sigma_j = \emptyset) (\mu(\cup(\sigma_i)_{i=1\ldots\infty}) = \sum_{i=1\ldots\infty} \mu(\sigma_i) \Leftrightarrow \lim_{n\to \infty}||\mu(\cup(\sigma_i)_{i=n\ldots \infty})||_B = 0)$



Variation of vector measure:

$|\mu|(\sigma)=\sup_{\forall(\sigma\in\Sigma )((\sigma_i)_{i\in I}\colon i\neq j \Rightarrow \sigma_i \cap \sigma_j = \emptyset\land \cup (\sigma_i)_{i\in I} = \sigma)} \sum_{i\in I}||\mu(\sigma_i)||_B$

If $|\mu|(S) < \infty$ the measure has bounded variation.



Absolutely continuous: $\mu \ll \nu \triangleq \forall\sigma\in\Sigma\colon \mu(\sigma)=0 \Leftarrow \nu(\sigma)=0$



Pushforward measure: $\forall \sigma_2\in\Sigma_2\colon(F_\sharp\mu_1)(\sigma_2) \triangleq \mu_1(F^{-1}(\sigma_2)) \equiv (F^{-1}⨾\mu_1)(\sigma_2)$



Let's use a funky notation for integral: $\int_A f \mathrm{d} \mu_A \triangleq \int(A,f,\mu_A)$

Change of variables formula: 
$
\int(S_2, g, F_\sharp \mu_1) \equiv \int(S_2, g, F^{-1}⨾\mu_1) = \int(S_1, F⨾g, \mu_1) \\
$

[Bochner integral](https://en.wikipedia.org/wiki/Bochner_integral) :

 Iverson Bracket: $[[P]] \triangleq \begin{cases} P=\top \mapsto 1 \\ P=\bot \mapsto 0 \end{cases}$

Let $B$ be a Banach space (compatible with the codomain of the Iverson Bracket).

Disjoint: $(\sigma_i)_{i\in I}\colon i\neq j \Rightarrow \sigma_i \cap \sigma_j = \emptyset$

Mutually disjoint: $(\sigma_i)_{i\in I}\colon \sigma_i\neq \sigma_j \Rightarrow \sigma_i \cap \sigma_j = \emptyset$

Distinct: $(b_i)_{i\in I}\colon i\neq j \Rightarrow b_i \neq b_j$

A simple function: $s \mapsto \sum_{i=1}^n [[s\in \sigma_{1i}]] b_i$ with disjoint $\sigma_{1i}\in\Sigma_1$ and distinct $b_i\in B$ 

If $\mu_1(\sigma_{1i})$ is finite whenever $b_i\neq 0_B$ then the simple function is integrable:

$\int(S_1, S_1\ni s\mapsto \sum_{i=1}^n[[s\in \sigma_{1i}]]b_i, \mu_1) \triangleq \sum_{i=1}^n \mu_1(\sigma_{1i}) b_i$

$B$ has the Radon-Nikodym property with respect to $\mu_1$ if for every countably-additive vector measure $\gamma_1$ with values in $B$ which has bounded variation and is absolutely continuous with respect to $\mu_1$, there is a $\mu_1$-integrable function $g\colon S_1\to B$ such that 

$$
\forall (\sigma_1\in\Sigma_1)\colon\gamma_1(\sigma_1) = \int(\sigma_1, g, \mu_1)
$$

So, revisiting the change of variable formula, we get...?
$$
\int(S_2,g,F^{-1}⨾\mu_1) = \int(S_2,g, \sigma_1\mapsto \textstyle\int(\sigma_1, \frac{\mathrm{d}F^{-1}⨾\mu_1}{\mathrm{d}\mu_1},\mu_1 ))
$$
Followed by Lebesgue Differentiation Theorem, which shows that it equals the determinant of the jacobian of the inverse

$$
\frac{\mathrm{d}F^{-1}⨾\mu_1}{\mathrm{d}\mu_1} \triangleq |\det (DF^{-1})| =|\det (DF)|^{-1}
$$
Then (some substitutions that I did not follow) ... calculus change of variable formula.

