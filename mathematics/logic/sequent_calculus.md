# OBJECT LANGUAGE

- A wff in a language is valid if it is true for every interpretation of the language.
- A wff in a language is satisfiable if it is true for at least one interpretation of the language.
- A sentence is a wff with no free variables.
- A sentence that is true by a particular assignment is satisfied by that assignment.
- A sentence is consistent if it is true under at least one interpretation.
- A sentence is logically valid if it is satisfied by every interpretation.

- terms
  - variables
    - given values from the domain of discourse through variable assignment
  - function symbols
    - given values from (the powerset of?) the domain of discourse through the interpretation
  - 0-ary function symbols
    - 0
  - n-ary function symbols applied to n terms:
    - f(t_1, ..., t_n)
- atomic formula
  - 0-ary predicate symbols
    - ⊤
    - ⊥
  - 2-ary predicate symbol = applied to 2 terms:
    - t_1 = t_2
  - n-ary predicate symbol applied to n terms:
    - R(t_1, ..., t_n)
- well formed formula (wff)
  - 1-ary symbol ¬ applied to wff:
    - ¬A
  - 2-ary connective ∧ applied to 2 wffs:
    - A ∧ B is true if A and B are both true; otherwise, it is false.
  - existential quantifier applied to a variable and a wff:
    - ∃x A
  - universal quantifier applied to a variable and a wff:
    - ∀x A
  - Extras:
    - 2-ary connective → applied to 2 wffs (material implication is the truth function of this connective):
      - A → B is true if and only if B can be true and A can be false but not vice versa.
    - 2-ary connective ∨ applied to 2 wffs:
      - A ∨ B is true if A or B (or both) are true; if both are false, the statement is false.
    - 2-ary connective ↔ applied to 2 wffs:
      - A ↔ B is true only if both A and B are false, or both A and B are true.

# METALINGUISTICS

- ⊢
  - logical consequence
  - 'A' ⊢S 'B' posits: there is a derivation in the formal proof system S from from the premise 'A' to the conclusion 'B'.

- ⊨
  - semantic consequence
  - 'A' ⊨L 'B' posits: on every interpretation of the non-logical vocabulary of language L, if 'A' is true, so is 'B'.

# SEQUENT CALCULUS RULES

- L∧ ( ...,'A∧B',⊢,... ) ↦ ( ...,'A','B',⊢,... )
- L∨ ( ...,'A∨B',⊢,... ) ↦ ( ...,'A',⊢,... ),( ...,'B',⊢,... )
- L→ ( ...,'A→B',⊢,... ) ↦ ( ...,⊢,...,'A' ),( ...,'B',⊢,... )
- L¬ ( ...,'¬A',⊢,... )  ↦ ( ...,⊢,...,'A' )
- R∧ ( ...,⊢,...,'A∧B' ) ↦ ( ...,⊢,...,'A' ),( ...,⊢,...,'B' )
- R∨ ( ...,⊢,...,'A∨B' ) ↦ ( ...,⊢,...,'A','B' )
- R→ ( ...,⊢,...,'A→B' ) ↦ ( ...,'A',⊢,...,'B' )
- R¬ ( ...,⊢,...,'¬A' )  ↦ ( ...,'A',⊢,... )
- Axiom ('p','r',⊢,'q','r')

'x','y' : Variables
A variable binding operator such as the existential and universal quantifiers binds the variable to a wff. It is no longer free when bound.
't': Term
'A','B': wffs
L,R : *sequence of wffs (0 or more)
'A'['t'/'x'] replace every free occurence of 'x' with 't' in A, with the restriction that no occurence of any variable in 't' becomes bound in 'A'['t'/'x']
W: Weakening, C: Contraction, P: Permutation

Introduce:
- I  	() ↦ ( 'A',⊢,'A' )
Prune:
- Cut	( L1,⊢,R1,'A' ),( 'A',L2,⊢,R2 ) ↦ ( L1,L2,⊢,R1,R2 )
Combine:
- ∨L 	( L1,'A',⊢,R1 ),( L2,'B'⊢,R2 ) ↦ ( L1,L2,'A∨B',⊢,R1,R2 )
- ∧R 	( L1,⊢,'A',R1 ),( L2,⊢,'B',R2 ) ↦ ( L1,L2,⊢,'A∧B',R1,R2 )
Cross side:
- →L 	( L1,⊢,'A',R1 ),( L2,'B',⊢,R2 ) ↦ ( L1,L2,'A→B',⊢,R1,R2 )
- →R 	( L1,'A',⊢,'B',R1 ) ↦ ( L1,⊢,'A→B',R1 )
- ¬L 	( L1,⊢,'A',R1 ) ↦ ( L1,'¬A',⊢,R1 )
- ¬R 	( L1,'A',⊢,R1 ) ↦ ( L1,⊢,'¬A',R1 )
Rewrite left side:
- ∧L1	( L1,'A',⊢,R1 ) ↦ ( L1,'A∧B',⊢,R1 )
- ∧L2	( L1,'B',⊢,R1 ) ↦ ( L1,'A∧B',⊢,R1 )
- ∀L 	( L1,'A'['t'/'x'],⊢,R1 ) ↦ ( L1,'∀xA',⊢,R1 )
- ∃L 	( L1,'A'['y'/'x'],⊢,R1 ) ↦ ( L1,'∃xA',⊢,R1 )
  - 'y' must not occur free anywhere in the transformed sequent
- WL 	( L1,⊢,R1 ) ↦ ( L1,'A',⊢,R1 )
Rewrite right side:
- ∨R1 	( L1,⊢,'A',R1 ) ↦ ( L1,⊢,'A∨B',R1 )
- ∨R2 	( L1,⊢,'B',R1 ) ↦ ( L1,⊢,'A∨B',R1 )
- ∃R 	( L1,⊢,'A'['t'/'x'],R1 ) ↦ ( L1,⊢,'∃xA',R1 )
- ∀R 	( L1,⊢,'A'['y'/'x'],R1 ) ↦ ( L1,⊢,'∀xA',R1 )
   - 'y' must not occur free anywhere in the transformed sequent
- WR 	( L1,⊢,R1 ) ↦ ( L1,⊢,'A',R1 )
Contract:
- CL 	( L1,'A','A',⊢,R1 ) ↦ ( L1,'A',⊢,R1 )
- CR 	( L1,⊢,'A','A',R1 ) ↦ ( L1,⊢,'A',R1 )
Permute:
- PL 	( L1,'A','B',L2,⊢,R1 ) ↦ ( L1,'B','A',L2,⊢,R1 )
- PR 	( L1,⊢,R1,'A','B',R2 ) ↦ ( L1,⊢,'B','A',R2 )

Examples
https://en.wikipedia.org/wiki/Sequent_calculus#Structural_rules
Law of excluded middle
I
( 'A',⊢,'A' )
¬R
( ⊢,'¬A','A' )
∨R2
( ⊢,'A∨¬A','A' )
PR
( ⊢,'A','A∨¬A' )
∨R1
( ⊢,'A∨¬A','A∨¬A' )
CR
( ⊢,'A∨¬A' )
