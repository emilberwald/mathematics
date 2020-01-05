[![Build Status](https://dev.azure.com/emilberwald/mathematics/_apis/build/status/emilberwald.mathematics?branchName=master)](https://dev.azure.com/emilberwald/mathematics/_build/latest?definitionId=2&branchName=master)
# mathematics

Implementing math to understand the details...

## no dev:
```
poetry install --no-dev
```
## dev:
```
poetry install
```
## extras:
```
poetry install -E doc
```
## dev-extras:
It seems the poetry project does not like extras in the dev-section, so will fall back on pip:
```
poetry run pip install -r requirements-dev.txt
```
# docs
In powershell:
```powershell
poetry install
poetry install -E doc
$env:SPHINX_APIDOC_OPTIONS = "members,undoc-members,private-members,special-members,show-inheritance"
poetry run sphinx-apidoc --full -a -o "docs" ./mathematics
Write-Output '' | Out-File -FilePath docs/conf.py -Encoding "UTF8" -Append
Write-Output 'extensions.append("sphinx.ext.mathjax")' | Out-File -FilePath docs/conf.py -Encoding "UTF8" -Append
Write-Output 'extensions.append("sphinxcontrib.bibtex")' | Out-File -FilePath docs/conf.py -Encoding "UTF8" -Append
Write-Output 'mathjax_path="MathJax/es5/tex-mml-chtml.js"' | Out-File -FilePath docs/conf.py -Encoding "UTF8" -Append
git clone --depth 1 --branch 3.0.0 https://github.com/mathjax/MathJax.git docs/_static/MathJax
pushd
cd docs
poetry run make.bat html
popd
```
