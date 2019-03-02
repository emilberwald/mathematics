"""[summary]

Residual
    $R(u_k) \neq 0$
    We want to have: 
        $R(u_{k+1}) = 0$
    We taylor expand:
       $R(u_{k+1}) = R(u_k) + dR/du_k \Delta u$
    We solve for $\Delta u$ and update
        u_{k+1} = u_k + \Delta u
    Rince and repeat...
"""


# def find_zero(residual, u0):
#     pass
